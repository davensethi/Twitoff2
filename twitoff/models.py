""" SQLAlchemy models and utlity  funcitons for twittoff"""


from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()

# User table with Columns id and name 
class User(DB.Model):
    """Twitter Users corresponding to Tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return "<User: {}>".format(self.name)


#Tweet table with column id, text, and user_id 
class Tweet(DB.Model):
    """tweet related to a user"""
    id = DB.Column(DB.BigInteger,primary_key=True)
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user =DB.relationship("User", backref=DB.backref("tweets", lazy=True))

def __repr__(self):
    return "<Tweet: {}>".format(self.text)

#example users but remember they don't tweets
def insert_example_users():
    """Example Users"""
    bill = User(id=1, name="BillGates")
    ellon = User(id=2, name='ElonMusk')
    DB.session.add(bill)
    DB.session.add(ellon)
    DB.session.commit()