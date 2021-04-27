from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from my_app import photos, db
from my_app.community.forms import ProfileForm, EditProfileForm
from my_app.models import Profile, User
# , EditProfileForm
community_bp = Blueprint('community_bp', __name__, url_prefix='/community')


@community_bp.route('/')
@login_required
def index():
    return render_template('community.html')


@community_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = Profile.query.join(User).filter(User.id == current_user.id).first()
    if profile:
        return redirect(url_for('community_bp.update_profile'))
    else:
        return redirect(url_for('community_bp.create_profile'))


@community_bp.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()  # This should be familiar from login and signup routes in auth
    if request.method == 'POST' and form.validate_on_submit():
        filename = None  # Set the filename for the photo to None since this is the default if the user hasn't chosen to add a profile photo
        if 'photo' in request.files:  # Let's you check the submitted form contains a photo (photo is the field name we used in the ProfileForm class)
            if request.files['photo'].filename != '':  # As long as the filename isn't empty then save the photo
                filename = photos.save(request.files['photo'])  # This saves the photo using the global variable photos to get the location to save to
        p = Profile(username=form.username.data, photo=filename, bio=form.bio.data,
                    user_id=current_user.id)  # Build a new profile to be added to the database based on the fields in the form
        db.session.add(p)  # Add the new Profile to the database session
        db.session.commit()  # This saves the new Profile to the database
        return redirect(url_for('community_bp.display_profiles', username=p.username))
    return render_template('profile.html', form=form)


@community_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()  # Find the existing profile for this user
    form = ProfileForm(
        obj=profile)  # Pre-populate the form by loading the profile using obj=. This relies on the field names in the Profile class in model matching the field names in the ProfileForm class, otherwise you have to explicitly state each field e.g. if the form used bio and the model used biography you would need to add bio = profile.biography
    if request.method == 'POST' and form.validate_on_submit():
        if 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            profile.photo = filename  # Updates the photo field# Updates the country field
        profile.bio = form.bio.data  # Updates the bio field
        profile.username = form.username.data  # Updates the user field
        db.session.commit()  # Save the changes to the database
        return redirect(url_for('community_bp.display_profiles', username=profile.username))
    return render_template('profile.html', form=form)


@community_bp.route('/display_profiles', methods=['POST', 'GET'])
@community_bp.route('/display_profiles/<username>/', methods=['POST', 'GET'])
@login_required
def display_profiles(username=None):
    results = None
    if username is None:
        if request.method == 'POST':
            term = request.form['search_term']
            if term == "":
                flash("Enter a name to search for")
                return redirect(url_for("community_bp.index"))
            results = Profile.query.filter(Profile.username.contains(term)).all()
    else:
        results = Profile.query.filter_by(username=username).all()
    if not results:
        flash("No users found.")
        return redirect(url_for("community_bp.index"))
    # The following iterates through the results and adds the full url to a list of urls
    urls = []
    for result in results:
        url = photos.url(
            result.photo)  # uses the global photos plus the photo file name to determine the full url path
        urls.append(url)
    return render_template('display_profile.html', profiles=zip(results, urls))  # Note the zip to pass both lists as a parameter


@community_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
