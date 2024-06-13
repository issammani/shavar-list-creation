from configparser import ConfigParser
import sys
import os
from requests import auth

# For local testing purposes, make sure to set RS_TESTING_ENVIRONMENT to True,
# ENVIRONMENT to "dev", and EXECUTION_ENVIRONMENT to "GKE"

execution_environment = os.getenv("EXECUTION_ENVIRONMENT", "JENKINS")
# One of "userpass" or "token"
rs_auth_method = os.getenv("REMOTE_SETTINGS_AUTH_METHOD", "userpass")

config = ConfigParser(os.environ)
ini_file = "shavar_list_creation.ini"

# For local testing and GKE environments we want to use the rs_*.ini file
if execution_environment != "JENKINS":
    environment = os.getenv("ENVIRONMENT", "stage")
    ini_file = f"rs_{environment}.ini"

filenames = config.read(ini_file)

if not filenames:
    print(f"Error reading .ini file!", file=sys.stderr)
    sys.exit(-1)

# Class to handle Bearer Token Authentication
class BearerAuth(auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["Authorization"] = self.token
        return r