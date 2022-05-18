from wtforms.validators import InputRequired
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from flask_wtf import FlaskForm

class PitchForm(FlaskForm):
    """
    Class to create a wtf form for creating a pitch
    """
    pitch_title = StringField('Pitch title',validators=[InputRequired()])
    pitch_category = SelectField('Pitch Category', choices = [('Select category','Select category'),('life', 'Life'), ('code', 'Code'),('promotion','Promotion'),('pickup','Pickup Lines')], validators=[InputRequired()])
    pitch_comment = TextAreaField('Pitch')
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    """
    Class to create a wtf form for creating a pitch
    """
    opinion = TextAreaField('Comment')
    submit = SubmitField('Submit')

class CategoryForm(FlaskForm):
    """
    Class to create a wtf form for creating a pitch
    """
    name =  StringField('Category Name', validators=[InputRequired()])
    submit = SubmitField('Create')