from flask import render_template, request
import requests
from .import bp as main
from ...forms import PokemonForm


from flask_login import login_required



@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')


@main.route('/pokemon', methods=['GET','POST'])
@login_required
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