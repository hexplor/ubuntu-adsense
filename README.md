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

- **Ubuntu** (or other Linux distribution) with the GNOME desktop environment.
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
5. Enter a name (e.g., `AdSenseTaskbarApp`) and click **Create**.
6. Click **Download JSON** to get your `client_secret.json` file.
7. Save this file in a secure location (e.g., `/home/yourusername/client_secret.json`).

Note: If Google asks your for a consent app, create it first.

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

Eventually [follow official github install instructions](https://github.com/p-e-w/argos) to install Argos properly. 

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
#!/usr/bin/env python3

import os
import datetime
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Paths to your credentials
CLIENT_SECRETS_FILE = '/home/yourusername/client_secret.json'  # Update with your actual path
TOKEN_PICKLE = '/home/yourusername/token.pickle'               # Update with your actual path

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
        accounts = service.accounts().list().execute()
        account_id = accounts['accounts'][0]['name']

        # Generate the report for today's earnings
        report = service.accounts().reports().generate(
            account=account_id,
            dateRange='TODAY',
            metrics=['ESTIMATED_EARNINGS']
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

- Replace `/home/yourusername/client_secret.json` and `/home/yourusername/token.pickle` with the actual paths to your `client_secret.json` and desired location for `token.pickle`.
- Ensure that the shebang line (`#!/usr/bin/env python3`) points to the correct Python interpreter.

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
- After authentication, the script will save the credentials to `token.pickle`.

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
  - Delete `token.pickle` and rerun the script to re-authenticate.
    ```bash
    rm /home/yourusername/token.pickle
    ~/.config/argos/adsense.1h.py
    ```
- **API Errors:**
  - Ensure the AdSense Management API is enabled in your Google Cloud project.
  - Verify that your AdSense account is active and has the necessary permissions.
- **Script Displays Filename Instead of Earnings:**
  - Ensure the script outputs the earnings on the first line.
  - Check that all file paths in the script are absolute and correct.
  - Make sure all required Python libraries are installed system-wide.
- **Python Dependencies Not Found:**
  - If the script works when run manually but not with Argos, ensure that the Python libraries are installed in the system's Python environment.
    ```bash
    sudo pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```
- **Shebang Line Issues:**
  - Ensure the shebang line at the top of the script points to the correct Python interpreter.
    - Use `#!/usr/bin/env python3` for the system's default Python 3.
    - If using a virtual environment, provide the absolute path to the Python interpreter.

## Security Considerations

- **Protect Your Credentials:**
  - Keep `client_secret.json` and `token.pickle` in a secure location.
  - Ensure file permissions prevent unauthorized access.
- **Do Not Share Sensitive Information:**
  - Avoid committing `client_secret.json` or `token.pickle` to version control systems like GitHub.
  - Use placeholders or examples when sharing paths and account IDs.

## Acknowledgments

- **Argos Extension:** [Argos](https://extensions.gnome.org/extension/1176/argos/) by Pablo Bortolameotti.
- **Google APIs Client Library for Python:** [google-api-python-client](https://github.com/googleapis/google-api-python-client).
- **Google AdSense Management API:** [AdSense Management API v2](https://developers.google.com/adsense/management/reference/rest/v2).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Notes:**

- **Using `pickle` for Credentials:**
  - The script uses `pickle` to store OAuth 2.0 credentials.
  - Ensure that the `token.pickle` file is stored securely.
- **Python Interpreter Path:**
  - If you're using a specific Python environment (e.g., Anaconda), ensure the shebang line points to the correct interpreter.
    - For example: `#!/home/yourusername/miniconda3/bin/python3`
  - Adjust the shebang line accordingly if you encounter issues.

**Example of Adjusted Shebang Line:**

```python
#!/home/yourusername/miniconda3/bin/python3
```

- Replace `/home/yourusername/miniconda3/bin/python3` with the path to your Python interpreter.
