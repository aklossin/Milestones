from app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from app import app
from app.models.goal import Goal

db = 'milestone_schema'

class Milestone():

    def __init__(self, data):

        self.id = data['id']
        self.stone_name = data['stone_name']
        self.stone_description = data['stone_description']
        self.target_date = data['target_date']
        self.completed_date = ['completed_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.parent = None

    @staticmethod
    def validation(data):
        is_valid = True
        if data['stone_name'] == '':
            is_valid = False
            flash('Milestone needs to have a name')

        return is_valid

    @classmethod
    def create_milestone(cls, data):

        query = """
        INSERT INTO milestones(stone_name, stone_description, target_date, created_at, updated_at, goal_id)
        VALUES (%(stone_name)s, %(stone_description)s, %(target_date)s, NOW(), NOW(), %(goal_id)s);
        """
        result =  connectToMySQL(db).query_db(query, data)
        data2 = {
            'id' : result
        }
        query2 = """
        SELECT *
        FROM milestones 
        WHERE id = %(id)s;
        """
        result2 =  connectToMySQL(db).query_db(query2, data2)
        selected = Milestone(result2[0])
        print(selected.id)
        return selected

    @staticmethod
    def show_milestone(selected):

        data = {
            'id' : selected
        }
        query = """
        SELECT *
        FROM milestones
        WHERE id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)
        return result[0]

    @staticmethod
    def edit_milestone(data):

        query = """UPDATE milestones
        SET stone_name = %(stone_name)s,
        stone_description = %(stone_description)s, 
        target_date = %(target_date)s,
        completed_date = %(completed_date)s, 
        updated_at = NOW() 
        WHERE id = %(id)s;
        """
        connectToMySQL(db).query_db(query, data)
        return data

    @staticmethod
    def delete_milestone(goal, selected):

        data = {
            'id' : selected,
            'goal_id' : goal
        }
        query = """
        DELETE
        FROM milestones
        WHERE id = %(id)s
        AND goal_id = %(goal_id)s;
        """
        connectToMySQL(db).query_db(query, data)

    @classmethod
    def goal_milestones(cls, goal):
        data = {
            'id' : goal
        }
        query = """
        SELECT *
        FROM milestones
        JOIN goals on milestones.goal_id = goals.id
        WHERE goal_id = %(id)s;
        """
        results = connectToMySQL(db).query_db(query, data)
        milestones = []
        for index in results:
            milestone = cls(index)
            milestone_goal = {
                'id' : index['goals.id'],
                'goal_name' : index['goal_name'],
                'goal_type' : index['goal_type'],
                'goal_description' : index['goal_description'],
                'goal_start' : index['goal_start'],
                'goal_end' : index['goal_end'],
                'created_at' : index['goals.created_at'],
                'updated_at' : index['goals.updated_at']
            }
            parent = Goal(milestone_goal)
            Milestone.parent = parent
            milestones.append(milestone)
        return milestones