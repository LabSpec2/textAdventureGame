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
    return render_template("new_game.html")
    
    
if __name__ == "__main__":
    app.run(debug=True)


#broken umbrella,ashen-wood stake,torn pillow,apple,garlick,lighter,broken rake,porcelain plate,copper spoon,revolver with silver bullets,small stick<br>