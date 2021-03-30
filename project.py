import sqlite3

conn = sqlite3.connect('C:/Users/Awilix/Desktop/Python MP6/Project.db')
c = conn.cursor()
queue = []

def create_table_inc():
    c.execute("CREATE TABLE IF NOT EXISTS project_inc (ID INT, TITLE VARCHAR, SIZE INT, PRIORITY INT)")

def create_table_com():
    c.execute("CREATE TABLE IF NOT EXISTS project_com (ID INT, TITLE VARCHAR, SIZE INT, PRIORITY INT)")

def details():
    while True:
        try:
            sid = input("PROJECT ID:        ")
            sti = input("PROJECT TITLE:     ")
            ssi = input("PROJECT SIZE:      ")
            spr = input("PROJECT PRIORITY:  ")
            if (sid.isdigit() == True and ssi.isdigit() and spr.isdigit() == True):
                c.execute("INSERT INTO project_inc (ID, TITLE, SIZE, PRIORITY) VALUES (?, ?, ?, ?)", (sid, sti, ssi,spr))
                conn.commit()
                print("Project has been saved!")
                break
            else:
                raise ValueError
        except ValueError:
            print("Incorrect Input")

def view():
    while(True):
        print("-View Projects")
        print("--1. One Project")
        print("--2. Completed Project")
        print("--3. All Projects")
        try: 
            x = int(input("Chooose: "))
            if int(x) < 0:
                raise out_of_range_exp("Error")
            else:
                if int(x) == 1:
                    id = input("ID Number: ")
                    sql = "SELECT ID, TITLE, SIZE, PRIORITY FROM project_inc where ID = ?"
                    for row in c.execute(sql, [(id)]):
                        print ("=>PROJECT ID:       " + str(row[0]))
                        print ("PROJECT TITLE:      " + str(row[1]))
                        print ("PROJECT SIZE:       " + str(row[2]))
                        print ("PROJECT PRIORITY:   " + str(row[3]))
                        break
                elif int(x) == 2:
                    sql = "SELECT * FROM project_com"
                    for row in c.execute(sql):
                        print ("=>PROJECT ID:       " + str(row[0]))
                        print ("PROJECT TITLE:      " + str(row[1]))
                        print ("PROJECT SIZE:       " + str(row[2]))
                        print ("PROJECT PRIORITY:   " + str(row[3]))
                    break
                elif int(x) == 3:
                    sql = "SELECT * FROM project_inc"
                    # ORDER BY PRIORITY ASC, SIZE ASC
                    for row in c.execute(sql):
                        print ("=>PROJECT ID:       " + str(row[0]))
                        print ("PROJECT TITLE:      " + str(row[1]))
                        print ("PROJECT SIZE:       " + str(row[2]))
                        print ("PROJECT PRIORITY:   " + str(row[3]))
                    break
        except out_of_range_exp as e:
            print(e)
        except ValueError:
            print("CHOOSE BETWEEN 1-3")

def schedule():
    while(True):
        try: 
            x = int(input("Chooose: "))
            if int(x) < 0:
                raise out_of_range_exp("Error")
            else:
                if int(x) == 1:
                    sql = "SELECT * FROM project_inc ORDER BY PRIORITY ASC, SIZE ASC"
                    for row in c.execute(sql):
                        queue.append((row[0],row[1],row[2],row[3]))
                elif int(x) == 2:
                    for i in range(len(queue)):
                        print ("=>PROJECT ID:       " + str(queue[i][0]))
                        print ("PROJECT TITLE:      " + str(queue[i][1]))
                        print ("PROJECT SIZE:       " + str(queue[i][2]))
                        print ("PROJECT PRIORITY:   " + str(queue[i][3]))                  
        except out_of_range_exp as e:
            print(e)
        except ValueError:
            print("CHOOSE BETWEEN 1-2") 
        break  

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
        print("CHOOSE BETWEEN 1-5")