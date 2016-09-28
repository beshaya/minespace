from flask import Flask

import posts

app = Flask(__name__)
app.config.from_pyfile('config.py')
posts.init_app(app)

class AchievementPoster:
    def __init__(self):
        pass
    
    def Post(self, player, achievement):
        my_post = posts.Achievement(player, achievement)
        with app.app_context():
            print my_post
            posts.db.session.add(my_post)
            posts.db.session.commit()
    
if __name__ == "__main__":
    #print "Adding test post: bshaya got the achievement: [Posted on minespace]"
    #poster = AchievementPoster()
    #poster.Post("bshaya", "Posted on minespace")
    with app.app_context():
        all_posts = posts.Achievement.query.all()
        print all_posts
