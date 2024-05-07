from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['banking_automation']
collection = db['bank_data']

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        # Get form data
        account_number = request.form['account_number']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        location = request.form['location']
        district = request.form['district']
        
        # Insert data into MongoDB
        account_data = {
            'account_number': account_number,
            'first_name': first_name,
            'last_name': last_name,
            'location': location,
            'district': district,
        }
        collection.insert_one(account_data)
        
        return redirect('/')
    else:
        return render_template('create_account.html')

@app.route('/display_records')
def display_records():
    records = collection.find()
    return render_template('display_records.html', records=records)

@app.route('/interest_cal')
def interest_calculator():
    return render_template('interest_cal.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_query']
    records = collection.find({'$or': [{'first_name': search_query}, {'last_name': search_query}]})
    return render_template('display_records.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
