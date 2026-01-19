import os 
class Config:
    SQLALCHEMY_DATABASE_URI = (
        'postgresql://neondb_owner:npg_M8IRz5fpyPSs@ep-silent-mud-ahoblu0u-pooler.c-3.us-east-1.aws.neon.tech/neondb'
        '?sslmode=require&channel_binding=require'
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
        "connect_args": {
            "connect_timeout": 10,
            "sslmode": "require"
        }
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "2409")
      
    
"""
class Configured:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///clusters.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "2409")


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