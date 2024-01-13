from firebase_admin import initialize_app
from components import get_component
from package_index import package
import logging

logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

app = initialize_app()
