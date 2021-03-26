from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_mission"

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)

@app.route("/")
def home():
    # find data record
    mars_results = mongo.db.collection.find_one()

    # return the data template
    return render_template ('index.html', mars_results = mars_results)



@app.route("/scrape")
def scrape():
    # run function
    mars_results = mongo.db.collection
    mars_data = scrape_mars.scrape()
    mars_results.update({}, mars_data, upsert = True)
    
    # redirect to homepage
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
