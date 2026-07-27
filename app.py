import pandas as pd
import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="نظام موافقة المشتريات الشهري", page_icon="📊", layout="wide"
)

# 2. نظام تسجيل الدخول (اليوزر والباسورد لمسؤولي المشتريات)
USER_CREDENTIALS = {
    "yahia": "1234",  # الأدمن (أنت)
    "purchasing1": "pass123",  # موظف المشتريات 1
    "purchasing2": "pass456",  # موظف المشتريات 2
}


def check_login():
  if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

  if not st.session_state.logged_in:
    st.title("🔐 تسجيل دخول نظام المشتريات")
    username = st.text_input("اسم المستخدم (Username)")
    password = st.text_input("كلمة المرور (Password)", type="password")

    if st.button("دخول"):
      if (
          username in USER_CREDENTIALS
          and USER_CREDENTIALS[username] == password
      ):
        st.session_state.logged_in = True
        st.session_state.username = username
        st.rerun()
      else:
        st.error("اسم المستخدم أو كلمة المرور خطأ")
    return False
  return True


if not check_login():
  st.stop()

# --- الشاشة الرئيسية للنظام ---
st.title("📋 نظام مراجعة وموافقة المشتريات الشهرية")
st.write(f"أهلاً بك، **{st.session_state.username}**")

# زرار تسجيل خروج
if st.sidebar.button("تسجيل خروج"):
  st.session_state.logged_in = False
  st.rerun()

# 3. مكان رفع شيت المبيعات الشهري
st.sidebar.header("📁 إدارة الملفات")
uploaded_file = st.sidebar.file_uploader(
    "ارفع شيت المبيعات الشهري (Excel)", type=["xlsx", "xls"]
)

if uploaded_file is not None:
  # قراءة الشيت
  df = pd.read_excel(uploaded_file)
  st.success("تم اعتماد شيت المبيعات الشهري بنجاح! 🚀")

  # البحث عن عمود المورد (Supplier)
  supplier_col = next((c for c in df.columns if "supplie" in c.lower()), None)

  if supplier_col:
    # قائمة الموردين
    suppliers = df[supplier_col].dropna().unique()
    selected_supplier = st.selectbox(
        "اختر المورد للمراجعة:", options=suppliers
    )

    # فلترة الأصناف حسب المورد المختار
    filtered_df = df[df[supplier_col] == selected_supplier]

    st.subheader(
        f"الأصناف وحركات المبيعات الخاصة بالمورد: {selected_supplier}"
    )
    st.dataframe(filtered_df, use_container_width=True)

    # إجمالي الكميات لو عمود QTY موجود
    qty_col = next((c for c in df.columns if "qty" in c.lower()), None)
    if qty_col:
      total_qty = filtered_df[qty_col].sum()
      st.info(f"📦 إجمالي الكميات المطلوبة للمورد ده: **{total_qty}**")

    # زرار الموافقة وإرسال الميل
    if st.button("إرسال الموافقة للمورد ✉️"):
      # هنا هنربط إرسال الإيميل الفعلي لاحقاً
      st.success(
          f"تم إرسال الموافقة الخاصة بالصنف/الكميات للمورد ({selected_supplier})"
          " بنجاح وتم توثيقها!"
      )
  else:
    st.error("لم يتم العثور على عمود المورد (Supplier) في شيت الإكسل المرفوع.")
else:
  st.warning(
      "⚠️ برجاء من المسؤول رفع شيت المبيعات الشهري من القائمة الجانبية للبدء."
  )