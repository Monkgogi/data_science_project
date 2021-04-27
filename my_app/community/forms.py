from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError, Length

from my_app.models import Profile
from my_app import photos


class ProfileForm(FlaskForm):
    """ Class for the profile form """
    username = StringField(label='Username', validators=[DataRequired(message='Username is required')])
    bio = TextAreaField(label='Bio', description='Write something about yourself')
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])

    def validate_username(self, username):
        profile = Profile.query.filter_by(username=username.data).first()
        if profile is not None:
            raise ValidationError('Username already exists, please choose another username')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    bio = TextAreaField(label='Bio', validators=[Length(min=0, max=140)])
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])
    submit = SubmitField('Submit')
