from flask import render_template, redirect, render_template_string, session, request
from app import app
from app.models.goal import Goal
from app.models.milestone import Milestone
from app.controllers import users

@app.route('/<selected>/goal/new')
def goal_in(selected):
    return render_template('create_goal.html')

@app.route('/goal/create', methods=['POST'])
def create_goal():
    if not Goal.validation(request.form):
        return render_template('create_goal.html')
    selected = Goal.create_goal(request.form)
    return redirect(f'/goal/display/{selected.id}')

@app.route('/goal/display/<selected>')
def display_goal(selected):
    goal = Goal.show_goal(selected)
    milestones = Milestone.goal_milestones(selected)
    return render_template('goal.html', goal = goal, milestones = milestones)

@app.route('/edit/<selected>')
def edit_goal(selected):
    goal = Goal.show_goal(selected)
    return render_template('edit_goal.html', goal = goal)

@app.route('/change/goal', methods=['POST'])
def change_goal():
    if not Goal.validation(request.form):
        return render_template('edit_goal.html', goal = request.form)
    Goal.edit_goal(request.form)
    goal = request.form['id']
    return redirect(f'/goal/display/{goal}')

@app.route('/delete/<selected>')
def delete_goal(selected):
    Goal.delete_goal(selected)
    user = session['id']
    return redirect(f'/{user}/dashboard')