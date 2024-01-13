# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
import google.cloud.firestore
import requests

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import firestore
from firebase_functions import https_fn, options
import logging


log = logging.getLogger(__name__)


def get_package(req: https_fn.Request) -> https_fn.Response:
    # Parse the JSON request
    req_json = req.get_json()
    if not req_json:
        return https_fn.Response("No JSON body provided", status=400)
    name = req_json["name"]

    log.debug(f"Getting package {name}")
    db: google.cloud.firestore.Client = firestore.client()

    doc = db.collection("packages").document(name).get()

    if not doc.exists:
        return https_fn.Response(f"Package \"{name}\" not found", status=404)

    # Send back a message that we've successfully written the message
    return doc.to_dict()


def post_package(req: https_fn.Request) -> https_fn.Response:
    # Parse the JSON request
    req_json = req.get_json()
    if not req_json:
        return https_fn.Response("No JSON body provided", status=400)

    name = req_json["name"]
    db: google.cloud.firestore.Client = firestore.client()

    # Make sure a package under that name doesn't already exist
    if db.collection("packages").document(name).get().exists:
        return https_fn.Response(f"Package \"{name}\" already exists", status=400)

    # Get the README
    repo_url = req_json["repo_url"]
    try:
        protocol, _, github_dot_com, github_user, github_repo, *_ = repo_url.split("/")
        if not (protocol == "https:" and github_dot_com == "github.com"):
            raise ValueError
    except ValueError:
        return https_fn.Response(
            f"Invalid repo URL {repo_url}. Only Github is supported for the moment",
            status=400,
        )

    r = requests.get(
        f"https://raw.githubusercontent.com/{github_user}/{github_repo}/main/README.md",
        timeout=5,
    )

    if r.status_code != 200:
        log.warning(f"Could not get README from {repo_url}")
        readme = "Create a REAMDE.md"
    else:
        readme = r.text

    # Add the package to the database
    doc = db.collection("packages").document(name)
    doc.set(
        {
            "name": name,
            "repo_url": repo_url,
            "description": readme,
        }
    )

    # Send back a message that we've successfully written the message
    return https_fn.Response("Package added")


@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def package(req: https_fn.Request) -> https_fn.Response:
    """Update the package referenced by this request."""
    if req.method == "GET":
        return get_package(req)
    elif req.method == "POST":
        return post_package(req)
    else:
        return https_fn.Response("Invalid method", status=400)
