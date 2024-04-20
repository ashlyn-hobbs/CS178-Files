# Author: Ashlyn Hobbs
# Date: 4/1/2024
# Description: Flask web application that allows users to add, update, delete, and view user data stored in a DynamoDB database, incorporating user authentication and displaying data based on user preferences by utilizing an sql world database.

from flask import Flask
from flask import render_template
from flask import session
from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = "Users"

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

# Route for home page
@app.route('/')
def home():
    return render_template('homepage.html')

# Route for adding a new user
@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        lastname = request.form['lastname']
        language = request.form['language']
        
        # Process the data (e.g., add it to a database)
        # Add user to DynamoDB
        table.put_item(Item={'name': name, 'lastname': lastname, 'language': language})
        
        flash('User added successfully!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')

# Route for logging in a user
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        language = request.form['language']
        
        try:
            # Query DynamoDB for user
            response = table.query(
                KeyConditionExpression=Key('name').eq(name)
            )
            
            if 'Items' in response and response['Items']:
                user = response['Items'][0]
                if user['language'] == language:
                    session['username'] = name
                    session['preflanguage'] = language
                    return redirect(url_for('display_countries'))
            else:
                flash('Invalid username or language!', 'error')
                return redirect(url_for('login'))
        
        except Exception as e:
            flash('An error occurred: {}'.format(str(e)), 'error')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
    
# imports all functions from dbcode.py file so that they may be utilized
from dbcode import *
# Route for displaying countries based on user's preferred language
@app.route('/display-countries')
def display_countries():
    if 'language' in session:
        language = session['preflanguage']
        countries = get_list_of_countries(language)
        return render_template('display_countries.html', countries=countries)
    else:
        flash('Please log in first!', 'error')
        return redirect(url_for('login'))


# Route for displaying all users from the nosql database
@app.route('/display-users')
def display_users():
    response = table.scan()
    users_info = response.get('Items', [])  # Get all items from DynamoDB response
    return render_template('display_users.html', users=users_info)

# Route for deleting a user
@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        name = request.form['name']
        
        # Delete user from DynamoDB
        response = table.delete_item(
            Key={'name': name}
        )
        
        flash('User deleted successfully!', 'success')
        
        return redirect(url_for('home'))
    else:
        return render_template('delete_user.html')
        
# Route for updating user details
# Credit to ChatGPT for the language placeholder idea after I got a CLIENT ERROR code for it
# I asked about the error and provided my code, to which ChatGPT modified it according to what you see below
@app.route('/update-user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        language = request.form['language']
        
        # Update user details in DynamoDB
        response = table.update_item(
            Key={'name': name},
            UpdateExpression='SET lastname = :val1, #lang = :val2',  # Use placeholder for 'language' attribute
            ExpressionAttributeValues={
                ':val1': lastname,
                ':val2': language
            },
            ExpressionAttributeNames={
                "#lang": "language"  # Define placeholder for 'language' attribute
            }
        )
        
        flash('User updated successfully!', 'success')
        return redirect(url_for('home'))
    else:
        return render_template('update_user.html')


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)