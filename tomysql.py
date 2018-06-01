import time
import MySQLdb as mdb

### MYSQL SETTINGS ###

data_base_hostname = "localhost"     # MySQL host ip address or name

data_base_database = ""               # MySQL database name

data_base_username = ""           # MySQL database user name

data_base_password = ""         # MySQL database password

### MYSQL SETUP ###

data_base = mdb.connect(data_base_hostname,  # connect with MySQL database
                        data_base_username,
                        data_base_password,
                        data_base_database)

data_base_cursor = data_base.cursor()        # prepare a cursor object

def store_mysql(sensor_data):

    vars_to_sql = []
    keys_to_sql = []
    data_list = []

    data_list = sensor_data

    for key, value in data_list.items():

        if key == 'Data_Storage_Time_Stamp':
            value = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        vars_to_sql.append(value)
        keys_to_sql.append(key)

    keys_to_sql = ', '.join(keys_to_sql)

    try:
        # Execute the SQL command

        queryText = "INSERT INTO Environment_Parameters(%s) VALUES %r"
        queryArgs = (keys_to_sql, tuple(vars_to_sql))
        data_base_cursor.execute(queryText % queryArgs)
        print('Successfully Added record to mysql')
        data_base.commit()

    except mdb.Error as e:

        try:

            print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        except IndexError:

            print ("MySQL Error: %s" % str(e))

        # Rollback in case there is any error

        data_base.rollback()

        print('ERROR adding record to MYSQL')

