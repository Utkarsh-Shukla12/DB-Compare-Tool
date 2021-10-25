# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 19:00:43 2021

@author: utkarsh.shukla
"""

from tkinter import *

root = Tk()


#Define the Title for the Application

root.title("DB Compare tool")
# Creating a Label Widget

myLabel1 = Label (root, text = "Utkarsh Shukla!!")

myLabel2 = Label (root, text = "My Name is Utkarsh Shukla!! :)")

myLabel3 = Label (root, text = "                         ->     ")
# Showing it onto the Screen

myLabel1.grid(row = 0, column = 0)
myLabel3.grid(row = 0, column = 2)
myLabel2.grid(row = 1, column = 5)

root.mainloop()
