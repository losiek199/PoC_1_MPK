import get_data
import os


TEMP_URL_PLACEHOLDER = 'https://www.wroclaw.pl/open-data/87b09b32-f076-4475-8ec9-6020ed1f9ac0/OtwartyWroclaw_rozklad_jazdy_GTFS.zip'
TEMP_SAVE_PATH = 'tmp'
TEMP_DIR_NAME = 'downloadedFiles.zip'
file_destination = os.path.join(os.getcwd(),TEMP_SAVE_PATH,TEMP_DIR_NAME)

def create_dir(path):
    print('Creating dir:', path)
    os.mkdir(path)

def assign_dir_privelages(path, mode=0o777):
    for root, dir, files in os.walk(path, topdown=False):
        for dir in [os.path.join(root,d) for d in dir]:
            os.chmod(dir, mode)
            print('Permission granted:', dir)
        for file in [os.path.join(root,f) for f in files]:
            os.chmod(file, mode)
            print('Permission granted:', file)
def main():
    try:
        get_data.download_file(TEMP_URL_PLACEHOLDER, file_destination)
    except Exception as e:
        raise(e)


if __name__ == '__main__':
    download_path = os.path.join(os.getcwd(), TEMP_SAVE_PATH)
    if not os.path.exists(download_path):
        create_dir(download_path)

    main()