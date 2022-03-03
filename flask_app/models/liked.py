from flask_app.config.mysqlconnection import connectToMySQL



class Liked():
    def __init__(self, db_data):
        self.user_id = db_data['user_id']
        self.show_id = db_data['show_id']

    @classmethod
    def like(cls, data):
        query = "INSERT INTO `black`.`liked` (`show_id`, `user_id`) VALUES (%(show_id)s, %(user_id)s );"
        return connectToMySQL('black').query_db(query,data)

##############################################################################################################

    @classmethod
    def liked_by (cls,data):
        query = "select * from liked where user_id = %(id)s"
        print(query)
        return connectToMySQL('black').query_db(query,data)


##############################################################################################################


    @classmethod
    def unlike(cls,data):
        query = "DELETE FROM `black`.`liked` WHERE (`show_id` = %(show_id)s) and (`user_id` = %(user_id)s);"
        return connectToMySQL('black').query_db(query,data)


###############################################################################################################

    @classmethod
    def total_likes(cls, data):
        query = 'SELECT COUNT(show_id) as show_id from liked where show_id = %(id)s'
        print(query)
        return connectToMySQL('black').query_db(query,data)