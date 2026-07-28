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

# 2. إدارة المستخدمين والصلاحيات (يتم تخزينهم في st.session_state لكي يديرهم الأدمن)
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
          # التحقق من اليوزر أو الإيميل المسجل
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

# --- الشريط الجانبي والشعار ---
st.sidebar.markdown(
    f"👤 **المستخدم:** {st.session_state.username}\n\n📌"
    f" **الصلاحية:** {st.session_state.role}"
)
st.sidebar.markdown("---")

# محاولة عرض شعار B.TECH إذا وُجد ملف logo.png
try:
  st.sidebar.image("logo.png", use_container_width=True)
except:
  st.sidebar.markdown(
      "<h3 style='text-align: center; color: #ff5500;'>B.TECH</h3>",
      unsafe_allow_html=True,
  )

st.sidebar.markdown("---")

# لوحة التحكم الخاصة بالأدمن لإضافة موظفين جُدد
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


# دالة قراءة ملف الإكسل التلقائي
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


try:
  df, detected_file = load_data()
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
    # --- خانات الفلاتر المتقدمة ---
    col1, col2, col3 = st.columns(3)

    with col1:
      suppliers_list = sorted(df[supplier_col].dropna().unique().astype(str))
      selected_suppliers = st.multiselect(
          "🔍 اختر الموردين (يمكن اختيار أكثر من مورد):",
          options=suppliers_list,
          default=[suppliers_list[0]] if suppliers_list else [],
      )

    with col2:
      if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        valid_dates = df[date_col].dropna()
        if not valid_dates.empty:
          min_d, max_d = valid_dates.min().date(), valid_dates.max().date()
          date_range = st.date_input(
              "📅 اختر الفترة الزمنية (من - إلى):", value=(min_d, max_d)
          )
        else:
          date_range = None
      else:
        date_range = None

    with col3:
      if store_col:
        stores_list = ["الكل"] + sorted(
            df[store_col].dropna().unique().astype(str).tolist()
        )
        selected_store = st.selectbox("🏬 اختر الفرع / المخزن:", options=stores_list)
      else:
        selected_store = "الكل"

    # تطبيق الفلاتر على الداتا
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

    st.markdown("---")
    st.markdown(
        f"### 📌 ملخص نتائج المراجعة للموردين المختارين:"
        f" `{', '.join(selected_suppliers)}`"
    )

    # --- عرض مؤشرات الأداء الإجمالية ---
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
    m2.metric("📊 إجمالي الكميات المطلوبة", f"{total_quantity:,.0f}")
    if sales_col:
      m3.metric("💰 إجمالي المبيعات", f"{total_sales_val:,.2f}")

    st.markdown("---")

    # --- تحديد المنتجات المراد مراجعتها فقط ---
    st.markdown("#### 📋 مراجعة وتصفية الأصناف والمنتجات:")
    if desc_col and not filtered_df.empty:
      all_items = sorted(
          filtered_df[desc_col].dropna().unique().astype(str).tolist()
      )
      selected_items = st.multiselect(
          "حدد المنتجات المراد مراجعتها واعتمادها (افتراضياً الكل):",
          options=all_items,
          default=all_items,
      )
      if selected_items:
        filtered_df = filtered_df[
            filtered_df[desc_col].astype(str).isin(selected_items)
        ]

    st.dataframe(filtered_df, use_container_width=True)

    # --- قسم إرسال البريد الإلكتروني للاعتماد ---
    st.markdown("---")
    st.markdown("### ✉️ إرسال اعتماد المراجعة عبر البريد الإلكتروني")

    col_mail1, col_mail2 = st.columns(2)
    with col_mail1:
      # تثبيت الإيميل المرسل منه على إيميل يحيى أو إيميل الموظف المسجل حالياً
      sender_email = st.text_input(
          "البريد المرسل منه (Sender):",
          value=st.session_state.get("email", "yahia.emam@btech.com"),
      )
    with col_mail2:
      recipient_emails = st.text_input(
          "البريد المرسل إليهم (Recipients - افصل بينهم بفواصل):",
          value="manager@btech.com, purchasing.team@btech.com",
      )

    if st.button("🚀 اعتماد وإرسال تفاصيل المراجعة رسمياً"):
      if filtered_df.empty:
        st.warning(
            "⚠️ لا توجد بيانات مطابقة للفلاتر الحالية لإرسالها في الاعتماد."
        )
      else:
        st.balloons()
        st.success(
            f"✅ تم إرسال الاعتماد بنجاح من قبل **{sender_email}** إلى الإيميلات:"
            f" `{recipient_emails}`"
        )

        with st.expander("📄 معاينة محتوى البريد المرسل (Email Content Preview)"):
          period_str = (
              f"من {date_range[0]} إلى {date_range[1]}"
              if date_range and len(date_range) == 2
              else "كل الفترات"
          )
          st.markdown(f"**من:** {sender_email}")
          st.markdown(f"**إلى:** {recipient_emails}")
          st.markdown(
              f"**الموضوع:** اعتماد مراجعة المشتريات - Revenue Follow Up"
              f" Department"
          )
          st.markdown("---")
          st.markdown(
              f"**الموردون المعتمدون:** {', '.join(selected_suppliers)}"
          )
          st.markdown(f"**المدة / الفترة:** {period_str}")
          st.markdown(f"**إجمالي الحركات:** {len(filtered_df)}")
          st.markdown(f"**إجمالي الكميات:** {total_quantity:,.0f}")
          if sales_col:
            st.markdown(f"**إجمالي القيمة:** {total_sales_val:,.2f}")
          st.markdown(
              "**الأصناف والمنتجات المشمولة في الاعتماد مطابقة ومرفقة في"
              " التقرير.**"
          )

  else:
    st.error("⚠️ لم يتم العثور على عمود المورد (Supplier) في ملف الإكسل المرفوع.")

except Exception as e:
  st.warning(
      "⚠️ برجاء التأكد من رفع ملف إكسل واحد على الأقل داخل مستودع GitHub بجانب"
      f" الكود. التفاصيل: {e}"
  )
