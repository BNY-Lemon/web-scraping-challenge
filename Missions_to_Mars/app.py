from flask import Flask, render_template, jsonify, redirect
from scrape_mars import scrape as myScrape

import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.team_db

# Set route
@app.route('/')
def index():
    # Store the entire team collection in a list
    teams = db.team.find_one()
    print(teams)

    # Return the template with the teams list passed in
    return render_template('index.html', teams=teams)

@app.route('/scrape')
def scrape():
    db.team.update({}, myScrape(), upsert= True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
