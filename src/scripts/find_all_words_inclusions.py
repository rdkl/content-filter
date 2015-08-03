#!/usr/bin/env python
#-*- coding: utf-8 -*-

import cPickle
import os
import sqlite3
import sys

project_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) +
                               "/../..")
sys.path.append(project_path)

import src.matcher
import src.timer

# ------------------------------------------------------------------------------
def fetch_rows(cursor, rows_number=100):
    fetch = cursor.fetchmany
    while True:
        rows = fetch(rows_number)
        if not rows:
            break

        for row in rows:
            yield row

# ------------------------------------------------------------------------------
def get_inclusions(cursor):
    timer = src.timer.Timer()

    # Initialize the matcher.
    matcher = src.matcher.Matcher("../../data/ethnic_words.txt")
    words = matcher.GetDict()

    cursor.execute('SELECT max(text_database_index) FROM texts')
    max_id = cursor.fetchone()[0]

    cursor.execute("SELECT text_database_index, lem_text FROM texts")

    timer.set_point()
    result = {}
    for item in fetch_rows(cursor):
        found_words = matcher.FindWordsInText(item[1].encode("utf-8"))
        if found_words:
            result[item[0]] = found_words

        if item[0] % 50000 == 0:
            output =  "%.2f%% done (%d from %d)" % \
                (float(item[0]) / max_id * 100.0, item[0], max_id)
            timer.print_from_last_point(output)

    with open("../../data/words_inclusions.txt", "w") as log:
        cPickle.dump([found_words, words], log)

# ------------------------------------------------------------------------------
def copy_table(table_name, src_filename, dest):
    print "Copying %s..."  % (table_name),

    dest.execute("DROP TABLE IF EXISTS %s" % table_name)
    dest.execute("ATTACH DATABASE \"%s\" AS dest_db;" % src_filename)
    dest.execute("CREATE TABLE %s AS SELECT * FROM dest_db.%s;" % (table_name,
                                                                   table_name))
    dest.commit()
    print "Copied."

# ------------------------------------------------------------------------------
def choose_rowids(number):
    [found_words_dict, words] = cPickle.load(
        open("../../data/words_inclusions.txt"))
    found_words_number = {key : len(value)
                          for key, value in found_words_dict.items()}
    found_words_counts = {key : sum(value.values())
                          for key, value in found_words_dict.items()}

    words_diff_sorted, keys_diff = \
        zip(*sorted(zip(found_words_number.values(),
                        found_words_number.keys()),
                    reverse=True))
    words_counts_sorted, keys_count = \
        zip(*sorted(zip(found_words_counts.values(),
                        found_words_counts.keys()),
                    reverse=True))

    chosen_docs = {}
    for item in keys_diff[:number] + keys_count[:number]:
        chosen_docs[item] = 0

    return chosen_docs.keys()

# ------------------------------------------------------------------------------
def make_local_sql_database(full_database_path):

    local_database = sqlite3.connect('../../data/sqlite_local.db')
    local_database.execute('pragma foreign_keys=ON')

    full_database = sqlite3.connect(full_database_path)

    copy_table("states", full_database_path, local_database)

    full_database.execute("CREATE TABLE IF NOT EXISTS chosen_ids "
                          "(key INTEGER UNIQUE)")
    rowids = choose_rowids(500)
    for rowid in rowids:
        full_database.execute("INSERT INTO chosen_ids(key) VALUES (%d)" \
                               % rowid)

    result = full_database.execute("SELECT * FROM texts "
                                   "WHERE text_database_index IN "
                                   "(SELECT key FROM chosen_ids);")

    local_database.execute("DROP TABLE IF EXISTS texts;")
    local_database.execute("""
      CREATE TABLE IF NOT EXISTS texts (
          text_database_index INTEGER PRIMARY KEY,
          lem_text TEXT,
          non_lem_text TEXT NOT NULL,
          state INTEGER
        )
      """)

    for row in result:
        local_database.execute("INSERT INTO texts "
                       "(text_database_index, lem_text, non_lem_text, state) "
                       "VALUES (%d, '%s', '%s', %d)" \
                       % (row[0], row[1], row[2], row[3]))

    full_database.execute("DROP TABLE chosen_ids;")
    full_database.commit()
    local_database.commit()
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    conn = sqlite3.connect('/mnt/data/Sync/content-filter/data_sqlite.db')
    conn.execute('pragma foreign_keys=ON')

    # get_inclusions(conn.cursor())
    make_local_sql_database('/mnt/data/Sync/content-filter/data_sqlite.db')