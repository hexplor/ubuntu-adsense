# Display Google AdSense Earnings on GNOME Taskbar

This project provides a Python script that displays your Google AdSense earnings on the GNOME taskbar in Ubuntu, using the Argos extension. It allows you to monitor your AdSense earnings in real-time without needing to log into your AdSense account.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [1. Set Up Google AdSense API Access](#1-set-up-google-adsense-api-access)
  - [2. Install Required Python Libraries](#2-install-required-python-libraries)
  - [3. Install Argos GNOME Shell Extension](#3-install-argos-gnome-shell-extension)
  - [4. Set Up the Script](#4-set-up-the-script)
  - [5. Authenticate with Google AdSense](#5-authenticate-with-google-adsense)
- [Usage](#usage)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Features

- **Real-Time Earnings Display:** Shows your current day's Google AdSense earnings directly on the GNOME taskbar.
- **Automatic Updates:** The script refreshes at a specified interval, ensuring your earnings are up-to-date.
- **Secure Authentication:** Uses OAuth 2.0 for secure access to your AdSense data.
- **Customizable:** Easily adjust the update frequency and display icons to suit your preferences.

## Prerequisites

- **Ubuntu** with the GNOME desktop environment.
- **Python 3** installed.
- A **Google AdSense** account with API access.
- **Argos** GNOME Shell extension.
- Basic knowledge of using the terminal.

## Installation

### 1. Set Up Google AdSense API Access

#### a. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click on **Select a project** > **New Project**.
3. Enter a project name (e.g., `AdSenseTaskbarDisplay`) and click **Create**.

#### b. Enable the AdSense Management API

1. In the Cloud Console, navigate to **APIs & Services** > **Library**.
2. Search for **AdSense Management API**.
3. Click on it and then click **Enable**.

#### c. Create OAuth 2.0 Credentials

1. Go to **APIs & Services** > **Credentials**.
2. Click **Create Credentials** > **OAuth client ID**.
3. Select **Desktop app** as the application type.
4. Enter a name (e.g., `AdSenseTaskbarApp`) and click **Create**.
5. Click **Download JSON** to get your `client_secret.json` file.
6. Save this file in a secure location (e.g., `/home/yourusername/client_secret.json`).

### 2. Install Required Python Libraries

Open a terminal and run:

```bash
sudo pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 3. Install Argos GNOME Shell Extension

#### a. Install Argos

1. Visit the [Argos extension page](https://extensions.gnome.org/extension/1176/argos/) on the GNOME Extensions website.
2. Toggle the switch to **ON** to install it.

#### b. Install GNOME Extensions Support (if needed)

If you cannot install extensions from the browser, install the GNOME Shell integration package:

```bash
sudo apt install chrome-gnome-shell
```

### 4. Set Up the Script

#### a. Create the Argos Scripts Directory

```bash
mkdir -p ~/.config/argos
```

#### b. Download or Create the Script

Create a new file named `adsense.1h.py` in `~/.config/argos/`:

```bash
nano ~/.config/argos/adsense.1h.py
```

Paste the following code into the file:

```python
#!/usr/bin/python3

import os
import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Paths to your credentials
CLIENT_SECRETS_FILE = '/home/yourusername/client_secret.json'  # Update with your actual path
TOKEN_JSON = '/home/yourusername/token.json'  # Update with your actual path

# AdSense API scope
SCOPES = ['https://www.googleapis.com/auth/adsense.readonly']

def get_service():
    creds = None
    if os.path.exists(TOKEN_JSON):
        creds = Credentials.from_authorized_user_file(TOKEN_JSON, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_JSON, 'w') as token:
            token.write(creds.to_json())
    service = build('adsense', 'v2', credentials=creds)
    return service

def main():
    try:
        service = get_service()

        # Use your AdSense account ID directly
        account_id = 'accounts/pub-XXXXXXXXXXXXXXXX'  # Replace with your actual account ID

        # Generate the report for today's earnings
        today = datetime.date.today()
        report_request = {
            'dateRange': {
                'startDate': {
                    'year': today.year,
                    'month': today.month,
                    'day': today.day
                },
                'endDate': {
                    'year': today.year,
                    'month': today.month,
                    'day': today.day
                }
            },
            'metrics': ['ESTIMATED_EARNINGS']
        }

        # Call the API to generate the report
        report = service.accounts().reports().generate(
            account=account_id,
            body=report_request
        ).execute()

        # Extract earnings from the report
        earnings = report['totals']['cells'][0]['value']
        currency_code = report['headers'][0]['currencyCode']
        print(f"💰 AdSense Today: {earnings} {currency_code}")

    except Exception as e:
        # Handle exceptions and display errors in Argos dropdown
        print("AdSense Earnings")
        print("---")
        print("Error fetching earnings:")
        print(str(e))

if __name__ == '__main__':
    main()
```

**Important:**

- Replace `/home/yourusername/client_secret.json` and `/home/yourusername/token.json` with the actual paths to your `client_secret.json` and desired location for `token.json`.
- Replace `'accounts/pub-XXXXXXXXXXXXXXXX'` with your actual AdSense account ID (e.g., `'accounts/pub-1234567890123456'`).

#### c. Make the Script Executable

```bash
chmod +x ~/.config/argos/adsense.1h.py
```

### 5. Authenticate with Google AdSense

The first time you run the script, it needs to authenticate with your Google account.

#### a. Run the Script Manually

```bash
~/.config/argos/adsense.1h.py
```

- A browser window will open prompting you to log in to your Google account and grant permissions.
- After authentication, the script will save the credentials to `token.json`.

## Usage

- The script will display your AdSense earnings on the GNOME taskbar.
- Argos will automatically execute the script every hour, as indicated by `.1h` in the script name.
- To refresh the display manually, you can click on the Argos icon and select **Refresh** or reload GNOME Shell.

## Customization

- **Update Frequency:** Change `.1h` in the script name to `.30m` for every 30 minutes, `.5m` for every 5 minutes, etc.
  - For example, to refresh every 30 minutes, rename the script to `adsense.30m.py`.
- **Icon Customization:** Edit the `print` statement in the script to change the icon or text.
  - Replace `💰` with any other icon or text you prefer.

## Troubleshooting

- **Script Not Displayed on Taskbar:**
  - Ensure the script is executable and located in `~/.config/argos/`.
  - Verify that Argos extension is installed and enabled.
  - Reload GNOME Shell by pressing `Alt + F2`, typing `r`, and pressing `Enter`.
- **Authentication Issues:**
  - Delete `token.json` and rerun the script to re-authenticate.
    ```bash
    rm /home/yourusername/token.json
    ~/.config/argos/adsense.1h.py
    ```
- **API Errors:**
  - Ensure the AdSense Management API is enabled in your Google Cloud project.
  - Verify that your AdSense account is active and has the necessary permissions.
- **Script Displays Filename Instead of Earnings:**
  - Ensure the script outputs the earnings on the first line.
  - Check that all file paths in the script are absolute and correct.
  - Make sure all required Python libraries are installed system-wide.

## Security Considerations

- **Protect Your Credentials:**
  - Keep `client_secret.json` and `token.json` in a secure location.
  - Ensure file permissions prevent unauthorized access.
- **Do Not Share Sensitive Information:**
  - Avoid committing `client_secret.json` or `token.json` to version control systems like GitHub.

## Acknowledgments

- **Argos Extension:** [Argos](https://extensions.gnome.org/extension/1176/argos/) by Pablo Bortolameotti.
- **Google APIs Client Library for Python:** [google-api-python-client](https://github.com/googleapis/google-api-python-client).
- **Google AdSense Management API:** [AdSense Management API v2](https://developers.google.com/adsense/management/reference/rest/v2).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
