import os

class Config:
    FLASK_APP = os.environ.get('FLASK_APP', 'app.py')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    SECRET_KEY = os.environ['SECRET_KEY']
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'chat:'
    SESSION_REDIS = os.environ['REDIS_URL']

class ContentID:
    CONTENT_SID_FIRST_MESSAGE = os.environ.get('CONTENT_SID_FIRST_MESSAGE', 'default_first_message_sid')
    CONTENT_SID_DATES = os.environ.get('CONTENT_SID_DATES', 'default_dates_sid')
    CONTENT_SID_SLOTS = os.environ.get('CONTENT_SID_SLOTS', 'default_slots_sid')
    CONTENT_SID_EMPLOYEES = os.environ.get('CONTENT_SID_EMPLOYEES', 'default_employees_sid')