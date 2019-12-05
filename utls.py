from flask import Flask, render_template, request,send_file ,jsonify ,Response
import shutil
import os
import numpy as np
import pymysql as sql
import pymysql.cursors



def connection():
   import pymysql 
   conn=pymysql.connect("localhost","root","","facelog",cursorclass=pymysql.cursors.DictCursor )
   c=conn.cursor()
   return conn,c
