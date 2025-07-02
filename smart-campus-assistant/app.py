from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import timedelta
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=10)

# In-memory users dictionary
users = {}


@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))


@app.route('/index')
def index():
    return render_template("index.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        users[username] = {
            "email": email,
            "password": password
        }
        flash("Sign in successful! Please log in.")

        return redirect("/login")
    return render_template("signin.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["username"] = username
            flash("Logged in successfully!")
            return redirect(url_for('index'))
        else:
            error = "Invalid credentials"
            return render_template("login.html", error=error)
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if 'username' in session:
        return render_template("index.html", username=session['username'])
    flash("Please login to access the dashboard.")
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully!")
    return redirect(url_for('index'))


@app.route('/events')
def events():
    if "username" in session:
        return render_template("events.html", username=session["username"])
    flash("Please login to access Events.")
    return redirect(url_for("login"))


@app.route('/get_events')
def get_events():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify([
        {"title": "Project Review", "start": "2025-05-10"},
        {"title": "Semester Exam", "start": "2025-05-25"},
        {"title": "Dance Practice", "start": "2025-05-12"}
    ])


@app.route('/calendar')
def calendar():
    if "username" in session:
        return render_template('calendar.html', username=session["username"])
    flash("Please login to access Calendar.")
    return redirect(url_for("login"))


@app.route('/taskmanager')
def taskmanager():
    if "username" in session:
        return render_template('taskmanager.html', username=session["username"])
    flash("Please login to access Task Manager.")
    return redirect(url_for("login"))


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    with open('registrations.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data['name'], data['email'], data['event']])
    return jsonify({'message': 'Registration successful!'})


@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    task_due = request.form['task_due']
    return redirect(url_for('taskmanager'))


if __name__ == '__main__':
    app.run(debug=True)
