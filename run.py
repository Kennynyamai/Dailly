from app import app
from flask_migrate import Migrate





if __name__ == '__main__':
    # When running this script directly, start the development server
    from flask_migrate import upgrade
    with app.app_context():
        upgrade()
    # Start the development server
    app.run(debug=False)