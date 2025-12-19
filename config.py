import os
from supabase import create_client, Client

class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL") #'https://oivrozgjypetuxiorfik.supabase.co'
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    SUPABASE_DB_USER = os.getenv("SUPABASE_DB_USER")
    SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")
    SUPABASE_DB_NAME = os.getenv("SUPABASE_DB_NAME")
    SUPABASE_DB_HOST = os.getenv("SUPABASE_DB_HOST")  # db.<project-ref>.supabase.co

    SQLALCHEMY_DATABASE_URI = f'postgresql://{SUPABASE_DB_USER}:{SUPABASE_DB_PASSWORD}@{SUPABASE_DB_HOST}:5432/{SUPABASE_DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER") # or verified Brevo email
    
# Optional: create Supabase client if useful
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
