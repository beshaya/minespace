from datetime import datetime
import json

import pyrebase

firebase = None
db = None
user = None

def init_app(app):
    global firebase, db, user

    firebase = pyrebase.initialize_app(app.config['FIREBASE_CONFIG'])
    db = firebase.database()
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password("minecraft@fullerstack.me", "icanhazachievement")

def init_standalone(config):
    global firebase, db, user

    firebase = pyrebase.initialize_app(config.FIREBASE_CONFIG)
    db = firebase.database()
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password("minecraft@fullerstack.me", "icanhazachievement")    
    
class Model:
    __tablename__ = '/'
       
    @classmethod
    def GetAll(cls):
        global db, user
        response = db.child(cls.__tablename__).get(user['idToken'])
        return [cls.FromDict(x.item[1]) for x in response.pyres]

    @classmethod
    def FromDict(cls, dct):
        instance = cls.__new__(cls)
        for key in dct:
            setattr(instance, key, dct[key])

        return instance
            
    def ToJson(self):
        dct = self.__dict__
        #return json.dumps(dct)
        return dct

# Write item to firebase
def Push(item):
    global db, user
    db.child(item.__tablename__).push(item.ToJson(), user['idToken'])
    
class Achievement(Model):
    __tablename__ = '/achievements'
    def __init__(self, player, achievement, date=None):
        self.player = player
        self.achievement = achievement
        if date is None:
            date = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
        self.date = date

    def __repr__(self):
        return "<Achievement player=%s name=%s date=%s>" % (self.player, self.achievement,
                                                            self.date)
    
class Post(Model):
    __tablename__ = '/posts'
    def __init__(self, player, content, imageUrl="", date=None):
        self.author = author
        self.authorId = authorId
        self.content = content
        if date is None:
            date = datetime.utcnow()
        self.date = date

    def __repr__(self):
        return "<Post player=%s content=%s>" % (self.user, self.achievement, self.date)

if __name__ == "__main__":
    ach = Achievement("nineof36", "starting a fire")
    #Push(ach)
    print(Achievement.GetAll())
