import sys
import os

def run_command(string):
    print("Running command: " + string)
    os.system(string)