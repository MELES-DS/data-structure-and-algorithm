# Dictionary to store student data
students = {}


class Student:
    def __init__(self, student_id, name, score, credit_hour, course):
        self.student_id = student_id
        self.name = name
        self.score = score
        self.credit_hour = credit_hour
        self.course = course

    def get_info(self):
        return f" Name: {self.name}, ID:  {self.student_id},  Course: {self.course}, Credit hour: {self.credit_hour}"

    def get_course(self):
        return self.course

    def get_score(self):
        return f"Score out of 100 is: {self.score} and grade is:{self.get_grade()}"

    def get_credit_hour(self):
        return self.credit_hour

    def get_grade(self):
        if self.score >= 90:
            return "A"
        elif 80 <= self.score < 90:
            return "B"
        elif 70 <= self.score < 80:
            return "C"
        elif 60 <= self.score < 70:
            return "D"
        else:
            return "F"

def display_menu():
    print('''             ################################################################
             $$                Welcome to Student Management System        $$
             $$                                                            $$
             $$                         1. Teacher Login                   $$
             $$                         2. Student Login                   $$
             $$                         3. Exit                            $$
             ################################################################''')

def main():
    while True:
        display_menu()
        choice = input(("\nEnter your choice: ")

        if choice == '1':
            teacher_login()
        elif choice == '2':
            student_id = input("\nEnter your ID number: ")
            if student_id in students:
                print("\nLogin successful!")
                student_menu(student_id)
            else:
                print("\nStudent not found. Please contact your teacher.")
        elif choice == '3':
            print("\nThank you for using our Student Management System!")
            break
        else:
            print("\nInvalid choice. Please try again.")

# Hardcoded teacher username and password
teacher_username = "teacher"
teacher_password = "password"

def teacher_login():
    username = input("\nEnter your username: ")
    password = input("Enter your password: ")

    if username == teacher_username and password == teacher_password:
        print("\nLogin successful!")
        teacher_menu()
    else:
        print("\nInvalid username or password. Please try again.")

def teacher_menu():
    while True:
        print("\nTeacher Menu")
        print("1. Add New Student")
        print("2. View Student List")
        print("3. Calculate Grade")
        print("4. Logout")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            add_student()
        elif choice == '2':
            view_student_list()
        elif choice == '3':
            calculate_grade()
        elif choice == '4':
            print("\nLogged out successfully!")
            break
        else:
            print("\nInvalid choice. Please try again.")


def add_student():
    student_id = input("\nEnter student's ID number: ")
    if student_id in students:
        print("\nStudent already exists.")
        return

    name = input("Enter student's name: ")
    course = input("Enter student's course: ")
    score = float(input("Enter student's score: "))
    if score > 100:
        print("Score cannot be greater than 100.")
        return
    credit_hour = int(input("Enter student's credit hour: "))

    new_student = Student(student_id, name, score, credit_hour, course)
    students[student_id] = new_student
    print("\nStudent added successfully!")

    # Add the new student to the file
    with open("new_students.txt", "a+") as file:
        file.write(f"{name},{student_id},{course},{score},{credit_hour}\n")

def view_student_list():
    if students:
        print("\nStudent List")
        for student_id, student in students.items():
            print(student.get_info())
    else:
        print("\nNo students found.")

def calculate_grade():
    student_id = input("\nEnter student's ID number: ")
    student_registed = students.get(student_id)
    if not student_registed:
        print("\nStudent not found.")
        return

    grade = student_registed.get_grade()
    print(f"\nGrade for student {student_id} is {grade}")

def student_menu(student_id):
    while True:
        print("\nStudent Menu")
        print("1. View Course")
        print("2. View Result")
        print("3. View Credit Hour")
        print("4. Logout")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            print(f"\nCourse for student {student_id} is {students[student_id].get_course()}")
        elif choice == '2':
            print(f"\nResult for student {student_id} is {students[student_id].get_score()}")
        elif choice == '3':
            print(f"\nCredit Hour for student {student_id} is {students[student_id].get_credit_hour()}")
        elif choice == '4':
            print("\nLogged out successfully!")
            break
        else:
            print("\nInvalid choice. Please try again.")

# Call the main function to start the program
main()
