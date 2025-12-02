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

#　ダイアログ定義
#　ログインダイアログ

@st.dialog("ログイン")
def login_dialog():
    mail_address = st.text_input("メールアドレス")
    password = st.text_input("パスワード", type="password")

    if st.button("ログイン"):
        result = (
            supabase.table("usermaster")
            .select("*")
            .eq("mail_address", mail_address)
            .eq("password", password)
            .execute()
        )

        if result.data:
            st.session_state.user = result.data[0]  # ログイン成功
            st.success("ログイン成功")
            st.switch_page("pages/dashboard.py")
        else:
            st.error("メールアドレスまたはパスワードが正しくありません。")

#　新規登録ダイアログ

@st.dialog("新規登録")
def signup_dialog():
    name = st.text_input("ユーザー名")
    mail_address = st.text_input("メールアドレス")
    password = st.text_input("パスワード", type="password")
    password2 = st.text_input("パスワード（確認）", type="password")
    amazon_id = st.text_input("Amazon ID（任意）")

    if st.button("アカウント作成"):
        if not name.strip():
            st.error("ユーザー名は必須です。")
            return
        elif not mail_address.strip():
            st.error("メールアドレスは必須です。")
            return
        elif not password:
            st.error("パスワードは必須です。")
            return
        elif password != password2:
            st.error("パスワードが一致しません")
            return
        # Supabase usermaster に追加
        result = (
            supabase.table("usermaster")
            .insert({"name": name, "mail_address": mail_address, "password": password})
            .execute()
        )

        st.success("アカウントを作成しました。ログインしてください。")


#  LP（トップページ）

col1, col2, col3 = st.columns([4, 1, 1])

with col2:
    if st.button("ログイン"):
        login_dialog()

with col3:
    if st.button("新規登録"):
        signup_dialog()

st.header("サンタさんチャットアプリへようこそ！")
st.subheader("説明文")
st.write("text")
st.write("・")
st.write("・")
st.write("・")
st.write("text")