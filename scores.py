# from app import app
from flask import Flask,render_template
import json
import sqlite3
from datetime import datetime

app = Flask(__name__)

def readData():        
        db=sqlite3.connect('myDB.sqlite')
        c = db.cursor()  
        check_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='myTable';"
        c.execute(check_query)
        result = c.fetchone()
        if result == None:
            print("Reading rushing.js was started!")

            with open('rushing.json', encoding='utf-8-sig') as json_file:
                json_data = json.loads(json_file.read())
    
                #Aim of this block is to get the list of the columns in the JSON file.
                columns = []
                column = []
                for data in json_data:
                    column = list(data.keys())
                    for col in column:
                        if "[" + col + "]" not in columns:
                            columns.append("[" + col + "]")

                                
                #Here we get values of the columns in the JSON file in the right order.   
                value = []
                values = [] 
                for data in json_data:
                    # for i in columns:
                    for i in column:
                        value.append(str(dict(data).get(i)))   
                    values.append(list(value)) 
                    value.clear()
                
                print("Reading rushing.js was completed!")
    
                #Time to generate the create and insert queries and apply it to the sqlite3 database       
                print("Writing data into myTable was started!")

                create_query = "create table if not exists myTable ({0})".format(" text,".join(columns))
                insert_query = "insert into myTable ({0}) values (?{1})".format(",".join(columns), ",?" * (len(columns)-1))     
                print("create_query:{}".format(create_query))
                c.execute(create_query)
                c.executemany(insert_query , values)
                values.clear()
                
                print("Writing data into myTable was completed!")

                print("insert has completed at " + str(datetime.now())) 

            db.commit()
            c.close()

@app.route('/')
def home():
    readData()
    return render_template('home.html')

@app.route('/table')
def table():
    headings = ("Player", "Team", "Pos","Att","Att/G","Yds","Avg","Yds/G","TD","Lng","1st","1st%","20+","40+","FUM")

    db=sqlite3.connect('myDB.sqlite')
    c = db.cursor()  
    select_query = "SELECT * FROM myTable;"
    c.execute(select_query)
    data=c.fetchall()
    return render_template('table.html', headings=headings, data=data)

@app.route('/about')
def about():
    return render_template('about.html')

