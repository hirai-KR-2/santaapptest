import streamlit as st
from supabase import create_client, Client
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

user = st.session_state.user
name = user["name"]  # usermaster の name カラム

st.title(f"ようこそ、{name} さん！")

st.sidebar("お子さんのお名前")