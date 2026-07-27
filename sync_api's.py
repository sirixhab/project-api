# not just reading one API and printing it; you're translating one API's data model into another API's data model
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()














# NOTE:
# -> it introduces schema mapping -- GitHub's issue JSON and Trello's card JSON look nothing alike, 
#    even though they represent similar ideas ("a thing that needs to be tracked").
# -> This translation layer — deciding how one system's fields map to another's, and 
#    handling fields that don't have a direct equivalent — is the actual skill this project teaches. 
#    It's exactly what you'd do connecting a CRM to a support ticketing system, or a payment provider to an internal ledger.