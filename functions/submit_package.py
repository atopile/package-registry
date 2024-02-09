import json
from firebase_admin import firestore, initialize_app
from firebase_functions import firestore_fn, https_fn
import requests  # Make sure requests is installed

firestore_client = firestore.client()

@https_fn.on_request()
def submit_package(request, firestore_client=firestore_client):
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
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
        data = req_json.get("data", {})

        print("data: ", req_json)

        package_data = {
            "url": req_json.get("url"),
            "email": req_json.get("email"),
            "description": req_json.get("description"),
            "submittedAt": firestore.SERVER_TIMESTAMP
        }

        print("package_data: ", package_data)
        firestore_client.collection('packageSubmissions').add(package_data)

        # Send notification to Discord
        discord_webhook_url = 'https://discord.com/api/webhooks/1205617728921010237/F7mmOwdn6TeWaZuM963uqQx2FoHccRMcB0eBSGIb5uhT-2GB4_Ch6Z5zWt-dEDlKXeDu'
        discord_message = {
            "content": f"New package submission: {req_json.get('description')} from {req_json.get('email')}"
        }
        response = requests.post(discord_webhook_url, json=discord_message)
        if response.status_code != 204:
            print(f"Failed to send message to Discord, status code: {response.status_code}")

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
