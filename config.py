import os 
#from supabase import create_client, Client

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///clusters.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "2409" # os.getenv("SECRET_KEY")
    DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
    
"""
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER") # or verified Brevo email
    
    # Backup --- Config ---
    EMAIL_FROM = os.getenv("EMAIL_FROM")
    EMAIL_TO = os.getenv("EMAIL_TO")
    GMAIL_USER = os.getenv("GMAIL_USER")
    GMAIL_PASS = os.getenv("GMAIL_PASS")   # Use an App Password if 2FA is enabled
    

    SUPABASE_URL = os.getenv("SUPABASE_URL") #'https://oivrozgjypetuxiorfik.supabase.co'
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    SUPABASE_DB_USER = os.getenv("SUPABASE_DB_USER")
    SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")
    SUPABASE_DB_NAME = os.getenv("SUPABASE_DB_NAME")
    SUPABASE_DB_HOST = os.getenv("SUPABASE_DB_HOST")  # db.<project-ref>.supabase.co

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{SUPABASE_DB_USER}:{SUPABASE_DB_PASSWORD}@{SUPABASE_DB_HOST}:5432/{SUPABASE_DB_NAME}?sslmode=require'

 
# Optional: create Supabase client if useful
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
"""