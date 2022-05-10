from flask import render_template, request
import requests
from .import bp as main
from ...forms import PokemonForm
from app.models import Pokemon, Pokedex


from flask_login import login_required, current_user



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
        # try:
            
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
        new_pokemon=Pokemon()
        new_pokemon.poki_from_dict(pokemon_dict)
        new_pokemon.save()
        

        new_pokedex=Pokedex()
        new_pokedex.user_id=current_user.id
        new_pokedex.poke_id = new_pokemon.poke_id
        my_pokemon = Pokedex.query.filter_by(user_id = current_user.id).all()

        pokemons=''
        my_names=[]
        pokemon_list=[]
        for entry in my_pokemon:
            p=Pokemon.query.filter_by(poke_id = entry.poke_id).first().pokemon_name
            my_names.append(p)

        if new_pokemon.pokemon_name in my_names:

            print('Cannot select same pokemon')
        else:
            if len(my_names)  < 5:
                current_user.collect_poke(new_pokemon)
            else:
                print('You already have 5 pokemon')
        pokemons = current_user.pokemon.all()
        pokemon_list=pokemons[:5]
        #     print(pokemon_list)
        # else:
        #     pokemons = current_user.pokemon.all()
        #     pokemon_list=pokemons[:5]

        #     print('Already in list')


        
        

        



        return render_template('pokemon.html.j2', pokemons=pokemon_list, form=form)
        # except:
        #     error_string = "You had an error"
        #     return render_template('pokemon.html.j2', error=error_string, form=form)
    return render_template('pokemon.html.j2', form=form)