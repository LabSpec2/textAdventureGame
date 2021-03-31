from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

inv = ['broken umbrella','copper spoon','ashen-wood stake','garlick','torn pillow','broken rake','revolver with silver bullets','porcelain plate','apple','lighter','small stick']
_name='Harry Dresden'
_hp=30
_stats=[5,4,5,3,3]
@app.route("/story/")
def story():
    return render_template("story_template.html", inventory = inv,name = _name,hp=_hp,stat=_stats)
    
@app.route("/<_name>")
def user(_name):
    return render_template("story_template.html", name = _name)
	
@app.route("/hero/")
def hero():
    return render_template("hero.html", points = 25)
    
    
if __name__ == "__main__":
    app.run(debug=True)
'''

#broken umbrella,ashen-wood stake,torn pillow,apple,garlick,lighter,broken rake,porcelain plate,copper spoon,revolver with silver bullets,small stick<br>

from flask import Flask, redirect, url_for, render_template, request
import random

class Stats:
    def __init__(self):
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.wisdom = 0
        self.charisma = 0
    
    def add(self, add_strength=0, add_dexterity=0, add_constitution=0, add_wisdom=0, add_charisma=0):
        self.strength += add_strength
        self.dexterity += add_dexterity
        self.constitution += add_constitution
        self.wisdom += add_wisdom
        self.charisma = add_charisma

class Hero:
    hero_id_counter = 0
    def __init__(self,  name = "User"):
        self.hero_id = Hero.hero_id_counter
        Hero.hero_id_counter = Hero.hero_id_counter + 1
        self.name = name
        self.stats = Stats()
        self.HP = random.randint(20, 35)

def upgrade(self, stat_name, points):
    if stat_name == "strength":
        self.stats.add(add_strength=points)
    elif stat_name == "dexterity":
        self.stats.add(add_dexterity=points)
    elif stat_name == "constitution":
        self.stats.add(add_constitution=points)
    elif stat_name == "wisdom":
        self.stats.add(add_wisdom=points)
    else:
        self.stats.add(add_charisma=points)

app = Flask(__name__)
temp_hero = Hero(name = "Wedrownik")
upgrade(temp_hero, stat_name="strength", points=int(5))

@app.route("/")
def home():
    return render_template("index.html", hero=temp_hero)

@app.route("/story/")
def story():
    return render_template("story_template.html", hero=temp_hero)
    
@app.route("/story/add/<ile>")
def ile(ile):
    upgrade(temp_hero, stat_name="strength", points=int(ile))
    return render_template("story_template.html", hero=temp_hero)

#////////////////////////////////////////////////
@app.route('/form')
def form():
    return render_template('form.html', hero=temp_hero)

@app.route('/', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"Try going to '/form' to submit form"
    if request.method == 'POST':
        temp_hero.name = list(request.form.values())[0]
        return render_template("index.html", hero=temp_hero)
        #return render_template('data.html', form_data=form_data)

#//////////////////////////////////////////////////
if __name__ == "__main__":
    app.run(debug=True)
    '''