from app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from app import app
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)
rege = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
db = 'milestone_schema'
pwlength = 8

class User():

    def __init__(self, data):

        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.birthday = data['birthday']
        self.gender = data['gender']
        self.city = data['city']
        self.bio = data['bio']
        self.goals = []

    @staticmethod
    def validation(data):

        is_valid = True
        if data['first_name'] == '':
            is_valid = False
            flash('First name cannot be empty')
        if data['last_name'] == '':
            is_valid = False
            flash('Last name cannot be empty')
        if data['email'] == '':
            is_valid = False
            flash('Email cannot be empty')
        if User.check_email(data):
            flash('Email already registered to an account')
            is_valid = False
        if data['password'] == '':
            is_valid = False
            flash('Password cannot be empty')
        if data['password'] != data['confirm']:
            is_valid = False
            flash('Passwords do not match')
        
        return is_valid

    @staticmethod
    def parse_input(data):

        data = {
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'email' : data['email'],
            'password' : bcrypt.generate_password_hash(data['password'])
        }

        return data
    
    @staticmethod
    def check_login(data):

        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s
        """
        result = connectToMySQL(db).query_db(query, data)
        if not result or bcrypt.check_password_hash(result[0]['password'], data['password']) == False:
            flash('Email or Password is incorrect.', 'login')
            return False
        selected = User.user_info(result)

        return selected

    @classmethod
    def user_info(cls, data):

        user_info = {
            'id' : data[0]['id'],
            'first_name' : data[0]['first_name'],
            'last_name' : data[0]['last_name'],
            'email' : data[0]['email'],
            'birthday' : data[0]['birthday'],
            'gender' : data[0]['gender'],
            'city' : data[0]['city'],
            'bio' : data[0]['bio'],
            'created_at' : data[0]['created_at'],
            'updated_at' : data[0]['updated_at']
        }
        selected = User(user_info)
        User.create_session(user_info)
        
        return selected

    @staticmethod
    def create_session(data):
        session['id'] = data['id']
        session['name'] = data['first_name'] + ' ' + data['last_name']
        session['email'] = data['email']
        session['birthday'] = data['birthday']
        session['gender'] = data['gender']
        session['city'] = data['city']
        session['created_at'] = data['created_at']
        session['bio'] = data['bio']
        # session['user_picture'] = data['user_picture']

    @classmethod
    def check_email(cls, data):

        data = {
            'email' : data['email']
        }
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s
        """
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False

        return True

    @classmethod
    def create_user(cls, data):

        data = User.parse_input(data)
        query = """
        INSERT INTO users(first_name, last_name, email, password, created_at, updated_at)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());
        """
        result =  connectToMySQL(db).query_db(query, data)
        data2 = {
            'id' : result
        }
        query2 = """
        SELECT *
        FROM users
        WHERE id = %(id)s;
        """

        result2 =  connectToMySQL(db).query_db(query2, data2)
        User.create_session(result2[0])
        selected = User(result2[0])
    
        return selected

    @staticmethod
    def edit_user(data):
        
        query = """UPDATE users
        SET birthday = %(birthday)s,
        bio = %(bio)s, 
        city = %(city)s, 
        gender = %(gender)s,
        updated_at = NOW() 
        WHERE id = %(id)s;
        """
        session['bio'] = data['bio']
        session['birthday'] = data['birthday']
        session['gender'] = data['gender']
        session['city'] = data['city']
        return data['id']

    def logout():

        session.clear()