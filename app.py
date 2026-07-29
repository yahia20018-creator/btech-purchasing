from datetime import datetime
import glob
import urllib.parse
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
    /* خلفية عامة احترافية */
    .main {background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
    
    /* تصميم الأزرار */
    .stButton>button {
        background: linear-gradient(135deg, #1f3bb3 0%, #0d238a 100%);
        color: white;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
        padding: 0.6rem;
        border: none;
        box-shadow: 0 4px 6px rgba(31, 59, 179, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff5500 0%, #e04800 100%);
        box-shadow: 0 6px 12px rgba(255, 85, 0, 0.3);
        color: white;
    }

    /* شعار B.TECH احترافي في القائمة الجانبية */
    .btech-logo {
        text-align: center;
        background: linear-gradient(135deg, #1f3bb3 0%, #0d238a 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        font-size: 26px;
        font-weight: bold;
        letter-spacing: 3px;
        margin-bottom: 20px;
        box-shadow: 0px 6px 15px rgba(31,59,179,0.3);
        border-bottom: 4px solid #ff5500;
    }

    /* بطاقة الإجماليات المتحركة */
    .side-metric-box {
        background-color: #ffffff;
        padding: 22px;
        border-radius: 15px;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.06);
        border-left: 6px solid #ff5500;
        margin-bottom: 20px;
        text-align: center;
        border-top: 1px solid #eaeaea;
        border-bottom: 1px solid #eaeaea;
        border-right: 1px solid #eaeaea;
    }

    /* كروت الأقسام والتدقيق */
    .section-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 20px;
        border: 1px solid #eef0f4;
    }

    /* تكبير وتنسيق جملة عرض الأصناف */
    .details-checkbox label p {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #1f3bb3 !important;
    }
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
          "email": "yahia20018@gmail.com",
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
            ].get("email", "yahia20018@gmail.com")
            st.rerun()
          else:
            st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
    return False
  return True


if not check_login():
  st.stop()

# --- الشريط الجانبي وشعار B.TECH الفخم ---
st.sidebar.markdown(
    f"👤 **المستخدم:** {st.session_state.username}\n\n📌"
    f" **الصلاحية:** {st.session_state.role}"
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    '<div class="btech-logo">B . TECH <br><span'
    ' style="font-size:13px; font-weight:normal; letter-spacing:1px; color:#ffccaa;">Revenue'
    ' Control</span></div>',
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

# --- الواجهة الرئيسية الاحترافية ---
st.markdown(
    "<h1 style='color: #1f3bb3; font-weight: 800;'>📊 B.TECH - Revenue Follow"
    " Up Department</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color: #666; font-size: 16px;'>نظام التدقيق المالي، مراجعة"
    " الموردين، وإرسال الاعتمادات الشهرية بدقة فائقة.</p>",
    unsafe_allow_html=True,
)
st.markdown("---")


# دالة قراءة ملف الإكسل
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
    # --- بطاقة الفلاتر الأساسية ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

    if not selected_suppliers:
      st.warning("⚠️ برجاء اختيار مورد واحد على الأقل للبدء في العرض.")
    else:
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

      final_selected_df = filtered_df.copy()

      # --- خيار عرض وتحديد تفاصيل الأصناف مع تنسيق فخم ---
      st.markdown('<div class="section-card details-checkbox">', unsafe_allow_html=True)
      show_details = st.checkbox(
          "📋 عرض تفاصيل الأصناف (اختر المنتجات المراد مراجعتها واعتمادها)"
      )
      st.markdown("</div>", unsafe_allow_html=True)

      selected_item_rows = []

      if show_details:
        st.markdown(
            f"### 📦 مراجعة أصناف الموردين: `{', '.join(selected_suppliers)}`"
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

          # تقسيم الشاشة: جدول الأصناف (يسار) ومربعات الإجماليات المتحركة بجوارها (يمين)
          col_items_list, col_live_metrics = st.columns([2.3, 1])

          with col_items_list:
            st.markdown(
                "<p style='color:#5500; font-weight:bold; font-size:16px;'>حدد"
                " الأصناف المطلوبة للاعتماد:</p>",
                unsafe_allow_html=True,
            )
            for index, row in items_summary.iterrows():
              item_name = row[desc_col]
              item_qty = row[qty_col]
              item_sales = row[sales_col] if sales_col else 0

              c_box, c_name, c_qty = st.columns([0.4, 4.6, 2])
              with c_box:
                is_checked = st.checkbox(
                    "تحديد",
                    value=True,
                    key=f"item_chk_{index}",
                    label_visibility="collapsed",
                )
              with c_name:
                st.markdown(
                    f"<b style='font-size:15px; color:#222;'>{item_name}</b>",
                    unsafe_allow_html=True,
                )
              with c_qty:
                st.markdown(
                    f"<b style='font-size:15px; color:#1f3bb3;'>الكمية:"
                    f" {item_qty:,.0f}</b>",
                    unsafe_allow_html=True,
                )

              if is_checked:
                selected_item_rows.append(item_name)

          # تحديث الداتا بناءً على الأصناف المحددة
          final_selected_df = filtered_df[
              filtered_df[desc_col].astype(str).isin(selected_item_rows)
          ]

          # --- الإجماليات المتحركة بجوار الأصناف مباشرة ---
          with col_live_metrics:
            st.markdown(
                "#### 📊 الإجمالي المعتمد المباشر", unsafe_allow_html=True
            )
            st.markdown('<div class="side-metric-box">', unsafe_allow_html=True)
            st.metric(
                "📦 إجمالي الحركات", f"{len(final_selected_df):,}"
            )
            st.markdown("---")
            st.metric(
                "📊 إجمالي الكميات",
                f"{final_selected_df[qty_col].sum() if qty_col and not final_selected_df.empty else 0:,.0f}",
            )
            if sales_col:
              st.markdown("---")
              st.metric(
                  "💰 إجمالي المبيعات",
                  f"{final_selected_df[sales_col].sum() if not final_selected_df.empty else 0:,.2f}",
              )
            st.markdown("</div>", unsafe_allow_html=True)

        else:
          st.dataframe(filtered_df, use_container_width=True)
      else:
        # لو مش مفعل التفاصيل، نعرض كروت الإجماليات بشكل فخم في الأعلى
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(
            f"### 📌 الإجمالي العام للقطاع للموردين والمحدد: `"
            f"{', '.join(selected_suppliers)}`"
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
        m2.metric("📊 إجمالي الكميات المعتمدة", f"{total_quantity:,.0f}")
        if sales_col:
          m3.metric("💰 إجمالي المبيعات", f"{total_sales_val:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

      # --- قسم إرسال البريد الإلكتروني عبر Gmail ---
      st.markdown('<div class="section-card">', unsafe_allow_html=True)
      st.markdown("### ✉️ إرسال اعتماد المراجعة عبر البريد الإلكتروني")

      sender_email = st.text_input(
          "البريد المرسل منه (Sender):", value="yahia20018@gmail.com"
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
      recipients_str = ",".join(recipients_list)

      if st.button("🚀 اعتماد وإرسال تفاصيل المراجعة رسمياً عبر Gmail"):
        if final_selected_df.empty:
          st.warning(
              "⚠️ لا توجد أصناف محددة أو بيانات مطابقة للفلاتر الحالية للإرسال."
          )
        elif not recipients_list:
          st.warning("⚠️ برجاء كتابة بريد إلكتروني واحد على الأقل للمرسل إليه.")
        else:
          st.balloons()

          period_str = (
              f"من {date_range[0]} إلى {date_range[1]}"
              if date_range and len(date_range) == 2
              else "كل الفترات"
          )
          total_qty_val = (
              final_selected_df[qty_col].sum()
              if qty_col and not final_selected_df.empty
              else 0
          )
          total_val = (
              final_selected_df[sales_col].sum()
              if sales_col and not final_selected_df.empty
              else 0
          )

          email_subject = urllib.parse.quote(
              "B.TECH - اعتماد مراجعة مشتريات الموردين (Revenue Follow Up)"
          )
          email_body = urllib.parse.quote(
              f"مرحباً,\n\nتم اعتماد مراجعة المشتريات للقطاع بالبيانات الآتية:\n"
              f"- مرسل من حساب: {sender_email}\n"
              f"- الموردون المعتمدون: {', '.join(selected_suppliers)}\n"
              f"- الفترة الزمنية: {period_str}\n"
              f"- إجمالي الحركات المعتمدة: {len(final_selected_df)}\n"
              f"- إجمالي الكميات المعتمدة: {total_qty_val:,.0f}\n"
              f"- إجمالي القيمة: {total_val:,.2f}\n\n"
              f"مع تحيات قسم Revenue Follow Up - B.TECH"
          )

          gmail_link = f"https://mail.google.com/mail/?view=cm&fs=1&to={recipients_str}&su={email_subject}&body={email_body}"

          st.markdown(
              f'<a href="{gmail_link}" target="_blank"><button'
              ' style="background: linear-gradient(135deg, #ff5500 0%,'
              ' #e04800 100%); color:white; padding:14px 24px; border:none;'
              ' border-radius:10px; font-weight:bold; font-size:17px;'
              ' cursor:pointer; width:100%; box-shadow: 0 4px 10px rgba(255,85,0,0.3);">📧'
              ' اضغط هنا لفتح نافذة Gmail وإرسال الاعتماد فوراً</button></a>',
              unsafe_allow_html=True,
          )

          st.success(
              f"✅ تم تجهيز رسالة الاعتماد بنجاح من حسابك ({sender_email}) إلى"
              f" العناوين: `{recipients_str}`. اضغط على الزر البرتقالي أعلاه لفتح"
              " Gmail وإرسالها فوراً!"
          )
      st.markdown("</div>", unsafe_allow_html=True)

  else:
    st.error("⚠️ لم يتم العثور على عمود المورد (Supplier) في ملف الإكسل المرفوع.")
