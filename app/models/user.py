from uuid import uuid4
from app.sqla import sqla

class User(sqla.Model):
    
    id = sqla.Column(sqla.Integer, primary_key=True)
    uuid = sqla.Column(sqla.String(64), nullable=False, default=lambda: str(uuid4())) 
    email = sqla.Column(sqla.String(100), unique=True)
    password = sqla.Column(sqla.String(100))
    username = sqla.Column(sqla.String(1000))

    def get_id(self):
        return self.id

    def get_uuid(self):
        return self.uuid    
    
    def get_email(self):
        return self.question
    
    def get_password(self):
        return self.answer
    
    def get_username(self):
        return self.answer