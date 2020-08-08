# -*- encoding=utf8 -*-
__author__ = "yeziyezi"
import sys
import os
from airtest_arknights import SimpleExcuter
from airtest.cli.parser import cli_setup
from airtest.core.api import auto_setup
import logging
import getopt
logging.getLogger("airtest").setLevel(logging.ERROR)
print("connecting to device...")
if not cli_setup():
    auto_setup(__file__, logdir=True, devices=[
        "Android://127.0.0.1:5037/127.0.0.1:7555?cap_method=JAVACAP&&ori_method=ADBORI",
    ], project_root=os.getcwd())
print("device connected.")
print("please input battle times:", end="")
times = int(input())
print("task started.target times :"+str(times))

# excute times
SimpleExcuter().excute(times)