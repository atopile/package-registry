# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
import json
import math

import google.cloud.firestore
# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import firestore, initialize_app
from firebase_functions import firestore_fn, https_fn
from pint import UnitRegistry

ureg = UnitRegistry() # If you have custom unit definitions


@https_fn.on_request()
def get_component(req: https_fn.Request) -> https_fn.Response:
    """Takes a JSON of component requirements and returns a suitable component from ato database."""
    # Setup Firestore client
    firestore_client: google.cloud.firestore.Client = firestore.client()

    # Parse the JSON request
    req_json = req.get_json()
    if not req_json:
        return https_fn.Response("No JSON body provided", status=400)

    # Get the component type
    component_type = req_json.get("mpn")
    if not component_type:
        return https_fn.Response("No component type provided", status=400)

    if component_type == "Resistor":
        return get_resistor_or_capacitor(req_json, firestore_client)
    elif component_type == "Capacitor":
        return get_resistor_or_capacitor(req_json, firestore_client)
    elif component_type == "Mosfet":
        return get_mosfet(req_json, firestore_client)

    else:
        return https_fn.Response("Invalid component type provided", status=400)

def get_resistor_or_capacitor(req_json, firestore_client):
    try:
        component_type = req_json.get("type")
        if not component_type:
            raise ValueError("Component type is required (Resistor or Capacitor).")

        value_json = req_json.get("value")
        if value_json:
            value_data = json.loads(value_json)
            min_value = ureg.Quantity(value_data.get("min_val"), value_data.get("unit"))
            max_value = ureg.Quantity(value_data.get("max_val"), value_data.get("unit"))

            # Convert to a standard unit if necessary, e.g., ohms
            min_value = min_value.to(ureg.ohm).magnitude
            max_value = max_value.to(ureg.ohm).magnitude
        else:
            min_value = None
            max_value = None

        package = req_json.get("package", "").lstrip('C').lstrip('R')

        # Query and filter
        query = firestore_client.collection("components").where("type", "==", component_type)
        results = query.stream()
        components = [doc.to_dict() for doc in results]

        filtered_components = []
        for component in components:
            valid = True
            component_min_value = component.get("min_value")
            component_max_value = component.get("max_value")

            if (component_min_value is None or math.isnan(component_min_value) or
                min_value is not None and component_min_value < min_value):
                valid = False
            if (component_max_value is None or math.isnan(component_max_value) or
                max_value is not None and component_max_value > max_value):
                valid = False
            if package and component.get("Package") != package:
                valid = False
            if component.get("Stock", 0) <= 100:  # Check stock only if other conditions are met
                valid = False
            if valid:
                filtered_components.append(component)

        if not filtered_components:
            return https_fn.Response(
                json.dumps({"error": "No components found that match the criteria."}),
                status=404,
                content_type='application/json'
            )

        # Select the best component
        basic_components = [component for component in filtered_components if component.get("basic-extended") == "Basic"]
        if basic_components:
            best_component = min(basic_components, key=lambda component: component["Price (USD)"])
        else:
            best_component = min(filtered_components, key=lambda component: component["Price (USD)"])

        return https_fn.Response(
            json.dumps({"Best Component": best_component}),
            status=200,
            content_type='application/json'
        )

    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=400,
            content_type='application/json'
        )

def get_mosfet(req_json, firestore_client):
    try:
        # Retrieve the request parameters
        polarity = req_json.get("polarity")
        ds_voltage = req_json.get("drain_source_voltage")
        current = req_json.get("current")
        on_resistance = req_json.get("on_resistance")
        power_dissipation = req_json.get("power_dissipation")
        safety_factor_current = req_json.get("safety_factor", 1.5)
        safety_factor_voltage = req_json.get("safety_factor", 1.5)
        package = req_json.get("package")

        if not polarity:
            raise ValueError("Polarity is required.")

        # Query the collection
        query = firestore_client.collection("mosfets").where("polarity", "==", polarity)
        results = query.stream()
        components = [doc.to_dict() for doc in results]
        print(len(components))
        # Filter components based on provided criteria
        filtered_components = []
        for component in components:
            valid = True
            if ds_voltage is not None and component.get("drain_source_voltage_V", 0) < ds_voltage * safety_factor_voltage:
                valid = False
            if current is not None and component.get("current_A", 0) < current * safety_factor_current:
                valid = False
            if on_resistance is not None and component.get("on_resistance_ohms", float('inf')) > on_resistance:
                valid = False
            if power_dissipation is not None and component.get("power_dissipation_W", 0) < power_dissipation:
                valid = False
            if component.get("Stock", 0) <= 100:
                valid = False
            if package and component.get("Package") != package:
                valid = False
            if valid:
                filtered_components.append(component)

        # Select the best component
        if not filtered_components:
            return https_fn.Response(
                json.dumps({"error": "No suitable MOSFETs found."}),
                status=404,
                content_type='application/json'
            )

        best_mosfet = min(filtered_components, key=lambda component: component["Price"][0]["price"] if component["Price"] else float('inf'))

        # Send back a JSON response with the best MOSFET
        return https_fn.Response(
            json.dumps({"Best Component": best_mosfet}),
            status=200,
            content_type='application/json'
        )

    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=400,
            content_type='application/json'
        )
