from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.firstname = db_data['firstname']
        self.lastname = db_data['lastname']
        self.email = db_data['email']
        self.password = db_data['password']


    #Create instance of data
    @classmethod
    def create(cls, data):
        query = "INSERT INTO `black`.`user` (`firstname`, `lastname`, `email`, `password`) VALUES (%(firstname)s, %(lastname)s, %(email)s, %(password)s);"
        return connectToMySQL("black").query_db(query,data)


    #retrieve all the data
    @classmethod
    def retrieve(cls):
        query = 'SELECT * FROM user'
        which = connectToMySQL('black').query_db(query)
        numbers = []
        for i in which:
            numbers.append(cls(i))
        return numbers


    #retriever all specific data
    @classmethod
    def retrieve_by(cls, data):
        query = "SELECT * FROM user WHERE id = %(id)s"
        return connectToMySQL('black').query_db(query, data)

    @classmethod
    def verify_email(cls,data):
        is_valid = True
        query = 'SELECT * FROM user WHERE email = %(email)s;'
        result = connectToMySQL("black").query_db(query,data)
        if len(result)  != 0:
            flash('This Email is already Taken', 'login')
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        result = connectToMySQL("black").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    #update data
    @classmethod
    def update(cls, data):
        query = "UPDATE `black`.`user` SET `firstname` = %(firstname)s, `lastname`=%(lastname)s, `email`= %(email)s, `password`= %(password)s WHERE (`id` = %(id)s);"
        return connectToMySQL('black').query_db(query, data)

    #delete row 
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM `black`.`user` WHERE (`id` = %(id)s);"
        return connectToMySQL('black').query_db(query, data)


    @staticmethod
    def validate(user):
        is_valid = True
        if len(user['firstname']) < 3:
            flash("firstname must be at least 3 characters.", 'create')
            is_valid = False
        if len(user['lastname']) < 3:
            flash("lastname must be at least 3 characters.", 'create')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'create')
            is_valid = False
        if len(user['password']) < 7:
            flash("password must be at least 7 characters", 'create')
            is_valid = False
        if user['password'] != user['password2']:
            flash('Both passwords must match', 'create')
            is_valid = False
        if len(user['password']) < 8:
            flash('password must be 8 characters', 'create')
            is_valid = False
        return is_valid