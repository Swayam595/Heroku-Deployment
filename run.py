from app import app
from db import db

db.init_app(app)

#### Creates the table if not present
@app.before_first_request
def create_tables():
    db.create_all() 
