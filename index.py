from flask import Flask, render_template
import posts
import config

app = Flask(__name__)
app.config.from_object(config)
posts.init_app(app)

@app.route("/")
def index():
    p = posts.Post.query.all()
    return render_template('index.html', post=p[0])

if __name__ == "__main__":
    app.run()
