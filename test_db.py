from winery import create_app, db
from flask import current_app

app = create_app()

with app.app_context():
    # Check if we have an app context
    print(f"Has app context: {current_app._get_current_object() is not None}")
    
    # Check if db is properly initialized
    try:
        # Try a simple database query
        result = db.session.execute(db.select(db.text("1"))).scalar()
        print(f"Database query result: {result}")
        print("Database connection successful!")
    except Exception as e:
        print(f"Database error: {e}")