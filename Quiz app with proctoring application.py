from tkinter import *
from tkinter import messagebox
import mysql.connector
import random
import datetime
import os
import threading
import time
import cv2

sql_password = "password"
database_name = "sysem1sdp"           #follow database naming rules for example no spaces and prefer creating a new database for proper working
username = "root"                 

def databaseIntitialization(username, sql_password, database_name):
    try:
        sql = mysql.connector.connect(host='localhost', username= username, password= sql_password)
        sqlcursor = sql.cursor()
        sqlcursor.execute('CREATE DATABASE ' + database_name + ';')
        db = mysql.connector.connect(host='localhost', username= username, password= sql_password, database=database_name)
        cursor = db.cursor()
        cursor.execute( 'CREATE TABLE testdetails(name varchar(50), total_marks int, time_mins int)' )
        cursor.execute( "CREATE TABLE students (id int, name varchar(50), roll int, username varchar(50), password varchar(50))" )
        cursor.execute( "CREATE TABLE records(id int, student_name varchar(50), roll int, username varchar(50), test_name varchar(50), total_marks int, obtained_marks int, time_stamp datetime, remark varchar(5))" )
        print("Database and tables added.\nInitialization process completed")
    except Exception:
        print("Already initialized.")

databaseIntitialization(username, sql_password, database_name)
#above function is just for installation purpose. It basically creates all required tables and database files
#you can comment it out if this is not your first time running code in the database

mydb = mysql.connector.connect(host='localhost', username= username, password= sql_password, database= database_name)

mycursor = mydb.cursor()


window1 = Tk()
#a window for main menu is created



def mainMenu():
    window1.title("Main Menu")
    window1.configure(bg='light cyan')
    window1.minsize(height=500, width=500)

    adminMenuButton = Button(window1, text="Admin Menu", height=2, width=20, bg='light blue', font='lucida 20', command= lambda : verificationPage("Admin"))
    studentMenuButton = Button(window1, text="Student Menu", height=2, width=20, bg='light blue', font='lucida 20', command= lambda : verificationPage("Student"))
    exitButton = Button(window1, text="Exit", height=2, width=20, bg='red', font='lucida 20', command = exit)


    adminMenuButton.pack(pady=50)
    studentMenuButton.pack(pady=50)
    exitButton.pack(pady=50)

    window1.mainloop()
#displays main menu window and the functions of it


def verificationPage(type):
    def verify():
        def verifyAdmin():
            username = entry1.get()
            password = entry2.get()
            
            if username == 'admin' and password == 'admin':
                page.destroy()
                messagebox.showinfo("login", "Welcome admin!")
                window1.withdraw()
                adminMenu()
            else:
                messagebox.showinfo("login", "Incorrect username or password.")
                
        
        def verifyStudent():
            username = entry1.get()
            password = entry2.get()
            mycursor.execute(f'''select * from Students where username = "{username}" and password = "{password}"''')
            try:
                name = mycursor.fetchone()[1]
                messagebox.showinfo("login", f"Welcome {name}!")
                page.destroy()
                window1.withdraw()
                studentMenu(username)
                
            except TypeError:
                messagebox.showinfo("login", "Incorrect username or password.")
                
                
        verifyAdmin() if type=="Admin" else verifyStudent()
    
    page = Tk()
    page.title(type+' login')
    page.geometry('250x100+650+300')
    
    label1 = Label(page, text="Enter Username")
    label2 = Label(page, text="Enter Password")
    
    entry1 = Entry(page)
    entry2 = Entry(page, show='*')
    
    loginButton = Button(page, text="Login", bg='light blue', command= verify)
    
    label1.grid(row=0, column=0)
    entry1.grid(row=0, column=1)
    label2.grid(row=1, column=0)
    entry2.grid(row=1, column=1)
    loginButton.grid(row=2, column=1, pady=5)
    
    page.mainloop()
#login for students and admin verified here




def adminMenu():
    def back():
        adminMenuPage.destroy()
        window1.deiconify()
        
    adminMenuPage = Tk()
    adminMenuPage.title('Admin Menu')
    adminMenuPage.configure(bg="light cyan")
    
    
    add_test = Button(adminMenuPage, text="Add Test", bg='light blue', height=2, width=20, font='levetica 20', command= askTestName)
    add_student = Button(adminMenuPage, text="Add Student", height=2, width=20, bg='light blue', font='levetica 20', command= addStudent)
    back_button = Button(adminMenuPage, text="Back to Main Menu", height=2, width=25, bg='grey', font='levetica 20', command = back)
    exit_button = Button(adminMenuPage, text="Exit", height=2, width=20, bg='red', font='levetica 20', command = exit)
    
    add_test.grid(row=0, column=0, padx=100, pady=80)
    add_student.grid(row=0, column=1, padx=100, pady=80)
    back_button.grid(row=1, column=0, padx=100, pady=80)
    exit_button.grid(row=1, column=1, padx=100, pady=80)
    
    
    adminMenuPage.mainloop()
#admin menu with all its functions

def askTestName():
    def check():
        entered_test_name = entry1.get().replace(' ', '_').lower()
        mycursor.execute(f'select name from testdetails where name="{entered_test_name}"')
        test = mycursor.fetchone()
        if test is None:
            askTestNamePage.destroy()
            addTest(entered_test_name)
        else:
            answer = messagebox.askyesno(title='Exception', message='Test already exists', detail='Do you want to overwrite it?')
            if answer:
                mycursor.execute(f'DELETE FROM {entered_test_name};')
                mycursor.execute(f'DELETE FROM TestDetails WHERE name="{entered_test_name}"')
                askTestNamePage.destroy()
                addTest(entered_test_name)
    
    askTestNamePage = Tk()
    askTestNamePage.title('Add Test')
    Label(askTestNamePage, text='Enter Test Name', font='lucida 15').pack()
    entry1 = Entry(askTestNamePage, font='lucida')
    entry1.pack()
    Button(askTestNamePage, text='Add Test',bg='light blue', font='lucida 15', command=check).pack(pady=10)
    askTestNamePage.mainloop()

def addTest(test_name):
    global number_of_questions
    def askTestDetails():
        def submit():
            global number_of_questions
            try:
                mycursor.execute(f"CREATE TABLE {test_name}(question_id int, question_text varchar(500), options varchar(500))")
            except Exception:
                pass
            try:
                number_of_questions = int(entry1.get())
                total_marks = int(entry2.get())
                time_limit = entry3.get()
                mycursor.execute(f'''INSERT INTO TestDetails VALUES ('{test_name}', {total_marks}, {time_limit});''')
                askTestNamePage.destroy()
                add()
            except Exception:
                messagebox.showinfo('Exception', 'Invalid Input')
        
        askTestNamePage = Tk()
        askTestNamePage.title('Enter Test Details')
        label1 = Label(askTestNamePage, text='Enter number of questions')
        label2 = Label(askTestNamePage, text='Enter total marks')
        label3 = Label(askTestNamePage, text='Enter duration in minutes')
        
        entry1 = Entry(askTestNamePage)
        entry2 = Entry(askTestNamePage)
        entry3 = Entry(askTestNamePage)
        
        button1 = Button(askTestNamePage, text='Submit', bg='light blue', command=submit)
        
        label1.grid(row=0, column=0) 
        entry1.grid(row=0, column=1)
        label2.grid(row=1, column=0)
        entry2.grid(row=1, column=1)
        label3.grid(row=2, column=0)
        entry3.grid(row=2, column=1)
        button1.grid(row=3, column=1)
        
        askTestNamePage.mainloop()
    
    def add():
        def addQuestion():
            global question_number, number_of_questions
            
            question_text = questionText.get('1.0', 'end-1c')
            options = []
            options.append(CorrectOptionText.get('1.0', 'end-1c'))
            options.append(Option2Text.get('1.0', 'end-1c'))
            options.append(Option3Text.get('1.0', 'end-1c'))
            options.append(Option4Text.get('1.0', 'end-1c'))
            
            questionText.delete('1.0', 'end')
            CorrectOptionText.delete('1.0', 'end')
            Option2Text.delete('1.0', 'end')
            Option3Text.delete('1.0', 'end')
            Option4Text.delete('1.0', 'end')
            
            mycursor.execute(f'''INSERT INTO {test_name} VALUES ({question_number}, "{question_text}", "{"--".join(options)}");''')
            
            questionLabel.config(text=f'Enter question {question_number+1} text')
            
            if question_number == number_of_questions-1:
                next_button.config(text='Submit')
            
            if question_number == number_of_questions:
                mydb.commit()
                #all the data is committed to the database at once to avoid filling in half data
                addTestPage.destroy()
                messagebox.showinfo('Add Test', 'Test Added Successfully.')
                
            question_number += 1
        
        global question_number
        question_number = 1
        addTestPage = Tk()
        addTestPage.title('Add Test')
        addTestPage.state('zoomed')
        
        questionLabel = Label(addTestPage, text=f'Enter question {question_number} text:', font='Levetica 15')
        CorrectOptionLabel = Label(addTestPage, text=f'Enter correct option:', font='Levetica 15')
        Option2Label = Label(addTestPage, text=f'Enter 2nd option:', font='Levetica 15')
        Option3Label = Label(addTestPage, text=f'Enter 3rd option:', font='Levetica 15')
        Option4Label = Label(addTestPage, text=f'Enter 4th option:', font='Levetica 15')

        questionText = Text(addTestPage, height=15, width=60, bg='light pink')
        CorrectOptionText = Text(addTestPage, height=15, width=30, bg='light green')
        Option2Text = Text(addTestPage, height=10, width=30, bg='light yellow')
        Option3Text = Text(addTestPage, height=10, width=30, bg='light yellow')
        Option4Text = Text(addTestPage, height=10, width=30, bg='light yellow')

        next_button = Button(addTestPage, text='Add', font='Levetica 15', bg='light blue', command= addQuestion)
        if question_number == number_of_questions:
            next_button.config(text='Submit')
        
        questionLabel.grid(row=0, column=0, padx=20, pady=20)
        questionText.grid(row=0, column=1, padx=20, pady=20)
        CorrectOptionLabel.grid(row=0, column=2, padx=50, pady=20)
        CorrectOptionText.grid(row=0, column=3, padx=0, pady=50)
        Option2Label.grid(row=2, column=0, padx=20, pady=20)
        Option2Text.grid(row=2, column=1, padx=20, pady=20)
        Option3Label.grid(row=2, column=2, padx=20, pady=20)
        Option3Text.grid(row=2, column=3, padx=20, pady=20)
        Option4Label.grid(row=4, column=0, padx=20, pady=20)
        Option4Text.grid(row=4, column=1, padx=20, pady=20)
        next_button.grid(row=4, column=2, pady=20, columnspan=3)

        addTestPage.mainloop()
        
        
        
    askTestDetails()

def addStudent():
    def submit():
        student_name = entry1.get()
        roll_number = entry2.get()
        username = entry3.get()
        password = entry4.get()
        
        mycursor.execute(f"select username from students where username = '{username}'")
        if not mycursor.fetchone() is None:
            messagebox.showinfo("Exception", 'Username already taken.')
        else:
            mycursor.execute('select MAX(id) from Students')
            maximum = mycursor.fetchone()[0]
            if maximum is None:
                ID = 1
            else:
                ID = maximum + 1
                
            try:
                mycursor.execute(f'''insert into Students(id, name, roll, username, password) VALUES ({ID}, '{student_name}', '{roll_number}', '{username}', '{password}') ''')
                mydb.commit()
                messagebox.showinfo('Add Student', f'{student_name} has been added.')
                entry1.delete(0, END)
                entry2.delete(0, END)
                entry3.delete(0, END)
                entry4.delete(0, END)
            except Exception:
                messagebox.showinfo("Student already exists.")
        

    addStudentPage = Tk()
    addStudentPage.title('Add Student Portal')
    addStudentPage.state('zoomed')
    
    label1 = Label(addStudentPage, text= 'Enter Student Name', font='lucida 20').pack()
    entry1 = Entry(addStudentPage, font='lucida 20')
    entry1.pack()
    label2 = Label(addStudentPage, text= 'Enter Roll Number', font='lucida 20').pack()
    entry2 = Entry(addStudentPage, font='lucida 20')
    entry2.pack()
    label3 = Label(addStudentPage, text= 'Enter Username', font='lucida 20').pack()
    entry3 = Entry(addStudentPage, font='lucida 20')
    entry3.pack()
    label4 = Label(addStudentPage, text= 'Enter Password', font='lucida 20').pack()
    entry4 = Entry(addStudentPage, font='lucida 20')
    entry4.pack()
    
    submit_button = Button(addStudentPage, text='Submit', font='lucida 20', command= submit, bg='light blue')
    submit_button.pack(pady=20)
    
    
    addStudentPage.mainloop()




def studentMenu(username):
    def back():
        studentMenuPage.destroy()
        window1.deiconify()
        
    def viewTest():
        testName = e1.get()
        testName = testName.replace(' ', '_').lower()
        mycursor.execute(f'''select * from testdetails where name="{testName}";''')
        table = mycursor.fetchone()
        if table is not None:
            studentMenuPage.destroy()
            messagebox.showinfo("Test","Here are the test details.")
            showTestDetails(table, username)
        else:
            messagebox.showinfo("Test", "Invalid test name.")
            
            
            
        
    studentMenuPage = Tk()
    studentMenuPage.title('Student Menu')
    studentMenuPage.configure(bg="light cyan")
    studentMenuPage.minsize(250, 40)
    
    label1 = Label(studentMenuPage, text="Enter Test Name", bg="light cyan", font='lucida 15')
    e1 = Entry(studentMenuPage, font='lucida 15')
    test_button = Button(studentMenuPage, text='View Test Details', bg='light blue', font='lucida 15', command= viewTest)
    back_button = Button(studentMenuPage, text='Back to Main Menu',bg='grey', font='lucida 15', command= back)
    
    label1.grid(row=0, column=0, padx=10, pady=8)
    e1.grid(row=0, column= 1, padx=10, pady=8)
    test_button.grid(row=1, column=1, padx=10, pady=8)
    back_button.grid(row=1, column=0, padx=10, pady=8)
    
    studentMenuPage.mainloop()


def showTestDetails(table, username):
    def back():
        testDetailsPage.destroy()
        studentMenu(username)
        
    def start():
        messagebox.showinfo("Test", 'All the best!')
        window1.destroy()
        testDetailsPage.destroy()
        startTest(username, test_details)
    
    test_details = table
    mycursor.execute(f"select * from {test_details[0]}")
    number_of_questions = len(mycursor.fetchall())
    
    testDetailsPage = Tk()
    testDetailsPage.title('Test Details')
    testDetailsPage.geometry('360x140+580+270')
    testDetailsPage
    
    label1 = Label(testDetailsPage, text=test_details[0].replace('_', " ").upper())
    label1.config(font=("Times New Roman", 25))
    label2 = Label(testDetailsPage, text="Total Marks: ")
    label3 = Label(testDetailsPage, text=test_details[1])
    label4 = Label(testDetailsPage, text="Test Duration: ")
    label5 = Label(testDetailsPage, text=str(test_details[2])+' mins')
    label6 = Label(testDetailsPage, text="Number of Questions: ")
    label7 = Label(testDetailsPage, text=number_of_questions)
    label8 = Label(testDetailsPage, text="Student's Username: ")
    label9 = Label(testDetailsPage, text=username)
    space = Label(testDetailsPage, text='         ')
    
    start_test = Button(testDetailsPage, text="Start Test", bg='light green', command=start)
    back_button = Button(testDetailsPage, text="Back", bg='grey', command=back)
    
    
    label1.grid(row=0, column=0, columnspan=4, sticky='NSWE')
    label2.grid(row=1, column=0)
    label3.grid(row=1, column=1)
    label4.grid(row=1, column=3)
    label5.grid(row=1, column=4)
    label6.grid(row=2, column=0)
    label7.grid(row=2, column=1)
    label8.grid(row=2, column=3)
    label9.grid(row=2, column=4)
    space.grid(row=3, column=2)
    back_button.grid(row=4, column=0, columnspan=2, sticky='NSWE', padx=50)
    start_test.grid(row=4, column=3, columnspan=4, sticky='NSWE', padx=50)
    
    
    testDetailsPage.mainloop()

def startTest(username, test_details):
    def displayResult():
        mycursor.execute(f'select * from Students where username = "{username}"')
        student_details = mycursor.fetchone()
        mycursor.fetchall()
        mycursor.execute('select MAX(id) from Records')
        maximum = mycursor.fetchone()[0]
        if maximum is None:
            ID = 1
        else:
            ID = maximum + 1
        
        if marks_obtained*100/total_marks > 35:
            remarks = 'PASS'
        else:
            remarks = 'FAIL'
        
        mycursor.execute(f'''insert into Records VALUES ({ID}, "{student_details[1]}", {student_details[2]}, "{student_details[3]}", "{testName}", {total_marks}, {marks_obtained}, "{timestamp}", "{remarks}") ''')
        mydb.commit()
        
        file = open(f"{student_details[1]} {testName.replace('_', ' ')}.txt", 'w')
        file.writelines(f"\t\t\t\t\t\t{testName.upper().replace('_', ' ')} REPORT\n\t\t\t\t\t\t\t\t\t\t\t Record ID: {ID}\n\nStudent's Name:\t{student_details[1]}\t\t\t\tRoll Number:\t{student_details[2]}\nTotal Marks:\t{total_marks}\t\t\t\t\t\tObtained Marks:\t{marks_obtained}\nTime:\t\t\t{datetime.datetime.now()}\t\tRemarks:\t\t{remarks}")
        file.close()
        
        os.startfile(f"{student_details[1]} {testName.replace('_', ' ')}.txt")
        
    
    
    def timer(timeleft):
        global istestrunning
        while timeleft and istestrunning:
            mins, secs = divmod(timeleft, 60)
            timer = '{:02d}mins {:02d}secs\nleft'.format(mins, secs)
            timerLabel.config(text=timer)
            time.sleep(1)
            timeleft -= 1
        if timeleft==0:
            timerLabel.config(text="00mins 00secs\nleft")
            messagebox.showinfo('Test','Time Over.\nTest submitted.')
            displayResult()
            testWindow.destroy()
            
    def proctor():
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        warnings = 3
        while warnings>0:
            _, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            if len(faces) >1:
                warnings -= 1
                messagebox.showinfo('Proctor Warning',f"More than one face detected.\nWarnings remaining: {warnings}")
            time.sleep(5)
        messagebox.showinfo('Proctor', 'Your Examinition has been terminated.')
        testWindow.destroy()
    
    
    
    global marks_obtained, question_number, number_of_questions, istestrunning
    marks_obtained = 0
    question_number = 0
    istestrunning = True
    
    timestamp = datetime.datetime.now()
    testName = test_details[0]
    total_time = test_details[2]
    mycursor.execute(f'''select * from {testName}''')
    test_data = mycursor.fetchall()
    random.shuffle(test_data)
    number_of_questions = len(test_data)
    options = [row[2].split('--') for row in test_data]
    correct_options = [row[0] for row in options]
    for i in options:
        random.shuffle(i)
    shuffled_options = [i for i in options]
    questions = [row[1] for row in test_data]
    
    total_marks = test_details[1]
    marks_per_question = total_marks/number_of_questions
    
    
    testWindow = Tk()
    testWindow.title(testName.replace('_', " ").upper())
    testWindow.state('zoomed')
    testWindow.config(bg='light cyan')
    
    def checkAnswer():
        global marks_obtained, question_number, number_of_questions, istestrunning
        
        if chosen_option.get() == correct_options[question_number]:
            marks_obtained += marks_per_question
        
        question_number += 1
        
        if question_number == number_of_questions:
            istestrunning = False
            messagebox.showinfo("Test", 'Test Submitted.')
            testWindow.destroy()
            displayResult()
            
        else:
            questionLabel.config(text="Question "+str(question_number+1)+"\n"+questions[question_number])
            option1Radio.config(text=shuffled_options[question_number][0], variable=chosen_option, value=shuffled_options[question_number][0])
            option2Radio.config(text=shuffled_options[question_number][1], variable=chosen_option, value=shuffled_options[question_number][1])
            option3Radio.config(text=shuffled_options[question_number][2], variable=chosen_option, value=shuffled_options[question_number][2])
            option4Radio.config(text=shuffled_options[question_number][3], variable=chosen_option, value=shuffled_options[question_number][3])
        
    thread1 = threading.Thread(target=lambda : timer(total_time*60))
    timerLabel=Label(testWindow, font='lucida 20', bg='light pink')
    timerLabel.pack(anchor='ne', padx=50, pady=5)
    thread1.start()
    
    thread2 = threading.Thread(target=proctor)
    thread2.start()
    
        
        
    questionLabel = Label(testWindow, text="Question "+str(question_number+1)+"\n"+questions[question_number], font='lucida 20 bold', bg="light cyan")
    
    
    chosen_option = StringVar()
    chosen_option.set('ok')
    
    option1Radio = Radiobutton(testWindow, text=shuffled_options[question_number][0], variable=chosen_option, value=shuffled_options[question_number][0], font='lucida 20', bg="light cyan")
    option2Radio = Radiobutton(testWindow, text=shuffled_options[question_number][1], variable=chosen_option, value=shuffled_options[question_number][1], font='lucida 20', bg="light cyan")
    option3Radio = Radiobutton(testWindow, text=shuffled_options[question_number][2], variable=chosen_option, value=shuffled_options[question_number][2], font='lucida 20', bg="light cyan")
    option4Radio = Radiobutton(testWindow, text=shuffled_options[question_number][3], variable=chosen_option, value=shuffled_options[question_number][3], font='lucida 20', bg="light cyan")
    
    submit_button = Button(testWindow, text='Submit', bg='light green', command = checkAnswer, font='lucida 20 bold')
    
    questionLabel.pack(pady=50)
    option1Radio.pack()
    option2Radio.pack()
    option3Radio.pack()
    option4Radio.pack()
    submit_button.pack(pady=50)
    testWindow.mainloop()
    
    



if __name__ == '__main__':
    mainMenu()
    os._exit(0)
