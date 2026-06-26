from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection, init_db

app = Flask(__name__)

"""
Session is imported from Flask (see the first line). The session object is a proxy that 
allows you to store data specific to a user across requests. The session object is 
automatically available in the Flask request context once the app is running, so you do 
not necessarily  need to import it in every file if you are only accessing it in route 
functions. 

To use session, you need to have a secret key set in your Flask app (see below).  This key 
can be any string of your choice, but for security reasons, it should be a complex and
unpredictable value (e.g., generated randomly as below). 

The secret key is needed to **sign** session cookies. If you want **encrypted** sessions, 
you need to implement additional measures.
"""
app.secret_key = os.urandom(24)

# Initialize database, if it does not exist
if not os.path.exists('cookbook.db'):
    init_db()

def login_required(f):
    """
    This is a **decorator function** to restrict access to routes that require a user 
    to be logged in.

    A decorator function is a special type of function that modifies the behavior of another 
    function. Decorators are often used to add functionality or modify routes and request 
    handling in a clean and readable way.

    In the lectures, we have already used decorators like app.route('/'), which specifies the 
    URL endpoints that trigger a particular function (in this case '/').
    """
    # Preserve the original function's metadata (name, docstring, etc.)
    @wraps(f)  
    def decorated_function(*args, **kwargs):
        # Check if 'user_id' exists in the session to verify if the user is logged in.
        if 'user_id' not in session:
            # If not logged in, redirect the user to the 'index' route.
            return redirect(url_for('index'))
        # If logged in, proceed to call the original route function
        return f(*args, **kwargs)
    # Return the decorated function to be used as a decorator
    return decorated_function 

@app.route('/', methods=['GET', 'POST'])
def index():
    """Home page: handle login, registration, and display user preferences."""
    ingredients_list = ['dairy', 'egg', 'meat', 'nuts']
    current_unwanted = []

    # We have imported request from Flask in the first line. 
    # Here we check if the HTTP request method is POST, indicating form submission
    if request.method == 'POST':
        # Retrieve the 'action' parameter from the submitted form
        # See in index.html that possible "action"s are login and register 
        action = request.form.get('action')

        if action == 'login':

            # Extract username and password from the form data
            username = request.form['username']
            password = request.form['password']

            # Establish a connection to the database
            conn = get_db_connection()

            """
            Note that when passing multiple parameters to execute, we had used something like
            rows = conn.execute (" SELECT * FROM user 
                WHERE username =? and password =?", (username , digest))

            Here we will pass a single parameter (username) to the prepared statement. To pass 
            a single parameter, you need to create a singleton tuple by including a comma after 
            the element, i.e. (username,).
            """
            # Query the database for a user with the provided username and close
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            conn.close()

            # Verify if user exists and the provided password matches the stored hash
            if user and check_password_hash(user['password'], password):
                # Store user information in session to keep the user logged in
                session['user_id'] = user['id']
                session['username'] = user['username']
                # Redirect to the recipe search page upon successful login
                return redirect(url_for('search_recipe'))
            else:
                # Flash an error message if login credentials are invalid
                flash('Invalid username or password')

        elif action == 'register':
            # Extract username and password from the form data
            username = request.form['username']
            password = request.form['password']
            # Hash the password for secure storage using a cryptographic hash function
            hashed_password = generate_password_hash(password)
            # For new users, set all ingredients to OK (1)
            dairy = 1
            egg = 1
            meat = 1
            nuts = 1
            try:
                # Establish a connection to the database
                conn = get_db_connection()
                # Insert the new user into the 'users' table with their username,
                # hashed password, and the default ingredient restrictions
                conn.execute('''
                    INSERT INTO users (username, password, dairy, egg, meat, nuts)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (username, hashed_password, dairy, egg, meat, nuts))
                # Commit the transaction to save changes to the database 
                # and close the connection
                conn.commit()
                conn.close()
                # Inform the user that account creation was successful 
                # and prompt to log in
                flash('Account created! Please log in.')
            except sqlite3.IntegrityError:
                # Handle the case where the username already exists 
                # (violates UNIQUE constraint, see database.py)
                flash('Username already exists.')
    else:
        # If logged in, fetch user preferences
        if 'user_id' in session:
            # Establish a connection to the database
            conn = get_db_connection()
            """
            Here we retrieve the user's dietary preferences for the specific ingredients.
            We are selecting the columns dairy, egg, meat, and nuts from the users table 
            where the id matches session['user_id']. Using fetchone() retrieves that single 
            row (since id is unique).

            """
            user = conn.execute('SELECT dairy, egg, meat, nuts FROM users WHERE id = ?', (session['user_id'],)).fetchone()
            conn.close()
            
            # Collect ingredients where user wants to avoid (value=0)
            current_unwanted = []
            # Loop through each ingredient in the predefined list of ingredients
            for ingredient in ingredients_list:
                # Check if the user has marked this ingredient 
                # as unwanted (value=0)
                if user[ingredient] == 0:
                    # Add the ingredient to the list of unwanted ingredients
                    current_unwanted.append(ingredient)

    return render_template('index.html', 
                           ingredients=ingredients_list, 
                           current_unwanted=current_unwanted)

@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    """
    Handle the '/add_recipe' route, allowing logged-in users to add new recipes.
    Supports both GET (render form) and POST (process form submission) methods.
    """
    if request.method == 'POST':
        # Extract form data submitted by the user
        name = request.form['name']
        description = request.form['description']
        dish_type = request.form['dish_type']
        selected_ingredients = request.form.getlist('ingredients')

        print(f'selected_ingredients {selected_ingredients}')

        # Map selected ingredients to binary flags for database storage
        dairy = 1 if 'dairy' in selected_ingredients else 0
        egg = 1 if 'egg' in selected_ingredients else 0
        nuts = 1 if 'nuts' in selected_ingredients else 0
        meat = 1 if 'meat' in selected_ingredients else 0

        # Establish a connection to the database
        conn = get_db_connection()
        # Insert the new recipe into the 'recipes' table
        conn.execute(
            'INSERT INTO recipes (name, description, dish_type, dairy, egg, meat, nuts) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (name, description, dish_type, dairy, egg, meat, nuts)
        )
        
        # Commit the transaction to save changes 
        # and close the connection
        conn.commit()
        conn.close()

        # Provide user feedback that the recipe was added successfully
        flash('Recipe added successfully!')
            
        # Redirect user to the recipe search page after adding
        return redirect(url_for('add_recipe'))

    return render_template('add_recipe.html')

@app.route('/search_recipe', methods=['GET', 'POST'])
@login_required
def search_recipe():
    """
    Search for recipes excluding user's unwanted ingredients.
    Initialize an empty list to store the resulting recipes.
    """

    # Initialize an empty list of recipes
    recipes = []

    if request.method == 'POST':
        dish_type = request.form['dish_type']

        # To fetch user's unwanted ingredients preferences from the database
        # establish a new connection
        conn = get_db_connection()

        # Execute query to get the user's preferences for dairy, egg, meat, nuts
        user = conn.execute('SELECT dairy, egg, meat, nuts FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()

        # Initialize list to hold SQL conditions for filtering recipes
        conditions = []

        # Loop through each ingredient category
        for ingredient in ['dairy', 'egg', 'meat', 'nuts']:
            # If user has marked this ingredient as unwanted (value 0),
            # add a condition to exclude recipes containing this ingredient
            if user[ingredient] == 0:
                conditions.append(f"{ingredient} = 0")

        # Start building the base SQL query to select recipes 
        # matching the specified dish type
        base_query = 'SELECT * FROM recipes WHERE dish_type = ?'
        # If there are any conditions (unwanted ingredients to exclude)
        if conditions:
            # Append them to the base query with AND operators
            base_query += ' AND ' + ' AND '.join(conditions)

        print(f'new base_query {base_query}')

        # Establish a connection to the database
        conn = get_db_connection()

        """
        Below, we will finalize the query and execute it to fetch recipes matching all 
        criteria.
        In this part, I give an example for the use of **cursor** object. A cursor is an 
        object used in database programming to manage the context of a fetch operation. It 
        acts as a pointer that allows you to traverse, fetch, and manipulate database query 
        results. In particular, it enables you to iterate over query results efficiently 
        (row by row), when dealing with multiple rows.

        A more consice alternative to the below is:
        recipes = conn.execute(base_query, (dish_type,)).fetchall()
        """

        cursor = conn.execute(base_query, (dish_type,))
        for row in cursor:
            recipes.append(row)
        conn.close()

    # Render the search results page, passing the list of recipes to the template
    return render_template('search_recipe.html', recipes=recipes)

@app.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    """Handle user preferences for unwanted ingredients."""

    # List of all possible ingredients that can be marked as unwanted
    ingredients = ['dairy', 'egg', 'meat', 'nuts']

    # Initialize an empty list to store user's current unwanted ingredients
    current_unwanted = []

    if request.method == 'POST':
        # Handle form submission to update preferences
        # Retrieve list of ingredients user wants to avoid from form data
        unwanted = request.form.getlist('unwanted_ingredients') 

        # Initialize default: assume all ingredients are wanted (value=1)
        updates = {
            'dairy': 1,
            'egg': 1,
            'meat': 1,
            'nuts': 1
        }
        # For each ingredient the user wants to avoid, 
        # update its value to 0
        for ingredient in unwanted:
            if ingredient in updates:
                updates[ingredient] = 0

        # Connect to the database to update user's preferences
        conn = get_db_connection()

        # Execute UPDATE statement to set preferences based on user input
        conn.execute('''
            UPDATE users
            SET dairy = ?, egg = ?, meat = ?, nuts = ?
            WHERE id = ?
        ''', (updates['dairy'], updates['egg'], updates['meat'], updates['nuts'], session['user_id']))
        # Commit the changes to the database and then close the connection
        conn.commit()
        conn.close()

        # Provide feedback to the user that preferences have been updated
        flash('Preferences updated.')
        
        # Redirect user to the recipe search page after updating preferences
        return redirect(url_for('search_recipe'))

    # Fetch current preferences
    conn = get_db_connection()
    user = conn.execute('SELECT dairy, egg, meat, nuts FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()

    if user:
        for ingredient in ingredients:
            if user[ingredient] == 0:
                current_unwanted.append(ingredient)

    return render_template('preferences.html', ingredients=ingredients, current_unwanted=current_unwanted)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
