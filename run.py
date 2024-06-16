import logging
from app import create_app

app = create_app()

# Set up logging
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    app.run(debug=True)
