from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<task %r> " % self.id


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "there was an error in adding your task"

    else:
        tasks = Todo.query.order_by(Todo.date_create).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was a problem in deleting the task'


@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'something went wrong with that go back and try again'

    else:
        return render_template('update.html', task =  task )

    # try:
    #     db.session.update(task_to_update)
    #     db.session.commit()
    #     return redirect('/')
    # except:
    #     return 'there is a problem in updating the task . '


# @app.route('/')
# @app.route('/<user>')
# def index(user=None):
#      return  render_template("user.html", user = user)
#
#
# @app.route('/shopping')
# def shopping():
#     food =  ['cheese', 'banana','guava','black berry','orange']
#     return  render_template("shopping.html",food = food)

# @app.route('/tuna')
# def tuna():
#     return "remember the day red "
#
# @app.route('/profile/<username>')
# def  profile(username):
#     return "<h1>the name of the user is : " + username + "</h1>"
#
# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     return "<h1>hey! the post id of the given post </h1> {}" .format(post_id)
#

if __name__ == "__main__":
    app.run(debug=True)
