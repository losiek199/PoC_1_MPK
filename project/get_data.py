import requests
import os
import zipfile
import app

"""
module responsible for downloading data
from mpk wroclaw site, file downloaded from provided endpoint"""
TEMP = 'unpacked'

def download_file(file_url, save_path):
    """downloads file into target location"""
    req = requests.get(file_url, allow_redirects=True)
    #check status
    req.raise_for_status()
    #write file
    try:
        with open(save_path, 'wb') as file:
            for chunk in req.iter_content():
                file.write(chunk)
    #unpacking zipped file
        return unzip_file(save_path)
    except PermissionError:
        app.assign_dir_privelages(save_path)
        download_file(file_url, save_path)

def unzip_file(file_path):
    """unpack file into temporary directory and remove source file afterwards"""
    #unpack destination
    write_path = os.path.join(os.path.join(os.getcwd(), app.TEMP_SAVE_PATH, TEMP))
    #check dir existance and create if needed
    try:
        if not os.path.exists(write_path):
            app.create_dir(write_path)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(write_path)
        os.remove(file_path)
        return write_path
    except PermissionError as e:
        print('Permission error:', e)
        app.assign_dir_privelages(write_path)
        unzip_file(file_path)


