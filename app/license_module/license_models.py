from app.extensions import db

"""
Models for license
"""

class License(db.Model):
    """
    This class represents the license table
    """
    __tablename__ = 'license'

    id = db.Column(db.Integer, primary_key=True)
    certificate = db.Column(db.Text)
    cluster_id = db.Column(db.String(100))
    pods = db.Column(db.Integer)
   
    def __repr__(self):
        return '<id: {}>'.format(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()