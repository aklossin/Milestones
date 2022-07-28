from app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from app import app
from app.models import user

db = 'milestone_schema'

class Goal():

    def __init__(self, data):

        self.id = data['id']
        self.goal_name = data['goal_name']
        self.goal_type = data['goal_type']
        self.description = data['goal_description']
        self.goal_start = data['goal_start']
        self.goal_end = data['goal_end']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.milestones = []

    @staticmethod
    def validation(data):
        
        is_valid = True
        if data['goal_name'] == '':
            is_valid = False
            flash('Your goal needs to have a title')
        if data['goal_start'] == '':
            is_valid = False
            flash('Your goal should have a start date')
        if data['goal_end'] == '':
            is_valid = False
            flash('Your goal should have an end date')
        
        return is_valid  

    @classmethod
    def create_goal(cls, data):

        query = """
        INSERT INTO goals(goal_name, goal_type, goal_description, goal_start, goal_end, created_at, updated_at, user_id)
        VALUES (%(goal_name)s, %(goal_type)s, %(goal_description)s, %(goal_start)s, %(goal_end)s, NOW(), NOW(), %(user_id)s);
        """
        result =  connectToMySQL(db).query_db(query, data)
        data2 = {
            'id' : result
        }
        query2 = """
        SELECT *
        FROM goals
        WHERE id = %(id)s;
        """
        result2 =  connectToMySQL(db).query_db(query2, data2)
        selected = Goal(result2[0])
        return selected

    @staticmethod
    def show_goal(selected):

        data = {
            'id' : selected
        }
        query = """
        SELECT *
        FROM goals
        WHERE id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)
        return result[0]

    @staticmethod
    def edit_goal(data):

        query = """UPDATE goals
        SET goal_name = %(goal_name)s,
        goal_type = %(goal_type)s, 
        goal_description = %(goal_description)s,
        goal_start = %(goal_start)s, 
        goal_end = %(goal_end)s,
        updated_at = NOW() 
        WHERE id = %(id)s;
        """
        connectToMySQL(db).query_db(query, data)
        return data

    @staticmethod
    def delete_goal(selected):

        data = {
            'id' : selected,
            'user_id' : session['id']
        }
        query = """
        DELETE 
        FROM goals
        WHERE id = %(id)s
        AND user_id = %(user_id)s;
        """
        connectToMySQL(db).query_db(query, data)

    @classmethod
    def user_goals(cls):

        data = {
            'id' : session['id']
        }
        query = """
        SELECT *
        FROM goals
        JOIN users on goals.user_id = users.id
        WHERE user_id = %(id)s;
        """
        results = connectToMySQL(db).query_db(query, data)
        goals = []
        for index in results:
            goal = cls(index)
            goal_user = {
                'id' : index['users.id'],
                'first_name' : index['first_name'],
                'last_name' : index['last_name'],
                'email' : index['email'],
                'birthday' : index['birthday'],
                'bio' : index['bio'],
                'gender' : index['gender'],
                'city' : index['city'],
                'created_at' : index['users.created_at'],
                'updated_at' : index['users.updated_at']
            }
            creator = user.User(goal_user)
            Goal.creator = creator
            data2 = {
                'goal_id' : goal.id
            }
            query2 = """
            SELECT * FROM milestones
            WHERE goal_id = %(goal_id)s;
            """
            result2 = connectToMySQL(db).query_db(query2, data2)
            goal.milestones = len(result2)
            goals.append(goal)
        return goals
        
