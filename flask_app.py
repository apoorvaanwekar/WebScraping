import scrape_mars
from flask import Flask, render_template, redirect
import pymongo

# Create app
app = Flask(__name__)

# Connect to mongo
mongodb = "mongodb://localhost:27017"
mongo_clinet = pymongo.MongoClient(mongodb)
my_database = mongo_clinet.marsDB


@app.route("/")
def index():
    mars_data = db.mars.find_one()
    return render_template('index.html', mars_data=mars_data)

@app.route("/scrape")
def scrape_data():
    mars_data = scrape_mars.scrape()
    db.mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)