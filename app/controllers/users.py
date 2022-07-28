from flask import render_template, redirect, session, request
from app import app
from app.models.user import User
from app.models.goal import Goal

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/regi', methods=['POST'])
def create():
    if not User.validation(request.form):
        return render_template('register.html')
    selected = User.create_user(request.form)
    return redirect(f'/{selected.id}/dashboard')

@app.route('/<selected>/profile')
def profile(selected):
    return render_template('profile.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/log', methods=['POST'])
def enter():
    if not User.check_login(request.form):
        return render_template('login.html')
    selected = User.check_login(request.form)
    return redirect(f'/{selected.id}/dashboard')

@app.route('/<user>/profile/edit')
def edit_profile(user):
    return render_template('edit_profile.html')

@app.route('/profile/change', methods=['POST'])
def make_changes():
    uploaded_file = request.files['file']
    uploaded_file.filename = 'user_picture.jpg'
    uploaded_file.save("app\static\media\\"+uploaded_file.filename)
    selected = User.edit_user(request.form)
    return redirect(f'/{selected}/profile')

@app.route(f'/<user>/dashboard')
def dashboard(user):
    goals = Goal.user_goals()
    return render_template('dashboard.html', goals = goals)

@app.route('/logout')
def logout():
    User.logout()
    return redirect('/login')