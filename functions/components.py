import json
from firebase_admin import firestore, initialize_app
from firebase_functions import firestore_fn, https_fn
from pint import UnitRegistry

ureg = UnitRegistry()  # If you have custom unit definitions
app = initialize_app()

IGNORED_PROPERTIES = ['designator_prefix', 'mpn']

firestore_client = firestore.client()

@https_fn.on_request()
def get_component(request, firestore_client=firestore_client):
    try:
        req_json = request.get_json()
        component_type = req_json.get("type", "").lower()
        if not component_type:
            raise ValueError("Component type is required.")

        physical_filters = {}
        property_filters = {"type": component_type}

        for key, value in req_json.items():
            if key in IGNORED_PROPERTIES or key in ["type"]:
                continue  # Skip ignored and separately handled properties

            if isinstance(value, dict) and "min_val" in value and "max_val" in value:
                base_min_val = convert_to_base_units(value["min_val"], value["unit"])
                base_max_val = convert_to_base_units(value["max_val"], value["unit"])
                physical_filters[key] = (base_min_val, base_max_val)
            else:
                property_filters[key] = value

        components = query_components(firestore_client, component_type, physical_filters, property_filters)

        if not components:
            return https_fn.Response(
                json.dumps({"error": "No components found that match the criteria."}),
                status=404,
                content_type='application/json'
            )

        best_component = select_best_component(components)

        return https_fn.Response(
            json.dumps({"bestComponent": best_component}),
            status=200,
            content_type='application/json'
        )

    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=400,
            content_type='application/json'
        )

def query_components(firestore_client, component_type, physical_filters=None, property_filters=None):
    query = firestore_client.collection("component_data").where("type", "==", component_type)

    # Apply property filters
    for prop, value in property_filters.items():
        if prop != "type":  # 'type' is already included in the query
            query = query.where(prop, "==", value)

    results = query.stream()
    components = [doc.to_dict() for doc in results]

    # Apply physical filters
    if physical_filters:
        components = [comp for comp in components if all(
            physical_filters[prop][0] <= comp.get(prop, {}).get('max_val', float('inf')) and
            physical_filters[prop][1] >= comp.get(prop, {}).get('min_val', 0)
            for prop in physical_filters
        )]

    return components

def convert_to_base_units(value, unit):
    quantity = ureg.Quantity(value, unit)
    base_unit = ureg.Quantity(1, unit).to_base_units().units
    return quantity.to(base_unit).magnitude

def select_best_component(components):
    in_stock_components = [comp for comp in components if comp.get("stock", 0) > 100]
    if in_stock_components:
        components = in_stock_components

    basic_parts = [comp for comp in components if comp.get("basic_part", False)]
    if basic_parts:
        components = basic_parts

    return min(components, key=lambda comp: comp.get("price_usd", float('inf')), default=None)
