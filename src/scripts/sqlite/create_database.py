#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sqlite3
import sys

project_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) +
                               "/../../..")
sys.path.append(project_path)

import src.file_reader
import src.text_item
import src.timer

# ------------------------------------------------------------------------------
def drop_tables(connection):
    connection.execute("DROP TABLE IF EXISTS states")
    connection.execute("DROP TABLE IF EXISTS texts")
    connection.execute("DROP TABLE IF EXISTS origin")
    connection.commit()

# ------------------------------------------------------------------------------
def create_tables_if_not_exist(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS states (
            state TEXT,
            state_index INTEGER PRIMARY KEY
        )
    """)

    # Fill states table.
    prefix = "INSERT INTO states(state, state_index) "
    for index, name in src.text_item.states.items():
        conn.execute(prefix + "VALUES (\'%s\', %d);" % (name, index))

    connection.execute("""
        CREATE TABLE IF NOT EXISTS origin (
            name TEXT,
            text_file_index INTEGER,
            text_database_index INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS texts (
          text_database_index INTEGER PRIMARY KEY,
          lem_text TEXT,
          non_lem_text TEXT NOT NULL,
          state INTEGER,
          FOREIGN KEY(text_database_index) REFERENCES origin(text_database_index),
          FOREIGN KEY(state) REFERENCES states(state_index)
         )
    """)
    connection.commit()

# ------------------------------------------------------------------------------
def load_data_from_csv(lemm_texts_filename, non_lemm_texts_filename, connect,
                       database_codename):
    timer = src.timer.Timer()

    cursor = connect.cursor()
    file_reader = src.file_reader.FileReader(lemm_texts_filename,
                                         non_lemm_texts_filename)

    errors_id = []
    index = 0
    for item in file_reader.GetTextGenerator():
        if len(item.text_full) > 10:
            try:
                insert_into_origin = \
                  "INSERT INTO origin (name, text_file_index)" \
                  "VALUES ('%s', %d)" % (database_codename, int(item.id))

                cursor.execute(insert_into_origin)

                # rowid -- unique number, inserted into origin.
                rowid = cursor.lastrowid
                insert_into_texts = \
                  "INSERT INTO texts " \
                  "VALUES (%d, '%s', '%s', 3)" % (rowid,
                      item.text_lem.replace("'", ""),
                      item.text_full.replace("'", ""))

                cursor.execute(insert_into_texts)
            except:
                errors_id.append(item.id)

        index += 1
        if index % 50000 == 0:
            timer.print_from_start(str(index) + " lines processed")

    connect.commit()
    timer.print_from_start("Lines: " + str(index))

    # Write errors into file.
    with open(project_path + "/data/sqlite_load_data_log.txt", "w") as log:
        for item in errors_id:
            print >>log, item

# ------------------------------------------------------------------------------
def make_backup_of_checked_files(db_name):
    pass

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    conn = sqlite3.connect('/mnt/data/Sync/content-filter/data_sqlite.db')
    conn.execute('pragma foreign_keys=ON')

    # drop_tables(conn)
    # create_tables_if_not_exist(conn)

    # load_data_from_csv("/mnt/data/ethnic_data/lem_doc_1581334.csv",
    #                   "/mnt/data/ethnic_data/no_lem_doc_1581334.csv",
    #                   conn, "doc_1581334.csv")

    # load_data_from_csv("/mnt/data/ethnic_data/comments_lem.csv",
    #                   "/mnt/data/ethnic_data/comments_origin.csv",
    #                    conn, "comments.csv")

    # load_data_from_csv(project_path + "/data/medium_ethnic_data_lem.csv",
    #                   project_path + "/data/medium_ethnic_data_no_lem.csv",
    #                   conn, "medium_data")
