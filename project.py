# Mam pip install tabulate muna kayo sa cmd para gumana
# or yung command sa anaconda

import sqlite3
from tabulate import tabulate

import os
# conn = sqlite3.connect('C:/Users/Awilix/Desktop/Python MP6/Project.db')
conn = sqlite3.connect('./project.db')
c = conn.cursor()
queue = []

def create_table_inc():
    c.execute("CREATE TABLE IF NOT EXISTS project_inc (ID INT, TITLE VARCHAR, SIZE INT, PRIORITY INT)")


def create_table_com():
    c.execute("CREATE TABLE IF NOT EXISTS project_com (ID INT, TITLE VARCHAR, SIZE INT, PRIORITY INT)")


def check_id(project_id):
    temp = c.execute("SELECT ID FROM project_inc WHERE ID=?", [project_id])
    arr = list(temp)
    return len(arr)


class Error(Exception):
    pass


class CustomError(Error):
    pass


class OutOfBounds(Error):
    pass


def printTable(sql):
    arr = []
    for row in c.execute(sql):
        arr.append(row)
    print(tabulate(arr, headers=['ID', 'TITLE', 'SIZE', 'PRIORITY']))


def details():
    # For inputing new project details 
    while True:
        print("### INPUT PROJECT DETAILS ###")
        try:
            project_id = int(input("PROJECT ID:       "))
            if check_id(project_id) > 0:
                raise CustomError
            project_title = input("PROJECT TITLE:    ")
            project_size = int(input("PROJECT SIZE:     "))
            project_priority = int(input("PROJECT PRIORITY: "))
            c.execute("INSERT INTO project_inc (ID, TITLE, SIZE, PRIORITY) VALUES (?, ?, ?, ?)", (project_id, project_title, project_size, project_priority))
            conn.commit()
            print("Project has been saved!")
            break
        except ValueError:
            print("!!! Incorrect Input !!!")
        except CustomError:
            print("!!! Project ID already exist. Please use a new one. !!!")
            

def view():
    # For viewing the projects and its details
    while True:
        print("### View Projects ###")
        print("1. One Project")
        print("2. Completed Project")
        print("3. All Projects")
        print("4. Back")
        try: 
            x = int(input("Choose: "))
            arr = []
            if x < 0 or x > 4:
                raise OutOfBounds
            if x == 1:
                project_id = int(input("ID Number: "))
                if check_id(project_id) <= 0:
                    raise CustomError
                else:
                    for row in c.execute("SELECT * FROM project_inc WHERE ID=?", [project_id]):
                        arr.append(row)
                    print(tabulate(arr, headers=['ID', 'TITLE', 'SIZE', 'PRIORITY']))
            elif x == 2:
                sql = "SELECT * FROM project_com"
                printTable(sql)
            elif x == 3:
                sql = "SELECT * FROM project_inc"
                # ORDER BY PRIORITY ASC, SIZE ASC
                printTable(sql)
            elif x == 4:
                break
        except ValueError:
            print('!!! INVALID INPUT !!!')
        except OutOfBounds:
            print('!!! CHOOSE BETWEEN 1-4 !!!')
        except CustomError:
            print('!!! Project ID does not exist. !!!')

def schedule():
    # For Sceduling of projects
    while True:
        print("### Schedule Projects ###")
        print("1. Create Schedule")
        print("2. View Updated Schedule")
        print("3. Back")
        try: 
            x = int(input("Choose: "))
            if x < 0 or x > 3:
                raise OutOfBounds
            if x == 1:
                sql = "SELECT * FROM project_inc ORDER BY PRIORITY DESC, SIZE DESC"
                for row in c.execute(sql):
                    queue.append([row[0], row[1], row[2], row[3]])
            elif x == 2:
                if queue == []:
                    raise CustomError
                print(tabulate(queue, headers=['ID', 'TITLE', 'SIZE', 'PRIORITY']))
            elif x == 3:
                break
        except ValueError:
            print('!!! INVALID INPUT !!!')
        except OutOfBounds:
            print('!!! CHOOSE BETWEEN 1-3 !!!')
        except CustomError:
            print('!!! No schedule created. Create one first. !!!')


def get_project():
    print('### Get a Project ###')
    if queue == []:
        print('!!! No schedule created. Create one first. !!!')
    else:
        print(tabulate(queue, headers=['ID', 'TITLE', 'SIZE', 'PRIORITY']))
        print('The top most project is removed')
        get_sched = queue.pop(0)
        c.execute("INSERT INTO project_com (ID, TITLE, SIZE, PRIORITY) VALUES (?, ?, ?, ?)", (get_sched[0], get_sched[1], get_sched[2], get_sched[3]))
        print(tabulate(queue, headers=['ID', 'TITLE', 'SIZE', 'PRIORITY']))
        
        c.execute("DELETE FROM project_inc WHERE ID = ?", (get_sched[0],))
        conn.commit()
        # queue.pop()

while(True):
    print('### MAIN MENU ###')
    print("1. Input Project Details")
    print("2. View Projects")
    print("3. Schedule Projects")
    print("4. Get a Project")
    print("5. Exit")
    create_table_inc()
    create_table_com()
    try: 
        x = int(input("Choose: "))
        if x < 1 or x > 5:
            raise ValueError
    except ValueError:
        print('!!! CHOOSE BETWEEN 1-5 !!!')
    if x == 1:
        details()
    elif x == 2:
        view()   
    elif x == 3:
        schedule()
    elif x == 4:
        get_project()   
    elif x == 5:
        break

c.close()