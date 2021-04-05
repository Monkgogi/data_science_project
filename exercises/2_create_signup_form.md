# Create a signup form

So far we have worked with views (remember MVC?) and controllers to render those views.

For this activity we will ultimately need to save the signup data which we will do in an SQLite database. The structure of this data is referred to as the 'model', indeed in many Flask apps it is often in a file called `models.py`.
However, for this activity we will focus on creating the form. We will look at database integration in a later activity.
 
The steps we will follow for this activity are:

1. Create a new python module called 'auth' and define the Blueprint
2. In `my_app/auth` create `forms.py` with a python class for the form  (Model (partial))
3. In `my_app/templates` create a Jinja2 template called `signup.html`  (View) 
4. Add a route for signup to `my_app/auth/routes.py`  (Controller)


## Create the auth package and define the Blueprint
If you don't remember how to do this, look back to the week 6 exercises.

## Create the signup form using Flask-WTF
You may need to refer to the [Flask-WTF documentation](https://flask-wtf.readthedocs.io/en/stable/) for this exercise.

To create a form we will create a Form class that inherits the Flask-WTF FlaskForm class.

The class will contain fields that represent the data we want to use for signup. The type of the field will be one of the [wtforms field types](https://wtforms.readthedocs.io/en/2.3.x/fields/) such as StringField, SelectField, EmailField etc. You can also create your own custom field if you need to for your coursework.

Each of the fields should be validated using the [wtforms validators](https://wtforms.readthedocs.io/en/2.3.x/validators/). We will use wtforms validators and in a later exercise we will also provide our own custom validators.

Create a new python file called `forms.py` in the `auth` package and add the following imports:

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo
```

Create the signup form class which inherits the FlaskForm class:

```python
class SignupForm(FlaskForm):
```
 
Add the following fields to the class:

- First name (must be provided)
- Last name (must be provided)
- Email address (must be provided, must meet HTML5 email format rules)
- Password (must be provided)
- Repeat password (must match 'Password')

You can find the full set of parameter that can be passed to a Field depending on its type in the [documentation]( [wtforms field types](https://wtforms.readthedocs.io/en/2.3.x/fields/)).

For our purposes providing a label that will be used to create the HTML form element and the list of validators will be enough.

```python
    first_name = StringField(label='First name', validators=[DataRequired()])
    last_name = StringField(label='Last name', validators=[DataRequired()])
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
```

We will later add a custom validator to check that the email address is not already registered, however we need to interact with the database to do this.

## Create the signup template

We need to create an HTML/Jinja2 template that represents each field in the form.

HTML forms use the `<form></form>` tag. A form tag accepts parameters that specify what should happen when the form is submitted. In our case we want to go to a new route called 'signup' which we can refer to use the url_for() syntax.

In addition, as we are using CSRF protection we need to provide a hidden field in the form.

A [basic form layout is shown in the documentation](https://flask-wtf.readthedocs.io/en/stable/quickstart.html#creating-forms).

The form might look something like this:

```jinja2
{% extends 'layout.html' %}
{% block content %}
    <form method="POST" action="{{ url_for('auth.signup') }}">
        {{ form.csrf_token }}
        {{ form.first_name.label }} {{ form.first_name() }} <br>
        {{ form.last_name.label }} {{ form.last_name() }} <br>
        {{ form.email.label }} {{ form.email() }} <br>
        {{ form.password.label }} {{ form.password() }} <br>
        {{ form.password_repeat.label }} {{ form.password_repeat() }} <br>
        <input type="submit" value="Sign up">
    </form>
{% endblock %}
```

If you want to add Bootstrap styling to the form checkout their [documentation](https://getbootstrap.com/docs/4.1/components/forms/). You can pass attributes to the fields such as class names and ids, for example:

```python
{{ form.first_name.label }} {{ form.first_name(class="form-field") }}
```

If you are using Flask-Bootstrap then they provide a helper function that automatically generates the fields for the form and adds bootstrap styling with minimal code:
```jinja2
{% import "bootstrap/wtf.html" as wtf %}
{{ wtf.quick_form(form) }}
```

If you don't use Flask-Bootstrap then you can write a Jinja2 template macro to generate forms and add styling. Read the [documentation here](https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/#forms-in-templates) which contains the necessary code.

## Add a route for signup
You need to add a route for sign up in auth.py.

To date we have not needed to specify the HTTP methods for our routes as we have just been generating static pages using the default 'GET'.
For the signup however we want to generate the blank form when the page is requested, and when the user presses the 'sign up' button then we instead treat it as a POST method.
We know the method is POST as this is what we specified in the HTML form tag:
```html 
<form method="POST" action="{{ url_for('auth.signup') }}">
```

The controller action first creates the form `form = SignupForm()` from the class in `forms.py`.

The form class has a method `validate_on_submit()` that checks if the validation rules were met.
If the form passes validation then let's take the `name` value from the form and use it to display a message back to the person.

If the form failed validation then display the form again.

The route returns the view using the `signup.html` template.

```python
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.first_name.data
        return f"Hello, {name}. You are signed up."
    return render_template('signup.html', title='Sign Up', form=form)
```

Stop and restart the Flask app and go to http://127.0.0.1:5000/signup/

Try out what happens when you do and don't meet the validation for each form.

## Create a login form
Use the knowledge gained from the steps above to create a login form with the following fields:
 
- email address
- password
- remember me checkbox

Stop and restart the Flask app and go to http://127.0.0.1:5000/login/

## Extend your knowledge
Using the online documentation try and add the following fields to the sign up, they progress in difficulty so try one at a time and check it works before moving to the next.

- a username field to sign up with validation that the length has to be between 8 and 12
- a title field that is a selection field type with the values Mr, Ms, Dr
- a photo field that allows the user to submit a thumbnail image of themselves (hint: try [Flask-WTF uploads](https://flask-wtf.readthedocs.io/en/stable/form.html#module-flask_wtf.file) or [Flask-Uploads](https://flask-uploads.readthedocs.io/en/latest/)).

