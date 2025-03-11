import os
from boxsdk import Client, OAuth2
#using a private key for Auth instead of developer token since (it is only cvalid for 60 mins)
#from boxsdk import Client, JWTAuth
import subprocess

FOLDER_ID = "140279085571"


def download_files_from_folder(client,videos):
    folder = client.folder(folder_id=FOLDER_ID).get()
    print(f'The folder is owned by: {folder.owned_by["login"]}')

    items = folder.get_items(limit=100, offset=0)

    folder_path = 'videos/'
    #get a list of all the files in the folder
    files = os.listdir(folder_path)
    #filter the list to include only .mp4 files
    downloaded_files = [file for file in files if file.endswith(".mp4")]
        
    for item in items:
        if item.name.replace('.mp4','') in videos and f'vd#{item.name}' not in downloaded_files:
            print("Downloading file: " + item.name)
            download_url = client.file(item.id).get_download_url()
            subprocess.call(f"wget {download_url}", shell=True)
            subprocess.call(f"mv download videos/vd#{item.name}", shell=True)


def main():
    #auth = JWTAuth.from_settings_file("Auth.json")
    auth = OAuth2(
        access_token="PEzLdrrPEjS4FEhaudqH7BGitPKRAtLG",
        client_id="ruw8s0v0hvwhjce1wmp9l01q31ab711l",
        client_secret="8MpHOS2xpsayQZOYJUJpLvx9QmROO34K",
    )
    client = Client(auth)

    with open("names_rest.txt", "r") as names_file:
        videos = names_file.read().split("\n")
    print(len(videos))

    download_files_from_folder(client,videos)
    os._exit(0)


if __name__ == "__main__":
    main()

