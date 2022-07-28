from flask import render_template, redirect, render_template_string, session, request
from app import app
from app.models.milestone import Milestone
from app.controllers import users

@app.route('/<selected>/milestone/new')
def milestone_in(selected):
    return render_template('create_milestone.html', selected = selected)

@app.route('/milestone/create', methods=['POST'])
def create_milestone():
    if not Milestone.validation(request.form):
        return render_template('create_milestone.html')
    selected = Milestone.create_milestone(request.form)
    goal = request.form['goal_id']
    return redirect(f'/goal/display/{goal}')
@app.route('/milestone/display/<selected>')
def display_milestone(selected):
    milestone = Milestone.show_milestone(selected)
    return render_template('milestone.html', milestone = milestone)
        
@app.route('/milestone/edit/<selected>')
def edit_milestone(selected):
    milestone = Milestone.show_milestone(selected)
    return render_template('edit_milestone.html', milestone = milestone)

@app.route('/change/milestone', methods=['POST'])
def change_milestone():
    if not Milestone.validation(request.form):
        return render_template('edit_milestone.html', milestone = request.form)
    Milestone.edit_milestone(request.form)
    milestone = request.form['id']
    return redirect(f'/milestone/display/{milestone}')

@app.route('/delete/milestone/<goal>/<selected>')
def delete_milestone(goal, selected):
    Milestone.delete_milestone(goal, selected)
    return redirect(f'/goal/display/{goal}')