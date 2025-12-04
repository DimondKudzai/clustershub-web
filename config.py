import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///clusters.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    secret_key = '2409'
    
"""

import os
from supabase import create_client, Client

class Config:
    SUPABASE_URL = 'https://oivrozgjypetuxiorfik.supabase.co'
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    SUPABASE_DB_USER = os.getenv("SUPABASE_DB_USER")
    SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")
    SUPABASE_DB_NAME = os.getenv("SUPABASE_DB_NAME")
    SUPABASE_DB_HOST = os.getenv("SUPABASE_DB_HOST")  # db.<project-ref>.supabase.co

    SQLALCHEMY_DATABASE_URI = f'postgresql://{SUPABASE_DB_USER}:{SUPABASE_DB_PASSWORD}@{SUPABASE_DB_HOST}:5432/{SUPABASE_DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    secret_key = '2409'

# Optional: create Supabase client if  useful
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

"""