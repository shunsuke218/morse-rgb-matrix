#!/usr/bin/env python
# -*- coding: utf-8 -*-

class config():
    # Constructor
    def __init__(self):
        self.global_status = ["info_thread"]

    # To String
    def __str__(self):
        return str(self.global_status)

    # Setter
    def set(self, status):
        self.global_status = [status]


    # Getter
    def get(self):
        return self.global_status[0]

    
