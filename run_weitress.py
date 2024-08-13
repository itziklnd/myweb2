from waitress import serve
from app import app  # Import the 'app' instance from 'myapp.py'

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)  # Adjust host and port if necessary
