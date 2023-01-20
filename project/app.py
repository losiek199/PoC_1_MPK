import os
import project.get_data as data
import project.db_controller as db
import project.api_handler as api

TEMP_URL_PLACEHOLDER = 'https://www.wroclaw.pl/open-data/87b09b32-f076-4475-8ec9-6020ed1f9ac0/OtwartyWroclaw_rozklad_jazdy_GTFS.zip'
TEMP_SAVE_PATH = 'tmp'
TEMP_DIR_NAME = 'downloadedFiles.zip'
file_destination = os.path.join(os.getcwd(), TEMP_SAVE_PATH, TEMP_DIR_NAME)

def main():
    # make sure that directory exists and grant needed privelages
    # download_path = os.path.join(os.getcwd(), TEMP_SAVE_PATH)
    # if not os.path.exists(download_path):
    #     data.create_dir(download_path)
    # # download zip from url and pass it to db
    # data_path = data.load_data_from_url(TEMP_URL_PLACEHOLDER, file_destination, TEMP_SAVE_PATH)

    # loading files into db
    session = db.Session()
    session.autocommit = True
    # for file in os.listdir(data_path):
    #     db.truncate_load_table(session, file.split('.')[0], os.path.join(data_path, file))
    #     data.delete_file(os.path.join(data_path, file))
    print('Loaded all files \n Loading city_trips table')
    db.load_city_trips()
    print('Loaded custom City_trips table')

    # starting flask
    api.run_server()

if __name__ == '__main__':
    main()

