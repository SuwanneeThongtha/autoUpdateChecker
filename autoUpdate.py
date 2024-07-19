import os
import datetime
import requests
import pickle

# Google Drive public link
GOOGLE_DRIVE_LINK = "https://drive.google.com/uc?export=download&id=1tuEWr7LQ5_6CRzLxjghG4tNvvekKa0ZA"

# Function to get the path from the file name.
def find_file(search_dir, file_name):
    for root, dirs, files in os.walk(search_dir):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

# Function to compare a local file with a file on Google Drive.
def check_file_update(file_path):
    try:
        # Get local file modification time
        local_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        local_mod_time = local_mod_time.replace(microsecond=0)  # Remove microseconds for comparison
        
        # Get Google Drive file
        response = requests.head(GOOGLE_DRIVE_LINK, allow_redirects=True)
        if response.status_code == 200:
            drive_mod_time = datetime.datetime.strptime(response.headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S %Z')
            drive_mod_time = drive_mod_time.replace(tzinfo=None)

            print(f"Local file last modified: {local_mod_time}")
            print(f"Google Drive file last modified: {drive_mod_time}")

            if local_mod_time > drive_mod_time:
                print("Local file is newer")
            elif local_mod_time < drive_mod_time:
                print("Google Drive file is newer")
            else:
                print("Both files have the same modification time")
        else:
            print(f"Failed to access Google Drive file. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Local file path
    file_name = "file_version.txt"
    search_dir = "D:\\autoUpdateChecker"
    LOCAL_FILE_PATH = find_file(search_dir, file_name)
    
    if LOCAL_FILE_PATH:
        print("file name: ", LOCAL_FILE_PATH)
        check_file_update(LOCAL_FILE_PATH)
    else:
        print("File not found.")
    
    # Keep the cmd window open
    os.system("pause")

if __name__ == "__main__":
    main()
