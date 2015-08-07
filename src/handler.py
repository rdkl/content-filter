#!/usr/bin/env python
# *- coding: utf-8 -*-

import random
import sqlite3

from text_item import TextItem


################################################################################
class Handler(object):
    def __init__(self, prefix="./"):
        self.__storage = sqlite3.connect("../data/sqlite_local.db")
        self.__gen = None

    # --------------------------------------------------------------------------
    def __get_text_gen(self):
            for item in self.__text_rows:
                yield TextItem(id=item[0], state=item[3],
                               text_lem=item[1].encode("utf-8"),
                               text_full=item[2].encode("utf-8"))

    # --------------------------------------------------------------------------
    def GetText(self):
        if not self.__gen:
            rows = self.__storage.execute("""
                SELECT * FROM texts
                WHERE state = 3;
                """)

            self.__text_rows = rows.fetchall()
            self.__gen = self.__get_text_gen()

        self.__last_item = self.__gen.next()
        return self.__last_item

    # --------------------------------------------------------------------------
    def SetState(self, state):
        self.__last_item.set_state(state)
        t = (self.__last_item.state, self.__last_item.id)
        self.__storage.execute("UPDATE texts SET state=? "
                               "WHERE text_database_index=?", t)
        self.__storage.commit()
        print "Cnahges: ", self.__storage.total_changes

    # --------------------------------------------------------------------------
    def __del__(self):
        self.__storage.commit()
        pass

    # --------------------------------------------------------------------------
################################################################################

if __name__ == "__main__":
    handler = Handler()
    print handler.GetText()
    handler.SetState(2)
    print handler.GetText()
