from app.sqla import sqla
from app.models.item import Item
from app.models.user_assessment import User_Assessment
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User_Assessment_Detail(sqla.Model):

    __tablename__ = "user_assessment_detail"
    
    id = sqla.Column(sqla.Integer, primary_key=True)
    user_assessment_id = sqla.Column(sqla.Integer, ForeignKey(User_Assessment.id))
    item_id = sqla.Column(sqla.Integer, ForeignKey(Item.id))
    score = sqla.Column(sqla.Integer)

    # Foreign Keys
    user_assessment = relationship("User_Assessment")
    item = relationship("Item")

    def get_id(self):
        return self.id

    def get_user_assessment_id(self):
        return self.user_assessment_id    

    def get_item_id(self):
        return self.item_id    
    
    def get_score(self):
        return self.score
