import threading
from tools import *
import firebase_admin
from firebase_admin import credentials, firestore
from rich import print

def process_chunk(component_chunk):
    for component in component_chunk:
        try:
            lcsc_id = component["JLCPCB Part #"]
            print("Getting data for: ", lcsc_id)
            # get footprint data
            footprint_data = get_footprint_data(lcsc_id)
            footprint = component["uuid"]
            # set footprint data and footprint
            component["footprint_data"] = {'kicad':footprint_data}
            component["footprint"] = {'kicad':footprint}
            upload_to_db("testin_123", component)
        except Exception as e:
            print(e)

def divide_chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

service_account_path = "/Users/narayanpowderly/Documents/atopile-workspace/package-registry-backend/atopile-880ca67acfe2.json"
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()
unparsed_parts = db.collection("unparsed-parts")

# load components from dont_have_footprint.txt
# ('C2620', None),
#  ('C2619', None),
# parse out the lcsc_id
dont_have_footprint = []
with open("dont_have_footprints.txt", "r") as f:
    for line in f:
        dont_have_footprint.append(line.strip().split(",")[0])

# print(dont_have_footprint)


# convert to dict
results = unparsed_parts.limit(19).stream()
components = [doc.to_dict() for doc in results]
# diodes = diodes[15:35]  # Limit for testing

# filter out components that have a footprint
filtered_components = [component for component in components if component["JLCPCB Part #"] not in dont_have_footprint]
print(len(filtered_components))
print(filtered_components)

# # Parameters for threading
# num_threads = 50  # Adjust as needed
# chunk_size = len(components) // num_threads

# # Create threads
# threads = []
# for chunk in divide_chunks(filtered_components, chunk_size):
#     thread = threading.Thread(target=process_chunk, args=(chunk,))
#     threads.append(thread)
#     thread.start()

# # Wait for all threads to complete
# for thread in threads:
#     thread.join()

# print("All threads have completed.")
