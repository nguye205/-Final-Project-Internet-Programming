from flask import Flask, session, request, Response, render_template, redirect, url_for
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import Regexp, ValidationError, Optional, InputRequired, Email, Length
import re
from flask.json import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from random import seed, randint
import sqlite3
# from sqlalchemy import create_engine
# from flask_session impfort Session
# from sqlalchemy.orm import scoped_session, sessionmaker

seed(1)
class ShopForm(FlaskForm):
    clothes = SubmitField("Clothes")
    accessories = SubmitField("Accessories")

csrf = CSRFProtect()
app = Flask(__name__)
Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate (app, db)
app.config["SECRET_KEY"] = "row the boat"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
csrf.init_app(app)
login_mng = LoginManager(app)
login_mng.login_view = 'login'
likeStatus = "I like this!"
API_KEY='t3SgmMBTAg4cHWzrjZJHAJhzDrGl9CGJ'
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=40)])
    rememberme = BooleanField('Remember me')

class UserAccount(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(40))
    mycart = db.relationship('Shoppingcart', backref='owner', lazy='dynamic')

class Inventory(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    img_path = db.Column(db.String(120), unique=True)
    category = db.Column(db.String(1))
    quantity = db.Column(db.Integer, default = 5)
    price = db.Column(db.Integer)
    cart = db.relationship('Shoppingcart', lazy='dynamic')

class Shoppingcart(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    quantity = db.Column(db.Integer)

class Review(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    rating = db.Column(db.Integer)
    description = db.Column(db.String())

class MostLiked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), db.ForeignKey('user_account.username'), nullable=False)
    itemname = db.Column(db.String(15), db.ForeignKey('inventory.name'), nullable=False)


@app.before_first_request
def inventoryInit():
    #This fucntion will reset the inventory table on first request.
    conn = None
    try:
        conn = sqlite3.connect("database.db")
    except Error as e:
        print(e)
    sql = 'DELETE FROM inventory'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

    newItem = Inventory(name = 'White Dress', img_path = '/static/img/category/category_1.png', category = 'c', price = 149.99)
    db.session.add(newItem)
    newItem = Inventory(name = 'Sport t-shirt', img_path = '/static/img/category/category_2.png', category = 'c', price = 49.99)
    db.session.add(newItem)
    newItem = Inventory(name = 'Red Plaid Dress', img_path = '/static/img/category/category_3.png', category = 'c', price = 99.99)
    db.session.add(newItem)
    newItem = Inventory(name = 'Black Dress', img_path = '/static/img/category/category_4.png', category = 'c', price = 199.99)
    db.session.add(newItem)
    newItem = Inventory(name = 'Gray Sweater', img_path = '/static/img/category/category_5.png', category = 'c', price = 49.99)
    db.session.add(newItem)
    newItem = Inventory(name = 'Camo t-shirt', img_path = '/static/img/category/category_6.png', category = 'c', price = 29.99)
    db.session.add(newItem)

    newItem = Inventory(name = 'Black Tie', img_path = '/static/img/category/category_7.jpg', category = 'a', price = 19.99)
    db.session.add(newItem)
    newItem = Inventory(name = 'Blue Tie', img_path = '/static/img/category/category_8.jpg', category = 'a', price = 19.99)
    db.session.add(newItem)
    newItem = Inventory(name = 'Burgundy Oxford Tie', img_path = '/static/img/category/category_9.jpg', category = 'a', price = 19.99)
    db.session.add(newItem)
    newItem = Inventory(name = 'Leather Belt', img_path = '/static/img/category/category_10.jpg', category = 'a', price = 24.99)
    db.session.add(newItem)
    newItem = Inventory(name = 'Leather Boots', img_path = '/static/img/category/category_11.jpg', category = 'a', price = 199.99)
    db.session.add(newItem)
    newItem = Inventory(name = 'Black Hat', img_path = '/static/img/category/category_12.jpg', category = 'a', price = 9.99)
    db.session.add(newItem)

    db.session.commit()
    db.session.close()
    return 0;

@login_mng.user_loader
def load_user(userId):
    return UserAccount.query.get(int(userId))

@app.route('/')
def index():
    #Get the top 3 selling item from all categories and display it on the front page
    form = ShopForm()
    conn = None
    try:
        conn = sqlite3.connect("database.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory ORDER BY quantity ASC LIMIT 3;")
    best_seller = cur.fetchall() #best_seller has the top 2 best selling item in the same category
    conn.close()
    return render_template("index.html", form=form, best_seller=best_seller, active_user='user' in session)

@app.route('/fashionNews', methods=['GET'])
def fashionNews():
    url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date=20190101&facet=true&facet_fields=day_of_week&facet_filter=true&fq=source%3A(%22The%20New%20York%20Times%22)&page=10&q=fashion&sort=relevance&api-key={API_KEY}'
    r = requests.get(url)
    r_json = r.json()
    for _ in range(1):
        value = randint(0, 10);
    headline = r_json["response"]["docs"][value]["headline"]["main"] #["docs"]["headline"]["main"]
    abstract = r_json["response"]["docs"][value]["abstract"]
    web_url = r_json["response"]["docs"][value]["web_url"]
    image = r_json["response"]["docs"][value]["multimedia"][0]["url"]
    # lead_par = r_json["lead_paragraph"]
    data = (headline,abstract,web_url,image)
    return jsonify(data)
    # return headline, abstract


@app.route('/category/<selection>', methods=['POST','GET'])
def category(selection):
    #display only the selected category
    form = ShopForm()
    conn = None
    try:
        conn = sqlite3.connect("database.db")
    except Error as e:
        print(e)
    cur = conn.cursor()

    if (selection == "Accessories"):
        cur.execute("SELECT * FROM inventory WHERE category ='a';")
    else:
        cur.execute("SELECT * FROM inventory WHERE category ='c';")

    data = cur.fetchall()
    conn.close()

    return render_template("category.html", form=form, category=selection, data = data, active_user='user' in session)

# New user Account
@app.route('/register.html', methods=['POST','GET'])
def register():
    Loginform = LoginForm()
    form = ShopForm()
    if Loginform.validate_on_submit():
        pw_hash = generate_password_hash(Loginform.password.data, method='sha1') # sha1 hashes creates 40 characters
        newUser = UserAccount(username=Loginform.username.data, password=pw_hash)
        db.session.add(newUser)
        try:
            db.session.commit()
        except:
            db.session.close()
            return '<h1 style="color: #111;font-size: 25px; font-weight: bold; letter-spacing: -1px; line-height: 1; text-align: center;" > You already have an account! <br><a href="/">Click this link to get redirected to the home page </a></h1> '
            return render_template("login.html", Loginform = Loginform, form = form, temp = 1)
        db.session.close()
        #return '<h1 style="width: 100%;font-size: 50pt;font-weight: bold;align-content: center;text-align: center;"> Created New User </h1> <a style="width: 100%;font-size: 50pt;font-weight: bold;align-content: center;text-align: center;" href="/">GO TO HOME </a>'
        return '<h1 style="color: #111;font-size: 25px; font-weight: bold; letter-spacing: -1px; line-height: 1; text-align: center;" > User has been created <br><a href="/login.html">Click this link to get redirected to the login page </a></h1> '

    return render_template("register.html", Loginform=Loginform, form = form)

@app.route('/login.html', methods=['POST','GET'])
def login():
    Loginform = LoginForm()
    form = ShopForm()

    if Loginform.validate_on_submit():
        user = UserAccount.query.filter_by(username=Loginform.username.data).first() # only get one result
        if user:        # if user exists, get the Password
            if check_password_hash(user.password, Loginform.password.data):
            # if user.password == form.password.data:
                login_user(user, remember=Loginform.rememberme.data)
                session['id'] = user.id
                session['user'] = user.username
                return redirect(url_for('index'))
        #return '<h1>Username or password does not exist</h1> <a href="/">GO TO HOME </a>'# if user doesn't exist
        return '<h1 style="color: #111;font-size: 25px; font-weight: bold; letter-spacing: -1px; line-height: 1; text-align: center;" > Username or password does not exist! <br><a href="/login.html">Click this link to get redirected to the login page </a></h1> '
    return render_template("login.html", Loginform=Loginform, form = form, active_user='user' in session)

@app.route('/logout.html')
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    session.pop('id', None)
    return redirect(url_for('index'))

@app.route('/contact.html', methods=['POST','GET'])
def contact():
    form = ShopForm()
    return render_template("contact.html", form=form, active_user='user' in session)

@app.route('/single-product.html/<item>', methods=['POST','GET'])
def singleProduct(item):
    #perform a certain action based on the "action" variable
    conn = None
    try:
        conn = sqlite3.connect("database.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory WHERE name = (?);", [item])
    data = cur.fetchall() #data has information about the item
    cur.execute("SELECT * FROM inventory WHERE category = (?) ORDER BY quantity ASC LIMIT 2;", [data[0][3]])
    best_seller = cur.fetchall() #best_seller has the top 2 best selling item in the same category

    cur.execute("select user_account.id, username, review.item_id, review.rating, review.description from user_account inner join review on user_account.id = review.user_id where review.item_id = (?);", [data[0][0]])
    review = cur.fetchall()
    userID = 0
    if ('id' in session):
        userID = session['id']
    print("userID is: ", userID)
    cur.execute("select * from most_liked where username = (?) AND itemname = (?);", [userID, data[0][1]])
    like = cur.fetchall()
    if (len(like)):
        likeStatus = "Loved"
    else:
        likeStatus = "Love"
    conn.close()
    form = ShopForm()
    category = "Clothes"
    if (data[0][3] == 'a'):
        category = "Accessories"
    return render_template("single-product.html", form=form, data=data, category=category, quantity=data[0][4], best_seller=best_seller, active_user='user' in session, review=review, likeStatus=likeStatus)

@app.route('/cart.html', methods=['POST','GET'])
@login_required
def cart():
    form = ShopForm()
    conn = None
    try:
        conn = sqlite3.connect("database.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    userID = 0
    if ('id' in session):
        userID = session['id']
    cur.execute("create table temptable as select item_id, SUM(quantity) as quantity from shoppingcart where user_id = (?) group by item_id;", [userID])
    cur.execute("select inventory.id, name, img_path, price, temptable.quantity, ROUND(temptable.quantity * price, 2) as total from inventory inner join temptable on inventory.id = temptable.item_id group by inventory.id;")
    myShoppingCart = cur.fetchall()
    cur.execute("drop table temptable;")
    conn.close()
    return render_template("cart.html", form=form, active_user='user' in session, myCart=myShoppingCart)

@app.route('/add_to_cart/<item>/<amount>')
def add_to_cart(item, amount):
    print(item)

    active_user = 'user' in session
    if (not active_user): #if user is not logged in, return 0
        return '0';
    userID = 0
    if ('id' in session):
        userID = session['id']

    conn = None
    try:
        conn = sqlite3.connect("database.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute("SELECT id FROM inventory WHERE name = (?);", [item])
    item_id = cur.fetchall()[0][0]
    cur.execute("UPDATE inventory SET quantity = quantity-(?) WHERE name=(?) AND quantity > 0;", [amount,item])
    cur.execute("INSERT INTO shoppingcart (user_id, item_id, quantity) VALUES((?), (?), (?));", [userID, item_id, amount])
    conn.commit()
    conn.close()
    return "1" #this return is here to make the compiler happy

@app.route('/i_love_this/<item>')
def i_love_this(item):
    print("I love this item: " + item)
    active_user = 'user' in session
    if (not active_user): #if user is not logged in, return 0
        return '0';

    userID = 0
    if ('id' in session):
        userID = session['id']

    conn = None
    try:
        conn = sqlite3.connect("database.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute("SELECT name FROM inventory WHERE name = (?);", [item])
    itemname = cur.fetchall()[0][0] #get the name of the item
    cur.execute("INSERT INTO most_liked (itemname,username) VALUES ((?),(?));",[itemname,userID])
    conn.commit()
    conn.close()
    return "1" #this return is here to make the compiler happy

@app.route('/save_my_review/<item>/<rating>/<review>')
def save_my_review(item, rating, review):

    active_user = 'user' in session
    if (not active_user): #if user is not logged in, return 0
        return '0';

    userID = 0
    if ('id' in session):
        userID = session['id']

    conn = None
    try:
        conn = sqlite3.connect("database.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute("SELECT id FROM inventory WHERE name = (?);", [item])
    item_id = cur.fetchall()[0][0] #get the id of the item
    cur.execute("INSERT INTO review (item_id,user_id,rating,description) VALUES ((?),(?),(?),(?));",[item_id,userID,rating,review])
    conn.commit()
    conn.close()
    return "1" #make the compiler happy
