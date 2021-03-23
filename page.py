from flask import Flask, redirect, url_for, render_template, request
import random
import enum
from random import randrange

class Stats:
    def __init__(self, skill_dict = {}):
        self.strength = skill_dict["strength"]
        self.dexterity = skill_dict["dexterity"]
        self.constitution = skill_dict["constitution"]
        self.wisdom = skill_dict["wisdom"]
        self.charisma = skill_dict["charisma"]
        
    def add(self, skill_dict):
        self.strength += skill_dict["strength"]
        self.dexterity += skill_dict["dexterity"]
        self.constitution += skill_dict["constitution"]
        self.wisdom += skill_dict["wisdom"]
        self.charisma += skill_dict["charisma"]
        
class MonsterType(enum.Enum):
	Vampire = 1
	Ghost = 2
	Ghoul = 3
	Zombie = 4
	Skeleton = 5
    
class Monster:
    def __init__(self, monster_type, attack_max, hp_max):
        self.type = type
        self.attack_max = attack_max
        self.hp_max = hp_max
    
    def getModifier():
        return 0 # dict tbd
    
    def getAttack():
        return 10 + randrange(attack_max) - getModifier()
        
class Hero:
    id_counter = 0
    def __init__(self,  name = "User"):
        self.id= Hero.id_counter
        Hero.id_counter = Hero.id_counter + 1
        self.name = name
        self.stats = Stats()
        self.HP = random.randint(20, 35)
        self.attack_range = attack_range
        
        self.hero_attack_mod = {MonsterType.Vampire: self.stats.charisma, MonsterType.Ghost: self.stats.wisdom} # tbd

    def upgrade(self, skill_dict):
        self.stats.add(skill_dict)
           
    def getAttack(monster_attacking):
        return 10 + randrange(attack_range) + self.hero_attack_mod(monster_attacking.type)
		
            
app = Flask(__name__)
temp_hero = Hero(name = "Wedrownik", attack_range=5)

@app.route("/")
def home():
    return render_template("index.html", hero=temp_hero)

@app.route("/story/")
def story():
    return render_template("story_template.html", hero=temp_hero)
   
#temp route   
@app.route("/story/add/<ile>")
def ile(ile):
    temp_hero.upgrade({"strength" : 7})
    return render_template("story_template.html", hero=temp_hero)

if __name__ == "__main__":
    app.run(debug=True)