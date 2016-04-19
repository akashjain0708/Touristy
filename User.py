from werkzeug.security import check_password_hash

"""
Class to handle User for Flask-Login
"""


class User:
    def __init__(self, user_id):
        """
        Method to initialize a User
        :param user_id: ID of the user
        :return:
        """
        self.id = user_id

    def is_authenticated(self):
        """
        Method to return if user is authenticated
        :return: True or False
        """
        return True

    def is_active(self):
        """
        Method to return if user is active
        :return: True or False
        """
        return True

    def is_anonymous(self):
        """
        Method to return if user is anonymous
        :return: False, always
        """
        return False

    def get_id(self):
        """
        Method to return if user ID
        :return: ID of the user
        """
        return self.id

    @staticmethod
    def validate_login(password_hash, password):
        """
        Method to validate password authentication
        :param password_hash: Hashed password from database
        :param password: Password entered by the user
        :return: True or False
        """
        print(password_hash, password)
        return check_password_hash(password_hash, password)
