from app import mysql
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


    