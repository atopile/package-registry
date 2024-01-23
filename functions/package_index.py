# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
import json
import logging
import re
from typing import Any

import google.cloud.firestore
import requests

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import firestore
from firebase_functions import https_fn, options

log = logging.getLogger(__name__)


@https_fn.on_request()
def get_package(req: https_fn.Request) -> https_fn.Response:
    # Parse the JSON request
    db: google.cloud.firestore.Client = firestore.client()
    req_json = req.get_json() or {}

    name = req_json["name"]

    doc = db.collection("packages").document(name).get()

    if not doc.exists:
        raise https_fn.HttpsError(
            https_fn.FunctionsErrorCode.NOT_FOUND, f'Package "{name}" not found'
        )

    # Send back a message that we've successfully written the message
    return {"data": doc.to_dict()}


@https_fn.on_request()
def list_packages(req: https_fn.Request) -> https_fn.Response:
    """
    List all the packages in the database.
    FIXME: this isn't remotely scalble, but it's fine for now.
    """
    db: google.cloud.firestore.Client = firestore.client()
    docs = db.collection("packages").stream()
    return {"data": [doc.to_dict() for doc in docs]}


@https_fn.on_request()
def add_package(req: https_fn.Request) -> https_fn.Response:
    # Parse the JSON request
    req_json = req.get_json()
    if not req_json:
        return https_fn.Response("No JSON body provided", status=400)

    name: str = req_json["name"]
    # Check the name is alphanumeric or underscore or dash only
    if re.compile(r"[^a-zA-Z0-9_-]").search(name):
        return https_fn.Response(
            f'Invalid package name "{name}". Only alphanumeric, dashes, and underscores are allowed.',
            status=400,
        )

    db: google.cloud.firestore.Client = firestore.client()

    # Make sure a package under that name doesn't already exist
    if db.collection("packages").document(name).get().exists:
        return https_fn.Response(f'Package "{name}" already exists', status=400)

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
    return https_fn.Response()
