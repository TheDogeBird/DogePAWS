import os


# Database settings
settings = {
    'db_name': 'DogePAWS',
    'db_user': 'DogePAWS',
    'db_password': 'DogePAWS!',
    'port': 5000
}

# Flask settings
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
SESSION_TYPE = 'filesystem'

# Server settings
SERVER_HOST = 'localhost'
SERVER_PORT = 5000

# Other settings
REMEMBER_COOKIE_DURATION = 600  # seconds
