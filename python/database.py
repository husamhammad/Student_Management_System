# Module Imports
import mariadb
import sys


######### Class for store the connection information to make access on database ##############
class DBConnector(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance") or not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, user: str, password: str, host: str, port: int, database: str):
        try:
            self.__conn = mariadb.connect(
                user=user, password=password, host=host, port=port, database=database
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.__cursor = self.__conn.cursor()

    ########## function to get data without any condition #########
    def get_data(self, table: str, fields: tuple) -> list:
        fields_str = ",".join(fields)
        query = f"""
            SELECT {fields_str}
            FROM {table}
        """
        result = []
        self.__cursor.execute(query)
        for data in self.__cursor:
            obj = {}
            for idx, d in enumerate(data):
                k = fields[idx]
                obj.update({f"{k}": d})
            result.append(obj)
        return result

    ########## function to get data with some condition #########

    def get_data_where(self, table: str, fields: tuple, where: str) -> list:
        fields_str = ",".join(fields)
        query = f"""
            SELECT {fields_str}
            FROM {table}
            WHERE {where}
        """
        result = []
        self.__cursor.execute(query)
        for data in self.__cursor:
            obj = {}
            for idx, d in enumerate(data):
                k = fields[idx]
                obj.update({f"{k}": d})
            result.append(obj)
        return result

    ########### Function to define the query execute ##############

    def run_sql(self, query):
        self.__cursor.execute(query)
        return self.__cursor

    ############# Function to make insert guery statment ###############

    def add_data(self, table: str, fields: tuple, values: tuple) -> list:
        fields_str = ",".join(fields)
        marks = ",".join(("? " * len(fields)).split())
        try:
            query = f"INSERT INTO {table} ({fields_str}) VALUES ({marks})"
            print(query)
            print(query)
            print(query)
            print(query)
            print(query)
            self.__cursor.execute(query, list(values))
            return True, self.__cursor.lastrowid
        except mariadb.Error as e:
            print(f"Faield to insert data to table: {e}")
            return False, -1

    ############ Function to make commit for query statment ########
    def commit(self):
        self.__conn.commit()

    def rollback(self):
        self.__conn.rollback()


############ Function to make object from class DBConnector to get all data from it and make access to database by them ###########
def connectdb():
    user = "root"
    password = "husam"
    host = "localhost"
    port = 3306
    DB_name = "student"

    conn = DBConnector(
        user=user, password=password, host=host, port=port, database=DB_name
    )
    return conn

######## Function to show all level from table levels ##########
def get_levels():
    connection = connectdb()
    ids = []
    names = []

    for data in connection.get_data(
            "levels",
            (
                    "level_id",
                    "level_name",
            ),
    ):
        level_id = data.get("level_id")
        level_name = data.get("level_name")
        if level_name and level_id:
            ids.append(level_id)
            names.append(level_name)
    return ids, names

###### function to get the address that input from user and store it in database
def add_address(connection, address):
    add = {
        "address": address,
    }
    return connection.add_data("addresses", add.keys(), add.values())

###### function to  store contact information on database

def add_contact(connection, mobile, email):
    contact = {
        "mobile_number": mobile,
        "email": email,
    }
    return connection.add_data("contacts", contact.keys(), contact.values())

###### function to  store student information on database

def add_student(connection, student_name, dob, level_id, address_id, contact_id):
    student = {
        "student_name": student_name,
        "dob": dob,
        "level_id": level_id,
        "address_id": address_id,
        "contact_id": contact_id,
    }
    return connection.add_data("students", student.keys(), student.values())

###### function to  store student details on database

def add_student_details(student_name, dob, level_id, mobile, email, address):
    connection = connectdb()
    con_done, con_row_id = add_contact(connection, mobile, email)
    if not con_done:
        print(f"Faild to add Contact for student")
        connection.rollback()
        return False
    add_done, add_row_id = add_address(connection, address)
    if not add_done:
        print(f"Faild to add Address for student")
        connection.rollback()
        return False
    std_done, std_id = add_student(
        connection, student_name, dob, level_id, add_row_id, con_row_id
    )
    if not std_done:
        print("Faild to add Student!")
        connection.rollback()
        return False
    connection.commit()
    print("Student Registerd succesfuly")
    return True

###### function to  store course details on database

def add_course_details(course_id, course_name, level, max_capacity, hour_rate):
    connection = connectdb()
    print(course_id, course_name, level, max_capacity, hour_rate)
    course = {
        "course_id": course_id,
        "course_name": course_name,
        "level_id": level,
        "max_capacity": int(max_capacity),
        "rate_per_hour": float(hour_rate),
    }
    is_added, cou_id = connection.add_data("courses", course.keys(), course.values())
    if not is_added:
        print(f"Faild to add Course")
        return False
    connection.commit()
    return True

###### function to enroll student in table enrollment_history on database

def student_enroll(std_id, course_id):
    connection = connectdb()
    # Check Student
    students = list(
        connection.get_data_where(
            "students", ("student_id", "level_id"), f"student_id='{std_id}'"
        )
    )
    if len(students) == 0:
        print(f"Student with id {std_id} Not found!")
        return False

    courses = list(
        connection.get_data_where(
            "courses",
            ("course_id", "level_id", "rate_per_hour", "max_capacity"),
            f"course_id='{course_id}'",
        )
    )
    if len(courses) == 0:
        print(f"Course with id {course_id} Not found!")
        return False

    std_level = students[0].get("level_id")
    cou_level = courses[0].get("level_id")

    if std_level != cou_level:
        print("Course has different Level from Student")
        return False

    courses_schedule = list(
        connection.get_data_where(
            "courses_schedule", ("course_id", "duration"), f"course_id='{course_id}'"
        )
    )
    if len(courses_schedule) == 0:
        print("The Course dose not has any Schedule yet !")
        return False

    student_in_course = list(
        connection.get_data_where(
            "enrollment_history", ("enroll_id",), f"student_id='{std_id}' AND course_id='{course_id}'"
        )
    )
    if len(student_in_course) > 0:
        print("The Student already enrolled to this course !")
        return False

    course_max_capacity = courses[0].get("max_capacity", -1)
    total_students_in_course = list(
        connection.get_data_where(
            "enrollment_history", ("enroll_id",), f"course_id='{course_id}'"
        )
    )
    if len(total_students_in_course) >= course_max_capacity:
        print("thie course is full and student can not enroll")
        return False
    rate_per_hour = courses[0].get("rate_per_hour", 0)
    total_hours = 0
    for cs in courses_schedule:
        total_hours += cs.get("duration", 0)
    from datetime import datetime
    enrollment_history = {
        "student_id": std_id,
        "course_id": course_id,
        "total_hours": total_hours,
        "total": total_hours * rate_per_hour,
        "enroll_date": datetime.now()
    }
    is_added, cou_id = connection.add_data("enrollment_history", enrollment_history.keys(), enrollment_history.values())
    if not is_added:
        print(f"Faild to Enroll!")
        return False
    connection.commit()
    return True


def add_course_schedule(course_id, weekday, start_time, duration, end_time):
    from datetime import datetime, timedelta
    print(course_id, weekday, start_time, duration, end_time)
    connection = connectdb()
    courses = list(
        connection.get_data_where(
            "courses",
            ("course_id", "level_id", "max_capacity"),
            f"course_id='{course_id}'",
        )
    )
    if len(courses) == 0:
        print(f"Course with id {course_id} Not found!")
        return False

    course_in_same_day = list(
        connection.get_data_where(
            "courses_schedule",
            ("course_id",),
            f"course_id='{course_id}' AND day='{weekday}'",
        )
    )
    if len(course_in_same_day) > 0:
        print(f"the course is already in {weekday}")
        return False

    start_str = datetime.strptime(start_time, '%H:%M:%S')
    end_str = datetime.strptime(end_time, '%H:%M:%S')
    query = f"""
          SELECT *
          FROM courses_schedule
          WHERE day='{weekday}' AND (
            (start_time BETWEEN '{start_str}' AND '{end_str}') 
            OR (DATE_ADD(start_time, INTERVAL {duration} HOUR) BETWEEN '{start_str}' AND '{end_str}') )"""
    courses = list(
        connection.run_sql(query)
    )
    if len(courses) > 0:
        print(f"there is overlapping with course time!")
        return False
    schedule = {
        "course_id": course_id,
        "day": weekday.capitalize(),
        "start_time": start_str,
        "duration": duration,
    }
    is_added, cou_id = connection.add_data("courses_schedule", schedule.keys(), schedule.values())
    if not is_added:
        print(f"Faild to add Course")
        return False
    connection.commit()
    return True

###### function to make schedule for student and store it in  table courses_schedule on database

def get_student_schedule(student_id):
    dbconnec = connectdb()
    # Check Student
    students = list(
        dbconnec.get_data_where(
            "students", ("student_id", "level_id"), f"student_id='{student_id}'"
        )
    )
    if len(students) == 0:
        print(f"Student with id {student_id} Not found!")
        return False, []
    data = list(dbconnec.run_sql(f"""
            SELECT s.course_name as course_name, sc.day as day, sc.start_time as start_time,
            DATE_ADD(sc.start_time, INTERVAL sc.duration HOUR) as end_time, sc.duration as duration
            FROM enrollment_history eh
            LEFT JOIN courses s ON s.course_id=eh.course_id
            LEFT JOIN courses_schedule sc ON sc.course_id=s.course_id
            WHERE eh.student_id='{student_id}' """))
    if len(data) == 0:
        print(f"Student dose not enroll to any course!")
        return False, []
    result = [
        {
            "course_name": course_name,
            "day": day,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "duration": duration,
        }
        for course_name, day, start_time, end_time, duration in data
    ]
    return True, result
