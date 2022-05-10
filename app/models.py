# from sqlalchemy import Integer
from app import db, login
from flask_login import UserMixin #IS ONLY USED FOR THE USER MODEL!!!!!!!!
from datetime import datetime as dt 
from werkzeug.security import generate_password_hash, check_password_hash





class Pokedex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poke_id = db.Column(db.Integer, db.ForeignKey('pokemon.poke_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    icon = db.Column(db.Integer)
    pokemon = db.relationship('Pokemon',
                    secondary = 'pokedex',
                    backref='users',
                    lazy='dynamic',
                    ) 

    # should return a unique identifying string
    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'

    # human readable version of rpr
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    # salts and hashes our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    # compares the user password to the password provided in the login form
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email=data['email']
        self.password = self.hash_password(data['password'])
        self.icon = data['icon']

    def get_icon_url(self):
        return f'https://avatars.dicebear.com/api/identicon/{self.icon}.svg'

    # save the user to the database
    def save(self):
        db.session.add(self)  #adds the user to the db session
        db.session.commit() #save everything in the session to the db
    
    def collect_poke(self, poke):
        self.pokemon.append(poke)
        db.session.commit()

    def remove_poke(self, poke):
        self.pokemen.remove(poke)
        db.session.commit()

    #check if user already collected pokemons 
    



    #if has not been collected by any user than add pokemon to the database

    #allow user to add up to 5 pokemon if less than this

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    # SELECT  * FROM user WHERE id = ???


class Pokemon(db.Model):
    poke_id = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String)
    ability_name = db.Column(db.String)
    base_experience = db.Column(db.Integer)
    sprite_url = db.Column(db.String)
    attack_base_stat = db.Column(db.Integer)
    hp_base_stat = db.Column(db.Integer)
    defense_base_stat = db.Column(db.Integer)
   

    # should return a unique identifying string; should have this when making a string
    def __repr__(self):
        return f'<Pokemon: {self.poke_id} | {self.pokemon_name}>'

    def poki_from_dict(self, pokemon_data):
        self.pokemon_name = pokemon_data['pokemon']
        self.ability_name = pokemon_data['ability_name']
        self.base_experience=pokemon_data['base_experience']
        self.sprite_url = pokemon_data['sprite_url']
        self.attack_base_stat = pokemon_data['attack_base_stat']
        self.hp_base_stat = pokemon_data['hp_base_stat']
        self.defense_base_stat = pokemon_data['defense_base_stat']
        self.sprite_url = pokemon_data['sprite_url']


    

    def save(self):
        db.session.add(self) #add the pokemon to db session
        db.session.commit() #save everything in the session in db

