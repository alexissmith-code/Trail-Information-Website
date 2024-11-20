from flask import *
from flask_login import *
from flask_sqlalchemy import *

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

app.app_context().push()

class Trails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trail_name = db.Column(db.String(40), nullable=False)
    miles = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            new_user = User(name=name, username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect('/')
        else:
            error_message = "Username not available. Please choose a different username."
            return render_template('create.html', error_message=error_message)
    return render_template('create.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and password == user.password:
            login_user(user)
            return redirect('/')
        else:
            error_message = "Incorrect username or password"
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')

@app.route('/new', methods=['GET','POST'])
@login_required
def new():
    if request.method == 'POST':
        trail_name = request.form['trail_name']
        miles = request.form['miles']
        difficulty = request.form['difficulty']
        existing_trail = Trails.query.filter_by(trail_name=trail_name).first()
        if existing_trail:
            error_message = f"Trail with the name '" + trail_name +"' already exists. Please choose a different name."
            return render_template('new.html', error_message=error_message)
        new_trail = Trails(trail_name=trail_name, miles=miles, difficulty=difficulty)
        db.session.add(new_trail)
        db.session.commit()
        return redirect('/view')
    return render_template('new.html')

@app.route('/view')
@login_required
def viewAll():
    usersearch = User.query.all()
    trailsearch = Trails.query.all()
    return render_template('view.html', usersearch=usersearch, trailsearch=trailsearch)


@app.route('/update', methods=['GET','POST'])
@login_required
def update():
    if request.method == 'POST':
        current_trail_name = request.form['trail_name']
        new_trail_name = request.form['newTrail_name']
        new_miles = request.form['newmiles']
        new_difficulty = request.form['newdifficulty']
        current_trail = Trails.query.filter_by(trail_name=current_trail_name).first()
        if current_trail:
            current_trail.trail_name = new_trail_name
            current_trail.miles = new_miles
            current_trail.difficulty = new_difficulty
            db.session.commit()

            return redirect('/view')
        else:
            error_message = "Trail not found. Please enter a valid trail name."
            return render_template('update.html', error_message=error_message)
    return render_template('update.html')

@app.route('/delete/trail/<int:id>')
@login_required
def delete_trail(id):
    trail = Trails.query.filter_by(id=id).first()
    if trail:
        db.session.delete(trail)
        db.session.commit()
    return redirect('/view')

@app.route('/delete/user/<int:id>')
@login_required
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect('/view')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.errorhandler(404)
def err404(err):
    return render_template('404.html', err=err)

@app.errorhandler(401)
def err401(err):
    return render_template('401.html', err=err)

app.config['SECRET_KEY'] = 'mySecretKey!'
login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(uid):
    user = User.query.get(uid)
    return user

with app.app_context():
    db.create_all()

if __name__== '__main__':
    app.run(debug=True)




