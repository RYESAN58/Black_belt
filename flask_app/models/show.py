from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Show:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.network = db_data['network']
        self.release = db_data['release']
        self.description = db_data['description']
        self.User_id = db_data['User_id']



    #Create instance of data
    @classmethod
    def create(cls, data):
        query = "INSERT INTO `black`.`shows` (`title`, `network`, `release`, `description`, `User_id`) VALUES (%(title)s, %(network)s, %(release)s, %(description)s, %(user_id)s);"
        return connectToMySQL("black").query_db(query,data)


    #retrieve all the data
    @classmethod
    def retrieve(cls):
        query = 'SELECT * FROM shows'
        which = connectToMySQL('black').query_db(query)
        descriptions = []
        for i in which:
            descriptions.append(cls(i))
        return descriptions


    #retriever all specific data
    @classmethod
    def retrieve_by(cls, data):
        query = "SELECT * FROM shows WHERE id = %(id)s"
        return connectToMySQL('black').query_db(query, data)


    #update data
    @classmethod
    def update(cls, data):
        query = "UPDATE `black`.`shows` SET `title` = %(title)s, `network` = %(network)s, `release` = %(release)s, `description` = %(description)s WHERE (`id` = %(id)s);"
        return connectToMySQL('black').query_db(query, data)


    #delete row 
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM `black`.`shows` WHERE (`id` = %(id)s);"
        return connectToMySQL('black').query_db(query, data)


    @staticmethod
    def validate(user):
        is_valid = True
        if len(user['title']) < 1:
            flash("title requiered")
            is_valid = False
        if len(user['network']) < 1:
            flash("Must have a network")
            is_valid = False
        if len(user['release']) < 1:
            flash("Must have a release")
            is_valid = False
        if len(user['description']) < 1 :
            flash("Must type something in description")
            is_valid = False
        return is_valid


    @classmethod
    def get_all_shows(cls):
        query = "select a.title , a.network ,a.release ,  a.id as shownum, b.id as user, concat(b.firstname, ' ', b.lastname) as owner from shows a join user b on a.user_id = b.id"
        print(query)
        return connectToMySQL('black').query_db(query)


    @classmethod
    def get_join(cls, data):
        query= "SELECT a.title ,a.network ,a.description ,a.release ,b.firstname ,b.lastname ,b.id ,a.id ,a.user_id FROM Shows a JOIN user b ON a.user_id = b.id where a.id = %(id)s"
        return connectToMySQL('black').query_db(query, data)


    @classmethod
    def like(cls, data):
        query = 'INSERT INTO `booksauthors`.`favorites` (`Author_id`, `book_id`) VALUES (%(Author_id)s, %(book_id)s);'
        return connectToMySQL('booksauthors').query_db(query,data)