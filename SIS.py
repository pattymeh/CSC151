# Student Information System
import csv
# Define variables
rec_fields = [ 'Id number','name','year level','gender','course']
sms_database = 'students.csv'
def show_menu():
    print("-------------------------------------------------------------------")
    print(" Welcome to Students Information System")
    print("-------------------------------------------------------------------")
    print("1. Display List of Students")
    print("2. Add New Students")
    print("3. Edit Student")
    print("4. Delete a Student")
    print("5. Search a Student by Id Number")
    print("6. Exit")
def create_record():
    print("-------------------------------------------------------------------")
    print(" Welcome to Students Information System")
    print("-------------------------------------------------------------------")
    global rec_fields
    global sms_database
    stud_data = []
    for field in rec_fields:
        value = input("Enter " + field + ": ")
        stud_data.append(value)

    with open(sms_database, "a", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows([stud_data])
    print("Data saved successfully")
    input("Press any key to continue")
    return
def display_student():
    global rec_fields
    global sms_database
    print("---Student Records---")
    with open(sms_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for k in rec_fields:
            print(k, end='\t |')
        print("\n-------------------------------------------------------------")
        for row in reader:
            for item in row:
                print(item, end="\t |")
            print("\n")
    input("Press any key to continue")
    
def edit_record():
    global rec_fields
    global sms_database
    
    print("--- Edit Student---")
    Id = input("Enter Id Number to Edit: ")
    idx_student = None
    edit_rec = []
    with open(sms_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        counter = 0
        for row in reader:
            if len(row) > 0:
                if Id == row[0]:
                    idx_student = counter
                    print("Student Found: at index ", idx_student)
                    stud_data = []
                    for field in rec_fields:
                        value = input("Enter " + field + ": ")
                        stud_data.append(value)
                    edit_rec.append(stud_data)
                else:
                    edit_rec.append(row)
                counter += 1

    if idx_student is not None:
        with open(sms_database, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(edit_rec)
    else:
        print("Id Number does not exist")

    input("Press any key to continue")

def delete_record():
    global rec_fields
    global sms_database
    
    print("--- Delete Student---")
    Id = input("Enter Id Number to delete: ")
    stud_locate = False
    edit_rec = []
    with open(sms_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        counter = 0
        for row in reader:
            if len(row) > 0:
                if Id != row[0]:
                    edit_rec.append(row)
                    counter += 1
                else:
                    stud_locate = True
    if stud_locate is True:
        with open(sms_database, "r", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(edit_rec)
        print("Id Number ", Id, "deleted successfully")
    else:
        print("Id Number does not exist")
    input("Press any key to continue")

def search_record():
    global rec_fields
    global sms_database
    print("--- Search Student---")
    Id = input("Enter Id Number to search: ")
    with open(sms_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 0:
                if Id == row[0]:
                   print("---Student Found---")
                   print("Id: ", row[0])
                   print("Name: ", row[1])
                   print("Year Level: ", row[2])
                   print("Gender: ", row[3])
                   print("Course: ", row[4])
                   break
        else:
            print("Id Number does not exist")
    input("Press any key to continue")

while True:
    show_menu()
    option = input("Enter your option: ")
    if option == '1':
        display_student()
    elif option == '2':
        create_record()
    elif option == '3':
        edit_record()
    elif option == '4':
        delete_record()
    elif option == '5':
        search_record()
    else:
        break


print("-------------------------------------------------------------------")
print(" Student Information System")
print("-------------------------------------------------------------------")   




























    
    
            
    
