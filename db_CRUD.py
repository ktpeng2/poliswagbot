from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

import config

DB_NAME = 'discordServers'

TABLES = {}
TABLES['Servers'] = (
    "CREATE TABLE `Servers` ("
    "   `guild_ID` BIGINT NOT NULL AUTO_INCREMENT,"
    "   `guild_NAME` varchar(40) NOT NULL,"
    "   PRIMARY KEY (`guild_ID`)"
    ") ENGINE=InnoDB"
)
TABLES['Members'] = (
    "CREATE TABLE `Members` ("
    "   `mem_KEY` int NOT NULL AUTO_INCREMENT,"
    "   `guild_ID` BIGINT NOT NULL,"
    "   `member_ID` BIGINT NOT NULL,"
    "   `member_EXP` int,"
    "   `member_CURRENCY` int,"
    "   PRIMARY KEY (`mem_KEY`),"
    "   FOREIGN KEY (`guild_ID`) REFERENCES Servers(`guild_ID`) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

def start_Connection():
    try:
        cnx = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_SERVER
        )
        print('connection successful!')
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def create_Database():
    cnx = start_Connection()
    cursor = cnx.cursor()
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME)
        )
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
    cursor.close()
    cnx.close()

def create_Tables():
    cnx = start_Connection()
    cursor = cnx.cursor()
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exist".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_Database(cursor)
            print("Database {} created sucessfully".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("table already exists")
            else:
                print(err.msg)
        else:
            print("OK")
    cursor.close()
    cnx.close()

def resetTables():
    cnx = start_Connection()
    cursor = cnx.cursor()

    dropTables = "DROP TABLE Members"
    cursor.execute(dropTables)
    print("Dropped table: Members")
    dropTables = "DROP TABLE Servers"
    cursor.execute(dropTables)
    print("Dropped table: Servers")

    cursor.close()
    cnx.close()

    create_Tables()

def insertTest(guildID, guildName):
    cnx = start_Connection()
    cursor = cnx.cursor()

    print(cursor.rowcount)

    add_server = (
        "INSERT INTO Servers "
        "   (guild_ID, guild_NAME)"
        "   VALUES (%s, %s)"
        )
    server_info = (guildID, guildName)

    cursor.execute(add_server, server_info)
    cnx.commit()

    print(cursor.rowcount)

    cursor.close()
    cnx.close()

def insertUser(guildID, memberID):
    cnx = start_Connection()
    cursor = cnx.cursor()

    add_user = (
        "INSERT INTO Members "
        "   (guild_ID, member_ID, member_EXP, member_CURRENCY)"
        "   VALUES (%s, %s, %s, %s)"
    )
    userInfo = (guildID, memberID, 0, 0)
    cursor.execute(add_user, userInfo)
    cnx.commit()

    print('member insert sucessful, check db')

    cursor.close()
    cnx.close()

def removeGuild(guildID):
    cnx = start_Connection()
    cursor = cnx.cursor()

    deleteGuild = "DELETE FROM `servers` WHERE `guild_ID` = %s"
    cursor.execute(deleteGuild, (guildID,))
    cnx.commit()

    cursor.close()
    cnx.close()