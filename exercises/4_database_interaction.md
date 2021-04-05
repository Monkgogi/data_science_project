# Interacting with the database for signup

In this activity we will improve the signup process by adding a custom validator that queries the database to check if
an email address has already been registered before sign up is completed, and once the signup form passes validation,
save a new user to the database in the user table.

You are likely to need to refer to the following:

- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [SQLAlchemy](https://www.sqlalchemy.org)

The steps we will need to carry out are:

1. Create a model that maps fields in the database to classes in the Flask app (in `my_app/models.py`)
2. Create the database when the app starts (in the `create_app()` function)
3. Add a custom validation to the SignupForm class to check whether an email address is already registered
4. Update the signup route to save the new user data to the database

We will also cover what to do if you already have a database table with data that you want to use instead of creating a
new database.

## Flask-SQLAlechemy v SQLAlchemy

A model in this context is a class, or number of classes, that represent the data used in your application.

Since many applications save that same data to a database, then SQLAlchemy provides functionality that lets us more
easily map a table in a database to a class in an application, where one object of that class represents a row in a
table. It implements a design pattern called ORM, Object Relational Mapper.

Flask-SQLAlchemy adds further functionality to SQLAlchemy to make it easier to work with for Flask applications.

It can be confusing to work out which functions are in Flask-SQLAlchemy and which are SQLAlchemy. The extensions
provided by Flask-SQLAlchemy
are [summmarised here](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#road-to-enlightenment).

## Create a 'model' of your data

Add a model for the signup data:

- firstname (Text, required)
- lastname (Text, required)
- email (Text, required)
- password (hashed rather than plain text)

In the following example we first state the tablename that the class maps to. You don't need to do this if the class
name is the same as the table name as Flask-SQLAlchemy handles it for you unless you override it. The table name is
derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case”. To override the
default table name, set the __tablename__ class attribute.

There is then a definition for each field. We will explore table relationships later in the course.

We will use the models in all of the modules for our app so create `models.py` in the `my_app` directory. Add the
following code:

```python
from my_app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"{self.id} {self.firstname} {self.lastname} {self.email} {self.password}"
```

## Create the database when the app starts

We already created a global SQLAlchemy database object in `__init__.py` which was configured with parameters that we put
in `config.py`.

We then initialised the database object to allow access in Flask in the `create_app` function.

Now we need to create the tables for the database to match the models defined in `models.py`.

To do that we can use a Flask-SQLAlchemy method `create_all()` which we place in `create_app` in a context. We already
create the dashboard with a context so we can add the create_all() after that, we need to also import the tables to
create from models.py:

```python
    with app.app_context():
    from dash_app.dash import init_dashboard

    app = init_dashboard(app)

    from my_app.models import User

    db.create_all()
```

Start your Flask app now and you should see that it creates a database in the data folder called `example.sqlite` which
is the name we gave in `app.config['SQLALCHEMY_DATABASE_URI']`.

If you are using PyCharm you can create a DataSource mapping to view the database contents and access a SQL console.

## Add a custom validation to the SignupForm class to check whether an email address is already registered

Let's return to `auth.forms.py` and add
a [custom validator](https://wtforms.readthedocs.io/en/2.3.x/validators/#custom-validators) that checks whether the
email address exists before it allows use to register a new user account.

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from my_app.models import User


class SignupForm(FlaskForm):
    first_name = StringField(label='First name', validators=[DataRequired(message='First name required')])
    last_name = StringField(label='Last name', validators=[DataRequired(message='Last name required')])
    email = EmailField(label='Email address', validators=[DataRequired(message='Email adddress required')])
    password = PasswordField(label='Password', validators=[DataRequired(message='Password required')])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address')
```

### Add custom validation to the LoginForm class

Use the knowledge you just gained in writing a custom validator for the signup form to implement custom validatios for
the login form:

- email: check if the email account exists, it not tell the user that the email address isn't registered.
- password: check that the password is valid for that email address, if not tell them the password is invalid.

## Update the signup route to save the new user data to the database

First let's add a methods to improve our user class so that our password is not saved as plain text and instead is set
using the werkzeug generate_password_hash and retrieved using the check_password_hash function.

```python
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "user"

    # etc

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
```

Modify `auth/auth.py` so that if the form passes validation then a new user is added to the database by creating a User
object with the form field data:

```python
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(firstname=form.first_name.data, lastname=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Hello, {user.firstname} {user.lastname}. You are signed up.")
        return redirect(url_for('main.index'))
    return render_template('signup.html', title='Sign Up', form=form)
```

However, if there is an error when saving to the database the above method will fail. Instead we will use a try/except:

```python
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        user = User(firstname=form.first_name.data, lastname=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Hello, {user.firstname} {user.lastname}. You are signed up.")
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to register {form.email.data}. ', 'error')
            return redirect(url_for('auth.signup'))
        return redirect(url_for('main.index'))
    return render_template('signup.html', title='Sign Up', form=form)
```

You should now be able to restart the app, signup a user and then try to sign up again with the same email address. You
can check the database to see if your details have been saved.

## Working with existing databases

You can use the above method to work with an existing database so long as you match the tablenames and fields in the
database to the table names and the fields in your models.py classes (take care to match upper/lower case).

However, you can save yourself from defining the columns in the classes by using a technique referred to as reflection
in the SQLAlchemy documentation.

The process for working with the database is slightly different.

In `create_app` you need to remove `db.create_all()` from `__init__.py` and replace it with:

```python
    with app.app_context():
        db.Model.metadata.reflect(bind=db.engine)
```

In `models.py` you can use this syntax instead:

```python
from my_app import db


class User(db.Model):
    __table__ = db.Model.metadata.tables['user']
```

There is another technique you could use that is explained in this video, [Interacting with an existing SQLite database using reflection and automap](https://www.youtube.com/watch?v=UK57IHzSh8I)