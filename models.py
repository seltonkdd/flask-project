from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, password, bio=''):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.bio = bio