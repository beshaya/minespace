from flask import Flask, render_template
import posts
import config

app = Flask(__name__)
app.config.from_object(config)
posts.init_app(app)

@app.route("/")
def index():
    a = posts.Achievement.query.all()
    a.reverse()
    p = posts.Post.query.all()
    return render_template('index.html', posts=p, achievements=a)

if __name__ == "__main__":
    app.run()
