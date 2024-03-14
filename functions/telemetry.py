import json
from firebase_admin import initialize_app, firestore
from firebase_functions import https_fn

# Initialize Firebase Admin SDK
# Note: This assumes that you've already set up Firebase Admin SDK elsewhere in your project
# and that you do not need to call initialize_app() here if it's already been called.
try:
    initialize_app()
except ValueError:
    pass  # App is already initialized

firestore_client = firestore.client()



@https_fn.on_request()
def log_telemetry(request, firestore_client=firestore_client):
    # Check for POST request
    if request.method != "POST":
        return ("Please send a POST request", 405)

    # Parse JSON data from request
    try:
        data = request.get_json()
    except Exception as e:
        return (f"Invalid JSON: {str(e)}", 400)


    # Validate the data structure
    required_keys = ["project_id", "user_id", "git_hash", "ato_error", "crash"]

    # Validate top-level keys
    if not all(key in data for key in required_keys):
        return ("Missing required data fields", 400)


    # add a timestamp to the data
    data['timestamp'] = firestore.SERVER_TIMESTAMP
    # Store the validated data in the 'telemetry' collection
    try:
        doc_ref = firestore_client.collection('telemetry').document()
        doc_ref.set(data)
    except Exception as e:
        return (f"Failed to log telemetry data: {str(e)}", 500)

    return ("Telemetry data logged successfully", 200)
