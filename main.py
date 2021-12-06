#!/usr/bin/env python3

import sys
import sqlite3
import datetime

con = sqlite3.connect('database')
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS todo (ID INTEGER PRIMARY KEY NOT NULL, TASK TEXT NOT NULL, DATE TEXT NOT NULL)")

def Error(err, typ):
    if err == 'delete':
        print("Error trying to delete note, check if the id of the note is correct")

    elif err == 'create':
        print("Error trying to create note, you forgot the text")

    elif err == 'update':
        if typ == 'id':
            print("Error trying to update a note, check if the id of the note is correct")

        elif typ == 'text':
            print("Error trying to update a note, you forgot the text")
    pass

def Help():
    print("#"*22)
    print("## TodoApp By Ryuvi ##")
    print("#"*22)
    print("Usage:\n  -c --create <text>: creates a task\n  -d --delete <id>: deletes a task\n  -u --update <id> <text>: updates a task\n  -s --show: show all the tasks\n  -h --help <none>: show this help message")
    pass

def createTodo(text):
    if text in ('', None):
        Error('create')
        Help()

    else:
        tempArr = []
        for item in cur.execute("select * from todo order by ID;"):
            tempArr.append(item[0])
        i = 0
        for item in tempArr:
            if item == i:
                i+=1
            else:
                break

        tempDic = {
            'id': i,
            'task': text,
            'modified': datetime.datetime.now().strftime("%x")
        }

        cur.execute("insert into todo values ({0}, '{1}', '{2}')".format(tempDic['id'], tempDic['task'], tempDic['modified']))
        con.commit()
        showTodo()
    pass

def deleteTodo(id):
    if id in ('', None):
        Error('delete')
        Help()
    else:
        cur.execute("delete from todo where id={0};".format(id))
        con.commit()
        showTodo()
    pass

def showTodo():
    print("Todo App\n")
    for data in cur.execute("select * from todo order by id;"):
        print("{0}. {1} | {2}".format(data[0], data[1], data[2]))
    pass

def updateTodo(id, text):
    if id in ('', None):
        Error('update', 'id')
        Help()
    elif text in ('', None):
        Error('update', 'text')
    else:
        cur.execute("update todo set TASK='{0}' where ID={1}".format(text, id))
        con.commit()
        showTodo()
    pass


if len(sys.argv) < 2 or sys.argv[1] in ('', None):
    Help()

elif sys.argv[1] in ('-s', '--show'):
    showTodo()

elif sys.argv[1] in ('-d', '--delete'):
    if sys.argv[2] in ('', None):
        Help()

    deleteTodo(sys.argv[2])

elif sys.argv[1] in ('-u', '--update'):
    if sys.argv[2] in ('', None) or sys.argv[3] in ('', None):
        Help()
    updateTodo(sys.argv[2], sys.argv[3])

elif sys.argv[1] in ('-c', '--create'):
    if sys.argv[2] in ('', None):
        Help()

    createTodo(sys.argv[2])
