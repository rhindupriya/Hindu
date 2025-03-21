from flask import Flask, request, jsonify
from db_connect import connect_to_mysql
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, EmailStr

app = Flask(__name__)

@app.route('/c', methods=['GET'])
def check():
    connection = connect_to_mysql()
    if connection:
        connection.close()
        return jsonify({"message": "Database successful"}), 200
    else:
        return jsonify({"error": "Database failed"}), 500


#Check Database Connection
@app.route('/check_connection', methods=['GET'])
def check_connection():
    connection = connect_to_mysql()
    if connection:
        connection.close()
        return jsonify({"message": "Database connection successful"}), 200
    else:
        return jsonify({"error": "Database connection failed"}), 500

@app.route('/a_projects/<int:project_id>', methods=['POST']) 
def assign_projects(project_id): 
    data = request.get_json() 
 
    startdate = data.get('start_date') 
    enddate = data.get('end_date') 
    userid = data.get('userid') 
    developer_id = data.get('developer_id') 
 
    connection = connect_to_mysql(   ) 
     
    if connection: 
        cursor = connection.cursor(dictionary=True)  # Fetch results as dictionary 
        query = "UPDATE project_create SET start_date=%s, end_date=%s, userid=%s, developer_id=%s WHERE id = %s" 
        cursor.execute(query, (startdate, enddate, userid, developer_id, project_id)) 
        connection.commit()  # Commit the transaction
         
        cursor.close() 
        connection.close() 
 
        return jsonify({"message": "Project updated successfully"}), 200 

@app.route('/si_projects/<int:project_id>', methods=['GET'])
def si_projects(project_id):
    connection = connect_to_mysql()
    
    if connection:
        cursor = connection.cursor(dictionary=True)  # Fetch results as dictionary
        query = "SELECT id, title, description FROM project_create WHERE id = %s"
        cursor.execute(query, (project_id,))
        project = cursor.fetchone()
        
        cursor.close()
        connection.close()

        if project:
            return jsonify({"project": project}), 200
        else:
            return jsonify({"message": "Project not found"}), 404

@app.route('/get_projects', methods=['GET'])
def get_projects():
    connection = connect_to_mysql()
    
    if connection:
        cursor = connection.cursor(dictionary=True)  # Fetch results as dictionary
        query = "SELECT id, title, description FROM project_create"
        cursor.execute(query)
        projects = cursor.fetchall()
        
        cursor.close()
        connection.close()

        return jsonify({"projects": projects}), 200


from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def connect_to_mysql():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            port=3306,
            password="Hindu@123",
            database="project_stack"
        )
    except Exception as e:
        print(f"Database Connection Error: {e}")
        return None

@app.route('/get_projects', methods=['GET'])
def get_projects():
    connection = connect_to_mysql()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id, title, description FROM project_create"
        cursor.execute(query)
        projects = cursor.fetchall()

        return jsonify({"projects": projects}), 200

    except Exception as e:
        return jsonify({"error": f"Database Error: {e}"}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/createteams', methods=['POST'])
def create_team():
    data = request.get_json()
    
    team_name = data.get('team_name')
    developer_id = data.get('developer_id')
    student1 = data.get('student1')
    student2 = data.get('student2')
    student3 = data.get('student3')
    end_date = data.get('end_date')

    connection = connect_to_mysql()

    if connection:
        cursor = connection.cursor()

        # Check if team already exists
        cursor.execute("SELECT COUNT(*) FROM team WHERE team_name = %s", (team_name,))
        result = cursor.fetchone()

        if result[0] > 0:
            return jsonify({"message": "Team with this name already exists"}), 400

        # Insert new team
        query = """
                INSERT INTO team (team_name, developer_id, student1, student2, student3, end_date) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
        values = (team_name, developer_id, student1, student2, student3, end_date)

        try:
            cursor.execute(query, values)
            connection.commit()
            return jsonify({"message": "Team created successfully"}), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({"message": "Database connection failed"}), 500

@app.route('/read_teams', methods=['GET'])
def get_teams():
    connection = connect_to_mysql()
    
    if connection:
        cursor = connection.cursor(dictionary=True)  # Fetch results as a dictionary
        query = "SELECT * FROM team"
        cursor.execute(query)
        teams = cursor.fetchall()
        
        cursor.close()
        connection.close()

        return jsonify({"message":"success", "data": teams}), 200

@app.route('/get_team/<int:team_id>', methods=['GET'])
def get_team(team_id):
    connection = connect_to_mysql()
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM team WHERE team_id = %s"
        cursor.execute(query, (team_id,))
        team = cursor.fetchone()
        
        cursor.close()
        connection.close()

        info = {
            "teamId": team['team_id'], "teamName":team['team_name'],
            "developer" : get_single_student(team['developer_id']),
            "student1" : get_single_student(team['student1']),
            "student2" : get_single_student(team['student2']),
            "student3" : get_single_student(team['student3']),
            "startDate": team['start_date'], "endDate" : team['end_date']
        }
        if team:
            return jsonify({"message": "Success", "data":info}), 200
        else:
            return jsonify({"message": "Team not found"}), 404

def get_single_student(student_id):
    connection = connect_to_mysql()
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id, username, mail, Mobile_Number, Role, Batch_Year, Mentor_Name FROM userdetails WHERE id = %s"
        cursor.execute(query, (student_id,))
        return cursor.fetchone()

#create student

@app.route('/create_student', methods=['POST'])
def create_stuent() :
    user = request.get_json()
    username = user.get('username')
    mail = user.get('mail')
    password = user.get('password')
    mobile_number = user.get('moblie_number')
    register_number =user.get('register_number') 
    batch_year = user.get('batch_year')
    mentor_number  = user.get('mentor_number')
    mentor_name = user.get('mentor_name')
    department = user.get('department')
    date_of_joining =  user.get('date_of_joining')

    password = "welcome"
    usertype = "Student"

    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM userdetails WHERE mail = %s OR register_number = %s", (mail, register_number))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"message": "Email or Register Number already exists"}), 409

    cursor.execute("""
        INSERT INTO userdetails 
        (username, mail, password, mobile_number, role, register_number, batch_year, mentor_number, mentor_name, department, date_of_joining) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        username, mail, password, mobile_number, usertype,
        register_number, batch_year, mentor_number, 
        mentor_name, department, date_of_joining
    ))
    conn.commit()

    return jsonify({"message": "User registered successfully"}), 200


    #create developer

#create developer
@app.route('/create_developer', methods=['POST'])
def create_developer():
    user = request.get_json()

    Bio_Id = user.get('Bio_Id')
    Employee_Id = user.get('Employee_Id')
    username = user.get('username')
    mail = user.get('mail')
    Mobile_Number = user.get('Mobile_Number')
    Designation = user.get('Designation')
    Tech_Stack = user.get('Tech_Stack')
    Experience = user.get('Experience')
    Linked_In = user.get('Linked_In')
    Portfolio = user.get('Portfolio')
    date_of_joining = user.get('date_of_joining')

    password = "welcome"

    conn = connect_to_mysql()
    cursor = conn.cursor()

    # Check for duplicate mail or Bio_Id
    cursor.execute("SELECT * FROM userdetails WHERE mail = %s OR Bio_Id = %s", (mail, Bio_Id))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"message": "mail or Bio_Id already exists"}), 400

    # Insert into userdetails table
    cursor.execute("""
        INSERT INTO userdetails 
        (Bio_Id, Employee_Id, username, mail, password, 
         Mobile_Number, Role, Designation, Tech_Stack, Experience, 
         LinkedIn, Portfolio, date_of_joining) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        Bio_Id, Employee_Id, username, mail, password,
        Mobile_Number, "Developer", Designation, Tech_Stack, Experience,
        Linked_In, Portfolio, date_of_joining
    ))

    conn.commit()
    

    return jsonify({"message": "Developer added successfully"}), 201


@app.route('/updateteam/<int:team_id>', methods=['POST'])
def update_team(team_id):
    data = request.get_json()
    
    team_name = data.get('team_name')
    developer_id = data.get('developer_id')
    student1 = data.get('student1')
    student2 = data.get('student2')
    student3 = data.get('student3')
    end_date = data.get('end_date')

    connection = connect_to_mysql()
    
    if connection:
        cursor = connection.cursor()
        query = """
                UPDATE team 
                SET team_name = %s, developer_id = %s, student1 = %s, student2 = %s, student3 = %s, end_date = %s 
                WHERE team_id = %s
                """
        values = (team_name, developer_id, student1, student2, student3, end_date, team_id)

        cursor.execute(query, values)
        connection.commit()
        
        cursor.close()
        connection.close()

        return jsonify({"message": "Team updated successfully!"}), 200

#delete Team
@app.route('/deleteteam/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    connection = connect_to_mysql()
    
    if connection:
        cursor = connection.cursor()
        query = "DELETE FROM team WHERE team_id = %s"
        cursor.execute(query, (team_id,))
        connection.commit()
        
        cursor.close()
        connection.close()

        return jsonify({"message": "Team deleted successfully!"}), 200

#get studets for creating team
@app.route('/get_students_for_team_creation', methods=['GET'])
def get_student_for_team_creation():
    conn = connect_to_mysql() 

    if conn:
        cursor = conn.cursor(dictionary=True)
        query  = """SELECT id, username, Mail, Mobile_Number, Register_Number FROM userdetails WHERE id NOT IN (SELECT student1 FROM team  UNION ALL
                    SELECT student2 FROM team
                    UNION ALL
                    SELECT student3 FROM team)"""
        cursor.execute(query)
        data = cursor.fetchall()
        return jsonify({"message": "Success", "data": data}), 200


@app.route('/leave_requests', methods=['GET'])
def add_leave_request():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    cursor = None  # ✅ Initialize cursor to avoid UnboundLocalError

    try:
        connection = connect_to_mysql()
        cursor = connection.cursor()

        # Extract values using .get() with defaults (to prevent KeyErrors)
        employee_id = data.get('employee_id')
        leave_from = data.get('leave_from')
        leave_to = data.get('leave_to')

        if not employee_id or not leave_from or not leave_to:
            return jsonify({'error': 'Missing required fields: employee_id, leave_from, leave_to'}), 400

        # Check for duplicate leave request
        check_query = """SELECT COUNT(*) FROM leave_applications 
                         WHERE employee_id = %s AND leave_from = %s AND leave_to = %s"""
        cursor.execute(check_query, (employee_id, leave_from, leave_to))
        (count,) = cursor.fetchone()

        if count > 0:
            return jsonify({'error': 'Duplicate leave request already exists'}), 409  # HTTP 409 Conflict

        # Insert new leave request if no duplicate exists
        insert_query = """INSERT INTO leave_applications 
                          (name, employee_id, designation, department, applied_date, leave_from, leave_to, no_of_days, application_type, reason, status) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending')"""

        cursor.execute(insert_query, (
            data.get('name', 'Unknown'),  # Default: 'Unknown' if name is missing
            employee_id, 
            data.get('designation', 'N/A'),
            data.get('department', 'N/A'),
            data.get('applied_date', '2024-01-01'),  # Default: A placeholder date
            leave_from,
            leave_to,
            data.get('no_of_days', 0),
            data.get('application_type', 'General Leave'),
            data.get('reason', 'No reason provided')
        ))

        connection.commit()
        return jsonify({'message': 'Leave request submitted successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()


@app.route('/leaves', methods=['GET'])
def get_leaves():
    conn = connect_to_mysql()  # ✅ Use the correct function name
    cursor = conn.cursor(dictionary=True)

    status = request.args.get('status', 'Pending')  # Get status from request
    query = "SELECT * FROM leave_applications WHERE status = %s"
    cursor.execute(query, (status,))
    leaves = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(leaves), 200

# if __name__ == '__main__':
#     app.run(debug=True)


@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    conn = connect_to_mysql()
    cursor = conn.cursor()

    # Check if the task already exists for the same registration_id and task_name
    check_query = """SELECT id FROM tasks WHERE registration_id = %s AND task_name = %s"""
    cursor.execute(check_query, (data['registration_id'], data['task_name']))
    existing_task = cursor.fetchone()

    if existing_task:
        return jsonify({"error": "Task already exists for this student!"}), 400  # HTTP 400: Bad Request

    # Insert the new task if no duplicate is found
    insert_query = """INSERT INTO tasks (registration_id, student_name, title, task_name, task_date, eta, status)
                      VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    
    cursor.execute(insert_query, (data['registration_id'], data['student_name'], data['title'], 
                                  data['task_name'], data['task_date'], data['eta'], data['status']))
    
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Task added successfully!"}), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = connect_to_mysql()
    cursor = conn.cursor(dictionary=True)

    registration_id = request.args.get('registration_id')
    status = request.args.get('status')
    developer_id = request.args.get('developer_id')  # New filter for Developer ID

    query = "SELECT * FROM tasks"
    params = []

    conditions = []
    if registration_id:
        conditions.append("registration_id = %s")
        params.append(registration_id)
    if status:
        conditions.append("status = %s")
        params.append(status)
    if developer_id:
        conditions.append("developer_id = %s")
        params.append(developer_id)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return jsonify(tasks), 200


@app.route('/tasks_by_student_id', methods=['GET'])
def student_id():
    conn = connect_to_mysql()
    cursor = conn.cursor(dictionary=True)

    student_id = request.args.get('student_id')
    status = request.args.get('status')

    query = "SELECT * FROM tasks"
    params = []

    if student_id and status:
        query += " WHERE student_id = %s AND status = %s"
        params = [student_id, status]
    elif student_id:
        query += " WHERE student_id = %s"
        params = [student_id]
    elif status:
        query += " WHERE status = %s"
        params = [status]

    cursor.execute(query, params)
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return jsonify(tasks), 200
    # if __name__ == '__main__':
#     app.run(debug=True)

   # GET API to fetch student details
@app.route('/api/students', methods=['GET'])
def get_students():
    connection = connect_to_mysql()
    cursor = connection.cursor()

    # Fetch 15 student records with required fields
    cursor.execute("""
        SELECT id, Register_Number, Mail, Mobile_Number, Department, Username, Batch_Year 
        FROM userdetails 
        WHERE Role = 'Student' 
    """)
    
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    # Convert data into JSON format
    students = [
        {
            "id": row[0],
            "reg_no": row[1],
            "email": row[2],
            "mobile_number": row[3],
            "department": row[4],
            "name": row[5],
            "batch_year": row[6]
        }
        for row in rows
    ]

    return jsonify({"status": "success", "students": students})

@app.route('/api/developers', methods=['GET'])
def get_developers():
    connection = connect_to_mysql()
    cursor = connection.cursor()

    # Fetch 15 developers
    cursor.execute("""
        SELECT Employee_Id, Username AS name, Mail AS email, Mobile_Number AS mobile_number, Date_of_joining
        FROM userdetails
        WHERE Role = 'Developer'
    """)
    
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    # Convert data into JSON format
    developers = [
        {
            "employee_id": row[0],
            "name": row[1],
            "email": row[2],
            "mobile_number": row[3],
            "date_of_joining": row[4].strftime("%Y-%m-%d") if row[4] else None
        }
        for row in rows
    ]

    return jsonify({"status": "success", "developers": developers})

@app.route('/get_attendentance_by_team_id', methods=['POST'])
def get_attendance_list_by_team_id():
    connection = connect_to_mysql()
    data = request.json
    cursor = connection.cursor()
    cursor = connection.cursor(dictionary=True)
    try:

        team_info = [] 

        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM attendance WHERE team_id = %s"
        cursor.execute(query, (data['team_id'],))
        teams = cursor.fetchall()
        # for team in teams:
        #     info = {
        #         "teamId": team['team_id'],
        #         "teamName": team['student2'],
        #         "students": [
        #             get_attendance_details(team['student1']),
        #             get_attendance_details(team['student2']),
        #             get_attendance_details(team['student3'])
        #         ]
        #     }
        #     team_info.append(info)

        if teams:
            return jsonify({"message": "Success", "data":teams}), 200
        else:
            return jsonify({"message": "Team not found"}), 404

    finally:
        cursor.close()
        connection.close()

def get_attendance_details(student_id):
    connection = connect_to_mysql()
    
    if connection:
        cursor = connection.cursor(dictionary=True)
        query  = """SELECT a.date, a.student_name, a.status, a.registration_id FROM team t 
                            left join userdetails u on t.student1 = u.id 
                            left join attendance a on a.registration_id = u.Register_Number 
                            where t.student1 = %s"""
        cursor.execute(query, (student_id,))
        return cursor.fetchone()

@app.post("/attendance")
def attendance():
    connection = connect_to_mysql()
    data = request.json
    cursor = connection.cursor()

    try:
        # Check if the record already exists for today
        cursor.execute(
            "SELECT COUNT(*) FROM attendance WHERE registration_id = %s AND date = %s",
            (data['registration_id'], data['date'])
        )
        result = cursor.fetchone()

        if result[0] > 0:
            # If record exists, update it
            cursor.execute(
                "UPDATE attendance SET status = %s WHERE registration_id = %s AND date = %s",
                (data['status'], data['registration_id'], data['date'])
            )
        else:
            # If record does not exist, insert a new one
            cursor.execute(
                "INSERT INTO attendance (registration_id, student_name, date, status, team_id) VALUES (%s, %s, %s, %s, %s)",
                (data['registration_id'], data['student_name'], data['date'], data['status'], data['team_id'])
            )

        connection.commit()
        return {"message": "Attendance updated successfully"}

    finally:
        cursor.close()
        connection.close()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('Username')
    email = data.get('Mail')
    
    password = data.get('Password')
    confirm_password = data.get('Confirm_Password')
    role = data.get('Role')

    # Validate input fields
    if not username or not email or not password or not confirm_password or not role:
        return jsonify({"error": "All fields are required"}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        try:
            if role == "Student":
                register_number = data.get("Register_Number")
                batch_year = data.get("Batch_Year")
                mentor_number = data.get("Mentor_Number")
                mentor_name = data.get("Mentor_Name")
                department = data.get("Department")

                query = """
                INSERT INTO userdetails (Username, Mail, Password, Role, Register_Number, 
                                   Batch_Year, Mentor_Number, Mentor_Name, Department)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (username, email, password, role, register_number, batch_year, mentor_number, mentor_name, department)

            elif role == "Developer":
                employee_id = data.get("Employee_Id")
                designation = data.get("Designation")
                tech_stack = data.get("Tech_Stack")
                experience = data.get("Experience")
                linkedin = data.get("LinkedIn")
                portfolio = data.get("Portfolio")

                query = """
                INSERT INTO userdetails (Username, Mail, Password, Role, Employee_Id, Designation, 
                                   Tech_Stack, Experience, LinkedIn, Portfolio)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (username, email, password, role, employee_id, designation, tech_stack, experience, linkedin, portfolio)

            elif role == "Admin":
                date_of_joining = data.get("Date_of_joining")

                query = """
                INSERT INTO userdetails (Username, Mail, Password, Role, Date_of_joining)
                VALUES (%s, %s, %s, %s, %s)
                """
                values = (username, email, password, role, date_of_joining)

            else:
                return jsonify({"error": "Invalid role"}), 400

            cursor.execute(query, values)
            connection.commit()
            return jsonify({"message": "Signup successful"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500


# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('Username')
    password = data.get('Password')

    # Validate input fields
    if not username or not password:
        return jsonify({"error": "Username and Password are required"}), 400

    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        try:
            query = "SELECT * FROM userdetails WHERE Username = %s AND Password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                return jsonify({"message": "Login successful", "data": {
                    "user_id":result[0], "username":result[1], "mail":result[2], "mobile":result[4],
                    "role":result[5], "regNo":result[6],"Batchyear":result[7],"mentorname":result[9],"mentorNo":result[8],
                    "departement":result[10],"Bioid":result[11],"employee":result[12],"designation":result[13],"TechStack":result[14],
                    "Experience":result[15],"linkedIn":result[16],"protfile":result[17],"DateofJioning":result[18]
                    }}), 200
            else:
                return jsonify({"error": "Invalid username or password"}), 401

        except Exception as e:
            return jsonify({"error": e}), 500
        
    else:
        return jsonify({"error": "Database connection failed", "login":connection.__doc__}), 500




# Reset Password Endpoint
@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('Mail')
    old_password = data.get('Old_Password')
    new_password = data.get('New_Password')

    if not email or not old_password or not new_password:
        return jsonify({"error": "All fields are required"}), 400

    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        try:
            query = "SELECT Password FROM userdetails WHERE Mail = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user and user[0] == old_password:
                update_query = "UPDATE userdetails SET Password = %s WHERE Mail = %s"
                cursor.execute(update_query, (new_password, email))
                connection.commit()
                return jsonify({"message": "Password reset successful"}), 200
            else:
                return jsonify({"error": "Invalid email or old password"}), 401

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500


if __name__ == '__main__':
    app.run(debug=True)
