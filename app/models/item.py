from app.sqla import sqla

class Item(sqla.Model):
    
    id = sqla.Column(sqla.Integer, primary_key=True)
    type = sqla.Column(sqla.String(128)) 
    text = sqla.Column(sqla.String(128))
    answer = sqla.Column(sqla.String(128))
    weight = sqla.Column(sqla.Float)

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type    
    
    def get_text(self):
        return self.text
    
    def get_answer(self):
        return self.answer
    
    def get_weight(self):
        return self.weight
    