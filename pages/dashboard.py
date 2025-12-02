import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ログインチェック
if "user" not in st.session_state:
    st.error("ログインしてください。")
    st.stop()

user = st.session_state.user
st.title(f"ようこそ、{user['name']} さん！")

#　サイドバー
st.sidebar.header("お子さんの選択")
# ユーザー情報に基づきお子さんの情報が登録されているか検索
def load_children():
    res = (
        supabase.table("childmaster")
        .select("*")
        .eq("user_id", user["user_id"])
        .order("created_at", desc=False)
        .execute()
    )
    return res.data or []

child_names = [child["name"] for child in st.session_state.children_list]

# プルダウン
selected_child = st.sidebar.selectbox(
    "お子さんを選択してください",
    child_names if child_names else ["登録されていません"]
)
if st.sidebar.button("お子さんを登録する"):
    st.dialog("お子さんプロフィール登録")

#ポップアップ
@st.dialog("新規登録")
def registration_dialog():
    name = st.text_input("お名前")
    birth_date = st.date_input("生年月日")
    gender = st.selectbox("性別" ,("男の子","女の子","選択しない"))

    if st.button("アカウント作成"):
        if not name.strip():
            st.error("お名前は必須です。")
            return
        elif not birth_date.strip():
            st.error("生年月日は必須です。")
            return
        elif not gender:
            st.error("性別は必須です。")
            return
        # Supabase childmaster に追加
        result = (
            supabase.table("childmaster")
            .insert({"user_id":user["user_id"], "name": name, "birth_date": birth_date, "gender": gender})
            .execute()
        )

        st.success("お子さんの情報を登録しました。")
