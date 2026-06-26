import sqlite3

def init_db():
    """
    Thsi function initializes the database by creating the necessary tables:
    - 'users' table to store user information and dietary preferences.
    - 'recipes' table to store recipe details and their ingredient information.
    """

    """ 
    We first establish a connection to the database with get_db_connection() function.
    
    As explained in the docstring of the function, conn can be used as a **context manager** 
    with the 'with' statement. This means that the __enter__() and __exit__() methods
    are called automatically.
    """
    with get_db_connection() as conn:
        """
        Here we create a **cursor** object to execute SQL statements. A cursor is an object 
        used to interact with the database. You may think of it as a pointer or a handle that
        facilitates communication with the database. The cursor is used to execute SQL 
        commands like SELECT, INSERT, UPDATE, etc.
        """

        cursor = conn.cursor()
        
        # Create 'users' table, if it doesn't already exist
        # Note that there is a comment after the double dash.
        # In SQL, -- is used to denote a single-line comment. 
        # Everything following -- on that line is considered a comment
        # and is ignored during execution.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique user ID, auto-incremented
                username TEXT UNIQUE NOT NULL,          -- Username, must be unique and not null
                password TEXT NOT NULL,                 -- User's password 
                dairy INTEGER,                        -- Dietary indicator for dairy (0 or 1)
                egg INTEGER,                          -- Dietary indicator for eggs (0 or 1)
                meat INTEGER,                         -- Dietary indicator for meat (0 or 1)
                nuts INTEGER                          -- Dietary indicator for nuts (0 or 1)
            )
        """)

        # Create 'recipes' table, if it doesn't already exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique recipe ID, auto-incremented
                name TEXT NOT NULL,                     -- Name of the recipe
                description TEXT,                       -- Description of the recipe
                dish_type TEXT NOT NULL,                -- Type of dish (e.g., starter, main)
                dairy INTEGER,                        -- Contains dairy (0 or 1)
                egg INTEGER,                          -- Contains eggs (0 or 1)
                meat INTEGER,                         -- Contains meat (0 or 1)
                nuts INTEGER                          -- Contains nuts (0 or 1)
            )
        """)


def get_db_connection():
    """
    Establishes a connection to the SQLite database.
    
    This function creates and returns a sqlite3.Connection object.n Python's sqlite3 module, 
    the Connection object does have __enter__ and __exit__ methods. This means that it can be
    used as a **context manager** with the 'with' statement. This allows you to manage the 
    connection's lifecycle more cleanly, automatically closing the connection when the block 
    is exited.  
    """
    conn = sqlite3.connect('cookbook.db')

    # This configures the SQLite connection such that query results are returned 
    # as row objects that behave like dictionaries.
    conn.row_factory = sqlite3.Row
    return conn
