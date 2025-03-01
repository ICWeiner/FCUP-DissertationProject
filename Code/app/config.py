'''Flask App configuration.'''
from os import environ, path
from dotenv import load_dotenv

# Specificy a `.env` file containing key/value config values
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:

    # General Config
    ENVIRONMENT = environ.get('ENVIRONMENT')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_DEBUG = environ.get('FLASK_DEBUG')
    SECRET_KEY = environ.get('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    UPLOAD_FOLDER = 'uploads'

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Proxmox credentials
    PROXMOX_USER =  environ.get('PROXMOX_USER')
    PROXMOX_PASSWORD =  environ.get('PROXMOX_PASSWORD')
    PROXMOX_HOST =  environ.get('PROXMOX_HOST')

    # Celery
    CELERY_CONFIG = 'config.CeleryConfig'

    

class CeleryConfig:
    # Celery
    CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = environ.get('CELERY_RESULT_BACKEND')
    #CELERY_TASK_ACKS_LATE = True TODO:still need to decide on this one
    #CELERY_WORKER_PREFETCH_MULTIPLIER = 1
    #CELERY_WORKER_CONCURRENCY = 4 by defaults this uses all available cores