from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# FORM SECTION
class PokemonForm(FlaskForm):
    name = StringField('Pokeman Name', validators=[DataRequired()])
    submit = SubmitField('Submit')