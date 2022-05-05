from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import PokemonForm, LoginForm, RegisterForm
from app import app
from .models import User
from flask_login import current_user, logout_user, login_user, login_required

# ROUTES SECTION
@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')


@app.route('/pokemon', methods=['GET','POST'])
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data

        # look up email address that is trying to log in
        u=User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash(f'Welcome to Pokemon World!', 'success')
            return redirect(url_for('index'))
        flash(f'Incorrect Email and Password', 'danger')
        return render_template('login.html.j2', form=form)
    return render_template('login.html.j2', form=form)

@app.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash(f'You have logged out','warning')
        return redirect(url_for('login'))
    


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data
            }
            # Create an empty User
            new_user_object = User()
            # build user with the form data
            new_user_object.from_dict(new_user_data)
            # save user to the database
            new_user_object.save()
        except:
            flash("There was an an unexpected error creating your account. Please try again later.", "danger")
            return render_template('register.html.j2', form=form)

        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html.j2', form=form)    

    