
import streamlit as st
import sqlite3
import hashlib

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def is_logged_in():
    return st.session_state.get("user") is not None

def get_current_user():
    return st.session_state.get("user")

def login_user():
    st.subheader("🔐 登录")
    email = st.text_input("邮箱")
    password = st.text_input("密码", type="password")
    if st.button("登录"):
        conn = sqlite3.connect("records.db")
        c = conn.cursor()
        c.execute("SELECT id, email, password_hash FROM users WHERE email=?", (email,))
        row = c.fetchone()
        conn.close()
        if row and hash_password(password) == row[2]:
            st.session_state.user = {"id": row[0], "email": row[1]}
            st.success("登录成功")
            st.rerun()
        else:
            st.error("邮箱或密码错误")

def register_user():
    st.subheader("📝 注册账号")
    email = st.text_input("邮箱")
    password = st.text_input("密码", type="password")
    if st.button("注册"):
        if len(password) < 6:
            st.warning("密码至少6位")
            return
        conn = sqlite3.connect("records.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, hash_password(password)))
            conn.commit()
            st.success("注册成功，请登录")
        except sqlite3.IntegrityError:
            st.error("邮箱已被注册")
        conn.close()

def logout_user():
    st.session_state.user = None
