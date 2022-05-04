from token import NAME
from flask import Flask, render_template, request
import requests
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class Config():
    SECRET_KEY = os.environ.get("SECRET_KEY")


class PokemonForm(FlaskForm):
    name = StringField('Pokeman Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


app=Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

  
@app.route('/pokemon', methods=['GET','POST'])
def pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit:
        # poke_name = request.form.get('pokemon_name')
        poke_name = form.name.data
        try:
            
            url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
            response = requests.get(url)
            pokemon = response.json()
            
            pokemon_dict={
                "pokemon":pokemon['name'],
                "ability_name":pokemon['abilities'][0]['ability']['name'],
                "base_experience":pokemon['base_experience'],
                "sprite_url":pokemon['sprites']['front_shiny'],
                "attack_base_stat":pokemon['stats'][1]['base_stat'],
                "hp_base_stat":pokemon['stats'][0]['base_stat'],
                "defense_base_stat":pokemon['stats'][2]['base_stat']
            }
            return render_template('pokemon.html.j2', pokemons=pokemon_dict, form=form)
        except:
            error_string = "You had an error"
            return render_template('pokemon.html.j2', error=error_string, form=form)
    return render_template('pokemon.html.j2', form=form)


    