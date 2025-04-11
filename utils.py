
import os
from datetime import datetime
import pandas as pd
import streamlit as st

def save_uploaded_images(record_id, files, descriptions):
    folder = f"uploads/{record_id}"
    os.makedirs(folder, exist_ok=True)
    for file, desc in zip(files, descriptions):
        filepath = os.path.join(folder, file.name)
        with open(filepath, "wb") as f:
            f.write(file.getbuffer())
        # 保存备注为txt
        with open(os.path.join(folder, f"{file.name}.txt"), "w", encoding="utf-8") as f:
            f.write(desc or "")

def export_excel(user_id):
    from database import get_user_records
    records = get_user_records(user_id)
    df = pd.DataFrame(records)
    if df.empty:
        st.warning("暂无记录")
        return
    filename = f"保研记录_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    with open(filename, "rb") as f:
        st.download_button("📥 下载 Excel", f, file_name=filename)
