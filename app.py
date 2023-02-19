import os
import openai
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from functools import wraps
# from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "key"
Session(app)

API_KEY = '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'
openai.api_key = API_KEY

model = 'text-davinci-003'

# openai.api_key = os.environ['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']


db = sqlite3.connect("classmate.db", check_same_thread=False)

topic = None

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signup")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    cursor = db.cursor()
    if request.method == "GET":
        cursor.execute("SELECT topics.course_id,courses.name, topics.name, description FROM ((courses INNER JOIN courses_users  ON courses.id = courses_users.course_id) INNER JOIN topics ON topics.course_id = courses.id) WHERE courses_users.user_id = ?", [session["user_id"]])
        courses = cursor.fetchall()

        cursor.execute("SELECT courses.name FROM courses INNER JOIN courses_users ON courses.id = courses_users.course_id WHERE courses_users.user_id = ?", [session["user_id"]])
        course_name_tuple = cursor.fetchall()
        course_names = []
        for course_name in course_name_tuple:
            course_names.append(course_name[0])
        course_names = list(course_names)


        course_dict = []
        for course in courses:
            new_dict = {}
            new_dict["course_name"] = course[1]
            new_dict["topic_name"] = course[2]
            new_dict["description"] = course[3]
 
            course_dict.append(new_dict)

        
        print(course_dict)
        cursor.close()
        return render_template("index.html", course_dict=course_dict, course_names=course_names)
    else:
        course = request.form.get("course")

        cursor.execute("SELECT topics.course_id,courses.name, topics.name, description FROM ((courses INNER JOIN courses_users  ON courses.id = courses_users.course_id) INNER JOIN topics ON topics.course_id = courses.id) WHERE courses_users.user_id = ? AND courses.name = ?", [session["user_id"], course])
        courses = cursor.fetchall()

        cursor.execute("SELECT courses.name FROM courses INNER JOIN courses_users ON courses.id = courses_users.course_id WHERE courses_users.user_id = ?", [session["user_id"]])
        course_name_tuple = cursor.fetchall()
        course_names = []
        for course_name in course_name_tuple:
            course_names.append(course_name[0])
        course_names = list(course_names)


        course_dict = []
        for course in courses:
            new_dict = {}
            new_dict["course_name"] = course[1]
            new_dict["topic_name"] = course[2]
            new_dict["description"] = course[3]
 
            course_dict.append(new_dict)

        
        print(course_dict)
        cursor.close()
        return render_template("index.html", course_dict=course_dict, course_names=course_names) 

@app.route("/topic", methods=["GET", "POST"])
@login_required
def topic():
    cursor = db.cursor()
    if request.method == "GET":
        cursor.close()
        return render_template("topic.html")
    else:
        if (isinstance(request.form.get("topic"), str)):
            global topic 
            topic = request.form.get("topic")
        cursor.execute("SELECT topics.course_id, topics.name, topics.description, topics.question1, topics.question2, topics.question3 FROM ((courses INNER JOIN courses_users  ON courses.id = courses_users.course_id) INNER JOIN topics ON topics.course_id = courses.id) WHERE courses_users.user_id = ? AND topics.name = ?", [session["user_id"], topic])
        topic_info = cursor.fetchall()
        questions = [topic_info[0][3], topic_info[0][4], topic_info[0][5]]


    

        cursor.execute("SELECT grade FROM users WHERE id = ?", [session["user_id"]])
        grade = cursor.fetchone()[0]
        print(grade)

        prefix_dict = {
            "question": f"Pretend I am {grade}. Please describe it so it is easy to understand for my age.A nswer in one or two paragraphs. If you cannot generate a response, say \"Hmm, sounds like a good question for your teacher.\"",
            "understanding": f"Pretend I am {grade}. I am having trouble understanding a concept in class.  Please give an explanation that is easy to understand for my age. Answer in one or two paragraphs. If you cannot generate a response, say \"Hmm, sounds like a good question for your teacher.\" Explain ",
            "show": f"Pretend I am {grade}. I would like you to show me a complex from class. Please describe it so it is easy to understand for my age. Answer in one or two paragraphs. If you cannot generate a response, say \"Hmm, sounds like a good question for your teacher.\" Show me how to ",
            "moreabout": f"Pretend I am {grade}. I would like to know more about something I'm learning in class. Please give me some information that would not be considered basic. Answer in one or two paragraphs. Please describe it so it is easy to understand for my age. If you cannot generate a response, say \"Hmm, sounds like a good question for your teacher.\" Tell me more about ",
            "example": f"Pretend I am {grade}. I would like an example for something I'm learning in class. Make sure it would be understandable for my age. If you cannot generate a response, say \"Hmm, sounds like a good question for your teacher.\" Give me an example of "
        }

        if (request.form.get("question")):
            question = (request.form.get("question"))
            prefix = prefix_dict["question"]
            response = call_api(prefix+question)

        elif (request.form.get("understanding")):
            question = (request.form.get("understanding"))
            prefix = prefix_dict["understanding"]
            response = call_api(prefix+question)

        elif (request.form.get("show")):
            question = (request.form.get("show"))
            prefix = prefix_dict["show"]
            response = call_api(prefix+question)
        elif (request.form.get("moreabout")):
            question = (request.form.get("moreabout"))
            prefix = prefix_dict["moreabout"]
            response = call_api(prefix+question)

        elif (request.form.get("example")):
            question = (request.form.get("example"))
            prefix = prefix_dict["example"]
            response = call_api(prefix+question)
        else:
            response = None
        print(response)

        cursor.close()
        return render_template("topic.html", topic=topic, questions=questions, response=response)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    cursor = db.cursor()

    if request.method == "POST":
        

        if (request.form.get("studentusername")):
            username = request.form.get("studentusername")
            account = "student"
            if not request.form.get("grade"):
                return "Error: must provide grade"
            grade = request.form.get("grade")
        elif (request.form.get("teacherusername")):
            username = request.form.get("teacherusername")
            account = "teacher"


        else:
            return "Error: must provide username"

        username_count = cursor.execute("SELECT COUNT(username) FROM users WHERE username = ?", [username])
        username_count = username_count.fetchone()[0]
        print(username_count)
        print(cursor.fetchall())

        # username = username[0]["COUNT(username)"]
        # Ensure username was submitted

        # Ensure password was submitted
        if (not request.form.get("password")):
            return "Error: must provide password"

        # Ensure confirmation was submitted
        if (not request.form.get("confirmation")):
            return "Error: must provide confirmation"

        # Ensure password confirm is same as password
        if (request.form.get("confirmation") != request.form.get("password")):
            return "Error: confirmation does not match password"

        # Ensure username does not exist
        if username_count != 0:
            return "Error: username already exists"

        # Insert new user into users table
        cursor.execute("INSERT INTO users (username, password, account, grade) VALUES(?, ?, ?, ?)", [username, request.form.get("password"), account, grade])
        db.commit()

        # Query database for username
        cursor.execute("SELECT * FROM users WHERE username = ?", [username])
        # cursor.execute("SELECT * FROM users")

        rows = cursor.fetchall()


        # Remember which user has logged in
        session["user_id"] = rows[0][1]
        print(session["user_id"])

        cursor.close()
        # Redirect user to home page
        return redirect("/")

    else:
        cursor.close()
        return render_template("signup.html")




@app.route("/login", methods=["GET", "POST"])
def login():
    cursor = db.cursor()
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return "Error: must provide username"

        # Ensure password was submitted
        if not request.form.get("password"):
            return "Error: must provide password"

        # Query database for username
        cursor.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])
        rows = cursor.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or (rows[0][2] != request.form.get("password")):
            return "Error: invalid username and/or password"

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        cursor.close()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        cursor.close()
        return render_template("login.html")

@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form\
    return redirect("/")


def call_api(prompt):
    response = openai.Completion.create(prompt=prompt, model=model, max_tokens=1000, n=1, temperature=0.9, stop=["--"])
    for result in response.choices:
        return result.text


# # openai explanation generator
# @app_route("/", methods=("GET", "POST"))
'''
def index1():
    if request.method=="POST":
        question = request.form["question"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt("question"),
            engine="davinci",
            temperature=0.9,
            max_tokens=512,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
        )

'''

    
if __name__ == "__main__":
    app.run(debug=True)