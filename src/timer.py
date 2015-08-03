#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time

################################################################################
class Timer(object):
    def __init__(self):
        self.__last_time = time.time()
        self.__start_time = time.time()
    # --------------------------------------------------------------------------
    def set_point(self):
        self.__last_time = time.time()

    # --------------------------------------------------------------------------
    def print_from_start(self, message):
        print message, "\nTime: %.2f\n" % (time.time() - self.__start_time)

    # --------------------------------------------------------------------------
    def print_from_last_point(self, message):
        print message, "\nTime: %.2f\n" % (time.time() - self.__last_time)

################################################################################