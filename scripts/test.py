import requests

# Replace this with your function's URL
url = "https://get-component-atsuhzfd5a-uc.a.run.app"

# JSON payload
# payload = {
#     "type": "Capacitor",
#     "min_value": 0.0000000008,
#     "max_value": 0.0000000014,
#     # "package": "R0805"
# }
# payload = {
#     "type": "mosfet",
#     "polarity": "N Channel",
#     "drain_source_voltage_V": 21,
#     "current_A": 2,
#     "on_resistance_ohms": 2,
#     "power_dissipation_W": 2
# }

payload = {
    "type": "mosfet",
    "polarity": "N Channel",
    "drain_source_voltage_V": 20,
    "current_A": 20,
    "on_resistance_ohms": 0.1,
    "power_dissipation_W": 23,
    "Package": "PDFN-8(5.2x6.2)"
}
# Make the POST request
response = requests.post(url, json=payload)

# Print the response
print("Status Code:", response.status_code)
print("JLCPN:", response.json()['Best Component']['LCSC Part #'])
# print(response.text)
