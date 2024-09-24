#!/usr/bin/python3

import os
import datetime
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Paths to your credentials
CLIENT_SECRETS_FILE = '/home/karolorzel/client_secret.json'
TOKEN_PICKLE = '/home/karolorzel/token.pickle'

# AdSense API scope
SCOPES = ['https://www.googleapis.com/auth/adsense.readonly']

def get_service():
    creds = None
    # Load credentials from the pickle file if it exists
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    # If no valid credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for next time
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)
    service = build('adsense', 'v2', credentials=creds)
    return service

def main():
    try:
        service = get_service()

        # Get the AdSense account ID
        accounts_response = service.accounts().list().execute()

        # Get the AdSense account ID
        accounts = service.accounts().list().execute()
        account_id = accounts['accounts'][0]['name']

        # Get today's date
        today = datetime.date.today().isoformat()

        # Generate the report for today's earnings
        report = service.accounts().reports().generate(
            account=account_id,
            dateRange='TODAY',
            metrics=['ESTIMATED_EARNINGS']
        ).execute()

        earnings = report['totals']['cells'][0]['value']
        print(f"💰 AdSense Today: ${earnings}")
    except Exception as e:
        print("Error fetching earnings")
        print("---")

if __name__ == '__main__':
    main()
