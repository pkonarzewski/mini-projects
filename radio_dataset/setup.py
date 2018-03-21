#
import os
import sqlite3
from shutil import copy
import datetime as dt

SQLITE_DB_NAME = "web_crawler.db3"


def create_database_file(db_name):
    print("Tworzenie struktury bazy")
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        # TABELA DLA PAJAKA (URL)
        c.execute('''CREATE TABLE `url_history` (
                     `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                     `url` TEXT UNIQUE,
                     `visited` INTEGER DEFAULT 0
        );''')
        conn.commit()

        # TABELA DLA DANYCH
        c.execute('''CREATE TABLE `songs_data` (
                  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                  `artist` INTEGER,
                  `song` TEXT,
                  `date` INTEGER,
                  `new_song_flag` INTEGER,
                  `station` INTEGER
                  );''')
        conn.commit()

        # KOPIOWANIE TABEL DO TESTOW DODAWANIA
        c.execute('''CREATE TABLE url_history_empty AS SELECT * FROM url_history WHERE 0;''')
        conn.commit()

        c.execute('''CREATE TABLE songs_data_empty AS SELECT * FROM songs_data WHERE 0;''')
        conn.commit()
    except sqlite3.OperationalError as detail:
        print("Blad sql: ", detail)
        os.remove(db_name)
    finally:
        conn.close()


def create_test_database(org_db_path):
    print("Tworzenie bazy testowej")
    test_db_path = os.path.join('tests', ("test_"+org_db_path))

    try:
        print("Usuwanie starej bazy testowej")
        if os.path.exists(test_db_path): os.remove(test_db_path)
        copy(org_db_path, test_db_path)
    except PermissionError:
        print("Brak dostepu do bazy '{}', cofam dzialanie".format(test_db_path))
        os.remove(org_db_path)
        return

    # TWORZENIE DANYCH TESTOWYCH
    conn = sqlite3.connect(test_db_path)
    c = conn.cursor()

    # DANE O PIOSENKACH
    # (id, artist, song, date, new_song_flag, station)
    songs_data = [(None, 'Darude', 'Sandstorm', dt.datetime(2015, 1, 1, 20, 45, 0), 0, 'rmf'),
                  (None, 'Enia', 'May it be', dt.datetime(2015, 1, 1, 20, 55, 0), 0, 'rmf'),
                  (None, 'Michael Jackson', 'Beatit', dt.datetime(2015, 1, 2, 20, 59, 0), 1, 'rmf'),
                  ]
    c.executemany('''INSERT INTO songs_data VALUES(?,?,?,?,?,?)''', songs_data)
    conn.commit()

    # DANE O LINKACH
    # (id, url, visited)
    urls_data = [(None, 'http://songs.arch/1', 1),
                 (None, 'http://songs.arch/2', 0),
                 (None, 'http://songs.arch/3', 0)]
    c.executemany('''INSERT INTO url_history VALUES(?,?,?)''', urls_data)
    conn.commit()

    conn.close()

# MAIN ===
# Tworzenie struktury bazy danych jezeli nie istnieje
if os.path.exists(SQLITE_DB_NAME):
    print("Baza istnieje, brak dzialania")
else:
    create_database_file(SQLITE_DB_NAME)
    create_test_database(SQLITE_DB_NAME)



