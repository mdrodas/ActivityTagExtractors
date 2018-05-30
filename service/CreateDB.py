import pyorient
import subprocess
import logging


def db_create_orientdb(name):
    server = 'localhost'
    port = 2424
    client = pyorient.OrientDB(server, port)
    session_id = client.connect("admin", "admin")
    exist = client.db_exists(name)
    try:
        if not exist:
            client.db_create(name)
            logging.info(name + ": Database Created.")
            exist = True
    except pyorient.PYORIENT_EXCEPTION as err:
        logging.critical("Failed to create DB: %" % err)

    return exist


def create_db(directory, filename):
    in_path = directory + filename
    db_name = 'framework_test2'
    exist = db_create_orientdb(db_name)
    if (not exist):
        subprocess.call([orientdb, in_path])


def populate_tenant(directory, filename):
    in_path2 = directory + filename
    subprocess.call([orientdb, in_path2])


def populate_place(directory, filename):
    in_path2 = directory + filename
    subprocess.call([orientdb, in_path2])


if __name__ == "__main__":
    create = False
    orientdb = 'C:\\Apps\\orientdb-community-2.2.18\\bin\\console.bat'
    directory1 = 'C:\\Users\\mdrodas\\PycharmProjects\\TagBuilder1\\resources\\orientdb\\'
    directory2 = 'C:\\Users\\mdrodas\\PycharmProjects\\TagBuilder1\\resources\\orientdb\\data\\Trento\\'
    file_schema = 'schema_original.osql'
    file_tenant = 'tenant.osql'
    file_place = 'places.osql'
    if (create):
        create_db(directory1, file_schema)

    # populate_tenant(directory1, file_tenant)

    populate_place()
