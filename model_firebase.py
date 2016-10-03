from datetime import datetime
import json

import pyrebase

firebase = None
db = None
user = None
email = None
pwd = None

def init_app(app):
    global firebase, db, user, email, pwd

    firebase = pyrebase.initialize_app(app.config['FIREBASE_CONFIG'])
    db = firebase.database()
    email = app.config['FIREBASE_EMAIL']
    pwd = app.config['FIREBASE_PWD']
    
def init_standalone(config):
    global firebase, db, user, email, pwd

    firebase = pyrebase.initialize_app(config.FIREBASE_CONFIG)
    db = firebase.database()
    email = config.FIREBASE_EMAIL
    pwd = config.FIREBASE_PWD

#@TODO(bshaya): Figure out when we can use refresh tokens.
def ReauthenticateIfNecessary():
    global firebase, user, email, pwd
    user = firebase.auth().sign_in_with_email_and_password(email, pwd)

# Write item to firebase
def Push(item):
    global db, user
    ReauthenticateIfNecessary()
    db.child(item.__tablename__).push(item.ToJson(), user['idToken'])

class Model:
    __tablename__ = '/'
    __sortby__ = 'date'
    @classmethod
    def GetAll(cls):
        global db, user
        ReauthenticateIfNecessary()
        response = db.child(cls.__tablename__).order_by_child(cls.__sortby__).get(user['idToken'])
        return [cls.FromDict(x.val()) for x in response.each()]

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
   
class Achievement(Model):
    __tablename__ = '/achievements'
    def __init__(self, player, achievement, date=None):
        self.player = player
        self.achievement = achievement
        if date is None:
            date = datetime.utcnow().isoformat()
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
            date = datetime.utcnow().isoformat()
        self.date = date

    def __repr__(self):
        return "<Post player={} content={}>".format(self.user, self.achievement, self.date)

class Player(Model):
    __tablename__ = '/players'
    __sortby__ = 'last_seen'
    def __init__(self, player, is_online, last_seen=None):
        self.player = player
        self.is_online = is_online
        if last_seen is None:
            last_seen = datetime.utcnow().isoformat()

        self.last_seen = last_seen

    def __repr__(self):
        return "<Player name={} online={} last_seen={}>".format(self.player, self.is_online, self.last_seen)

    def Set(self):
        global db, user
        ReauthenticateIfNecessary()
        db.child(self.__tablename__).child(self.player).set(self.ToJson(), user['idToken'])
       
if __name__ == "__main__":
    import config
    init_standalone(config)
    ach = Achievement("nineof36", "starting a fire")
    #Push(ach)
    print(Achievement.GetAll())
