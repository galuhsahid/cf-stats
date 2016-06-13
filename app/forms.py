from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed

class SubmitForm(Form):
	title = StringField('title', validators=[DataRequired()])
	target = StringField('title', validators=[DataRequired()])
	registration_opens = DateField('DatePicker', format='%Y-%m-%d', validators=[DataRequired()])
	registration_closes = DateField('DatePicker', format='%Y-%m-%d', validators=[DataRequired()])
	myFile = FileField('CSV file containing applicants', validators=[FileRequired(), FileAllowed(['csv'], 'CSV only!')])