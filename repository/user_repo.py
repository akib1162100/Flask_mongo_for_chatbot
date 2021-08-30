from app import mysql , mongo
from models.user import User
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash


def user_purse(field_names, values):
        user = dict(zip(field_names, values))
        return user

class User_repository():

    @staticmethod
    def get_all():
        users = []
        cursor = mysql.connect.cursor()
        try:
            cursor.execute("SELECT * FROM users")
            rv = cursor.fetchall()
            field_names = [i[0] for i in cursor.description]
            for i in range(len(rv)):
                user = user_purse(field_names,rv[i]) 
                users.append(user)
            return "OK",users,200
        except TypeError as e:
            return e,None,400
        except Exception as e:
            return e,None,400
        finally:
            cursor.close()
    
    @staticmethod
    def get_by_id(id):
        cursor = mysql.connection.cursor()
        user = None
        try:
            cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
            rv = cursor.fetchone()
            field_names = [i[0] for i in cursor.description]
            user = user_purse(field_names,rv)
            return "OK",user,200
        except MySQL.Error as e:
            return e,None,500
        except TypeError as e:
            return e,None,400
        except Exception as e:
            return e,None,400
        finally:
            cursor.close()

    @staticmethod
    def get_user_by_id(id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        rv = cursor.fetchone()
        field_names = [i[0] for i in cursor.description]
        user = user_purse(field_names,rv)
        return user
            

    @staticmethod
    def get_by_username( username):
        cursor = mysql.connection.cursor()
        user = None
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            rv = cursor.fetchone()
            field_names = [i[0] for i in cursor.description]
            user = user_purse(field_names,rv)
            return user
        except Exception as e:
            return None
        finally:
            cursor.close()

    @staticmethod
    def create(id, username, password):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''INSERT INTO users(username, password, id) VALUES(%s, %s, %s)''', (username,password,id))
            cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
            rv = cursor.fetchone()
            field_names = [i[0] for i in cursor.description]
            user = user_purse(field_names,rv)
            return "Created",user,201
        except MySQL.Error as e:
            return e,None,500
        except TypeError as e:
            return e,None,400
        except Exception as e:
            return e,None,400
        finally:
            cursor.close()

    @staticmethod
    def update(id,username, password):
        cursor = mysql.connection.cursor()
        user = None
        try:
            cursor.execute('''UPDATE users SET username = %s, password = %s WHERE id = %s''', (username, password, id))
            cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
            rv = cursor.fetchone()
            field_names = [i[0] for i in cursor.description]
            user = user_purse(field_names,rv)
            print(user)
            return "Updated",user,201
        except MySQL.Error as e:
            return e,None,500
        except TypeError as e:
            return e,None,400
        except Exception as e:
            return e,None,400
        finally:
            cursor.close()
        
    
    @staticmethod
    def delete(id):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = %s", (id,))
            return "SUCCESS",True,200
        except MySQL.Error as e:
            return e,None,500
        except TypeError as e:
            return e,None,400
        except Exception as e:
            return e,None,400
        finally:
            cursor.close()
    
    @staticmethod
    def get_all_ids():
        cursor = mysql.connection.cursor()
        ids = []
        cursor.execute("SELECT id FROM users")
        rv = cursor.fetchall()
        for i in range(len(rv)):
            ids.append(rv[i][0])
        cursor.close()
        return ids
    
    @staticmethod
    def update_jwt_token(id,jwt_token,last_login):
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE users SET jwt_token = %s, last_login = %s WHERE id = %s''', (jwt_token, last_login, id))
        cursor.close()

class User_mongo_repository():
    @staticmethod
    def get_all():
        users = []
        cursor = mongo.db.users.find()
        try:
            for user in cursor:
                users.append(user)
            return "Success",users,200
        except Exception as e:
            return e,None,400
        finally:
            cursor.close()

    @staticmethod

    def get_by_id(id):
        cursor = mongo.db.users.find_one({"id":id})
        if cursor:
            return "Success",cursor,200
        else:
            return "Not Found",None,404
    
    @staticmethod

    def get_by_username( username):
        cursor = mongo.db.users.find_one({"username":username})
        if cursor:
            return "Success",cursor,200
        else:
            return "Not Found",None,404
    
    @staticmethod
    def create(id, username, password):
        user = None
        try:
            cursor = mongo.db.users.insert_one({"id":id, "username":username, "password":password})
            user = mongo.db.users.find_one({"id":id})
            return "Created",user,201
        except Exception as e:
            return e,None,500
        # finally:
        #     cursor.close()
    
    @staticmethod
    def update(id,username, password):
        user = None
        try:
            cursor = mongo.db.users.update_one({"id":id}, {"$set":{"username":username, "password":password}})
            user = mongo.db.users.find_one({"id":id})
            return "Updated",user,201
        except Exception as e:
            return e,None,500
        finally:
            cursor.close()
    
    @staticmethod
    def delete(id):
        try:
            cursor = mongo.db.users.delete_one({"id":id})
            return "SUCCESS",True,200
        except Exception as e:
            return e,None,500
    
    @staticmethod
    def get_all_ids():
        cursor = mongo.db.users.find()
        ids = []
        for user in cursor:
            ids.append(user["id"])
        return ids
    
    @staticmethod
    def update_jwt_token(id,jwt_token,last_login):
        cursor = mongo.db.users.update_one({"id":id}, {"$set":{"jwt_token":jwt_token, "last_login":last_login}})
        return cursor


    