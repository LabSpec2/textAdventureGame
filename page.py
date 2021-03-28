from flask import Flask, redirect, url_for, render_template, request
import random
import enum
from random import randrange
from collections import defaultdict

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
    
class ItemType(enum.Enum):
    WoddenBat = 1,
    ThinStick = 2,
    Garlick = 3,
    Salt = 4,
    AspenWoodStake = 5,
    Revolver = 6,
    Apple = 7,
    EmptyCan = 8,
    BrokenUmbrella = 9,
    PlantPot = 10,
    SmallPainting = 11,
    OldShoe = 12,
    Pillow = 13
    
    
monster_hp = {MonsterType.Vampire:30, MonsterType.Ghost:18, MonsterType.Ghoul:12,\
              MonsterType.Zombie:9, MonsterType.Skeleton:3}  

monster_modifier = {MonsterType.Vampire:"dexterity", MonsterType.Ghost:"wisdom",\
                    MonsterType.Ghoul:"constitution", MonsterType.Zombie:"constitution",\
                    MonsterType.Skeleton:"dexterity"}

hero_modifier = {MonsterType.Vampire:"charisma", MonsterType.Ghost:"wisdom",\
                    MonsterType.Ghoul:"strength", MonsterType.Zombie:"dexterity",\
                    MonsterType.Skeleton:"strength"}
                    
item_stats = {ItemType.WoddenBat:{"dexterity":5,"constitution":4,"charisma":3},\
              ItemType.ThinStick:{"dexterity":2,"constitution":3,"charisma":4},\
              ItemType.Garlick:{"dexterity":0,"constitution":0,"charisma":7},\
              ItemType.Salt:{"dexterity":0,"constitution":0,"charisma":0},\
              ItemType.AspenWoodStake:{"dexterity":0,"constitution":1,"charisma":9},\
              ItemType.Revolver:{"dexterity":4,"constitution":2,"charisma":5},\
              ItemType.Apple:{"dexterity":0,"constitution":1,"charisma":0},\
              ItemType.EmptyCan:{"dexterity":1,"constitution":2,"charisma":0},\
              ItemType.BrokenUmbrella:{"dexterity":1,"constitution":2,"charisma":0},\
              ItemType.PlantPot:{"dexterity":1,"constitution":1,"charisma":1},\
              ItemType.SmallPainting:{"dexterity":2,"constitution":3,"charisma":1},\
              ItemType.OldShoe:{"dexterity":2,"constitution":1,"charisma":0},\
              ItemType.Pillow:{"dexterity":0,"constitution":5,"charisma":0}}


class Monster:
    def __init__(self, type):
        self.type = type
        self.hp_max = monster_hp[type]

    def getAttack(self, hero_attacking):
        return 10 + randrange(self.type) - hero_attacking.stats.getByName(monster_modifier[self.type])
        
class Hero:
    id_counter = 0
    def __init__(self,  name = "User",  attack_range=5):
        self.id= Hero.id_counter
        Hero.id_counter = Hero.id_counter + 1
        self.name = name
        self.stats = Stats()
        self.HP = random.randint(20, 35)
        self.attack_range = attack_range
        self.collected_items = []

    def upgrade(self, skill_dict):
        self.stats.add(skill_dict)
    
    def addItem(self, item):
        self.collected_items.append(item)
        dict_ = makeDict(item_stats[item])
        self.stats.add(dict_)
        
    def getAttack(self, monster_attacking):    
        return 10 + randrange(self.attack_range) + self.stats.getByName(hero_modifier[monster_attacking])


app = Flask(__name__)
temp_hero = Hero(name = "Wedrownik")

@app.route("/")
def home():
    return render_template("index.html", hero=temp_hero)

@app.route("/story/")
def story():
    return render_template("story_template.html", hero=temp_hero)
   
#temp route   
@app.route("/story/add/<ile>")
def ile(ile):
    temp_hero.upgrade(makeDict({"strength" : int(ile)}))
    return render_template("story_template.html", hero=temp_hero)

if __name__ == "__main__":
    app.run(debug=True)