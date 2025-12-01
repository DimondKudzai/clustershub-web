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
    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("SUPABASE_DB_USER")}:{os.getenv("SUPABASE_DB_PASSWORD")}@{SUPABASE_URL.split("//")[-1]}/{os.getenv("SUPABASE_DB_NAME")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

"""