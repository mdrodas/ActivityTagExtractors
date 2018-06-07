from util.FileManager import FileManager
import pyorient
import subprocess
import logging


def db_create_orientdb(server, name, user, passw):
    #server = 'localhost'
    port = 2424
    client = pyorient.OrientDB(server, port)
    session_id = client.connect(user, passw)
    exist = client.db_exists(name)
    try:
        if not exist:
            client.db_create(name)
            logging.info(name + ": Database Created.")
            exist = True
    except pyorient.PYORIENT_EXCEPTION as err:
        logging.critical("Failed to create DB: %" % err)

    return exist


def change_connect(server, db_name, user, passw, directory, in_filename, out_filename):
    in_path = directory + in_filename
    out_path = directory + out_filename
    my_connect = "CONNECT remote:{0}/{1} {2} {3};".format(server, db_name, user, passw)
    fileManager = FileManager()
    fileManager.new_in(directory, in_filename)
    fileManager.new_out(directory, out_filename)
    myFile = fileManager.readFile(True)
    first = True
    for line in myFile:
        #print("what? " + line)
        if line.find("CONNECT remote:") != -1:
            if (first):
                fileManager.writeFile(my_connect, "w+")
                first = False
            else:
                fileManager.writeFile(my_connect)
        else:
            if (first):
                fileManager.writeFile(line, "w+")
                first = False
            else:
                fileManager.writeFile(line)


def create_db(directory, in_filename, out_filename):
    in_path = directory + in_filename
    in_path2 = directory + out_filename
    global server
    global db_name
    global user
    global passw
    global orientdb
    change_connect(server, db_name, user, passw, directory, in_filename, out_filename)

    exist = db_create_orientdb(server, db_name, user, passw)
    if (exist):
        subprocess.call([orientdb, in_path2])


def populate_tenant(directory, in_filename, out_filename):
    global server
    global db_name
    global user
    global passw
    global orientdb
    change_connect(server, db_name, user, passw, directory, in_filename, out_filename)

    in_path2 = directory + out_filename
    subprocess.call([orientdb, in_path2])


def populate_place(directory, in_filename, out_filename):
    global server
    global db_name
    global user
    global passw
    global orientdb
    change_connect(server, db_name, user, passw, directory, in_filename, out_filename)

    in_path2 = directory + out_filename
    subprocess.call([orientdb, in_path2])


if __name__ == "__main__":
    server = "127.0.0.1"
    db_name = 'framework_test4'
    user = "admin"
    passw = "admin"

    create = True
    orientdb = 'C:\\Apps\\orientdb-community-2.2.18\\bin\\console.bat'
    directory1 = 'C:\\Users\\mdrodas\\PycharmProjects\\TagBuilder1\\resources\\orientdb\\'
    directory2 = 'C:\\Users\\mdrodas\\PycharmProjects\\TagBuilder1\\resources\\orientdb\\data\\Trento\\'
    file_schema = 'schema_original.osql'
    file_schema2 = 'schema_original2.osql'
    file_tenant = 'tenant.osql'
    file_tenant2 = 'tenant2.osql'
    file_place = 'places.osql'
    file_place2 = 'places2.osql'
    if (create):
        create_db(directory1, file_schema, file_schema2)
        populate_tenant(directory1, file_tenant, file_tenant2)
        populate_place(directory2, file_place, file_place2)
