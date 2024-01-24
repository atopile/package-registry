from firebase_admin import initialize_app
from components import *
from package_index import *
import logging

logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

app = initialize_app()
