from flask import Flask, render_template, request
import feedparser

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/rss", methods=['GET', 'POST'])
def rss():
    rss_url = request.form['rss_url']
    feed = feedparser.parse(rss_url)
    print(feed)
    return render_template('rss.html', feed=feed)

if __name__ == '__main__':
    app.run(debug=True)