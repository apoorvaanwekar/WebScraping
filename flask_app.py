import scrape_mars
from flask import Flask, render_template, redirect
import pymongo

# Create app
app = Flask(__name__)

# Connect to mongo
mongodb = "mongodb://localhost:27017"
mongo_clinet = pymongo.MongoClient(mongodb)
my_db = mongo_clinet.mars_db


@app.route("/")
def index():
    marsdata = my_db.mars.find_one()
    return render_template('index.html', mars_data=marsdata)

@app.route("/scrape")
def scrape_data():
    marsdata = scrape_mars.scrape()
    my_db.mars.update(
        {},
        marsdata,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)
    
if __name__ == "__main__":
    app.run(debug=True)