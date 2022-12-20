import get_data
import db_controller
import api_handler
import os


TEMP_URL_PLACEHOLDER = 'https://www.wroclaw.pl/open-data/87b09b32-f076-4475-8ec9-6020ed1f9ac0/OtwartyWroclaw_rozklad_jazdy_GTFS.zip'
TEMP_SAVE_PATH = 'tmp'
TEMP_DIR_NAME = 'downloadedFiles.zip'
file_destination = os.path.join(os.getcwd(), TEMP_SAVE_PATH, TEMP_DIR_NAME)


def main():
    # load data
    # try:
    #     dir_path = get_data.download_file(TEMP_URL_PLACEHOLDER, file_destination)
    # except Exception as e:
    #     raise(e)
    # populate db with data
    get_data.load_data_from_url(TEMP_URL_PLACEHOLDER, file_destination)
    # for file in os.listdir(dir_path):
    #     #truncate - load table with specified file prefix
    #     db_controller.truncate_load_table(file.split('.')[0], os.path.join(dir_path, file))
    #     # remove file after load
    #     get_data.delete_file(os.path.join(dir_path, file))
    db_controller.load_city_trips()
    # starting flask
    api_handler.run_server()


if __name__ == '__main__':
    #initializing db connection
    download_path = os.path.join(os.getcwd(), TEMP_SAVE_PATH)
    if not os.path.exists(download_path):
        create_dir(download_path)
    #handling data_load
    main()

