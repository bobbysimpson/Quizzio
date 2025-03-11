from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, email, username, password_hash):
        self.id = user_id  # Flask-Login expects the user identifier to be stored in `id`
        self.email = email
        self.username = username
        self.password_hash = password_hash

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data.get("user_id"),
            email=data.get("email"),
            username=data.get("username"),
            password_hash=data.get("password_hash")
        )