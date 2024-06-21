#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 17:36:19 2024

@author: lisa
"""

def relative_change(ref,change):
    return str(100*(change-ref)/ref)+" %"