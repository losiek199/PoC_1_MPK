import db_controller
import api_handler
import os
import get_data


TEMP_URL_PLACEHOLDER = 'https://www.wroclaw.pl/open-data/87b09b32-f076-4475-8ec9-6020ed1f9ac0/OtwartyWroclaw_rozklad_jazdy_GTFS.zip'
TEMP_SAVE_PATH = 'tmp'
TEMP_DIR_NAME = 'downloadedFiles.zip'
file_destination = os.path.join(os.getcwd(), TEMP_SAVE_PATH, TEMP_DIR_NAME)


def main():
    # make sure that directory exists and grant needed privelages
    # download_path = os.path.join(os.getcwd(), TEMP_SAVE_PATH)
    # if not os.path.exists(download_path):
    #     get_data.create_dir(download_path)
    # download zip from url and pass it to db
    # get_data.load_data_from_url(TEMP_URL_PLACEHOLDER, file_destination)
    # load city trips table
    # db_controller.load_city_trips()
    # starting flask
    api_handler.run_server()


if __name__ == '__main__':
    main()

