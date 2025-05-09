from flask import Flask, redirect, render_template, request, url_for
from flask import flash, session
from flask_sqlalchemy import SQLAlchemy
from app.models import db, User
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learnova.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'learnova.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # (optional, but recommended)

app.secret_key = 'your_secret_key'


# Home Page Route
@app.route('/')
def home():
    return render_template('home.html', title="Learnova - The Best Place to Learn")

# Admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    return render_template('admin/admin_dashboard.html') 

@app.route('/active_users')
def active_users():
    return render_template('admin/active_users.html')

    # Example users list
    users = [
        {"id": 1, "name": "John Doe", "email": "john.doe@example.com", "role": "Student", "status": "Active"},
        {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com", "role": "Teacher", "status": "Active"},
    ]
    return render_template('active_users.html', users=users)

# Add User Route
@app.route('/add_user', methods=['POST'])
def add_user():
    # Retrieve form data
    name = request.form['name']
    email = request.form['email']
    role = request.form['role']

    # Logic to save the user (e.g., database insertion)
    print(f"User Added: {name}, {email}, {role}")  # Simulate saving user

    # Redirect back to Active Users page
    return redirect(url_for('active_users'))

@app.route('/upcoming_exams')
def upcoming_exams():
    return render_template('admin/upcoming_exams.html')

@app.route('/manage_users')
def manage_users():
    return render_template('admin/manage_users.html')

# Teacher Dashboard Route
@app.route('/teacher_dashboard')
def teacher_dashboard():
    if session.get('role') != 'teacher':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    return render_template('teacher/teacher_dashboard.html')


@app.route('/teacher/upload_exam_details')
def upload_exam_details():
    return render_template('teacher/upload_exam_details.html')

@app.route('/teacher/assign_students')
def assign_students():
    return render_template('teacher/assign_students.html')

@app.route('/submit_exam_details', methods=['POST'])
def submit_exam_details():
    # Handle form submission here (e.g., save to database)
    exam_name = request.form['exam_name']
    subject = request.form['subject']
    date = request.form['date']
    time = request.form['time']
    # Add logic to save exam details
    return f'Exam "{exam_name}" submitted successfully!'

@app.route('/assign_students_to_exam', methods=['POST'])
def assign_students_to_exam():
    # Handle form submission here (e.g., save to database)
    exam_id = request.form['exam_id']
    students = request.form.getlist('students[]')  # List of selected student IDs
    # Add logic to assign students to the selected exam
    return f'Students assigned to exam ID {exam_id} successfully!'

@app.route('/student_dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    return render_template('student/student_dashboard.html')

# Repeat similar checks for teacher_dashboard and admin_dashboard


@app.route('/student/attend_exam', methods=['GET', 'POST'])
def attend_exam():
    if request.method == 'POST':
        # Handle exam selection logic here
        exam_id = request.form['exam_id']
        return f"You have started the exam with ID {exam_id}."
    return render_template('student/attend_exam.html')

@app.route('/student/view_results')
def view_results():
    # Render results page
    return render_template('student/view_results.html') 

@app.route('/student/study_materials')
def study_materials():
    # Render results page
    return render_template('student/study_materials.html') 

@app.route('/student/chatbot')
def chat_bot():
    # Render results page
    return render_template('student/chatbot.html') 

# About Page Route
@app.route('/about')
def about():
    return render_template('about.html', title="About Learnova")

# Contact Page Route
@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact Us")


users = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']  # <-- Make sure this is here!
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # ... validation code ...

        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter((User.username==username)|(User.email==username)).first()
        if user and user.check_password(password):
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful!', 'success')
            # Redirect based on user role
            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Unknown user role!', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Invalid username/email or password!', 'danger')
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))  # Redirect to home or login page




if __name__ == '__main__':
    app.run(debug=True)
