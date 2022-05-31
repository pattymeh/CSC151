from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import tkinter.messagebox
import os
import sqlite3


#####################################################################################################################################################################################

class sis(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        all_frame = tk.Frame(self)
        all_frame.pack(side="top", fill="both", expand = True)
        all_frame.rowconfigure(0, weight=1)
        all_frame.columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Students, Home, Courses):
            frame = F(all_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show(Home)
    def show(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()

#####################################################################################################################################################################################

def iExit():
            iExit = tkinter.messagebox.askyesno("Student Information System","Confirm if you want to exit")
            if iExit > 0:
                root.destroy()
                return
class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        label = tk.Label(self, text="Student Information System", font=("Osaka", 40))
        label.place(x=310,y=20)

        home = tk.Button(self, text="Home",font=("Osaka",16,"bold"),bd=0, width = 10, bg="Cadet Blue", fg="Black", command=lambda: controller.show(Home))
        home.place(x=380,y=300)
        home.config(cursor= "hand2")
        
        course = tk.Button(self, text="Course",font=("Osaka",16,"bold"),bd=0, width = 10, bg="Cadet Blue", fg="Black", command=lambda: controller.show(Courses))
        course.place(x=568,y=300)
        course.config(cursor= "hand2")
        
        students = tk.Button(self, text="Register",font=("Osaka",16,"bold"),bd=0, width = 10, bg="Cadet Blue", fg="Black", command=lambda: controller.show(Students))
        students.place(x=750,y=300)
        students.config(cursor= "hand2")

        students = tk.Button(self, text="Exit",font=("Osaka",15,"bold"),bd=0, width = 10, bg="Cadet Blue", fg="Black", command=iExit)
        students.place(x=1100,y=460)
        students.config(cursor= "hand2")

        
        
######################################################################################################################################################################################      

class Courses(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("Student Information System")
        
        label = tk.Label(self, text="Course", font=("Osaka", 40))
        label.place(x=130,y=20)
        
        Course_Code = StringVar()
        Course_Name = StringVar()
        SearchBar_Var = StringVar()
        
        def tablec():
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS courses (Course_Code TEXT PRIMARY KEY, Course_Name TEXT)") 
            conn.commit() 
            conn.close()
            
        def add_course():
            if Course_Code.get() == "" or Course_Name.get() == "" : 
                tkinter.messagebox.showinfo("SIS", "Fill in the box")
            else:
                conn = sqlite3.connect("sis_v2.db")
                c = conn.cursor()         
                c.execute("INSERT INTO courses(Course_Code,Course_Name) VALUES (?,?)",(Course_Code.get(),Course_Name.get()))        
                conn.commit()           
                conn.close()
                Course_Code.set('')
                Course_Name.set('') 
                tkinter.messagebox.showinfo("SIS", "Added!")
                display_course()
              
        def display_course():
            self.course_list.delete(*self.course_list.get_children())
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            for row in rows:
                self.course_list.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
        
        def update_course():
            for selected in self.course_list.selection():
                conn = sqlite3.connect("sis_v2.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE courses SET Course_Code=?, Course_Name=? WHERE Course_Code=?", (Course_Code.get(),Course_Name.get(), self.course_list.set(selected, '#1')))  
                conn.commit()
                tkinter.messagebox.showinfo("SIS", "Updated!")
                display_course()
                clear()
                conn.close()
                
        def edit_course():
            x = self.course_list.focus()
            if x == "":
                tkinter.messagebox.showerror("SIS", "Select a course!")
                return
            values = self.course_list.item(x, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])
                    
        def delete_course(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("SIS", "Delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("sis_v2.db")
                    cur = con.cursor()
                    x = self.course_list.selection()[0]
                    id_no = self.course_list.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM courses WHERE Course_Code = ?",(id_no,))                   
                    con.commit()
                    self.course_list.delete(x)
                    tkinter.messagebox.showinfo("SIS", "Deleted!")
                    display_course()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("SIS", "This course has students!")
                
        def search_course():
            Course_Code = SearchBar_Var.get()                
            con = sqlite3.connect("sis_v2.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM courses WHERE Course_Code = ?",(Course_Code,))
            con.commit()
            self.course_list.delete(*self.course_list.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.course_list.insert("", tk.END, text=row[0], values=row[0:])
            con.close()

        def iExit():
            iExit = tkinter.messagebox.askyesno("Student Information System","Confirm if you want to exit")
            if iExit > 0:
                root.destroy()
                return
        def clear():
            Course_Code.set('')
            Course_Name.set('') 
            
        def OnDoubleclick(event):
            item = self.course_list.selection()[0]
            values = self.course_list.item(item, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])

        
        
        self.lblccode = Label(self, font=("Osaka", 12, "bold"), text="Course Code:", padx=5, pady=5)
        self.lblccode.place(x=125,y=144)
        self.txtccode = Entry(self, font=("Osaka", 13), textvariable=Course_Code, width=31)
        self.txtccode.place(x=270,y=150)

        self.lblcname = Label(self, font=("Osaka", 12,"bold"), text="Course Name:", padx=5, pady=5)
        self.lblcname.place(x=125,y=205)
        self.txtcname = Entry(self, font=("Osaka", 13), textvariable=Course_Name, width=31)
        self.txtcname.place(x=270,y=210)
        
        self.SearchBar = Entry(self, font=("Osaka", 11), textvariable=SearchBar_Var, bd=0,bg="Gray",width=31)
        self.SearchBar.place(x=876,y=110)
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1215,y=140,height=390)

        self.course_list = ttk.Treeview(self, columns=("Course Code","Course Name"), height = 18, yscrollcommand=scrollbar.set)

        self.course_list.heading("Course Code", text="Course Code", anchor=W)
        self.course_list.heading("Course Name", text="Course Name",anchor=W)
        self.course_list['show'] = 'headings'

        self.course_list.column("Course Code", width=200, anchor=W, stretch=False)
        self.course_list.column("Course Name", width=430, stretch=False)
        
        self.course_list.bind("<Double-1> ", OnDoubleclick)


        self.course_list.place(x=575,y=140)
        scrollbar.config(command=self.course_list.yview)
            
        #======================================================================Buttons======================================================================#

        self.adds = Button(self, text="Add", font=('Osaka', 11, ), height=1, width=10, bd=1, bg="Cadet Blue", fg="Black",command=add_course)
        self.adds.place(x=100,y=300)
        self.adds.config(cursor= "hand2")

        self.update = Button(self, text="Update", font=('Osaka', 11), height=1, width=10, bd=1, bg="Cadet Blue", fg="Black", command=update_course) 
        self.update.place(x=200,y=300)
        self.update.config(cursor= "hand2")

        self.clear = Button(self, text="Clear", font=('Osaka', 11), height=1, width=10, bd=1, bg="Cadet Blue", fg="Black", command=clear)
        self.clear.place(x=300,y=300)
        self.clear.config(cursor= "hand2")

        self.delete = Button(self, text="Delete", font=('Osaka', 11), height=1, width=10, bd=1, bg="Cadet Blue", fg="Black", command=delete_course)
        self.delete.place(x=400,y=300)
        self.delete.config(cursor= "hand2")

        self.search = Button(self, text="Search", font=('Osaka', 11, 'bold'),bd=0, bg= "Cadet Blue", fg="Black", command=search_course)
        self.search.place(x=1160,y=100)
        self.search.config(cursor= "hand2")

        self.display = Button(self, text="Display", font=('Osaka', 13, 'bold'), bd=0, width=10, bg="Cadet Blue", fg="Black", command=display_course)
        self.display.place(x=700,y=105)
        self.display.config(cursor= "hand2")

        home = tk.Button(self, text="Home",font=("Osaka",13,"bold"),bd=0, width = 10, bg="Cadet Blue", fg="Black", command=lambda: controller.show(Home))
        home.place(x=575,y=105)
        home.config(cursor= "hand2")
        
        tablec()
        display_course()

#####################################################################################################################################################################################

class Students(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title("Student Information System")
        
       
        
        Student_ID = StringVar()
        Student_Name = StringVar()       
        Student_YearLevel = StringVar()
        Student_Gender = StringVar()
        Course_Code = StringVar()
        SearchBar_Var = StringVar()
        

        def tables():
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS students (Student_ID TEXT PRIMARY KEY, Student_Name TEXT, Course_Code TEXT, \
                      Student_YearLevel TEXT, Student_Gender TEXT, \
                      FOREIGN KEY(Course_Code) REFERENCES courses(Course_Code) ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()    
        
        def add_stud():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("Student Information System", "Fill in the box")
            else:  
                ID = Student_ID.get()
                ID_list = []
                for i in ID:
                    ID_list.append(i)
                a = ID.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("Student Information System", "ID Format:YYYY-NNNN")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("Student Information System", "ID Format:YYYY-NNNN")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("Student Information System", "ID Format:YYYY-NNNN")
                        else:
                            x = ID.split("-")  
                            year = x[0]
                            number = x[1]
                            if year.isdigit()==False or number.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("Student Information System", "ID Number does not exist")
                                except:
                                    pass
                            elif year==" " or number==" ":
                                try:
                                    tkinter.messagebox.showerror("Student Information System", "ID Number does not exist")
                                except:
                                    pass
                            else:
                                try:
                                    conn = sqlite3.connect("sis_v2.db")
                                    c = conn.cursor() 
                                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                    c.execute("INSERT INTO students(Student_ID,Student_Name,Course_Code,Student_YearLevel,Student_Gender) VALUES (?,?,?,?,?)",\
                                                          (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get()))                                       
                                                                       
                                    tkinter.messagebox.showinfo("ID Number does not exist", "Student record is successfully added!")
                                    conn.commit() 
                                    clear()
                                    display_stud()
                                    conn.close()
                                except:
                                    ids=[]
                                    conn = sqlite3.connect("sis_v2.db")
                                    c = conn.cursor()
                                    c.execute("SELECT * FROM students")
                                    rows = c.fetchall()
                                    for row in rows:
                                        ids.append(row[0])
                                    if ID in ids:
                                       tkinter.messagebox.showerror("Student Information System", "ID Number already exists")
                                    else: 
                                       tkinter.messagebox.showerror("Student Information System", "Course Unavailable")
                                   
                    else:
                        tkinter.messagebox.showerror("Student Information System", "ID Number does not exist")
                else:
                    tkinter.messagebox.showerror("Student Information System", "ID Number does not exist")
                 
        def update_stud():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("Student Information System", "Select a student")
            else:
                for selected in self.studentlist.selection():
                    conn = sqlite3.connect("sis_v2.db")
                    cur = conn.cursor()
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("UPDATE students SET Student_ID=?, Student_Name=?, Course_Code=?, Student_YearLevel=?,Student_Gender=?\
                          WHERE Student_ID=?", (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get(),\
                              self.studentlist.set(selected, '#1')))
                    conn.commit()
                    tkinter.messagebox.showinfo("Student Information System", "Student record has been updated!")
                    display_stud()
                    clear()
                    conn.close()
        
        def delete_stud():   
            try:
                messageDelete = tkinter.messagebox.askyesno("Delete record", "Are you sure you want to delete this student record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("sis_v2.db")
                    cur = con.cursor()
                    x = self.studentlist.selection()[0]
                    id_no = self.studentlist.item(x)["values"][0]
                    cur.execute("DELETE FROM students WHERE Student_ID = ?",(id_no,))                   
                    con.commit()
                    self.studentlist.delete(x)
                    tkinter.messagebox.showinfo("Student Information System", "Student record is deleted successfully!")
                    display_stud()
                    clear()
                    con.close()                    
            except Exception as e:
                print(e)
                
        def search_stud():
            Student_ID = SearchBar_Var.get()
            try:  
                con = sqlite3.connect("sis_v2.db")
                cur = con.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM students")
                con.commit()
                self.studentlist.delete(*self.studentlist.get_children())
                rows = cur.fetchall()
                for row in rows:
                    if row[0].startswith(Student_ID):
                        self.studentlist.insert("", tk.END, text=row[0], values=row[0:])
                con.close()
            except:
                tkinter.messagebox.showerror("Student Information System", "ID Number does not exist")           
                
        def display_stud():
            self.studentlist.delete(*self.studentlist.get_children())
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            for row in rows:
                self.studentlist.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
                            
        def edit_stud():
            x = self.studentlist.focus()
            if x == "":
                tkinter.messagebox.showerror("Student Information System", "Select a data")
                return
            values = self.studentlist.item(x, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])
        
        def clear():
            Student_ID.set('')
            Student_Name.set('') 
            Student_YearLevel.set('')
            Student_Gender.set('')
            Course_Code.set('')
            
        def OnDoubleClick(event):
            item = self.studentlist.selection()[0]
            values = self.studentlist.item(item, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])


                
        #==================================================================Label With Entry=================================================================#


        label = tk.Label(self, text="Student Information System ", font=("Osaka", 40))
        label.place(x=300,y=20)
        
        self.lblid = Label(self, font=("Osaka", 12,"bold"), text="ID Number:", padx=5, pady=5)
        self.lblid.place(x=125,y=144)
        self.txtid = Entry(self, font=("Osaka", 13), textvariable=Student_ID, width=25)
        self.txtid.place(x=255,y=150)

        self.lblname = Label(self, font=("Osaka", 12,"bold"), text="Name:", padx=5, pady=5)
        self.lblname.place(x=125,y=200)
        self.txtname = Entry(self, font=("Osaka", 13), textvariable=Student_Name, width=25)
        self.txtname.place(x=255,y=200)
        
        self.lblc = Label(self, font=("Osaka", 12,"bold"), text="Course Code:", padx=5, pady=5)
        self.lblc.place(x=125,y=250)
        self.txtyear = ttk.Combobox(self, value=["BSChe", "BSME" , "BSEM", "BSMET", "BSCERE", "BSIAM", "BSECE","BSEE","BSCpE" , "BSCE", "BSEnvET",
                                                 "BSBIO(Bdv)", "BSPHYSICS","BSMATH","BSBIO(PlBio)", "BSMARINE BIO", "BSBIO(MCB)", "BSCHEM", "BSBIO(GEN)" , "BSBIO(AnBio)", "BSSTAT",
                                                 "BSCS", "BSIT", "BSCA", "CCS",
                                                 "BSE (CHEM.)", "BSED CHEM", "BTLED-HE", "BPED", "BSED FIL", "BEED (SCH)", "BEED SCI MAT", "BPE-SPE", "BSED MATH", "BSED PHYS", "BEED Lang Ed", "BSED BIO", "BTVTED-DT", "BTLED-IA", "BSE(G.S)", "CPRT",
                                                 "BA LCS", "BA FIL", "BS PHIL", "BA PAN", "BS PSYCH", "SSSP", "ABENG", "BA HISTORY", "BA SOCIO", "BA PSYCH", "BA ELS", "BA POL SCI",
                                                 "BSA", "BS Econ", "BSBA-BE", "BSBA", "BSENTREP", "BSBA-MM",
                                                 "BSN"
                                                ], state="readonly", font=("Osaka", 12), textvariable=Course_Code, width=25)
        self.txtyear.place(x=255,y=250)
        

        self.lblyear = Label(self, font=("Osaka", 12,"bold"), text="Year Level:", padx=5, pady=5)
        self.lblyear.place(x=125,y=300)
        self.txtyear = ttk.Combobox(self, value=["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"], state="readonly", font=("Osaka", 13), textvariable=Student_YearLevel, width=25)
        self.txtyear.place(x=255,y=300)
        
        self.lblgender = Label(self, font=("Osaka", 12,"bold"), text="Gender:", padx=5, pady=5)
        self.lblgender.place(x=125,y=350)
        self.txtgender = ttk.Combobox(self, value=["Male", "Female"], font=("Osaka", 13), state="readonly", textvariable=Student_Gender, width=25)
        self.txtgender.place(x=255,y=350)

        self.SearchBar = Entry(self, font=("Osaka", 11), textvariable=SearchBar_Var, bd=0,bg="White", width=31)
        self.SearchBar.place(x=876,y=110)

        #======================================================================Treeview=====================================================================#
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1215,y=140,height=390)

        self.studentlist = ttk.Treeview(self, columns=("ID Number", "Name", "Course", "Year Level", "Gender"), height = 18, yscrollcommand=scrollbar.set)

        self.studentlist.heading("ID Number", text="ID Number", anchor=W)
        self.studentlist.heading("Name", text="Name",anchor=W)
        self.studentlist.heading("Course", text="Course",anchor=W)
        self.studentlist.heading("Year Level", text="Year Level",anchor=W)
        self.studentlist.heading("Gender", text="Gender",anchor=W)
        self.studentlist['show'] = 'headings'

        self.studentlist.column("ID Number", width=100, anchor=W, stretch=False)
        self.studentlist.column("Name", width=200, stretch=False)
        self.studentlist.column("Course", width=130, anchor=W, stretch=False)
        self.studentlist.column("Year Level", width=100, anchor=W, stretch=False)
        self.studentlist.column("Gender", width=100, anchor=W, stretch=False)
        
        self.studentlist.bind("<Double-1>",OnDoubleClick)
        
        

        self.studentlist.place(x=575,y=140)
        scrollbar.config(command=self.studentlist.yview)
        
        #======================================================================Buttons======================================================================#
        

        home = tk.Button(self, text="Home",font=("Osaka",12,"bold"),bd=0, width = 7, bg="Cadet Blue", fg="Black",  command=lambda: controller.show(Home))
        home.place(x=575,y=105)
        home.config(cursor= "hand2")

        self.add = Button(self, text="Add", font=('Osaka', 12), height=1, width=10, bd=1,  bg="Cadet Blue", fg="Black", command=add_stud)
        self.add.place(x=150,y=420)
        self.add.config(cursor= "hand2")

        self.update = Button(self, text="Edit", font=('Osaka', 12), height=1, width=10, bd=1, bg="Cadet Blue", fg="Black", command=update_stud)
        self.update.place(x=250,y=420)
        self.update.config(cursor= "hand2")

        self.clear = Button(self, text="Clear", font=('Osaka', 12), height=1, width=10, bd=1, bg="Cadet Blue", fg="Black", command=clear)
        self.clear.place(x=350,y=420)
        self.clear.config(cursor= "hand2")

        self.delete = Button(self, text="Delete", font=('Osaka', 12), height=1, width=10, bd=1, bg="Cadet Blue", fg="Black", command=delete_stud)
        self.delete.place(x=450,y=420)
        self.delete.config(cursor= "hand2")

        self.search = Button(self, text="Search", font=('Osaka', 12, 'bold'),bd=0, bg= "Cadet Blue", fg="Black", command=search_stud)
        self.search.place(x=1140,y=100)
        self.search.config(cursor= "hand2")

        self.display = Button(self, text="Display", font=('Osaka', 12, 'bold'), bd=0, width=7,  bg="Cadet Blue", fg="Black",command = display_stud)
        self.display.place(x=660,y=105)
        self.display.config(cursor= "hand2")

        tables()
        display_stud()

#####################################################################################################################################################################################

root = sis()
root.geometry("1260x600")

root.mainloop()
