"""
WSGI entry point for production deployment
"""
from webapp import app

if __name__ == "__main__":
    app.run()