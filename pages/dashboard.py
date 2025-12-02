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

st.sidebar.header("お子さんの選択")
# 子どもの名前だけをプルダウン候補にする
children_res = (
    supabase.table("childmaster")
    .select("*")
    .eq("user_id", user["user_id"])
    .order("created_at", desc=False)
    .execute()
)

selected_child = st.sidebar.selectbox(
    "お子さんを選択してください",
    name if name else ["登録されていません"]
)

if st.sidebar.button("新しいお子さんを登録する"):

    with st.dialog("お子さんの新規登録"):
        child_name = st.text_input("子供の名前")
        birth_date = st.date_input("誕生日")
        gender = st.radio("性別", ["男の子", "女の子", "選択しない"])

        if st.button("登録する"):
            # バリデーション
            if not child_name.strip():
                st.error("子供の名前は必須です。")
            else:
                # DBへ登録
                result = supabase.table("childmaster").insert({
                    "user_id": user["user_id"],
                    "name": child_name,
                    "birth_date": birth_date.isoformat(),  # date型を文字列に変換
                    "gender": gender
                }).execute()

                if result.error:
                    st.error(f"登録に失敗しました: {result.error.message}")
                else:
                    st.success("お子さんを登録しました！")
