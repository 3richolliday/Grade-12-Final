from app.sqla import sqla

class User_Assessment(sqla.Model):

    __tablename__ = "user_assessment"
    
    id = sqla.Column(sqla.Integer, primary_key=True)
    user_id = sqla.Column(sqla.Integer)
    total_score_possible = sqla.Column(sqla.Integer)
    date_completed = sqla.Column(sqla.String)
    total_score = sqla.Column(sqla.Float)
    

    def get_id(self):
        return self.id
    
    def get_user_id(self):
        return self.user_id

    def get_total_score_possible(self):
        return self.total_score_possible    
    
    def get_date_completed(self):
        return self.date_completed
    
    def get_total_score(self):
        return self.total_score
    

    