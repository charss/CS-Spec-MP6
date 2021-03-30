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
    temp = c.execute("SELECT ID FROM project_inc WHERE ID=?", project_id)
    arr = list(temp)
    return len(arr)

class Error(Exception):
    pass

class CustomError(Error):
    pass

def details():
    _ = os.system('cls')
    while True:
        print("### INPUT PROJECT DETAILS ###")
        try:
            sid = input("PROJECT ID:       ")
            sti = input("PROJECT TITLE:    ")
            ssi = input("PROJECT SIZE:     ")
            spr = input("PROJECT PRIORITY: ")
            if (sid.isdigit() == True and ssi.isdigit() and spr.isdigit() == True):
                if check_id(sid) > 0:
                    raise CustomError
                else:
                    c.execute("INSERT INTO project_inc (ID, TITLE, SIZE, PRIORITY) VALUES (?, ?, ?, ?)", (sid, sti, ssi,spr))
                    conn.commit()
                    print("Project has been saved!")
                os.system("pause")
                break
            else:
                raise ValueError
        except ValueError:
            _ = os.system('cls')
            print("!!! Incorrect Input !!!")
        except CustomError:
            _ = os.system('cls')
            print("!!! Project ID already exist. Please use a new one. !!!")

def view():
    _ = os.system('cls')
    while(True):
        print("### View Projects ###")
        print("1. One Project")
        print("2. Completed Project")
        print("3. All Projects")
        print("4. Back")
        try: 
            x = int(input("Chooose: "))
            if int(x) < 0:
                raise out_of_range_exp("!!! Error !!!")
            else:
                print("-------------------------------------------")
                arr = []
                if int(x) == 1:
                    project_id = input("ID Number: ")
                    sql = "SELECT ID, TITLE, SIZE, PRIORITY FROM project_inc where ID=?"

                    # hey = check_id(project_id)
                    if check_id(project_id) < 0:
                        raise CustomError
                    else:
                        for row in c.execute("SELECT * FROM project_inc WHERE ID=?", project_id):
                            arr.append(row)
                            break
                        print(tabulate(arr, headers=['ID', 'TITLE', 'SIZE', 'PRIORITY']))
                elif int(x) == 2:
                    sql = "SELECT * FROM project_com"
                    for row in c.execute(sql):
                        arr.append(row)
                    print(tabulate(arr, headers=['ID', 'TITLE', 'SIZE', 'PRIORITY']))
                elif int(x) == 3:
                    sql = "SELECT * FROM project_inc"
                    # ORDER BY PRIORITY ASC, SIZE ASC
                    for row in c.execute(sql):
                        arr.append(row)
                    print(tabulate(arr, headers=['ID', 'TITLE', 'SIZE', 'PRIORITY']))
                elif int(x) == 4:
                    break
                break
        except out_of_range_exp as e:
            print(e)
        except ValueError:
            print("!!! CHOOSE BETWEEN 1-3 !!!")
        except CustomError:
            _ = os.system('cls')
            print("!!! Project ID doesn't exist. !!!")

def schedule():
    _ = os.system('cls')
    while(True):
        print("### Schedule Project ###")
        print("1. Create Schedule")
        print("2. View Updated Schedule")
        print("3. Back")
        try: 
            x = int(input("Chooose: "))
            if int(x) < 0:
                raise out_of_range_exp("Error")
            else:
                if int(x) == 1:
                    sql = "SELECT * FROM project_inc ORDER BY PRIORITY ASC, SIZE ASC"
                    for row in c.execute(sql):
                        queue.append((row[0], row[1], row[2], row[3]))
                elif int(x) == 2:
                    if queue == []:
                        raise CustomError
                    for i in range(len(queue)):
                        print ("=>PROJECT ID:       " + str(queue[i][0]))
                        print ("PROJECT TITLE:      " + str(queue[i][1]))
                        print ("PROJECT SIZE:       " + str(queue[i][2]))
                        print ("PROJECT PRIORITY:   " + str(queue[i][3]))                  
                elif int(x) == 3:
                    break
        except out_of_range_exp as e:
            print(e)
        except ValueError:
            _ = os.system('cls')
            print("!!! CHOOSE BETWEEN 1-2 !!!") 
        except CustomError:
            _ = os.system('cls')
            print("No schedule created. Create one first.")


def get_project():
    print ("=>PROJECT ID:       " + str(queue[0][0]))
    print ("PROJECT TITLE:      " + str(queue[0][1]))
    print ("PROJECT SIZE:       " + str(queue[0][2]))
    print ("PROJECT PRIORITY:   " + str(queue[0][3]))
    c.execute("INSERT INTO project_com (ID, TITLE, SIZE, PRIORITY) VALUES (?, ?, ?, ?)", (queue[0][0], queue[0][1], queue[0][2],queue[0][3]))
    c.execute("DELETE FROM project_inc WHERE ID = ?", (queue[0][0],))
    conn.commit()
    queue.pop()

class out_of_range_exp(Exception):
    pass

while(True):
    _ = os.system('cls')
    print('### MAIN MENU ###')
    print("1. Input Project Details")
    print("2. View Projects")
    print("3. Schedule Projects")
    print("4. Get a Project")
    print("5. Exit")
    create_table_inc()
    create_table_com()
    try: 
        x = int(input("Chooose: "))
        if int(x) < 0:
            raise out_of_range_exp("Error")
        else:
            if int(x) == 1:
                details()
            elif int(x) == 2:
                view()   
            elif int(x) == 3:
                schedule()
            elif int(x) == 4:
                get_project()   
            elif int(x) == 5:
                break
    except out_of_range_exp as e:
        print(e)
    except ValueError:
        print("!!! CHOOSE BETWEEN 1-5 !!!")

c.close()