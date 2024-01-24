from tools import *
import firebase_admin
from firebase_admin import credentials, firestore


service_account_path = "/Users/narayanpowderly/Documents/atopile-workspace/package-registry-backend/atopile-880ca67acfe2.json"

if not firebase_admin._apps:  # Check if already initialized to prevent reinitialization
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)


db = firestore.client()
unparsed_parts = db.collection(
    "unparsed-parts"
)

# convert to dict
results = unparsed_parts.stream()
components = [doc.to_dict() for doc in results]
print(len(components))


inductors = []
for component in components:
    if "Power Inductors" in component["Description"]:
        inductors.append(component)

print(len(inductors))

inductors = inductors[15:-1]

for inductor in inductors:
        try:
            # get component data
            print("Getting data for: ", inductor["JLCPCB Part #"])
            page = get_html(lcsc_id=inductor["JLCPCB Part #"])

            # check type:
            get_type(page)

            data = (create_inductor_data(page))

            upload_to_db("component_data",data)

            # log file to csv of parsed parts to prevent re-parsing
            upload_to_db("parsed-parts",data)

        except Exception as e:
            print(e)
            continue
