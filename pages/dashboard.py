import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ログインチェック
if "user" not in st.session_state:
    st.error("ログインしてください。")
    st.stop()

user = st.session_state.user
name = user["name"]  # ユーザー名

st.title(f"ようこそ、{name} さん！")

# --------------------------
# サイドバー
# --------------------------
st.sidebar.header("お子さんの選択")

# 子ども一覧を取得
children_res = (
    supabase.table("childmaster")
    .select("*")
    .eq("user_id", user["user_id"])
    .order("created_at", desc=False)
    .execute()
)

children_list = children_res.data or []
child_names = [child["name"] for child in children_list]

# プルダウン
selected_child = st.sidebar.selectbox(
    "お子さんを選択してください",
    child_names if child_names else ["登録されていません"]
)

# 新規登録ボタン
if st.sidebar.button("新しいお子さんを登録する"):
    dialog = st.dialog("お子さんの新規登録")  # ← context managerではなく変数に代入

    child_name = dialog.text_input("子供の名前")
    birth_date = dialog.date_input("誕生日")
    gender = dialog.radio("性別", ["男の子", "女の子", "選択しない"])

    if dialog.button("登録する"):
        if not child_name.strip():
            st.error("子供の名前は必須です。")
        else:
            # DBへ登録
            result = supabase.table("childmaster").insert({
                "user_id": user["user_id"],
                "name": child_name,
                "birth_date": birth_date.isoformat(),
                "gender": gender
            }).execute()

            if result.error:
                st.error(f"登録に失敗しました: {result.error.message}")
            else:
                st.success("お子さんを登録しました！")
