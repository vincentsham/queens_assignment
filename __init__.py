from flask import Flask, render_template, request
from stackoverflow import StackOverflowQuestions, MyThread
import random

app = Flask(__name__)
newest = StackOverflowQuestions("Newest")
votes = StackOverflowQuestions("Votes")
newest.crawl_pages()
votes.crawl_pages()
th = MyThread([newest.crawl_pages,votes.crawl_pages])
th.start()


@app.route('/main')
def homepage():
    option = request.args.get('q', default = None, type = str)
    if option == None or option == "newest":
        data = newest
    else:
        data = votes
    l = len(data.questions)
    return render_template("main.html",data = data,l=l,option = option)

if __name__ == "__main__":
    app.run()