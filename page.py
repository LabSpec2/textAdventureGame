from flask import Flask, redirect, url_for, render_template

class Stats:
    def __init__(self):
        self.strength = 0
        self.wisdom = 0
        self.speed = 0
    
    def add(self, add_str=0, add_wisdom=0, add_speed=0):
        self.strength += add_str
        self.wisdom += add_wisdom
        self.speed += add_speed

class Hero:
    def __init__(self, name):
        self.name = name
        self.stats = Stats()
        
    def upgrade(self, stat_name, points):
        if  stat_name == "strength":
            self.stats.add(add_str=points)
        elif stat_name == "wisdom":
            self.stats.add(add_wisdom=points)
        else:
            self.stats.add(add_speed=points)
            
app = Flask(__name__)
temp_hero = Hero(name="Jakub Wędrowycz")

@app.route("/")
def home():
    return render_template("index.html", hero=temp_hero)

@app.route("/story/")
def story():
    return render_template("story_template.html", hero=temp_hero)
    
@app.route("/story/add/<ile>")
def ile(ile):
    temp_hero.upgrade(stat_name="strength",points=int(ile))
    return render_template("story_template.html", hero=temp_hero)

if __name__ == "__main__":
    app.run(debug=True)