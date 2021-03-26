from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri = 'mongodb://localhost:27017/mars_mission')

@app.route("/")
def home():
    # find data record
    mars_dictionary = mongo.db.collection.find_one()

    # return the data template
    return render_template ('index.html', mars_dictionary = mars_dictionary)



@app.route("/scrape")
def scrape():
    # run function
    mars_dictionary = scrape_mars.scrape()

    # updatate mongodb
    mongo.db.collection.update({}, mars_dictionary, upsert = True)

    # redirect to homepage
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
