from flask import Flask, render_template, request
from database import connectdb

SECRIT_KEY = "dTJ(K68{^M#3e`q}ZXCARE}TJ(K68{"
app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


######## Function to get Courses Information from database #############
@app.get("/courses")
def courses():
    connection = connectdb()
    query = """
        SELECT cs.course_name as course_name, lvs.level_name as level_name,
            cs.max_capacity as max_capacity, cs.rate_per_hour as rate_per_hour 
        FROM courses cs
        LEFT JOIN levels lvs ON cs.level_id=lvs.level_id
        ORDER BY cs.course_id DESC
    """
    result = list(connection.run_sql(query))
    context = [
        {
            "course_name": course_name,
            "level_name": level_name,
            "max_capacity": max_capacity,
            "rate_per_hour": rate_per_hour,
        }
        for course_name, level_name, max_capacity, rate_per_hour in result
    ]
    return render_template("courses.html", courses=context)


############ Function to get all formation for students from database ###########

@app.get("/students")
def students():
    connection = connectdb()
    query = """
        SELECT std.student_name as student_name, lvs.level_name as level_name,
            std.dob as dob, cts.mobile_number as mobile_number, cts.email as email,
            ad.address as address

        FROM students std
        LEFT JOIN levels lvs ON std.level_id=lvs.level_id
        LEFT JOIN contacts cts ON std.contact_id=cts.contact_id
        LEFT JOIN addresses ad ON std.address_id=ad.address_id
        ORDER BY std.student_id DESC
    """
    result = list(connection.run_sql(query))
    context = [
        {
            "student_name": student_name,
            "level_name": level_name,
            "dob": dob,
            "mobile_number": mobile_number,
            "email": email,
            "address": address,
        }
        for student_name, level_name, dob, mobile_number, email, address in result
    ]
    return render_template("students.html", students=context)


############ Function to Get all schedules information from database ################
@app.get("/schedules")
def schedules():
    connection = connectdb()
    query = """
        SELECT c.course_name as course_name, lvs.level_name as level_name,
        cs.day as day, cs.duration as duration, cs.start_time as start_time, DATE_ADD(start_time, INTERVAL duration HOUR) as end_time
        FROM courses_schedule cs
        LEFT JOIN courses c ON cs.course_id=c.course_id
        LEFT JOIN levels lvs ON c.level_id=lvs.level_id
        ORDER BY start_time
    """
    result = list(connection.run_sql(query))
    friday = []
    saturday = []
    sunday = []
    monday = []
    tuesday = []
    wednesday = []
    thursday = []

    for course_name, level_name, day, duration, start_time, end_time in result:
        if f"{day}".lower() == "sunday":
            arr = sunday
        elif f"{day}".lower() == "monday":
            arr = monday
        elif f"{day}".lower() == "tuesday":
            arr = tuesday
        elif f"{day}".lower() == "wednesday":
            arr = wednesday
        elif f"{day}".lower() == "thursday":
            arr = thursday
        elif f"{day}".lower() == "friday":
            arr = friday
        elif f"{day}".lower() == "saturday":
            arr = saturday
        else:
            arr = sunday
        arr.append(
            {
                "course_name": course_name,
                "level_name": level_name,
                "day": day,
                "duration": duration,
                "start_time": str(start_time),
                "end_time": str(end_time),
            }
        )
    return render_template("schedules.html", sunday=sunday, monday=monday, thursday=thursday,
                           tuesday=tuesday, wednesday=wednesday, friday=friday, saturday=saturday)


################################   API Configuration  #############################################

@app.get("/api/version/students")
@app.get("/api/version/students/")
def api_students():

    ####### HTTP GET Request with Authorization By Key ###############

    access_token = request.headers.get('Authorization', "")
    if access_token != f"Bearer {SECRIT_KEY}":
        return {
            "ok": False,
            "code": 403,
            "length": 0,
            "students": [],
            "message": "Not Allowed to Accesses",
        }
    connection = connectdb()
    query = """
        SELECT std.student_id as id, std.student_name as student_name, lvs.level_name as level_name,
            std.dob as dob, cts.mobile_number as mobile_number, cts.email as email,
            ad.address as address
        FROM students std
        LEFT JOIN levels lvs ON std.level_id=lvs.level_id
        LEFT JOIN contacts cts ON std.contact_id=cts.contact_id
        LEFT JOIN addresses ad ON std.address_id=ad.address_id
        ORDER BY std.student_name
    """
    result = list(connection.run_sql(query))
    students = [
        {
            "student_name": student_name,
            "id": id,
            "level_name": level_name,
            "dob": str(dob),
            "mobile_number": mobile_number,
            "email": email,
            "address": address,
        }
        for id, student_name, level_name, dob, mobile_number, email, address in result
    ]
    return {
        "ok": True,
        "code": 200,
        "length": len(students),
        "data": students,
        "message": "Get Student Lists",
    }


@app.get("/api/version/students/<int:student_id>")
def api_student_details(student_id):
    access_token = request.headers.get('Authorization', "")
    if access_token != f"Bearer {SECRIT_KEY}":
        return {
            "ok": False,
            "code": 403,
            "student": {},
            "message": "Not Allowed to Accesses",
        }
    connection = connectdb()
    query = f"""
        SELECT std.student_id as student_id, std.student_name as student_name, lvs.level_name as level_name,
            std.dob as dob, cts.mobile_number as mobile_number, cts.email as email,
            ad.address as address
        FROM students std
        LEFT JOIN levels lvs ON std.level_id=lvs.level_id
        LEFT JOIN contacts cts ON std.contact_id=cts.contact_id
        LEFT JOIN addresses ad ON std.address_id=ad.address_id
        WHERE std.student_id={student_id}
        ORDER BY std.student_name
    """

    result = list(connection.run_sql(query))
    if len(result) == 0:
        return {
            "ok": False,
            "code": 404,
            "data": {},
            "search_id": student_id,
            "message": "Student not Found",
        }
    std = [
        {
            "student_name": student_name,
            "student_id": student_id,
            "level_name": level_name,
            "dob": str(dob),
            "mobile_number": mobile_number,
            "email": email,
            "address": address,
        }
        for student_id, student_name, level_name, dob, mobile_number, email, address in result
    ]
    return {
        "ok": True,
        "code": 200,
        "data": std[0],
        "search_id": student_id,
        "message": "Student Found",
    }


if __name__ == '__main__':
    app.run(debug=True)
