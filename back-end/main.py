import logging
from firebase_admin import initialize_app

logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])
app = initialize_app()


# Last, import all the other functions
from components import *
from package_index import *
from submit_package import *
