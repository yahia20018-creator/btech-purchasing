import glob
from datetime import datetime
import pandas as pd
import streamlit as st

# 1. إعدادات الصفحة وتنسيق الواجهة الاحترافي لـ B.TECH
st.set_page_config(
    page_title="Revenue Follow Up Department | B.TECH",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {
        background-color: #1f3bb3;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        padding: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #ff5500;
        color: white;
    }
    .css-18e3th9 {padding-top: 1rem;}
    </style>
""",
    unsafe_allow_html=True,
)

# 2. إدارة المستخدمين والصلاحيات
if "user_credentials" not in st.session_state:
  st.session_state.user_credentials = {
      "yahia": {
          "password": "1234",
          "role": "مدير النظام (Admin)",
          "email": "yahia.emam@btech.com",
      },
      "purchasing": {
          "password": "btech2026",
          "role": "موظف المتابعة (Revenue Follow Up)",
          "email": "purchasing.team@btech.com",
      },
  }


def check_login():
  if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

  if not st.session_state.logged_in:
    st.markdown(
        "<h2 style='text-align: center; color: #1f3bb3;'>🔐 B.TECH - Revenue"
        " Follow Up Department</h2>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
      with st.form("login_form"):
        username = st.text_input("اسم المستخدم أو الإيميل (Username)")
        password = st.text_input("كلمة المرور (Password)", type="password")
        submit = st.form_submit_button("تسجيل الدخول")

        if submit:
          matched_user = None
          for u, details in st.session_state.user_credentials.items():
            if u == username or details.get("email") == username:
              if details["password"] == password:
                matched_user = u
                break

          if matched_user:
            st.session_state.logged_in = True
            st.session_state.username = matched_user
            st.session_state.role = st.session_state.user_credentials[
                matched_user
            ]["role"]
            st.session_state.email = st.session_state.user_credentials[
                matched_user
            ].get("email", "yahia.emam@btech.com")
            st.rerun()
          else:
            st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
    return False
  return True


if not check_login():
  st.stop()

# --- الشريط الجانبي وشعار B.TECH ---
st.sidebar.markdown(
    f"👤 **المستخدم:** {st.session_state.username}\n\n📌"
    f" **الصلاحية:** {st.session_state.role}"
)
st.sidebar.markdown("---")

try:
  st.sidebar.image("logo.png", use_container_width=True)
except:
  st.sidebar.markdown(
      "<h2 style='text-align: center; color: #ff5500; font-weight: bold;'>B"
      " . TECH</h2>",
      unsafe_allow_html=True,
  )

st.sidebar.markdown("---")

if st.session_state.username == "yahia":
  with st.sidebar.expander("🛠️ إدارة الموظفين (لوحة الأدمن)"):
    st.markdown("### إضافة موظف جديد")
    with st.form("add_user_form"):
      new_username = st.text_input("يوزر الدخول (Username)")
      new_email = st.text_input("البريد الإلكتروني (Email)")
      new_password = st.text_input("كلمة المرور (Password)", type="password")
      add_submit = st.form_submit_button("إضافة الموظف للنظام")

      if add_submit:
        if new_username and new_email and new_password:
          st.session_state.user_credentials[new_username] = {
              "password": new_password,
              "role": "موظف المتابعة (Revenue Follow Up)",
              "email": new_email,
          }
          st.success(f"✅ تم إضافة الموظف ({new_username}) بنجاح!")
        else:
          st.error("⚠️ برجاء ملء كافة البيانات للإضافة.")

    st.markdown("---")
    st.markdown("**الموظفون الحاليون:**")
    for usr, info in st.session_state.user_credentials.items():
      st.text(f"- {usr} ({info['email']})")

  st.sidebar.markdown("---")

if st.sidebar.button("🚪 تسجيل خروج"):
  st.session_state.logged_in = False
  st.rerun()

# --- الواجهة الرئيسية ---
st.markdown(
    "<h1 style='color: #1f3bb3;'>📊 B.TECH - Revenue Follow Up Department</h1>",
    unsafe_allow_html=True,
)
st.markdown("نظام التدقيق، مراجعة الموردين، وإرسال الاعتمادات الشهرية بدقة فائقة.")
st.markdown("---")


# دالة قراءة ملف الإكسل مع مؤشر تحميل لمنع القلق
@st.cache_data
def load_data():
  excel_files = glob.glob("*.xlsx") + glob.glob("*.xls") + glob.glob("*.xlsm")
  if not excel_files:
    raise FileNotFoundError(
        "لم يتم العثور على أي ملف إكسل مرفوع في مستودع GitHub."
    )
  file_name = excel_files[0]
  df = pd.read_excel(file_name, header=0)
  df.columns = df.columns.str.strip()
  return df, file_name


with st.spinner("⏳ جاري تحميل البيانات وتجهيز النظام، برجاء الانتظار..."):
  try:
    df, detected_file = load_data()
    data_loaded = True
  except Exception as e:
    data_loaded = False
    st.warning(
        "⚠️ برجاء التأكد من رفع ملف إكسل واحد على الأقل داخل مستودع GitHub بجانب"
        f" الكود. التفاصيل: {e}"
    )

if data_loaded:
  st.success(
      f"✅ تم تحميل شيت البيانات بنجاح من الملف (`{detected_file}`) وجاهز"
      " للعمل!"
  )

  # التعرف الذكي على الأعمدة
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
  desc_col = next(
      (
          c
          for c in df.columns
          if "des" in c.lower() or "item" in c.lower() or "صنف" in c
      ),
      None,
  )

  if supplier_col:
    # --- الفلاتر الأساسية بترتيب شيك واحترافي ---
    st.markdown("### 🔍 فلاتر البحث والتدقيق")
    col_sup, col_date, col_store = st.columns(3)

    with col_sup:
      all_suppliers = sorted(df[supplier_col].dropna().unique().astype(str))
      selected_suppliers = st.multiselect(
          "🔍 اختر أو ابحث عن الموردين:",
          options=all_suppliers,
          default=[all_suppliers[0]] if all_suppliers else [],
      )

    with col_date:
      if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        valid_dates = df[date_col].dropna()
        if not valid_dates.empty:
          min_d, max_d = valid_dates.min().date(), valid_dates.max().date()
          date_range = st.date_input(
              "📅 الفترة الزمنية (من - إلى):", value=(min_d, max_d)
          )
        else:
          date_range = None
      else:
        date_range = None

    with col_store:
      if store_col:
        stores_list = ["الكل"] + sorted(
            df[store_col].dropna().unique().astype(str).tolist()
        )
        selected_store = st.selectbox("🏬 اختر الفرع / المخزن:", options=stores_list)
      else:
        selected_store = "الكل"

    if not selected_suppliers:
      st.warning("⚠️ برجاء اختيار مورد واحد على الأقل للبدء في العرض.")
    else:
      # تطبيق الفلاتر على الداتا الأساسية
      filtered_df = df[df[supplier_col].astype(str).isin(selected_suppliers)]

      if date_range and len(date_range) == 2 and date_col:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df[date_col].dt.date >= start_date)
            & (filtered_df[date_col].dt.date <= end_date)
        ]

      if selected_store != "الكل" and store_col:
        filtered_df = filtered_df[
            filtered_df[store_col].astype(str) == selected_store
        ]

      # تجهيز المتغيرات الافتراضية لعرض التفاصيل والأصناف
      final_selected_df = filtered_df.copy()

      # --- خيار عرض التفاصيل (الأصناف والكميات مع بوكسات تحديد) ---
      st.markdown("---")
      show_details = st.checkbox(
          "📋 عرض تفاصيل الأصناف (اختر المنتجات المراد مراجعتها واعتمادها)"
      )

      selected_item_rows = []
      if show_details:
        st.markdown(
            "#### 🔍 جدول الأصناف والكميات (حدد الأصناف المطلوبة للاعتماد):"
        )
        if desc_col and not filtered_df.empty:
          items_summary = (
              filtered_df.groupby(desc_col)
              .agg(
                  {
                      qty_col: "sum",
                      **({sales_col: "sum"} if sales_col else {}),
                  }
              )
              .reset_index()
          )

          for index, row in items_summary.iterrows():
            item_name = row[desc_col]
            item_qty = row[qty_col]
            item_sales = row[sales_col] if sales_col else 0

            c_box, c_name, c_qty, c_sales = st.columns([0.5, 5, 2, 2])
            with c_box:
              is_checked = st.checkbox(
                  "تحديد",
                  value=True,
                  key=f"item_chk_{index}",
                  label_visibility="collapsed",
              )
            with c_name:
              st.write(item_name)
            with c_qty:
              st.write(f"الكمية: **{item_qty:,.0f}**")
            with c_sales:
              if sales_col:
                st.write(f"المبيعات: **{item_sales:,.2f}**")

            if is_checked:
              selected_item_rows.append(item_name)

          # تحديث الداتا بناءً على الأصناف المحددة فقط
          final_selected_df = filtered_df[
              filtered_df[desc_col].astype(str).isin(selected_item_rows)
          ]
        else:
          st.dataframe(filtered_df, use_container_width=True)

      # --- عرض الإجمالي العام للقطاع (يتحدث أوتوماتيك بناءً على الأصناف المحددة) ---
      st.markdown("---")
      st.markdown(
          f"### 📌 الإجمالي العام للقطاع للموردين والأصناف المحددة:"
          f" `{', '.join(selected_suppliers)}`"
      )

      total_records = len(final_selected_df)
      total_quantity = (
          final_selected_df[qty_col].sum()
          if qty_col and not final_selected_df.empty
          else 0
      )
      total_sales_val = (
          final_selected_df[sales_col].sum()
          if sales_col and not final_selected_df.empty
          else 0
      )

      m1, m2, m3 = st.columns(3)
      m1.metric("📦 إجمالي عدد الحركات المعتمدة", total_records)
      m2.metric("📊 إجمالي الكميات المطلوبة", f"{total_quantity:,.0f}")
      if sales_col:
        m3.metric("💰 إجمالي المبيعات", f"{total_sales_val:,.2f}")

      # --- قسم إرسال البريد الإلكتروني للاعتماد أوتوماتيك ---
      st.markdown("---")
      st.markdown("### ✉️ إرسال اعتماد المراجعة عبر البريد الإلكتروني")

      sender_email = st.text_input(
          "البريد المرسل منه (Sender):",
          value=st.session_state.get("email", "yahia.emam@btech.com"),
          disabled=True,
      )

      st.markdown("**البريد المرسل إليهم (Recipients):**")
      col_m1, col_m2, col_m3 = st.columns(3)
      with col_m1:
        mail_1 = st.text_input("المرسل إليه (1):", value="manager@btech.com")
      with col_m2:
        mail_2 = st.text_input(
            "المرسل إليه (2):", value="purchasing.team@btech.com"
        )
      with col_m3:
        mail_3 = st.text_input("المرسل إليه (3 - اختياري):", value="")

      recipients_list = [m.strip() for m in [mail_1, mail_2, mail_3] if m.strip()]
      recipients_str = ", ".join(recipients_list)

      if st.button("🚀 اعتماد وإرسال تفاصيل المراجعة رسمياً"):
        if final_selected_df.empty:
          st.warning(
              "⚠️ لا توجد أصناف محددة أو بيانات مطابقة للفلاتر الحالية للإرسال."
          )
        elif not recipients_list:
          st.warning("⚠️ برجاء كتابة بريد إلكتروني واحد على الأقل للمرسل إليه.")
        else:
          st.balloons()

          # بناء محتوى البريد الإلكتروني وفتحه أوتوماتيك لإرسال الميل
          period_str = (
              f"من {date_range[0]} إلى {date_range[1]}"
              if date_range and len(date_range) == 2
              else "كل الفترات"
          )
          email_subject = (
              "B.TECH - اعتماد مراجعة مشتريات الموردين (Revenue Follow Up)"
          )
          email_body = (
              f"مرحباً,\n\nتم اعتماد مراجعة المشتريات للقطاع بالبيانات الآتية:\n"
              f"- الموردون المعتمدون: {', '.join(selected_suppliers)}\n"
              f"- الفترة الزمنية: {period_str}\n"
              f"- إجمالي الحركات المعتمدة: {len(final_selected_df)}\n"
              f"- إجمالي الكميات المعتمدة: {total_quantity:,.0f}\n"
              f"- إجمالي القيمة: {total_sales_val:,.2f}\n\n"
              f"مع تحيات قسم Revenue Follow Up - B.TECH"
          )

          import urllib.parse

          mailto_link = f"mailto:{recipients_str}?subject={urllib.parse.quote(email_subject)}&body={urllib.parse.quote(email_body)}"

          # كود جافاسكريبت لفتح عميل البريد أوتوماتيك لحظياً عند الضغط
          js_code = f"""
                <script>
                    window.location.href = "{mailto_link}";
                </script>
                """
          st.components.v1.html(js_code, height=0)
          st.success(
              f"✅ تم معالجة وإرسال الاعتماد أوتوماتيك من **{sender_email}** إلى"
              f" الإيميلات: `{recipients_str}` وتم فتح برنامج البريد الخاص بك!"
          )

  else:
    st.error("⚠️ لم يتم العثور على عمود المورد (Supplier) في ملف الإكسل المرفوع.")
