from sqlalchemy import Enum
from app.sqla import sqla
from app.assess.enums import Item_Type, Language_Type

class Item(sqla.Model):
    
    id = sqla.Column(sqla.Integer, primary_key=True)
    type = sqla.Column(Enum(Item_Type))
    question = sqla.Column(sqla.String(128))
    answer = sqla.Column(sqla.String(128))
    weight = sqla.Column(sqla.Float)
    language = sqla.Column(Enum(Language_Type), default=Language_Type.EN)
    # image = sqla.Column(sqla.Blob)

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type    
    
    def get_question(self):
        return self.question
    
    def get_answer(self):
        return self.answer
    
    def get_weight(self):
        return self.weight
    
    def get_language(self):
        return self.language
    