import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # 1. Get the URL from environment (Vercel)
    uri = os.environ.get('DATABASE_URL')
    
    # 2. Logic to handle the Postgres naming fix
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    # 3. Final URI assignment: Use the Cloud DB if it exists, else local SQLite
    SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # Extra: Disable tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False