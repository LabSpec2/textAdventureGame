from flask import Flask, redirect, url_for, render_template, request, jsonify
import random
import enum
import copy
from random import randrange
from collections import defaultdict

app = Flask(__name__)


def makeDict(dict_):
    to_return = defaultdict(int)
    for key, value in dict_.items():
        to_return[key] = value
    return to_return

class Stats:
    def __init__(self): 
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.wisdom = 0
        self.charisma = 0
        
    def add(self, dict_, max_=10):
        self.strength =  min(max_, self.strength + dict_["strength"])
        self.dexterity = min(max_, self.dexterity + dict_["dexterity"])
        self.constitution = min(max_, self.constitution + dict_["constitution"])
        self.wisdom = min(max_, self.wisdom + dict_["wisdom"])
        self.charisma = min(max_, self.charisma + dict_["charisma"])
           
    def getByName(self, name):
        if name == "strength":
            return self.strength
        if name == "dexterity":
            return self.dexterity
        if name == "constitution":
            return self.constitution
        if name == "wisdom":
            return self.wisdom
        if name == "charisma":
            return self.charisma     
        raise Exception('Unsupported stat: {}'.format(name))
         
        
class MonsterType(enum.Enum):
	Vampire = 15
	Ghost = 12
	Ghoul = 8
	Zombie = 6
	Skeleton = 1
    

monster_names = {MonsterType.Vampire:"Vampire", MonsterType.Ghost:"Ghost", MonsterType.Ghoul:"Ghoul",\
              MonsterType.Zombie:"Zombie", MonsterType.Skeleton:"Skeleton"}


monster_hp = {MonsterType.Vampire:30, MonsterType.Ghost:18, MonsterType.Ghoul:12,\
              MonsterType.Zombie:9, MonsterType.Skeleton:3}  

monster_modifier = {MonsterType.Vampire:"dexterity", MonsterType.Ghost:"wisdom",\
                    MonsterType.Ghoul:"constitution", MonsterType.Zombie:"constitution",\
                    MonsterType.Skeleton:"dexterity"}

hero_modifier = {MonsterType.Vampire:"charisma", MonsterType.Ghost:"wisdom",\
                    MonsterType.Ghoul:"strength", MonsterType.Zombie:"dexterity",\
                    MonsterType.Skeleton:"strength"}

# Powinno być jeszcze 'book'
item_stats = {"wooden bat":{"dexterity":5,"constitution":4,"charisma":3},\
              "thin stick":{"dexterity":2,"constitution":3,"charisma":4},\
              "garlic":{"dexterity":0,"constitution":0,"charisma":7},\
              "salt":{"dexterity":0,"constitution":0,"charisma":0},\
              "aspen-wood stake":{"dexterity":0,"constitution":1,"charisma":9},\
              "silver fork":{"dexterity":4,"constitution":2,"charisma":5},\
              "apple":{"dexterity":0,"constitution":1,"charisma":0},\
              "empty can":{"dexterity":1,"constitution":2,"charisma":0},\
              "broken umbrella":{"dexterity":1,"constitution":2,"charisma":0},\
              "plant pot":{"dexterity":1,"constitution":1,"charisma":1},\
              "small painting":{"dexterity":2,"constitution":3,"charisma":1},\
              "old shoe":{"dexterity":2,"constitution":1,"charisma":0},\
              "pillow":{"dexterity":0,"constitution":5,"charisma":0}}


item_text = {"wooden bat":"You grab the wooden bat and take a swing at the monster.\n",\
              "thin stick":"The stick seems rather feeble, but you hold it tight and aim for the creature's face.\n",\
              "garlic":"You clench the garlick in your fist and attempt to shove it in the monster's mouth.\n",\
              "salt":"Desperatly, you grab the pich of salt and throw it at the monster.\n",\
              "aspen-wood stake":"You take the wooden stake and aim straigth for the monsters heart.\n",\
              "silver fork":"The fork is tiny, but the silver will surly hurt the creature\n",\
              "apple":"You grab the... apple? Well, that might end up poorly. Desperatly, you throw it at the monster\n",\
              "empty can":"You grab the empty can and try to aim its sharp edge towards the monster.\n",\
              "broken umbrella":"You grab the umbrella and point its spiky end at the creature.\n",\
              "plant pot":"The plant pot might be a decent ranged weapon, but your not sure how it will do in meele. You grab it regardless\n",\
              "small painting":"Luckily, this painting was made on a wooden board. You wack the creature right in the face.\n",\
              "old shoe":"You grab the old shoe like a mace. It might be good, it has iron nails in the sole\n",\
              "pillow":"It might not be what you would wish you had, but in desperate times... The geese-featered pillow is pretty heavy!\n"}


class Monster:
    def __init__(self, type):
        self.type = type
        self.name = monster_names[type]
        self.HP = monster_hp[type]
        self.dead = False

    def getAttack(self, hero_attacking):
        return 10 + randrange(self.type.value) - hero_attacking.stats.getByName(monster_modifier[self.type])

monster_ = Monster(MonsterType.Ghoul)
        
class Hero:
    id_counter = 0
    def __init__(self,  name = "User",  attack_range=5):
        self.id= Hero.id_counter
        Hero.id_counter = Hero.id_counter + 1
        self.name = name
        self.stats = Stats()
        self.HP = 0
        self.stat_points = 0
        self.attack_range = attack_range
        self.items = [] 
    
        self.collected_items = ""
        self.dead = False

    def upgrade(self, skill_dict):
        self.stats.add(skill_dict)
    
    def addItem(self, item):
        new_thing="\n"+str(item)
        if item not in self.items:
            self.collected_items += new_thing
            self.items.append(str(item))
        #dict_ = makeDict(item_stats[item])
        #self.stats.add(dict_)
        
    def getAttack(self, monster_attacking):
        return 10 + randrange(self.attack_range) + self.stats.getByName(hero_modifier[monster_attacking.type])

@app.route("/")
def home():
    return render_template("index.html")

num_of_monsters = 5
hero_ = Hero()

def check_minus(val):
    return val > 0

def check_plus(val_HP, val_stats):
    return (val_HP > 0 and val_stats < 10)

@app.route("/story/", methods=['POST', 'GET'])
def story():
    if request.method == 'GET':
        return f"Try going to '/hero' to submit form"
    if request.method == 'POST':
        hero_.name = list(request.form.values())[0]
        if request.form['name'] == "Let's go!" and hero_.HP != 0:
            return render_template("enter.html", inventory = item_stats, hero=hero_)
        if request.form['name'] == "Roll the dice!":
            hero_.stats = Stats()
            
            hero_.stat_points = random.randint(20, 35)
            hero_.HP = random.randint(80, 100)
            hero_.collected_items = ""
            hero_.items = []

        if request.form['name'] == "str_plus" and check_plus(hero_.stat_points, hero_.stats.strength):
            hero_.stat_points -= 1
            hero_.upgrade(makeDict({"strength": 1}))
        if request.form['name'] == "str_minus" and check_minus(hero_.stats.strength):
            hero_.stat_points += 1
            hero_.upgrade(makeDict({"strength": -1}))

        if request.form['name'] == "dex_plus" and check_plus(hero_.stat_points, hero_.stats.dexterity):
            hero_.stat_points -= 1
            hero_.upgrade(makeDict({"dexterity": 1}))
        if request.form['name'] == "dex_minus" and check_minus(hero_.stats.dexterity):
            hero_.stat_points += 1
            hero_.upgrade(makeDict({"dexterity": -1}))

        if request.form['name'] == "con_plus" and check_plus(hero_.stat_points, hero_.stats.constitution):
            hero_.stat_points -= 1
            hero_.upgrade(makeDict({"constitution": 1}))
        if request.form['name'] == "con_minus" and check_minus(hero_.stats.constitution):
            hero_.stat_points += 1
            hero_.upgrade(makeDict({"constitution": -1}))

        if request.form['name'] == "wis_plus" and check_plus(hero_.stat_points, hero_.stats.wisdom):
            hero_.stat_points -= 1
            hero_.upgrade(makeDict({"wisdom": 1}))
        if request.form['name'] == "wis_minus" and check_minus(hero_.stats.wisdom):
            hero_.stat_points += 1
            hero_.upgrade(makeDict({"wisdom": -1}))

        if request.form['name'] == "cha_plus" and check_plus(hero_.stat_points, hero_.stats.charisma):
            hero_.stat_points -= 1
            hero_.upgrade(makeDict({"charisma": 1}))
        if request.form['name'] == "cha_minus" and check_minus(hero_.stats.charisma):
            hero_.stat_points += 1
            hero_.upgrade(makeDict({"charisma": -1}))
        return render_template("hero.html", hero=hero_)

def you_win():
    render_template("you_won.html", hero=hero_)

@app.route("/pick_item", methods=["POST"])
def pick_item():
    item = str(request.form)
    item = item[item.find("(") + 4: item.find(",") - 1]
    hero_.addItem(item)
    return str(hero_.collected_items)

monster_type = MonsterType.Vampire

@app.route("/pick_weapon", methods=["POST"])
def pick_weapon():
    item = str(request.form)
    item = item[item.find("(") + 4: item.find(",") - 1]
    print(item)
    text = monster_attack(monster_type, item)
    return text

def monster_attack(monster_type, item):
    monster_attacking = Monster(monster_type)
    # czy po uzyciu itemu do walki ma byc on usuwany z inventory
    # todo: dodac uaktualnianie HP w bocznym pasku
    texts = []
    while hero_.HP > 0 and monster_attacking.HP > 0:

        monster_att = monster_attacking.getAttack(hero_)
        texts.append(item_text[item])
        texts.append('The ' + str(monster_attacking.name) + ' attacks for ' + str(monster_att) + '!')
        hero_.HP -= monster_att

        if not hero_.HP > 0:
            hero_.dead = True
            texts.append('You are DEAD')
            return '<br/>'.join(texts)

        hero_att = hero_.getAttack(monster_attacking)
        texts.append('You attack and deal ' + str(hero_att) + ' damage!')
        monster_attacking.HP -= hero_att

        if not monster_attacking.HP > 0:
            monster_attacking.dead = True
            texts.append('Monster is DEAD. Good job!')
            return '<br/>'.join(texts)

@app.route("/room01/")
def room01():
    # tymczasowo
    if random.randint(0,10) > -1:
        #num_of_monsters:
        global num_of_monsters
        num_of_monsters -=1
        print("FIGHT RENDER")

        return render_template("fight.html", hero=hero_)
        if num_of_monsters==0:
            you_win()
    return render_template("room01.html", hero=hero_)

@app.route("/fight/")
def fight():
    return render_template("fight.html", hero=hero_)

@app.route("/hero/")
def hero():
    return render_template("hero.html", hero=hero_)

@app.route("/hall/")
def hall():
    return render_template("hall.html", hero=hero_)

@app.route("/library/")
def library():
    # tymczasowo
    return render_template("library.html", hero=hero_)

@app.route("/ballroom/")
def ballroom():
    # tymczasowo
    return render_template("ballroom.html", hero=hero_)

@app.route("/kitchen/")
def kitchen():
    # tymczasowo
    return render_template("kitchen.html", hero=hero_)

@app.route("/diningroom/")
def diningroom():
    # tymczasowo
    return render_template("diningroom.html", hero=hero_)

@app.route("/livingroom/")
def livingroom():
    # tymczasowo
    return render_template("livingroom.html", hero=hero_)

@app.route("/upstairscorridor/")
def upstairscorridor():
    # tymczasowo
    return render_template("upstairscorridor.html", hero=hero_)

@app.route("/studyroom/")
def studyroom():
    # tymczasowo
    return render_template("studyroom.html", hero=hero_)

@app.route("/masterbedroom/")
def masterbedroom():
    # tymczasowo
    return render_template("masterbedroom.html", hero=hero_)

@app.route("/bathroom/")
def bathroom():
    # tymczasowo
    return render_template("bathroom.html", hero=hero_)

@app.route("/smallcloset/")
def smallcloset():
    # tymczasowo
    return render_template("smallcloset.html", hero=hero_)

@app.route("/guestroom/")
def guestroom():
    # tymczasowo
    return render_template("guestroom.html", hero=hero_)

@app.route("/nannyroom/")
def nannyroom():
    # tymczasowo
    return render_template("nannyroom.html", hero=hero_)

@app.route("/nursery/")
def nursery():
    # tymczasowo
    return render_template("nursery.html", hero=hero_)

@app.route("/girlroom/")
def girlroom():
    # tymczasowo
    return render_template("girlroom.html", hero=hero_)

@app.route("/tinywashroom/")
def tinywashroom():
    # tymczasowo
    return render_template("tinywashroom.html", hero=hero_)

if __name__ == "__main__":
    app.run(debug=True)

'''monsters rutine:
num_of_monsters = 5
    at entry to each monster_enabled room:
    if rand(0-10) < num_of_monsters:
        num_of_monsters -=1
        monster_attack()
        if num_of_monsters==0:
            you_win()'''