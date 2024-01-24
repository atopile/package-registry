import glob
import os
import re
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path

import firebase_admin
import requests
from bs4 import BeautifulSoup
from firebase_admin import credentials, firestore
from pint import UnitRegistry

ureg = UnitRegistry()

import os
import shutil


def delete_files_and_folders_in_directory(directory):
    """
    Deletes all files and folders in the specified directory.

    Args:
    directory (str): Path to the directory where files and folders will be deleted.
    """
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return

    # Iterate over all files and folders in the directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        try:
            # If it's a file, delete it
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            # If it's a directory, delete the entire directory tree
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            print(f"Error deleting {item_path}: {e}")


def get_footprint_data(jlcpn, base_dir="/Users/narayanpowderly/Documents/atopile-workspace/package-registry-backend/temp"):
    # Create a unique temporary subdirectory within the base directory
    with tempfile.TemporaryDirectory(dir=base_dir) as temp_dir:
        # print(temp_dir)
        command = [
            "easyeda2kicad",
            "--full",
            f"--lcsc_id={jlcpn}",
            f"--output={temp_dir}/temp",
            "--overwrite",
            "--ato",
            f"--ato_file_path={temp_dir}",
        ]
        result = subprocess.run(command, capture_output=True, text=True)
    
        # read the ato file data glob matching with .ato extension
        ato_file_path = glob.glob(f"{temp_dir}/*.ato")[0]

        # read the kicad_mod file data
        kicad_mod_file_path = glob.glob(f"{temp_dir}/temp.pretty/*.kicad_mod")[0]

        # Read the contents of the .ato and .kicad_mod files
        ato_file_content = read_file(ato_file_path)
        kicad_mod_file_content = read_file(kicad_mod_file_path)

        # Parse the ato file and transform the kicad_mod file
        ato_mapping = parse_ato_file(ato_file_content)
        transformed_kicad_mod = transform_kicad_mod(kicad_mod_file_content, ato_mapping)

        # No need to manually delete the temporary directory; it's handled automatically

        return transformed_kicad_mod



def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def parse_ato_file(ato_content):
    signal_mapping = {}
    for line in ato_content.splitlines():
        if "~ pin" in line:
            parts = line.strip().split(" ~ pin ")
            signal = parts[0].split(" ")[-1]
            pin = "pin " + parts[1]
            if signal not in signal_mapping:
                signal_mapping[signal] = []
            signal_mapping[signal].append(pin)
    return signal_mapping


def transform_kicad_mod(kicad_mod_content, ato_mapping):
    desired_mapping = {"G": "G", "S": "S", "D": "D"}
    reverse_ato_mapping = {
        pin: signal for signal, pins in ato_mapping.items() for pin in pins
    }

    transformed_lines = []
    for line in kicad_mod_content.splitlines():
        if line.strip().startswith("(pad"):
            parts = line.strip().split(" ")
            original_pin = parts[1]
            signal = reverse_ato_mapping.get("pin " + original_pin)
            if signal and signal in desired_mapping:
                parts[1] = desired_mapping[signal]  # Apply the transformation
            transformed_line = "\t" + " ".join(parts)  # Adding tab indent
        else:
            transformed_line = "\t" + line.strip()
        transformed_lines.append(transformed_line)
    return "\n".join(transformed_lines)


def extract_product_details(html):
    """
    Extracts product details from the given HTML string based on the provided structure.

    Args:
    html (str): A string containing the HTML content.

    Returns:
    dict: A dictionary containing the extracted product details.
    """
    # A dictionary to hold the extracted details
    details = {}

    # Regular expression pattern to match the details
    pattern = r"<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>"

    # Find all matches in the HTML content
    matches = re.findall(pattern, html, re.DOTALL)

    # Process each match
    for match in matches:
        key = match[0].strip()
        value = re.sub(
            "<[^<]+?>", "", match[1]
        ).strip()  # Remove any HTML tags from the value
        details[key] = value

    return details


def extract_attribute_data(html):
    """
    Extracts attribute data from the given HTML string and returns it as a dictionary.

    Args:
    html (str): A string containing the HTML content.

    Returns:
    dict: A dictionary containing the extracted attribute names and values.
    """
    # Define the pattern to match the specified structure
    pattern = (
        r'\{(?:\s*attribute_name_en:\s*"([^"]+)"\s*,\s*attribute_value_name:\s*"([^"]+)"|'
        + r'\s*attribute_value_name:\s*"([^"]+)"\s*,\s*attribute_name_en:\s*"([^"]+)")\s*\}'
    )

    # Find all matches in the HTML content
    matches = re.findall(pattern, html)

    # Create a dictionary from the matches
    extracted_data = {}
    for match in matches:
        # Match could be in either of the two capturing groups, depending on the order in HTML
        attribute_name = match[0] if match[0] else match[3]
        attribute_value = match[1] if match[1] else match[2]
        extracted_data[attribute_name] = attribute_value
    return extracted_data


def extract_prices(html_content):
    """
    Extracts pricing details from the given HTML content.

    Args:
    html_content (str): A string containing the HTML content.

    Returns:
    list of tuples: A list where each tuple contains the quantity and the corresponding price.
    """
    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Extracting price information
    price_divs = soup.find_all("div", class_="flex items-center justify-between mt-14")
    prices = []

    for div in price_divs:
        # Extract quantity and price
        qty = div.find("span", class_="w-120 inline-block").text.strip()
        pr = div.find("span", class_="w-120 text-left").text.strip().replace("$", "")

        # Add to the list as a tuple
        prices.append((qty, float(pr)))

    return prices[0][1]


def generate_uuid():
    """
    Generates a UUID.

    Returns:
    str: A UUID with ato- prefix.
    """
    return f"ato-{uuid.uuid4()}"


def calculate_physical_properties(value=None, tolerance=None, min_val=None, max_val=None, unit=None):
    """
    [Function definition from the previous response]
    """
    properties = {}

    if value is not None and tolerance is not None:
        # Calculate min and max values based on tolerance
        nominal = ureg.Quantity(value, unit)
        tolerance_val = nominal * tolerance / 100
        min_val = nominal - tolerance_val
        max_val = nominal + tolerance_val
    elif min_val is not None and max_val is not None:
        # Calculate nominal value and tolerance
        min_val = ureg.Quantity(min_val, unit)
        max_val = ureg.Quantity(max_val, unit)
        nominal = (min_val + max_val) / 2
        tolerance_val = max_val - nominal
    else:
        raise ValueError("Either value with tolerance or min and max values must be provided.")

    # Convert and format the unit
    if unit == 'uH':
        nominal = nominal.to(ureg.henry)
        tolerance_val = tolerance_val.to(ureg.henry)
        min_val = min_val.to(ureg.henry)
        max_val = max_val.to(ureg.henry)

    properties['nominal'] = nominal.magnitude
    properties['tolerance'] = tolerance_val.magnitude
    properties['min_val'] = min_val.magnitude
    properties['max_val'] = max_val.magnitude
    properties['tolerance_pct'] = (tolerance_val / nominal * 100).magnitude
    properties['unit'] = str(nominal.units)

    return properties


def get_html(lcsc_id):
    """
    Returns the HTML content for the specified LCSC ID.

    Args:
    lcsc_id (str): The LCSC ID for the product.

    Returns:
    str: A string containing the HTML content.
    """
    # Define the URL for the product
    url = f"https://jlcpcb.com/partdetail/{lcsc_id}"

    # Get the HTML content
    response = requests.get(url)
    return response.text

def extract_stock(html_string):
    # Regular expression pattern to find stock level
    stock_pattern = r'Available Order Qty: (\d+)'

    # Search for the pattern in the HTML string
    match = re.search(stock_pattern, html_string)

    # Extract and return stock level if found, else return 0
    if match:
        return int(match.group(1))
    else:
        return 0

def process_physical_attribute(value, unit, tolerance=None, min_val=None):
    ureg = UnitRegistry()

    # Convert the value to a quantity with the correct unit
    quantity = ureg.Quantity(value, unit)

    if unit == "uH":
        # Convert to henries
        quantity = quantity.to(ureg.henry)
    elif unit.endswith("ohm"):
        # Convert to ohms, handling prefixes like milli, micro, etc.
        if 'm' in unit:  # milliohms
            quantity = quantity.to(ureg.milliohm)
        elif 'u' in unit:  # microohms
            quantity = quantity.to(ureg.microohm)
        else:
            # Keep in ohms, no conversion needed
            pass
    else:
        # Keep the original unit
        pass

    # Handle tolerance and min_val
    if tolerance is not None:
        tolerance_val = quantity * tolerance / 100
        min_val = quantity - tolerance_val if min_val is None else ureg.Quantity(min_val, unit)
        max_val = quantity + tolerance_val
    else:
        min_val = ureg.Quantity(min_val, unit) if min_val is not None else quantity
        max_val = quantity

    return {
        'nominal': quantity.magnitude,
        'min_val': min_val.magnitude if min_val is not None else None,
        'max_val': max_val.magnitude,
        'tolerance': tolerance,
        'unit': str(quantity.units)
    }

# print(process_physical_attribute(10, 'uH', 10, 9))
def get_type(html_content):
    # Function to extract attributes (Assuming you already have it implemented)
    attributes = extract_attribute_data(html_content)

    # Define keywords for different component types
    component_keywords = {
        "inductor": ["Inductor", "Power Inductors", "Choke", "Coil"]
        # Add more component types and their keywords here
    }

    for component_type, keywords in component_keywords.items():
        for keyword in keywords:
            # Check if any of the keywords are in the attributes (e.g., in the 'Type' attribute)
            if any(keyword in attributes.get(attr, '') for attr in ['Type', 'Description']):
                return component_type

    return "unknown"  # or None, if you prefer

def extract_value_and_unit(attribute_string):
    # Use regex to extract the value and unit
    match = re.match(r"([\d\.]+)(\w+)", attribute_string)
    if match:
        value, unit = match.groups()
        return float(value), unit
    else:
        return None, None

def create_inductor_data(html):
    attributes = extract_attribute_data(html)
    details = extract_product_details(html)

    # footprint stuff
    footprint = get_footprint_data(details['JLCPCB Part #'])
    inductance_value, inductance_unit = extract_value_and_unit(attributes['Inductance'])
    tolerance_value = float(re.search(r"±([\d\.]+)%", attributes['Tolerance']).group(1))
    current_value, current_unit = extract_value_and_unit(attributes['Rated Current'])

    inductor_data = {
        'uuid': generate_uuid(),
        'inductance': process_physical_attribute(inductance_value, inductance_unit, tolerance=tolerance_value),
        'current': process_physical_attribute(current_value, current_unit, min_val=0),
        'manufacturer': details['Manufacturer'],
        'lcsc_id': details['JLCPCB Part #'],
        'package': details['Package'],
        'description': details['Description'],
        'stock': extract_stock(html),
        'price': extract_prices(html),
        'footprint_data': {"kicad": get_footprint_data(details['JLCPCB Part #'])},
        'type': 'inductor'
    }
    # set the footprint name = uuid.kicad_mod
    inductor_data['footprint'] = {'kicad':inductor_data['uuid'] + ".kicad_mod"}

        # Optional: Saturation Current
    if 'Saturation Current (Isat)' in attributes:
        saturation_current_value, saturation_current_unit = extract_value_and_unit(attributes['Saturation Current (Isat)'])
        inductor_data['saturation_current'] = process_physical_attribute(saturation_current_value, saturation_current_unit, min_val=0)

    # Optional: Resistance
    if 'DC Resistance (DCR)' in attributes:
        resistance_value, resistance_unit = extract_value_and_unit(attributes['DC Resistance (DCR)'])
        inductor_data['resistance'] = process_physical_attribute(resistance_value, resistance_unit, tolerance=10)

    return inductor_data

def parse_diode_category(description):
    # Mapping of keywords to diode category names
    category_mapping = {
        "Schottky Barrier Diodes (SBD)": "schottky",
        "Fast Recovery Rectifiers": "fast_recovery",
        "Zener Diodes": "zener",
        "TVS": "tvs",
        "General Purpose": "general_purpose",
        "Switching Diode": "switching_diode"
    }

    for keyword, category in category_mapping.items():
        if keyword in description:
            return category

    return "unknown"  # Return 'unknown' or None if no category matches



def create_diode_data(html):
    attributes = extract_attribute_data(html)
    details = extract_product_details(html)

    # filter out dual diodes
    if 'dual' in details['Description'].lower():
        print("Dual diode found, skipping")
        return None

    diode_data = {
        'uuid': generate_uuid(),
        'manufacturer': details['Manufacturer'],
        'lcsc_id': details['JLCPCB Part #'],
        'package': details['Package'],
        'description': details['Description'],
        'stock': extract_stock(html),
        'price': extract_prices(html),
        'type': 'diode',
        'category': parse_diode_category(details['Description'])
    }
    # set the footprint name = uuid.kicad_mod
    diode_data['footprint'] = {'kicad':diode_data['uuid'] + ".kicad_mod"}

    # print("Getting footprint data for: ", details['JLCPCB Part #'])
    diode_data['footprint_data'] = {"kicad": get_footprint_data(details['JLCPCB Part #'])}
        # Optional: Saturation Current
    if 'Reverse Voltage (Vr)' in attributes:
        saturation_current_value, saturation_current_unit = extract_value_and_unit(attributes['Reverse Voltage (Vr)'])
        diode_data['reverse_voltage'] = process_physical_attribute(saturation_current_value, saturation_current_unit, tolerance=10)

    if 'Power Dissipation' in attributes:
        saturation_current_value, saturation_current_unit = extract_value_and_unit(attributes['Power Dissipation'])
        diode_data['power_dissipation'] = process_physical_attribute(saturation_current_value, saturation_current_unit, min_val=0)

    if 'Reverse Recovery Time (trr)' in attributes:
        saturation_current_value, saturation_current_unit = extract_value_and_unit(attributes['Reverse Recovery Time (trr)'])
        diode_data['reverse_recovery_time'] = process_physical_attribute(saturation_current_value, saturation_current_unit, tolerance=10)

    if 'Average Rectified Current (Io)' in attributes:
        saturation_current_value, saturation_current_unit = extract_value_and_unit(attributes['Average Rectified Current (Io)'])
        diode_data['average_rectified_current'] = process_physical_attribute(saturation_current_value, saturation_current_unit, tolerance=10)

    if 'Reverse Leakage Current' in attributes:
        reverse_leakage = attributes['Reverse Leakage Current'].split('@')[0]
        saturation_current_value, saturation_current_unit = extract_value_and_unit(reverse_leakage)
        diode_data['reverse_leakage_current'] = process_physical_attribute(saturation_current_value, saturation_current_unit, tolerance=10)

    if 'Zener Impedance (Zzt)' in attributes:
        saturation_current_value, saturation_current_unit = extract_value_and_unit(attributes['Zener Impedance (Zzt)'])
        diode_data['impedance'] = process_physical_attribute(saturation_current_value, saturation_current_unit, tolerance=10)

    if 'Forward Voltage (Vf@If)' in attributes:
        vf = attributes['Forward Voltage (Vf@If)'].split('@')[0]
        saturation_current_value, saturation_current_unit = extract_value_and_unit(vf)
        diode_data['forward_voltage'] = process_physical_attribute(saturation_current_value, saturation_current_unit, tolerance=10)

    if 'Zener Voltage (Range)' in attributes:
        min_val, max_val = attributes['Zener Voltage (Range)'].split('~')
        max_val, unit = extract_value_and_unit(max_val)
        min_val, unit = extract_value_and_unit(min_val)
        diode_data['forward_voltage'] = process_physical_attribute(max_val, unit, min_val=min_val)
    elif 'Zener Voltage (Nom)' in attributes:
        saturation_current_value, saturation_current_unit = extract_value_and_unit(attributes['Zener Voltage (Nom)'])
        diode_data['forward_voltage'] = process_physical_attribute(saturation_current_value, saturation_current_unit, tolerance=10)


    return diode_data



def upload_to_db(table, data):
    service_account_path = "/Users/narayanpowderly/Documents/atopile-workspace/package-registry-backend/atopile-880ca67acfe2.json"
    if not firebase_admin._apps:  # Check if already initialized to prevent reinitialization
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)

    # Connect to Firestore
    db = firestore.client()

    # name should be the uuid of the component
    name = data['uuid']

    # Create a reference to the document
    doc_ref = db.collection(table).document(name)

    # Write the document to the database
    doc_ref.set(data)