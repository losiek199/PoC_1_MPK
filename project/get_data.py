import requests
import os
import zipfile

"""
module responsible for downloading data
from mpk wroclaw site, file downloaded from provided endpoint"""
TEMP = 'unpacked'

def create_dir(path):
    """creates directory on local system"""
    print('Creating dir:', path)
    os.mkdir(path)

def assign_dir_privelages(path, mode=0o777):
    """assign needed privelages to directory"""
    for root, dir, files in os.walk(path, topdown=False):
        for dir in [os.path.join(root, d) for d in dir]:
            os.chmod(dir, mode)
            print('Permission granted:', dir)
        for file in [os.path.join(root, f) for f in files]:
            os.chmod(file, mode)
            print('Permission granted:', file)


def download_file(file_url, save_path, tmp_path):
    """downloads file from URL into target location"""
    req = requests.get(file_url, allow_redirects=True)
    #check status
    req.raise_for_status()
    #write file
    try:
        with open(save_path, 'wb') as file:
            for chunk in req.iter_content():
                file.write(chunk)
    #unpacking zipped file
        return unzip_file(save_path, tmp_path)
    except PermissionError:
        assign_dir_privelages(save_path)
        download_file(file_url, save_path)

def unzip_file(file_path, tmp_path):
    """unpack file into temporary directory and remove source file afterwards, returns directory where files were unpacked"""
    #unpack destination
    write_path = os.path.join(os.path.join(os.getcwd(), tmp_path, TEMP))
    #check dir existance and create if needed
    try:
        if not os.path.exists(write_path):
            create_dir(write_path)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(write_path)
        os.remove(file_path)
        return write_path
    except PermissionError as e:
        print('Permission error:', e)
        assign_dir_privelages(write_path)
        unzip_file(file_path)

def delete_file(file_path):
    """deletes file at specified file_path"""
    os.remove(file_path)

def load_data_from_url(url, directory, tmp_path):
    """downloads data from given url and ordres truncate load to DB"""
    # download files
    unpacked_dir = download_file(url, directory, tmp_path)
    return unpacked_dir

