from flask import redirect, render_template, request, flash, url_for
import requests
from .import bp as main
from ...forms import PokemonForm
from app.models import Pokemon, Pokedex, User


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

            flash(f"Cannot select same pokemon","danger")
        else:
            if len(my_names)  < 5:
                current_user.collect_poke(new_pokemon)
            else:
                flash(f"You already have 5 pokemon","danger")
        pokemons = current_user.pokemon.all()
        pokemon_list=pokemons[:5]
       
        return render_template('pokemon.html.j2', pokemons=pokemon_list, form=form)
        # except:
        #     error_string = "You had an error"
        #     return render_template('pokemon.html.j2', error=error_string, form=form)
    return render_template('pokemon.html.j2', form=form)

@main.route('/pokemon_team', methods=['GET','POST'])
@login_required
def pokemon_team():
    pokemons = current_user.pokemon.all()
    pokemon_list=pokemons[:5]
    return render_template('pokemon_team.html.j2', pokemons=pokemon_list)


@main.route('/pokemon_battle', methods=['GET','POST'])
@login_required
def pokemon_battle():
    
    users=User.query.filter(User.id != current_user.id).all()
    big_list = {}
    for user in users:
        pokemons = user.pokemon.all()
        pokemon_list=pokemons[:5]
        big_list[user.id]=pokemon_list
        

    # all_pokemons=users.pokemon.all()
   


            

       
        # hp_1=pokemon.poke_from_dict.hp_base_stat
        # hp_2=pokemon.poke_from_dict.hp_base_stat
        # atk_1=pokemon.poke_from_dict.attack_base
        # atk_2=pokemon.poke_from_dict.attack_base
        # # hp_a = current user
        # total_hp_a=sum(hp)
        # total_hp_b=sum(hp)
        # total_atk_a=sum(atk)
        # total_atk_b=sum(atk)
        # winner=''
        # while total_hp_a <= 0 or total_hp_b <= 0:
        #     # round
        #     total_hp_a = total_hp_a - total_atk_b
        #     total_hp_b = total_hp_b - total_atk_a

        #     # TODO replace user.* with correct annotation

        #     if total_hp_a <=0:
        #         current_user.loss_count += 1
        #         user.win_count += 1
        #     if total_hp_b <=0:
        #         current_user.win_count += 1
        #         user.loss_count += 1

        
        # return redirect(url_for("main.pokemon_battle"))

    return render_template('pokemon_battle.html.j2', pokemons=big_list, users=users)



@main.route('/pokemon_battle_view/<int:id>', methods=['GET','POST'])
@login_required
def pokemon_battle_view(id):
    # print("this sucks")
    user=User.query.get(id)
    print("poke battle current_user: ",current_user.id)
    print("poke battle user: ", user.id)
    if request.method == 'GET':
        
        curr=Pokedex.query
        print(curr)
        # u=Pokedex.query.filter(User.id)
        # print(u, "hi")

    return render_template('pokemon_battle.html.j2')


        

#         for user in users:
#             users=User.query.filter(User.id == current_user.id).all()    
#             pokemon_hp1 = user.pokemon.first().hp_base_stat
#             print(pokemon_hp1, "I am stressed")
#             pokemon_atk1 = user.pokemon.first().attack_base_stat
#         total_hp_a = sum(pokemon_hp1)
#         total_atk_a = sum(pokemon_atk1)
#         for second_user in users1:
#             users1=User.query.filter(User.id != current_user.id).all() 
#             pokemon_hp2 = second_user.pokemon.hp_base_stat
#             pokemon_atk2 = second_user.pokemon.attack_base_stat
#         total_hp_b = sum(pokemon_hp2)
#         total_atk_b = sum(pokemon_atk2)
#         winner=''
#         while total_hp_a <= 0 or total_hp_b <= 0:
#             # round
#             total_hp_a = total_hp_a - total_atk_b
#             total_hp_b = total_hp_b - total_atk_a

#             # TODO replace user.* with correct annotation

#             if total_hp_a <=0:
#                 current_user.loss_count += 1
#                 user.win_count += 1
#             if total_hp_b <=0:
#                 current_user.win_count += 1
#                 user.loss_count += 1

