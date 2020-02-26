# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 11:01:13 2020

author: Ramvinojen
email : nramvinojen@gmail.com
"""


import sys
from OnlyDef import Keypad
#from OnlyDef import Node

def main():
    
    if len(sys.argv) < 2:
        print("The file takes 1 agruments, input string eg: \"110\"")
        return
    
    InputString = sys.argv[1]
    print("Given input sequence :",  InputString)
    a = Keypad()
    result = a.compute_laziest_path(InputString)
    print(result)

if __name__ == "__main__":
    main()