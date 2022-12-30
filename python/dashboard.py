
from datetime import datetime
from database import get_levels, add_student_details, add_course_details, student_enroll, add_course_schedule, \
    get_student_schedule


########## function to ask user input student informaion ########

def add_student():
    print("\n")
    print("Register New Student!")

    ids, levels = get_levels()
    levels_str = ", ".join(levels)
    levels = [level.lower() for level in levels]

    student_name = ""
    dob = ""
    level = ""
    mobile = ""
    email = ""
    address = ""

    while True:
        student_name = input(
            "Enter Student Name : "
        )
        break

    while True:
        dob = input("Enter student date of birth.\n\t[!] Use format YYYY-MM-DD : ")
        dob = datetime.strptime(dob, "%Y-%m-%d")
        break

    while True:
        level = input("Enter student Level.\n\t[!] Select From ({}) : ".format(levels_str))
        level = level.lower()
        if level in levels:
            break
        print("Invalid Level Selected!")

    while True:
        mobile = input("Enter student mobile number.\n\t[!] Only Digits allowed : ")
        break

    while True:
        email = input("Enter student email.\n\t[!] Enter Valid Email : ")
        break

    while True:
        address = input(
            "Enter student address.\n\t[!] Only alphabetical,( _ ), ( - ), digits and white spaces\n\t[!] Multi spaces will ignored : "
        )
        break

    level = ids[levels.index(level)]
    added = add_student_details(student_name, dob, level, mobile, email, address)
    if added:
        print("Student Added successfully")

########## function to ask user input student informaion to enrol it in course ########

def enroll_course():
    std_id = input("Enter student Id. ")
    course_id = input("Enter course Id. ")
    added = student_enroll(std_id, course_id)
    if added:
        print("Student enroll successfully")

########## function to ask user input course informaion to create it ########

def add_course():
    print("\n")
    print("Add New Course!")

    ids, levels = get_levels()
    levels_str = ", ".join(levels)
    levels = [level.lower() for level in levels]

    course_id = -1
    course_name = ""
    level = ""
    max_capacity = 0
    hour_rate = -1
    while True:
        course_id = input("Enter Course Id : ")
        break

    while True:
        course_name = input(
            "Enter Course Name : "
        )
        break

    while True:
        max_capacity = input(
            "Enter Course Capacity: ")
        break

    while True:
        level = input("Enter Course Level.\n\t[!] Select From ({}) : ".format(levels_str))
        level = level.lower()
        if level in levels:
            break
        print("Invalid Level Selected!")

    while True:
        hour_rate = input("Enter Course Hour Rate: ")
        break

    level = ids[levels.index(level)]
    added = add_course_details(course_id, course_name, level, max_capacity, hour_rate)
    if added:
        print("Course Added successfully\n")


def create_schedule():
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekdays_str = ", ".join(weekdays)
    weekdays = [day.lower() for day in weekdays]
    weekday = ""
    course_id = ""
    course_time = ""
    duration = 0

    while True:
        weekday = input("Enter Weekday.\n\t[!] Select From ({}) : ".format(weekdays_str))
        weekday = weekday.lower()
        if weekday in weekdays:
            break
        print("Invalid Weekday Selected!")

    while len(course_id) == 0:
        course_id = input("Enter course Id. ")

    while True:
        course_time = input("Enter Start time.\n\t[!] Use format HH:MM 24 hour format : ")
        course_time = datetime.strptime(course_time, '%H:%M:%S')
        break

    end_time = None
    while True:
        duration = input("Enter Course Duration.\n\tOnly just Positive number values : ")
        break

    added = add_course_schedule(course_id, weekday, course_time, duration, end_time)
    if added:
        print("Course schedule Added successfully")


def display_schedule():
    std_id = input("Enter student Id. ")
    status, data = get_student_schedule(std_id)
    if status:
        print(data)


def main():
    while True:
        print("Welcome to Students Registration")
        print("----------------------------------")
        print("Select one of This options")
        print("[1] Register New Student")
        print("[2] Enroll Course")
        print("[3] Create New Course")
        print("[4] Create New Schedule")
        print("[5] Display Student Courses Schedule")
        print("[6] Exit")
        print("----------------------------------")
        try:
            option = int(input("\tYour Option : "))
        except:
            option = -1
        match option:
            case 1:
                add_student()
            case 2:
                enroll_course()
            case 3:
                add_course()
            case 4:
                create_schedule()
            case 5:
                display_schedule()
            case 6:
                print("Bye!")
                break
            case _:
                print("Option not recognized")


if __name__ == "__main__":
    main()
