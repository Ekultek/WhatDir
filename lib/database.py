import os
import json
import sqlite3

import lib.settings


def initialize():
    """
    initialize the database information
    """
    if not os.path.exists(lib.settings.DATABASE_FILE_PATH):
        try:
            os.makedirs(lib.settings.HOME)
        except:
            pass
    if not os.path.exists(lib.settings.DATABASE_FILE_PATH):
        cursor = sqlite3.connect(lib.settings.DATABASE_FILE_PATH)
        cursor.execute(
            'CREATE TABLE "cached_data" ('
            '`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
            '`netloc` TEXT NOT NULL,'
            '`information_array` TEXT NOT NULL'
            ')'
        )
    conn = sqlite3.connect(lib.settings.DATABASE_FILE_PATH, isolation_level=None, check_same_thread=False)
    return conn.cursor()


def fetch_stored_data(cursor):
    """
    fetch all cached data out of the database
    """
    try:
        stored_data = cursor.execute("SELECT * FROM cached_data")
        return stored_data.fetchall()
    except Exception:
        return []


def insert_website_info(cursor, netloc, results):
    """
    insert into the database
    """
    try:
        already_exists = False
        current_cache = fetch_stored_data(cursor)
        insert_id_num = len(current_cache) + 1
        for data in current_cache:
            _, stored_netloc, _ = data
            if stored_netloc == netloc:
                already_exists = True
        if not already_exists:
            cursor.execute(
                "INSERT INTO cached_data (id,netloc,information_array) VALUES (?,?,?)",
                (insert_id_num, netloc, json.dumps(results))
            )
    except Exception:
        return False
    return True