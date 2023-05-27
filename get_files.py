import os
import datetime
import requests
import time
from getpass import getpass

# Prompt user for API token and month
api_token = getpass("Enter your API token: ")
month = input("Enter the month (e.g., January, February, etc.): ")

# Get the start and end dates of the month
current_year = datetime.datetime.now().year
start_date = datetime.datetime.strptime(f"{month} {current_year}", "%B %Y")
end_date = start_date + datetime.timedelta(days=31)

# Format dates in ISO 8601 format
start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# Construct the JSON payload
payload = {
    "StartDate": start_date_str,
    "EndDate": end_date_str,
    "Status": "Completed"
}

# Make the API request
url = "https://sicredi.signanywhere.com/api/v6/envelope/find"
headers = {
    "apitoken": api_token,
    "Accept": "application/json"
}
response = requests.post(url, headers=headers, json=payload)

try:
    response.raise_for_status()
    data = response.json()

    # Check if envelopes are empty
    if not data['Envelopes']:
        print("No envelopes found for the given month.")
    else:
        # Create a folder for the month if it doesn't exist
        folder_name = month.lower()
        os.makedirs(folder_name, exist_ok=True)

        # Loop through the envelopes
        for envelope in data['Envelopes']:
            envelope_id = envelope['Id']
            print(f"Processing envelope with ID: {envelope_id}")

            # Make the GET request to retrieve envelope files
            files_url = f"https://sicredi.signanywhere.com/api/v6/envelope/{envelope_id}/files"
            files_headers = {
                "apitoken": api_token,
                "Accept": "application/json"
            }
            files_response = requests.get(files_url, headers=files_headers)
            files_response.raise_for_status()
            files_data = files_response.json()

            # Extract the FileIds from the response and download the files
            if 'Documents' in files_data:
                for document in files_data['Documents']:
                    file_id = document['FileId']
                    print(f"Downloading document file with ID: {file_id}")

                    # Make the GET request to download the file
                    download_url = f"https://sicredi.signanywhere.com/api/v6/file/{file_id}"
                    download_headers = {
                        "apitoken": api_token,
                        "Accept": "application/octet-stream"
                    }
                    download_response = requests.get(download_url, headers=download_headers)
                    download_response.raise_for_status()

                    # Get the file extension from the response content-type header
                    content_type = download_response.headers.get('content-type')
                    extension = content_type.split('/')[-1]

                    # Save the response content to a file with the correct extension
                    file_name = f"{folder_name}/{file_id}.{extension}"
                    with open(file_name, 'wb') as file:
                        file.write(download_response.content)

                    # Delay before the next request
                    time.sleep(1)

            # Extract the FileId from AuditTrail and download the file
            if 'AuditTrail' in files_data:
                audit_trail_file_id = files_data['AuditTrail'].get('FileId')
                if audit_trail_file_id:
                    print(f"Downloading audit trail file with ID: {audit_trail_file_id}")

                    # Make the GET request to download the audit trail file
                    download_url = f"https://sicredi.signanywhere.com/api/v6/file/{audit_trail_file_id}"
                    download_headers = {
                        "apitoken": api_token,
                        "Accept": "application/octet-stream"
                    }
                    download_response = requests.get(download_url, headers=download_headers)
                    download_response.raise_for_status()

                    # Get the file extension from the response content-type header
                    content_type = download_response.headers.get('content-type')
                    extension = content_type.split('/')[-1]

                    # Save the response content to a file with the correct extension
                    file_name = f"{folder_name}/{audit_trail_file_id}.{extension}"
                    with open(file_name, 'wb') as file:
                        file.write(download_response.content)

                    # Delay before the next request
                    time.sleep(1)

except requests.exceptions.HTTPError as errh:
    print("HTTP Error:", errh)
except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
except requests.exceptions.RequestException as err:
    print("Error:", err)
except KeyError:
    print("Error: Invalid response format.")
except ValueError:
    print("Error: Invalid response content.")
    