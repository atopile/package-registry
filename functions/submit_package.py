import json
from firebase_admin import firestore, initialize_app
from firebase_functions import firestore_fn, https_fn


firestore_client = firestore.client()

@https_fn.on_request()
def submit_package(request, firestore_client=firestore_client):
    try:
        req_json = request.get_json()
        print("Received package submission request with data:", req_json)

        # Extracting the 'data' object from the request JSON
        data = req_json.get("data", {})

        print("data: ", data)

        package_data = {
            "url": data.get("url"),
            "email": data.get("email"),
            "description": data.get("description"),
            "submittedAt": firestore.SERVER_TIMESTAMP
        }

        print("package_data: ", package_data)
        firestore_client.collection('packageSubmissions').add(package_data)
        return https_fn.Response(
            json.dumps({"data": {"message": "Package submitted successfully."}}),
            status=200,
            content_type='application/json',
        )

    except firestore.ClientError as e:
        print(f"Firestore client error: {str(e)}")
        return https_fn.Response(
            json.dumps({"error": "There was an issue with Firestore. Please try again later."}),
            status=500,
            content_type='application/json',
        )
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return https_fn.Response(
            json.dumps({"error": "Invalid JSON format. Please check your request payload."}),
            status=400,
            content_type='application/json',
        )
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return https_fn.Response(
            json.dumps({"error": "An unexpected error occurred. Please try again later."}),
            status=500,
            content_type='application/json',
        )
