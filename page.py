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


monster_hp = {MonsterType.Vampire:30, MonsterType.Ghost:9, MonsterType.Ghoul:12,\
              MonsterType.Zombie:9, MonsterType.Skeleton:3}  

monster_modifier = {MonsterType.Vampire:"dexterity", MonsterType.Ghost:"wisdom",\
                    MonsterType.Ghoul:"constitution", MonsterType.Zombie:"constitution",\
                    MonsterType.Skeleton:"dexterity"}

hero_modifier = {MonsterType.Vampire:"charisma", MonsterType.Ghost:"wisdom",\
                    MonsterType.Ghoul:"constitution", MonsterType.Zombie:"constitution",\
                    MonsterType.Skeleton:"dexterity"}
'''
                    {MonsterType.Vampire:"CHA", MonsterType.Ghost:"CHA",\
                    MonsterType.Ghoul:"CON", MonsterType.Zombie:"CON",\
                    MonsterType.Skeleton:"DEX"}

                    good: 3,5,1
                    decent: 2,3,0
                    dex-decent:3.2.0
                    not-pathetic: 2.1.1
                    bad: 1,0,0
                    magic-good:2.1.4
'''
item_stats = {"wooden rod":{"dexterity":3,"constitution":5,"charisma":1},\
              "broken umbrella":{"dexterity":2,"constitution":3,"charisma":0},\
              "shards of glass":{"dexterity":3,"constitution":2,"charisma":0},\
              "old book":{"dexterity":1,"constitution":0,"charisma":0},\
              "broken wineglass":{"dexterity":3,"constitution":2,"charisma":0},\
              "harp string":{"dexterity":3,"constitution":2,"charisma":0},\
              "garlic":{"dexterity":2,"constitution":0,"charisma":4},\
              "apple":{"dexterity":1,"constitution":0,"charisma":0},\
              "salt":{"dexterity":2,"constitution":0,"charisma":4},\
              "silver fork":{"dexterity":2,"constitution":0,"charisma":4},\
              "aspen-wood rod":{"dexterity":2,"constitution":0,"charisma":4},\
              "figurine":{"dexterity":1,"constitution":0,"charisma":0},\
              "rolled carpet":{"dexterity":2,"constitution":3,"charisma":0},\
              "thin planks":{"dexterity":2,"constitution":1,"charisma":1},\
              "quill":{"dexterity":1,"constitution":0,"charisma":0},\
              "handkerchief":{"dexterity":1,"constitution":0,"charisma":0},\
              "copper pipe":{"dexterity":3,"constitution":5,"charisma":1},\
              "shards of mirror":{"dexterity":3,"constitution":2,"charisma":0},\
              "silk robe":{"dexterity":1,"constitution":0,"charisma":0},\
              "vase":{"dexterity":2,"constitution":1,"charisma":1},\
              "frayed hat":{"dexterity":1,"constitution":0,"charisma":0},\
              "solid cane":{"dexterity":3,"constitution":5,"charisma":1},\
              "pillow":{"dexterity":2,"constitution":3,"charisma":0},\
              "wooden knob":{"dexterity":2,"constitution":1,"charisma":1},\
              "pacifier":{"dexterity":1,"constitution":0,"charisma":0},\
              "small painting":{"dexterity":2,"constitution":1,"charisma":1},\
              "stuffed bunny":{"dexterity":2,"constitution":3,"charisma":0},\
              "little blanket":{"dexterity":2,"constitution":1,"charisma":1},\
              "wooden horse":{"dexterity":3,"constitution":5,"charisma":1},\
              "porcelain doll":{"dexterity":2,"constitution":1,"charisma":1},\
              "caved jug":{"dexterity":2,"constitution":1,"charisma":1},\
              "thin sticks":{"dexterity":2,"constitution":1,"charisma":1}}



item_text = {"wooden rod":"You get a good grab at the solid wooden rod and take a swing at the monster.\n",\
              "broken umbrella":"You grab the umbrella and point its spiky end at the creature.\n",\
              "shards of glass":"Shards of glass are a bit awkward to hold, but they are sharp and can surly hurt the creature!\n",\
              "old book":"You grab the... old book? Well, that might end up poorly. Desperately, you throw it at the monster\n",\
              "broken wineglass":"Broken wineglass is a bit awkward to hold, but it's sharp and can surly hurt the creature!\n",\
              "harp string":"You grab the string desperately and lash it at the creature. It has quite some reach!\n",\
              "garlic":"You clench the garlic in your fist and attempt to shove it in the monster's mouth.\n",\
              "apple":"You grab the... apple? Well, that might end up poorly. Desperately, you throw it at the monster\n",\
              "salt":"Desperately, you grab the pinch of salt and throw it at the monster. Salt hurts them, right? Right?\n",\
              "silver fork":"The fork is tiny, but the silver will surly hurt the creature\n",\
              "aspen-wood rod":"Hey, it's basically an aspen-wood stake! You take the wooden rod and aim straight for the monsters heart.\n",\
              "figurine":"You grab the... porcelain figurine? Well, that might end up poorly. Desperately, you throw it at the monster\n",\
              "rolled carpet":"It might not be what you would wish you had, but in desperate times... The thick threaded carpet is pretty heavy!\n",\
              "thin planks":"The plank seems rather feeble, but you hold it tight and aim for the creature's face.\n",\
              "quill":"You grab the... quill? Well, that might end up poorly. Desperately, you throw it at the monster\n",\
              "handkerchief":"You grab the... handkerchief? Well, that might end up poorly. Desperately, you throw it at the monster\n",\
              "copper pipe":"You get a good grab at the copper pipe and take a swing at the monster.\n",\
              "shards of mirror":"Shards of mirror are a bit awkward to hold, but they are sharp and can surly hurt the creature!\n",\
              "silk robe":"You grab the... silk robe? Well, that might end up poorly. Desperately, you brandish it at the monster\n",\
              "vase":"The vase might be a decent ranged weapon, but you're not sure how it will do in melee. You grab it regardless.\n",\
              "frayed hat":"You grab the... frayed hat? Well, that might end up poorly. Desperately, you brandish it at the monster\n",\
              "solid cane":"You get a good grab at the solid cane and take a swing at the monster.\n",\
              "pillow":"It might not be what you would wish you had, but in desperate times... The geese-featered pillow is pretty heavy!\n",\
              "wooden knob":"You clench the small knob in your fist and try to use it as a knuckle-duster.\n",\
              "pacifier":"You grab the... pacifier? Well, that might end up poorly. Desperately, you throw it at the monster\n",\
              "small painting":"Luckily, this painting was made on a wooden board. You wack the creature right in the face.\n",\
              "stuffed bunny":"You grab the stuffed bunny... Well it's certainly an unusual weapon, but the toy is stuffed with sawdust and surprisingly heavy!\n",\
              "little blanket":"Every child knows that hiding under the blanket makes the monsters disappear... Maybe flailing it at them works as well?\n",\
              "wooden horse":"You grab a wooden horse. It’s shape is a bit awkward, but it is a solid piece of wood to hit the monster with.\n",\
              "porcelain doll":"You grab the... porcelain doll? Well, you surely find it unsettling, maybe so will the creature?\n",\
              "caved jug":"The jug might be a decent ranged weapon, but you're not sure how it will do in melee. You grab it regardless.\n",\
              "thin sticks":"The stick seems rather feeble, but you hold it tight and aim for the creature's face.\n"}


# global variable, that keeps last visited room
last_visited = ""


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

# todo: change randomly
monster_type = MonsterType.Vampire

@app.route("/pick_weapon", methods=["POST"])
def pick_weapon():
    item = str(request.form)
    item = item[item.find("(") + 4: item.find(",") - 1]
    print(item)
    # tu zmieniac randomly
    text = monster_attack(monster_type, item)
    return text

def monster_attack(monster_type, item):
    monster_attacking = Monster(monster_type)
    # czy po uzyciu itemu do walki ma byc on usuwany z inventory 
    # todo: dodac uaktualnianie HP w bocznym pasku
    texts = []
    texts.append(item_text[item])
    while hero_.HP > 0 and monster_attacking.HP > 0:

        monster_att = monster_attacking.getAttack(hero_)
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



@app.route("/fight/")
def fight(room="hall"):
    return render_template("fight.html", hero=hero_, room=room, monster = str(monster_type)[12:])

@app.route("/hero/")
def hero():
    return render_template("hero.html", hero=hero_)

@app.route("/hall/")
def hall():
    return render_template("hall.html", hero=hero_)


def check_if_monster_attack(name):
    global last_visited
    if not last_visited == name:
        last_visited = name
        if random.randint(0,10) > 7:            
            return True
    return False


@app.route("/library/")
def library():
    if check_if_monster_attack("library"):
        return render_template("fight.html", hero=hero_, room="library")
    return redirect(url_for('library_ok'))
    
@app.route("/library_ok/")
def library_ok():
    return render_template("library.html", hero=hero_)
    
@app.route("/ballroom/")
def ballroom():
    if check_if_monster_attack("ballroom"):
        return render_template("fight.html", hero=hero_, room="ballroom")
    return redirect(url_for('ballroom_ok'))
    
@app.route("/ballroom_ok/")
def ballroom_ok():
    return render_template("ballroom.html", hero=hero_)

@app.route("/kitchen/")
def kitchen():
    if check_if_monster_attack("kitchen"):
        return render_template("fight.html", hero=hero_, room="kitchen")
    return redirect(url_for('kitchen_ok'))
    
@app.route("/kitchen_ok/")
def kitchen_ok():
    return render_template("kitchen.html", hero=hero_)

@app.route("/diningroom/")
def diningroom():
    if check_if_monster_attack("diningroom"):
        return render_template("fight.html", hero=hero_, room="diningroom")
    return redirect(url_for('diningroom_ok'))

@app.route("/diningroom_ok/")
def diningroom_ok():
    return render_template("diningroom.html", hero=hero_)

@app.route("/livingroom/")
def livingroom():
    if check_if_monster_attack("livingroom"):
        return render_template("fight.html", hero=hero_, room="livingroom")
    return redirect(url_for('livingroom_ok'))
    
@app.route("/livingroom_ok/")
def livingroom_ok():
    return render_template("livingroom.html", hero=hero_)


@app.route("/upstairscorridor/")
def upstairscorridor():
    return render_template("upstairscorridor.html", hero=hero_)
    

@app.route("/studyroom/")
def studyroom():
    if check_if_monster_attack("studyroom"):
        return render_template("fight.html", hero=hero_, room="studyroom")
    return redirect(url_for('studyroom_ok'))

@app.route("/studyroom_ok/")
def studyroom_ok():
    return render_template("studyroom.html", hero=hero_)


@app.route("/masterbedroom/")
def masterbedroom():
    if check_if_monster_attack("masterbedroom"):
        return render_template("fight.html", hero=hero_, room="masterbedroom")
    return redirect(url_for('masterbedroom_ok'))
    
@app.route("/masterbedroom_ok/")
def masterbedroom_ok():
    return render_template("masterbedroom.html", hero=hero_)
    

@app.route("/bathroom/")
def bathroom():
    if check_if_monster_attack("bathroom"):
        return render_template("fight.html", hero=hero_, room="bathroom")
    return redirect(url_for('bathroom_ok'))
    
@app.route("/bathroom_ok/")
def bathroom_ok():
    return render_template("bathroom.html", hero=hero_)
    
    

@app.route("/smallcloset/")
def smallcloset():
    if check_if_monster_attack("smallcloset"):
        return render_template("fight.html", hero=hero_, room="smallcloset")
    return redirect(url_for('smallcloset_ok'))
    
@app.route("/smallcloset_ok/")
def smallcloset_ok():
    return render_template("smallcloset.html", hero=hero_)
    

@app.route("/guestroom/")
def guestroom():
    if check_if_monster_attack("guestroom"):
        return render_template("fight.html", hero=hero_, room="guestroom")
    return redirect(url_for('guestroom_ok'))

@app.route("/guestroom_ok/")
def guestroom_ok():
    return render_template("guestroom.html", hero=hero_)



@app.route("/nannyroom/")
def nannyroom():
    if check_if_monster_attack("nannyroom"):
        return render_template("fight.html", hero=hero_, room="nannyroom")
    return redirect(url_for('nannyroom_ok'))

@app.route("/nannyroom_ok/")
def nannyroom_ok():
    return render_template("nannyroom.html", hero=hero_)


@app.route("/nursery/")
def nursery():
    if check_if_monster_attack("nursery"):
        return render_template("fight.html", hero=hero_, room="nursery")
    return redirect(url_for('nursery_ok'))
 
@app.route("/nursery_ok/")
def nursery_ok():
    return render_template("nursery.html", hero=hero_)
 
    
@app.route("/girlroom/")
def girlroom():
    if check_if_monster_attack("girlroom"):
        return render_template("fight.html", hero=hero_, room="girlroom")
    return redirect(url_for('girlroom_ok'))
       
@app.route("/girlroom_ok/")
def girlroom_ok():
    return render_template("girlroom.html", hero=hero_)
    
    
@app.route("/tinywashroom/")
def tinywashroom():
    if check_if_monster_attack("tinywashroom"):
        return render_template("fight.html", hero=hero_, room="tinywashroom")
    return redirect(url_for('tinywashroom_ok'))

@app.route("/tinywashroom_ok/")
def tinywashroom_ok():
    return render_template("tinywashroom.html", hero=hero_)

if __name__ == "__main__":
    app.run(debug=True)
