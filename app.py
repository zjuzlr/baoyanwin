
import streamlit as st
from auth import login_user, logout_user, register_user, is_logged_in, get_current_user
from database import init_db, insert_record, get_user_records
from utils import save_uploaded_images, export_excel
import os
from datetime import datetime

st.set_page_config(page_title="保研记录系统", layout="wide")
init_db()

# 登录状态管理
if "user" not in st.session_state:
    st.session_state.user = None

# 登录或注册页面
if not is_logged_in():
    menu = st.sidebar.radio("菜单", ["登录", "注册"])
    if menu == "登录":
        login_user()
    elif menu == "注册":
        register_user()
    st.stop()

# 已登录页面
user = get_current_user()
st.sidebar.success(f"已登录：{user['email']}")
if st.sidebar.button("退出登录"):
    logout_user()
    st.rerun()

st.title("🚀 保研坞 · 小卫星计划")

# 填写记录
with st.form("record_form"):
    school = st.text_input("🎓 保研院校名称")
    interview_date = st.date_input("🗓️ 面试时间")
    process = st.text_area("🧪 考核流程")
    lesson = st.text_area("📌 经验教训")

    images = st.file_uploader("📷 上传图片（可多选）", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    descriptions = []
    for i in range(len(images)):
        descriptions.append(st.text_input(f"备注 - 图片{i+1}"))

    submitted = st.form_submit_button("✅ 提交记录")

if submitted:
    record_id = insert_record(user['id'], school, str(interview_date), process, lesson)
    save_uploaded_images(record_id, images, descriptions)
    st.success("记录已保存 ✅")

st.markdown("---")
st.subheader("📚 我的记录")
if st.button("📥 导出为 Excel"):
    export_excel(user['id'])

records = get_user_records(user['id'])
for r in records:
    with st.expander(f"📌 {r['school_name']} - {r['interview_date']}"):
        st.markdown(f"**考核流程：** {r['assessment_process']}")
        st.markdown(f"**经验教训：** {r['lessons_learned']}")
        image_dir = f"uploads/{r['id']}"
        if os.path.exists(image_dir):
            for file in os.listdir(image_dir):
                filepath = f"{image_dir}/{file}"
                if file.endswith(".txt"):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        st.caption(f"备注：{f.read()}")
                else:
                    st.image(filepath, width=300)
