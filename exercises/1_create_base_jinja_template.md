# Introduction to Jinja2 templates in Flask

You may find the following references useful for this activity:

- [Jinja 2 documentation](https://jinja.palletsprojects.com/en/2.11.x/)
- [Primer on Jinja 2 templating](https://realpython.com/primer-on-jinja-templating/)
- [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)

By the end of this activity you will have:

1. Created a base page layout (`layout.html`) that is common to all the pages of your web app
2. Created a page layout for the homepage (`index.html`) that inherits from the base layout
3. Edited the index route in `my_app/app.py` so that it renders `index.html` using the Flask
   function `render_template()`

Note that we are going to use Bootstrap 5 as the CSS for this example app though you are free to use any CSS. If you
choose to use Bootstrap you may also want to investigate using Flask-Bootstrap (which is not used in this example).

After each step you should restart the Flask app to see the effect of your changes.

## 1. Create a base page layout

This layout will provide all the common elements of your web pages such as:

- the overall html structure
- links to css (and javascript) files
- defined sections that will have page specific content

### 1.1 Create the overall HTML page structure

Get started by creating a new HTML5 file in the `my_app/templates` folder. This is typically called `base.html`
or `layout.html` though neither is mandatory.

If you do this in PyCharm by creating a new HTML file you will automatically have the following code created for you:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

</body>
</html>
```

### 1.2 Add the css stylesheet reference

Now add your css stylesheet(s) references. In the example we are going to use Bootstrap which has been downloaded to
the `static` folder. You may wish go use a CDN hosted version. Follow the instructions for your preferred method in
the [Bootstrap getting started documentation](https://getbootstrap.com/docs/5.0/getting-started/introduction/).

You do not want to use a specific path on your machine since this is unlikely to be the same for others working on the
same code as they will have their own locations they save projects to on their machines, as well as different operating
systems use different path notations. We know the css will always be in a `static` folder, even if the static folder
changes location, so it is useful to be able to specify the file relative to this.

Let's use a Jinja2 variable `{{ var }}` and within that use Python code that will generate the link to the CSS using a
Flask method called [`url_for()`](https://flask.palletsprojects.com/en/1.1.x/api/?highlight=url_for#flask.url_for)

Here is how you can use these within the HTML code:

```jinja2
<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/bootstrap.css') }}">
```

When the Flask app runs this would be converted to:

```jinja2
<link rel="stylesheet" type="text/css" href="static/css/bootstrap.css">
```

You can use this same structure to add any files in the `static` folder such as images or JavaScript.

### 1.3 Add the Bootstrap javascript

Refer to
the [Bootstrap starter template](https://getbootstrap.com/docs/5.0/getting-started/introduction/#starter-template) which
provides the links to use for the JavaScript. Some Bootstrap navbar functionality uses JavaScript so you will need to
provide these.

Javascript files are placed in the <script> tag and are typically placed at the end of the body section of a page. This
is to ensure that the page does not wait for the JavaScript to be available before it starts to render.

```html

<script src="{{ url_for('static', filename='js/bootstrap.bundle.js') }}"></script>
```

### 1.4 Add Jinja2 variables

Add the following Jinja2 variables to your code to provide variables for the page title and the main content block and
also to

```jinja2
{# Add to the head section #}
<title>{{title}}</title>

{# Add to the body section #}
<header>
{% include 'navigation.html' %}
</header>
<main>
<div class="container">
{% block content %}{% endblock %}
</div>
</main>
```

**NOTE** You will also need to create an empty html file in templates called `navigation.html` otherwise you will get an
error. We will add code to this file later in the activity.

## 2. Create an `index.html` that inherits from the base page

`index.html` inherits from `base.html` so all we need to provide is the content. We will pass in the variable for title
in the route.

```jinja2
{% extends 'layout.html' %}
{% block content %}
    <h1>{{ title }}</h1>
    <p>This is the my_app home page.</p>
{% endblock %}
```

## 3. Edited the index route in `my_app/app.py` so that it renders `index.html` using the Flask function `render_template()`

The my_app home page is currently defined in `my_app/main/routes.py`, replace the `return` statement
with `return render_template()`. You can pass the value for any variables when you render the template, in the case of
this app we want to page the page title.

```python
from flask import render_template


@app.route('/')
def index():
    return render_template('my_app/templates/index.html', title="Home page")
```

Now restart your Flask app.

**NOTE** You may need to comment out the login_manager in create_app() as we have not fully configured login yet and it
causes the Flask app to fail to load. If you are using the week7 starter repository then this has been done already.

## 4. Add a navigation bar

Use Bootstrap styling to create a navigation bar. For now it will include links to:

- my_app index
- community index
- Dash dashboard

Choose any of the [bootstrap navbar code](https://getbootstrap.com/docs/5.0/components/navbar/) and adapt it. Add it at
the start of the <body> section.

You could add the code to the base template, or you can create a template for the navbar.

Let's create a new html file in the templates folder called `navbar.html`. This will contain just enough code to create
the navbar bar, you don't need the entire HTML page structure.

Yours may look different to this depending on the same code you chose to copy, however here is a Bootstrap navbar with 3
links:

```jinja2
{# example navigation.html #}
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Navbar</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Community</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Dash app</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

As we copied the code from the Bootstrap site the `href="#"` needs to be changed to provide the correct URL for our
pages.

As with the CSS we will use a Jinja2 variable and the Flask `url_for()` as follows:

```jinja2
{# home page using main_bp blueprint #}
<a class="nav-link" href="{{ url_for("main_bp.index") }}">Home</a>

{# community blueprint home page #}
<a class="nav-link" href="{{ url_for("community_bp.index") }}">Community</a>

{# Dash app home page - this isn't a Flask route so we will have to specify the path #}
<a class="nav-link" href="/dash_app/">Dashboard</a>
```

## 5. Try it yourself

### Apply the base layout to the community module index page

Repeat the steps for `index` for the community index.

### Apply the same nav to the Dash app

You do not need to do this, if you find a working solution, well done!
