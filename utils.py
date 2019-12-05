from flask import Flask, render_template, request,send_file ,jsonify ,Response
import shutil
import os
import numpy as np




def connection():
   import pymysql 
   conn=pymysql.connect("localhost","root","","facelog" )
   c=conn.cursor()
   return conn,c
