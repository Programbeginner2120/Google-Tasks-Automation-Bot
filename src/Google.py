import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from schedule import every, repeat, run_pending
import logging
import Thread

logging.basicConfig(filename='./logging/bot_logging.log', encoding='utf-8', level=logging.DEBUG)
thread = None

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    pickle_file = f'./creds/token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    cred = None
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not (cred and cred.valid):
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        logging.error(e.__str__, e)
        logging.error(f'Failed to create service instance for {API_SERVICE_NAME}')
        os.remove(pickle_file)
        return None

@repeat(every().day.at("00:00"))
# @repeat(every(2).seconds)
def restore_oauth_creds():
    CLIENT_SECRET_FILE = './creds/client-secret-file.json'
    API_NAME = 'tasks'
    API_VERSION = 'v1'
    SCOPES = ['https://www.googleapis.com/auth/tasks']

    cred = None

    pickle_file = f'./creds/token_{API_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)
        if cred.expired:
            logging.debug("Deleting expired pickle file...")
            os.remove(os.path.join(os.getcwd(), pickle_file))
        if not cred.expired and cred.refresh_token:
            cred.refresh(Request())
            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)
            logging.debug(f"{pickle_file} refreshed!")
                
    else:
        logging.error("Failed to refresh auth token for some reason.")
        
    # thread = Thread.thread("scheduler thread", "1", restore_oauth_creds)
    # thread.start()
    # thread.join()


