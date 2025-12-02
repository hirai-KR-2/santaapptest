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

# --------------------------
# サイドバー
# --------------------------
st.sidebar.header("お子さんの選択")

# session_state で「子どもリスト更新フラグ」を管理
if "child_refresh" not in st.session_state:
    st.session_state.child_refresh = True

# 子どもリストを取得する関数
def load_children():
    res = (
        supabase.table("childmaster")
        .select("*")
        .eq("user_id", user["user_id"])
        .order("created_at", desc=False)
        .execute()
    )
    return res.data or []

# 子どもリストを更新
if st.session_state.child_refresh:
    st.session_state.children_list = load_children()
    st.session_state.child_refresh = False

child_names = [child["name"] for child in st.session_state.children_list]

# プルダウン
selected_child = st.sidebar.selectbox(
    "お子さんを選択してください",
    child_names if child_names else ["登録されていません"]
)

# --------------------------
# 新規登録ボタン
# --------------------------
if st.sidebar.button("新しいお子さんを登録する"):
    st.dialog("お子さんの新規登録")  # ポップアップ開始

    # フォーム用 session_state
    if "new_child_name" not in st.session_state:
        st.session_state.new_child_name = ""
        st.session_state.new_child_birth = date.today()
        st.session_state.new_child_gender = "選択しない"

    # フォーム
    st.session_state.new_child_name = st.text_input(
        "子供の名前", st.session_state.new_child_name
    )
    st.session_state.new_child_birth = st.date_input(
        "誕生日", st.session_state.new_child_birth
    )
    st.session_state.new_child_gender = st.radio(
        "性別", ["男の子", "女の子", "選択しない"], index=["男の子","女の子","選択しない"].index(st.session_state.new_child_gender)
    )

    if st.button("登録する"):
        if not st.session_state.new_child_name.strip():
            st.error("子供の名前は必須です。")
        else:
            # DB登録
            result = supabase.table("childmaster").insert({
                "user_id": user["user_id"],
                "name": st.session_state.new_child_name,
                "birth_date": st.session_state.new_child_birth.isoformat(),
                "gender": st.session_state.new_child_gender
            }).execute()

            if result.error:
                st.error(f"登録に失敗しました: {result.error.message}")
            else:
                st.success("お子さんを登録しました！")

                # フォームをリセット
                st.session_state.new_child_name = ""
                st.session_state.new_child_birth = date.today()
                st.session_state.new_child_gender = "選択しない"

                # 子どもリストを再読み込み
                st.session_state.child_refresh = True
                st.experimental_rerun()  # ページをリロードしてプルダウンを即更新
