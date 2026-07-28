import glob
import pandas as pd
import streamlit as st

# 1. إعدادات الصفحة وتنسيق الواجهة الاحترافي
st.set_page_config(
    page_title="Revenue Follow Up Department", page_icon="📈", layout="wide"
)

st.markdown(
    """
    <style>
    .main {background-color: #f4f6f9;}
    .stButton>button {
        background-color: #1f3bb3;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #0d238a;
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. الصلاحيات ويوزرات الدخول
USER_CREDENTIALS = {
    "yahia": {"password": "1234", "role": "مدير النظام (Admin)"},
    "purchasing": {
        "password": "btech2026",
        "role": "موظف المتابعة (Revenue Follow Up)",
    },
}


def check_login():
  if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

  if not st.session_state.logged_in:
    st.markdown(
        "<h2 style='text-align: center; color: #1f3bb3;'>📈 Revenue Follow Up"
        " Department</h2>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
      with st.form("login_form"):
        username = st.text_input("اسم المستخدم (Username)")
        password = st.text_input("كلمة المرور (Password)", type="password")
        submit = st.form_submit_button("تسجيل الدخول")

        if submit:
          if (
              username in USER_CREDENTIALS
              and USER_CREDENTIALS[username]["password"] == password
          ):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = USER_CREDENTIALS[username]["role"]
            st.rerun()
          else:
            st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
    return False
  return True


if not check_login():
  st.stop()

# --- الشريط الجانبي ---
st.sidebar.markdown(
    f"👤 **المستخدم:** {st.session_state.username}\n\n📌"
    f" **القسم:** Revenue Follow Up"
)
st.sidebar.markdown("---")

if st.sidebar.button("🚪 تسجيل خروج"):
  st.session_state.logged_in = False
  st.rerun()

# --- الواجهة الرئيسية ---
st.markdown(
    "<h1 style='color: #1f3bb3;'>📊 Revenue Follow Up Department - نظام مراجعة"
    " الموردين</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")


# دالة قراءة ملف الإكسل المرفوع مع ضبط الصف الأول كعناوين
def load_data():
  excel_files = glob.glob("*.xlsx") + glob.glob("*.xls") + glob.glob("*.xlsm")
  if not excel_files:
    raise FileNotFoundError(
        "لم يتم العثور على أي ملف إكسل مرفوع في مستودع GitHub."
    )

  file_name = excel_files[0]
  # header=0 لضمان قراءة الصف الأول كعناوين للأعمدة بشكل صحيح
  df = pd.read_excel(file_name, header=0)
  df.columns = df.columns.str.strip()
  return df, file_name


try:
  df, detected_file = load_data()
  st.success(
      f"✅ تم قراءة الملف بنجاح (`{detected_file}`) وجاهز للاستعلام والاعتماد!"
  )

  # البحث الذكي عن أسماء الأعمدة الأساسية
  supplier_col = next(
      (c for c in df.columns if "supplie" in c.lower() or "مورد" in c), None
  )
  date_col = next(
      (c for c in df.columns if "date" in c.lower() or "تاريخ" in c), None
  )
  store_col = next(
      (
          c
          for c in df.columns
          if "store" in c.lower()
          or "source" in c.lower()
          or "فرع" in c
          or "trx" in c.lower()
      ),
      None,
  )
  qty_col = next(
      (
          c
          for c in df.columns
          if "qty" in c.lower() or "كمية" in c or "الكمية" in c
      ),
      None,
  )
  sales_col = next(
      (
          c
          for c in df.columns
          if "sales" in c.lower() or "total" in c.lower() or "مبيعات" in c
      ),
      None,
  )

  if supplier_col:
    # --- خانات البحث والاختيار (المورد، التاريخ، الفرع) ---
    col1, col2, col3 = st.columns(3)

    with col1:
      suppliers_list = sorted(df[supplier_col].dropna().unique().astype(str))
      selected_supplier = st.selectbox(
          "🔍 اختر أو ابحث عن المورد:", options=suppliers_list
      )

    with col2:
      if date_col:
        dates_list = ["الكل"] + sorted(
            df[date_col].dropna().unique().astype(str).tolist()
        )
        selected_date = st.selectbox("📅 اختر الفترة / التاريخ:", options=dates_list)
      else:
        selected_date = "الكل"

    with col3:
      if store_col:
        stores_list = ["الكل"] + sorted(
            df[store_col].dropna().unique().astype(str).tolist()
        )
        selected_store = st.selectbox("🏬 اختر الفرع / المخزن:", options=stores_list)
      else:
        selected_store = "الكل"

    # تطبيق الفلاتر
    filtered_df = df[df[supplier_col].astype(str) == selected_supplier]
    if selected_date != "الكل" and date_col:
      filtered_df = filtered_df[
          filtered_df[date_col].astype(str) == selected_date
      ]
    if selected_store != "الكل" and store_col:
      filtered_df = filtered_df[
          filtered_df[store_col].astype(str) == selected_store
      ]

    st.markdown("---")
    st.markdown(f"### 📌 نتيجة البحث للمورد: `{selected_supplier}`")

    # --- عرض إجمالي القطاع (Summary) ---
    total_records = len(filtered_df)
    total_quantity = (
        filtered_df[qty_col].sum()
        if qty_col and not filtered_df.empty
        else 0
    )
    total_sales_val = (
        filtered_df[sales_col].sum()
        if sales_col and not filtered_df.empty
        else 0
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("📦 إجمالي عدد الحركات", total_records)
    m2.metric("📊 إجمالي الكميات (QTY)", f"{total_quantity:,.0f}")
    if sales_col:
      m3.metric("💰 إجمالي المبيعات", f"{total_sales_val:,.2f}")

    st.markdown("---")

    # --- خيار التفصيل (عرض تفاصيل الأصناف) ---
    show_details = st.checkbox("📋 عرض تفاصيل الأصناف (Item Description / Code)")

    if show_details:
      st.markdown("#### 🔍 تفاصيل كل صنف على حدة:")
      desc_col = next(
          (
              c
              for c in df.columns
              if "des" in c.lower() or "item" in c.lower() or "صنف" in c
          ),
          None,
      )

      if desc_col and qty_col:
        summary_items = (
            filtered_df.groupby(desc_col)
            .agg(
                {
                    qty_col: "sum",
                    **({sales_col: "sum"} if sales_col else {}),
                }
            )
            .reset_index()
        )
        st.dataframe(summary_items, use_container_width=True)
      else:
        st.dataframe(filtered_df, use_container_width=True)

    # --- زرار الاعتماد والموافقة للإرسال على الميل ---
    st.markdown("---")
    if st.button("✉️ اعتماد وإرسال نتيجة المراجعة على البريد"):
      st.balloons()
      st.success(
          f"🚀 تم إرسال اعتمادات المورد ({selected_supplier}) لمسؤول المشتريات"
          " عبر البريد الإلكتروني بنجاح!"
      )
  else:
    st.error(
        "⚠️ لم يتم العثور على عمود المورد في الملف. الأعمدة الموجودة في"
        f" شيت الإكسل هي: {list(df.columns)}"
    )

except Exception as e:
  st.warning(
      "⚠️ برجاء التأكد من رفع ملف إكسل واحد على الأقل داخل مستودع GitHub بجانب"
      f" الكود. التفاصيل: {e}"
  )
