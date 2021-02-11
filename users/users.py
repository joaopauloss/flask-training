import jwt
import datetime
from flask import current_app
# from constants import user_levels, token_active_time
import json


token_exception_messages = {
    'expired': 'Inactivity timeout has expired.',
    'forbidden': 'Forbidden access.',
    'invalid': 'Invalid authentication.'
}

token_active_time = {
    'days': 0,
    'hours': 0,
    'seconds': 600,
    't_days': 0,
    't_hours': 0,
    't_seconds': 30
}

user_levels = {
    "low": "level:low",
    "medium": "level:medium",
    "high": "level:high",
    "all": ["level:low", "level:medium", "level:high"]
}

class Users:

    def __init__(self):
        self.users_credentials = dict()
        self.load_credentials()

    def authenticate_user(self, user_name, password):
        """
        Authenticates the user login.
        :param user_name: User name
        :param password: User password
        :return: The token, if authorized.
        """
        user = self.users_credentials.get(user_name)
        if user:
            if user.get("pwd") == password:
                return self.encode_auth_token(user_name)

        return None


    def get_user_level(self, user_name):
        """
        Gets the user level as URI syntax.
        :param user_name: User name
        :return: User's level.
        """
        user = self.users_credentials.get(user_name)

        if user:
            return user_levels.get(user.get("level"))

        return None

    def load_credentials(self):
        """
        Loads the local text file of users' credentials
        """
        with open('credentials.txt') as file:
            data = file.readlines()

        self.users_credentials = json.loads(''.join(list(map(lambda x: x.replace('\n', ''), data))).strip())

    
    def encode_auth_token(self, user_name):
        """
        Generates the authentication token for a user at login stage.
        :param user_level: User's permission level
        :param user_name: User's unique name
        :return: Token with the user ID, permission level and expiration date.
        """
        try:
            is_testing = current_app.config.get("DEBUG") or current_app.config.get("TESTING")

            payload = {
                'iat': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=(token_active_time["t_days"] if is_testing else token_active_time["days"]),
                    hours=(token_active_time["t_hours"] if is_testing else token_active_time["hours"]),
                    seconds=(token_active_time["t_seconds"] if is_testing else token_active_time["seconds"])
                ),
                # 'aud': user_level,
                'user_name': user_name
            }

            return jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm='HS256')
        except Exception as e:
            return e

