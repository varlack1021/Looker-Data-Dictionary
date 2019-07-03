from __future__ import print_function
import pickle
import time
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from lookerapi import LookerApi


class GoogleApi(object):

    def __init__(self, spreadsheetId):

    #Sets data of spreadsheets to be called once
    self.spreadsheetId = spreadsheetId
    self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
    self.service = " "
    self.requests = 0
    self.auth()
    self.spreadsheetData = self.service.spreadsheets().get(
    spreadsheetId = spreadsheetId).execute()

    def auth(self):

    creds = None


    if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
    creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:

    if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())

    else:
    flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', self.scopes)
    creds = flow.run_local_server()

    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
    pickle.dump(creds, token)

    self.service = build('sheets', 'v4', credentials=creds)


##-- Creates in a new sheet in a given spreadsheet 
def create_sheet(self, title):

spreadsheet = {

    "requests": [
        {
        "addSheet": {
            "properties": {
            "title": title,
            "gridProperties": {
                "frozenRowCount": 1 
                    }    
                }
            }
        }
    ]
}

spreadsheet = self.service.spreadsheets().batchUpdate(spreadsheetId = self.spreadsheetId,
body = spreadsheet
).execute()

#Resizes the length of each columns by the data in them
#Assumes both spreadsheets has the same amount of sheets
#Sleeps the program to not exceed api call of 100 rquests/100 seconds
def auto_resize(self):

resize = {
    "requests": [
    {
        "autoResizeDimensions": {
            "dimensions": {
            "sheetId": "",
            "dimension": "COLUMNS",
            "startIndex": 0,
            "endIndex": 5
                }   
            }
        }
    ]
}

sheets = self.spreadsheetData["sheets"]


for index in range(len(sheets)):
    resize["requests"][0]["autoResizeDimensions"]["dimensions"]["sheetId"] = sheets[index]["properties"]["sheetId"] 
    self.service.spreadsheets().batchUpdate(spreadsheetId = self.spreadsheetId,
    body = resize).execute() 

    time.sleep(1.3)

##-- Writing to google sheets
def write(self, body, range_name, value_input_option):

    result = self.service.spreadsheets().values().update(
    spreadsheetId=self.spreadsheetId, range = range_name,
    valueInputOption=value_input_option, body=body).execute()


    time.sleep(1.4) 

##Checks to see if the given sheet name exists
def contains_sheet(self, sheet_name,):
    response = self.spreadsheetData

result = response["sheets"]

for index in range (len(result)):
    title = result[index]["properties"]["title"]
    if title == sheet_name: return True
