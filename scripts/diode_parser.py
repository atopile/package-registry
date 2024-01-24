import threading
from tools import *
import firebase_admin
from firebase_admin import credentials, firestore
from rich import print

def process_diode_chunk(diode_chunk):
    for diode in diode_chunk:
        try:
            print("Getting data for: ", diode["JLCPCB Part #"])
            page = get_html(lcsc_id=diode["JLCPCB Part #"])
            get_type(page)
            data = create_diode_data(page)
            upload_to_db("component_data", data)
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

# convert to dict
results = unparsed_parts.stream()
components = [doc.to_dict() for doc in results]
diodes = [component for component in components if "Diode" in component["Description"]]
# diodes = diodes[15:35]  # Limit for testing

# Parameters for threading
num_threads = 50  # Adjust as needed
chunk_size = len(diodes) // num_threads

# Create threads
threads = []
for diode_chunk in divide_chunks(diodes, chunk_size):
    thread = threading.Thread(target=process_diode_chunk, args=(diode_chunk,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("All threads have completed.")
