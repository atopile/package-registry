import json
from firebase_admin import firestore, initialize_app
from firebase_functions import firestore_fn, https_fn


firestore_client = firestore.client()

@https_fn.on_request()
def submit_package(request, firestore_client=firestore_client):
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type header
        # and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response(status=204, headers=headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    try:
        req_json = request.get_json()
        print("Received package submission request with data:", req_json)

        # Extracting the 'data' object from the request JSON
        # data = req_json.get("data", {}).get("data", {})
        data = firestore_fn.extract_data(request)
        data = data.get("data", {})

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
            headers=headers
        )

    except firestore.ClientError as e:
        print(f"Firestore client error: {str(e)}")
        return https_fn.Response(
            json.dumps({"error": "There was an issue with Firestore. Please try again later."}),
            status=500,
            content_type='application/json',
            headers=headers
        )
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return https_fn.Response(
            json.dumps({"error": "Invalid JSON format. Please check your request payload."}),
            status=400,
            content_type='application/json',
            headers=headers
        )
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return https_fn.Response(
            json.dumps({"error": "An unexpected error occurred. Please try again later."}),
            status=500,
            content_type='application/json',
            headers=headers
        )

