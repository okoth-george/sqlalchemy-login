from flask import Flask,  request
from create_db import *
import sqlite3

def login (username ,password ):
    data=request.json()
    username= data.get(username)
    password= data.get(password)

    conn = sqlite3.connect("my_database.db")  
    cursor = conn.cursor()
    cursor.execute("select from users where username = %s" ,(username,) )
    user = cursor.fetchone()
    conn.close
    cursor.close
    if user = username :

