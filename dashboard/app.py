"""
Rayan Stores - Ultimate Edition
Theme: Premium Black & Red
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import time
import io
from datetime import datetime
from fpdf import FPDF

# =====================
# LANGUAGE DICTIONARY
# =====================
LANG = {
    "English": {
        "store": "Rayan Mart", "wishlist": "Wishlist", "orders": "My Orders",
        "ai": "Rayan AI", "logout": "Logout", "cart": "Cart",
        "pay": "Confirm & Pay", "close_receipt": "Close Receipt",
        "download_receipt": "Download Receipt (.txt)",
        "download_pdf": "Download Receipt (.pdf)",
        "receipt_title": "RAYAN STORES - OFFICIAL RECEIPT",
        "order_id": "Order ID", "date": "Date & Time", "customer": "Customer",
        "items": "Items", "payment": "Payment Mode", "status": "Status",
        "total": "Total Paid", "coins": "SuperCoins Credited",
        "thank_you": "Thank you for shopping at Rayan Stores!",
        "category": "Textile Category", "search": "Search Fabrics...",
        "add": "Add", "save": "Save", "send": "Send",
        "coupon": "Coupon Code", "subtotal": "Subtotal", "payable": "Total Payable",
        "hello": "Hello", "coins_label": "Coins", "cart_label": "Cart",
        "free_del": "Free Delivery", "stock": "Stock",
        "nav_store": "Navigate", "admin_login": "Login as Admin",
        "send_otp": "Send OTP", "login_btn": "Login & Shop Now",
        "guest": "Continue as Guest", "otp_hint": "OTP sent! Use: 1234",
        "wrong_otp": "Wrong OTP. Use 1234.", "wrong_cred": "Wrong credentials. Try: admin / admin123",
        "hero_h1": "FESTIVE RAYAN SALE", "hero_p": "Pure Silk & Premium Cotton | Handpicked Collections",
        "cat_all": "All Collections", "cat_elec": "Silk Sarees", "cat_fash": "Cotton Wear",
        "cat_home": "Ethnic Wear", "cat_beau": "Suits & Materials", "cat_sport": "Home Textiles",
        "feedback": "Feedback", "rating": "Rate Experience", "comments": "Suggestions & Comments",
        "submit_fb": "Submit Feedback", "fb_thank_you": "Thank you for your valuable feedback!",
        "fb_summary": "Customer Feedback Analysis"
    },
    "Tamil": {
        "store": "ரயான் ஸ்டோர்ஸ்", "wishlist": "விருப்பப்பட்டியல்", "orders": "என் ஆர்டர்கள்",
        "ai": "ரயான் AI", "logout": "வெளியேறு", "cart": "கார்ட்",
        "pay": "உறுதிப்படுத்து & செலுத்து", "close_receipt": "ரசீதை மூடு",
        "download_receipt": "ரசீதை பதிவிறக்கு (.txt)",
        "download_pdf": "ரசீதை பதிவிறக்கு (.pdf)",
        "receipt_title": "ரயான் ஸ்டோர்ஸ் - உத்தியோகபூர்வ ரசீது",
        "order_id": "ஆர்டர் எண்", "date": "தேதி & நேரம்", "customer": "வாடிக்கையாளர்",
        "items": "பொருட்கள்", "payment": "பணம் செலுத்தும் முறை", "status": "நிலை",
        "total": "மொத்த கட்டணம்", "coins": "சூப்பர்காயின்கள் வழங்கப்பட்டன",
        "thank_you": "ரயான் ஸ்டோர்ஸில் வாங்கியதற்கு நன்றி!",
        "category": "வகைகள்", "search": "தேடு...",
        "add": "சேர்", "save": "சேமி", "send": "அனுப்பு",
        "coupon": "கூப்பன் குறியீடு", "subtotal": "கூட்டுத்தொகை", "payable": "செலுத்த வேண்டிய தொகை",
        "hello": "வணக்கம்", "coins_label": "காயின்கள்", "cart_label": "கார்ட்",
        "free_del": "இலவச டெலிவரி", "stock": "கையிருப்பு",
        "nav_store": "வழிசெல்", "admin_login": "நிர்வாகியாக உள்நுழை",
        "send_otp": "OTP அனுப்பு", "login_btn": "உள்நுழை & ஷாப் செய்",
        "guest": "விருந்தினராக தொடர்", "otp_hint": "OTP அனுப்பப்பட்டது! பயன்படுத்தவும்: 1234",
        "wrong_otp": "தவறான OTP. 1234 பயன்படுத்தவும்.", "wrong_cred": "தவறான நற்சான்றிதழ்கள். admin / admin123 முயற்சிக்கவும்.",
        "hero_h1": "பண்டிகை ரயான் விற்பனை", "hero_p": "தூய பட்டு மற்றும் பருத்தி ஆடைகள்",
        "cat_all": "அனைத்து தொகுப்புகள்", "cat_elec": "பட்டு சேலைகள்", "cat_fash": "பருத்தி ஆடைகள்",
        "cat_home": "பாரம்பரிய ஆடைகள்", "cat_beau": "சூட்கள்", "cat_sport": "வீட்டு ஜவுளிகள்",
        "feedback": "கருத்து", "rating": "அனுபவத்தை மதிப்பிடுங்கள்", "comments": "பரிந்துரைகள்",
        "submit_fb": "சமர்ப்பி", "fb_thank_you": "நன்றி!",
        "fb_summary": "வாடிக்கையாளர் கருத்து பகுப்பாய்வு"
    }
}

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Rayan Stores",
    layout="wide",
    page_icon="🛍️",
    initial_sidebar_state="expanded"
)

# =====================
# PREMIUM BLACK & RED THEME CSS
# =====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #0d0d0d;
        color: #f0f0f0;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #111111 !important;
        border-right: 2px solid #cc0000;
    }
    section[data-testid="stSidebar"] * {
        color: #f0f0f0 !important;
    }

    /* ── Navbar ── */
    .nav-bar {
        background: linear-gradient(90deg, #1a0000, #cc0000);
        padding: 14px 28px;
        border-radius: 8px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 15px rgba(204,0,0,0.4);
    }
    .nav-brand {
        font-size: 1.8rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: 2px;
    }
    .nav-brand span { color: #ff4444; }
    .nav-info {
        display: flex;
        gap: 28px;
        font-size: 14px;
        font-weight: 600;
        color: #ffe0e0;
    }

    /* ── Hero Banner ── */
    .hero {
        background: linear-gradient(135deg, #1a0000 0%, #cc0000 50%, #1a0000 100%);
        padding: 36px 40px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(204,0,0,0.3);
    }
    .hero h1 { margin: 0; font-size: 2.2rem; font-weight: 900; }
    .hero p  { margin: 8px 0 0; opacity: 0.9; font-size: 1rem; }

    /* ── Product Card ── */
    .prod-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        transition: all 0.25s ease;
        height: 100%;
    }
    .prod-card:hover {
        border-color: #cc0000;
        box-shadow: 0 6px 24px rgba(204,0,0,0.25);
        transform: translateY(-4px);
    }
    .prod-img {
        height: 150px;
        object-fit: contain;
        margin-bottom: 12px;
        border-radius: 6px;
    }
    .prod-name {
        font-size: 13px;
        font-weight: 600;
        color: #f0f0f0;
        height: 40px;
        overflow: hidden;
        line-height: 1.4;
    }
    .prod-rating { color: #ff9900; font-size: 12px; margin: 6px 0; }
    .prod-price  { font-size: 18px; font-weight: 700; color: #ff4444; }
    .prod-ship   { font-size: 11px; color: #666; margin-top: 4px; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #cc0000, #ff2222) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        box-shadow: 0 3px 10px rgba(204,0,0,0.3) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #ff2222, #cc0000) !important;
        box-shadow: 0 5px 18px rgba(204,0,0,0.5) !important;
    }

    /* ── Login Box ── */
    .login-box {
        background: #1a1a1a;
        border: 1px solid #cc0000;
        border-radius: 14px;
        padding: 40px;
        box-shadow: 0 8px 40px rgba(204,0,0,0.2);
        text-align: center;
    }
    .login-box h2 { color: #cc0000; font-weight: 900; }

    /* ── Receipt ── */
    .receipt {
        background: #1a1a1a;
        border: 2px dashed #cc0000;
        border-radius: 12px;
        padding: 32px;
    }
</style>
""", unsafe_allow_html=True)

# =====================
# SESSION STATE
# =====================
defaults = {
    'user': None, 'role': None, 'cart': [], 'wishlist': [],
    'orders': [], 'coins': 150, 'page': 'Login',
    'otp_sent': False, 'show_receipt': None, 'chat_history': [],
    'lang': 'English', 'feedback': []
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =====================
# PRODUCT CATALOG
# =====================
IMG = {
    "Silk1":   "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=400&q=80",
    "Silk2":   "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=400&q=80",
    "Cotton1": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400&q=80",
    "Cotton2": "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=400&q=80",
    "Ethnic1": "https://images.unsplash.com/photo-1597113366853-9a93ad3f1002?w=400&q=80",
    "Ethnic2": "https://images.unsplash.com/photo-1623091410901-00e2d268901f?w=400&q=80",
    "Suit1":   "https://images.unsplash.com/photo-1593030761757-71fae45fa0e7?w=400&q=80",
    "Suit2":   "https://images.unsplash.com/photo-1589310243389-96a5483213a8?w=400&q=80",
    "Shirt1":  "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&q=80",
    "Dhoti":   "https://images.unsplash.com/photo-1611601679655-7c8bc197f0c6?w=400&q=80",
    "Towel":   "https://images.unsplash.com/photo-1560064060-1f0124976cae?w=400&q=80",
    "BedSheet":"https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&q=80",
}

CATALOG = [
    {"id":1,  "name":"Kanchipuram Silk Saree",     "name_ta":"காஞ்சிபுரம் பட்டு சேலை",  "cat":"Silk Sarees","price":12500, "img":IMG["Silk1"],    "rating":4.9,"stock":10},
    {"id":2,  "name":"Banarasi Zari Saree",     "name_ta":"பனாரசி ஜரிகை சேலை",     "cat":"Silk Sarees","price":8900,  "img":IMG["Silk2"],    "rating":4.8,"stock":15},
    {"id":3,  "name":"Premium Cotton Saree",    "name_ta":"பிரீமியம் பருத்தி சேலை",  "cat":"Cotton Wear","price":2500,  "img":IMG["Cotton1"],  "rating":4.6,"stock":25},
    {"id":4,  "name":"Handloom Cotton Shirt",   "name_ta":"கைத்தறி பருத்தி சட்டை",   "cat":"Cotton Wear","price":1200,  "img":IMG["Shirt1"],   "rating":4.5,"stock":30},
    {"id":5,  "name":"Pure Silk Dhoti Set",      "name_ta":"தூய பட்டு வேட்டி செட்",   "cat":"Ethnic Wear","price":3500,  "img":IMG["Dhoti"],    "rating":4.7,"stock":20},
    {"id":6,  "name":"Wedding Silk Kurta",      "name_ta":"திருமண பட்டு குர்தா",    "cat":"Ethnic Wear","price":4800,  "img":IMG["Ethnic1"],  "rating":4.8,"stock":12},
    {"id":7,  "name":"Chanderi Suit Material",  "name_ta":"சந்தேரி சூட் மெட்டீரியல்", "cat":"Suits & Materials","price":2200, "img":IMG["Suit1"],    "rating":4.4,"stock":18},
    {"id":8,  "name":"Embroidered Fabric Set",   "name_ta":"பூவேலைப்பாடணிந்த துணி", "cat":"Suits & Materials","price":1800, "img":IMG["Suit2"],    "rating":4.3,"stock":11},
    {"id":9,  "name":"Cotton Bedspread Set",    "name_ta":"பருத்தி மெத்தை விரிப்பு",   "cat":"Home Textiles","price":1500, "img":IMG["BedSheet"], "rating":4.5,"stock":40},
    {"id":10, "name":"Egyptian Cotton Towels",  "name_ta":"எகிப்திய பருத்தி துண்டுகள்", "cat":"Home Textiles","price":950,  "img":IMG["Towel"],    "rating":4.6,"stock":50},
    {"id":11, "name":"Mysore Silk Special",      "name_ta":"மைசூர் பட்டு ஸ்பெஷல்",   "cat":"Silk Sarees","price":6500,  "img":IMG["Silk1"],    "rating":4.7,"stock":8},
    {"id":12, "name":"Linen Formal Trousers",    "name_ta":"லினன் பார்மல் பேன்ட்",    "cat":"Cotton Wear","price":1800,  "img":IMG["Cotton2"],  "rating":4.4,"stock":15},
    {"id":13, "name":"Soft Tussar Silk Saree",   "name_ta":"துஸ்ஸார் பட்டு சேலை",    "cat":"Silk Sarees","price":7500,  "img":IMG["Silk2"],    "rating":4.6,"stock":12},
    {"id":14, "name":"Chettinad Cotton Saree",   "name_ta":"செட்டிநாடு பருத்தி சேலை",  "cat":"Cotton Wear","price":3200,  "img":IMG["Cotton1"],  "rating":4.8,"stock":22},
    {"id":15, "name":"Designer Anarkali Suit",   "name_ta":"டிசைனர் அனார்கலி சூட்",    "cat":"Ethnic Wear","price":5500,  "img":IMG["Ethnic1"],  "rating":4.7,"stock":9},
    {"id":16, "name":"Georgette Material",       "name_ta":"ஜார்ஜெட் மெட்டீரியல்",     "cat":"Suits & Materials","price":1950, "img":IMG["Suit2"],    "rating":4.5,"stock":25},
    {"id":17, "name":"Pure Linen Mens Shirt",    "name_ta":"லினன் ஆண்கள் சட்டை",    "cat":"Cotton Wear","price":1500,  "img":IMG["Shirt1"],   "rating":4.6,"stock":35},
    {"id":18, "name":"Kids Cotton Kurta Set",    "name_ta":"பருத்தி குர்தா செட்",       "cat":"Ethnic Wear","price":1250,  "img":IMG["Ethnic2"],  "rating":4.4,"stock":18},
    {"id":19, "name":"Organza Floral Saree",     "name_ta":"ஆர்கன்சா பூக்கள் சேலை",   "cat":"Silk Sarees","price":4500,  "img":IMG["Silk1"],    "rating":4.5,"stock":14},
    {"id":20, "name":"Velvet Bedspread",         "name_ta":"வெல்வெட் மெத்தை விரிப்பு",   "cat":"Home Textiles","price":3800, "img":IMG["BedSheet"], "rating":4.7,"stock":30},
    {"id":21, "name":"Luxury Bath Robe",         "name_ta":"ஆடம்பர குளியல் ஆடை",    "cat":"Home Textiles","price":2100, "img":IMG["Towel"],    "rating":4.5,"stock":15},
    {"id":22, "name":"Mens Wedding Sherwani",    "name_ta":"ஆண்கள் திருமண ஷெர்வானி",  "cat":"Ethnic Wear","price":11500, "img":IMG["Ethnic1"],  "rating":4.8,"stock":5},
    {"id":23, "name":"Cotton Nightwear Set",     "name_ta":"பருத்தி இரவு ஆடை செட்",   "cat":"Cotton Wear","price":890,   "img":IMG["Cotton2"],  "rating":4.3,"stock":28},
    {"id":24, "name":"Pashmina Winter Shawl",    "name_ta":"பாஷ்மினா குளிர்கால ஷால்",   "cat":"Suits & Materials","price":2800, "img":IMG["Suit1"],    "rating":4.9,"stock":20}
]

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def plotly_dark_fig(fig):
    fig.update_layout(
        paper_bgcolor="#1a1a1a",
        plot_bgcolor="#1a1a1a",
        font_color="#f0f0f0",
        title_font_color="#ff4444",
    )
    return fig

def generate_pdf_receipt(order, T, user_name, view_time):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(204, 0, 0) # Rayan Red
    pdf.cell(0, 10, T['receipt_title'], 0, 1, 'C')
    
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Generated: {view_time}", 0, 1, 'C')
    pdf.ln(5)
    
    # Table Header
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Order Details", "B", 1)
    pdf.ln(2)
    
    pdf.set_font("Arial", '', 11)
    details = [
        (T['order_id'], f"#{order['id']}"),
        (T['date'], order['date']),
        (T['customer'], user_name),
        (T['payment'], order['pay_mode']),
        (T['status'], order['status'])
    ]
    
    for label, value in details:
        pdf.cell(50, 8, label, 0, 0)
        pdf.cell(0, 8, value, 0, 1, 'R')
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Purchased Items", "B", 1)
    pdf.ln(2)
    
    pdf.set_font("Arial", '', 11)
    for item in order['items']:
        pdf.cell(140, 8, item['name'], 0, 0)
        pdf.cell(0, 8, f"Rs.{item['price']:,}", 0, 1, 'R')
    
    pdf.ln(10)
    pdf.set_draw_color(204, 0, 0)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(204, 0, 0)
    pdf.cell(0, 10, f"TOTAL PAID: Rs.{order['total']:,.0f}", 0, 1, 'C')
    
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(255, 102, 0)
    pdf.cell(0, 8, f"{order['coins_earned']} {T['coins']}", 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, T['thank_you'], 0, 1, 'C')
    
    return pdf.output()

# ========================
# LOGIN PAGE
# ========================
if st.session_state.page == "Login":
    st.markdown("<br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.3, 1])
    with col:
        st.markdown("""
        <div class="login-box">
            <div style="font-size:2.2rem;font-weight:900;color:#ff4444;letter-spacing:3px;">
                RAYAN
            </div>
            <div style="font-size:1rem;color:#999;margin-bottom:24px;">
                Premium Shopping Platform
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        login_type = st.radio("Select Login Type", ["Customer Login", "Admin Login"], horizontal=True)

        if login_type == "Admin Login":
            st.markdown("#### Admin Credentials")
            adm_u = st.text_input("Username", placeholder="admin", key="adm_u")
            adm_p = st.text_input("Password", type="password", placeholder="••••••••", key="adm_p")
            if st.button("Login as Admin", use_container_width=True):
                if adm_u == ADMIN_USER and adm_p == ADMIN_PASS:
                    st.session_state.user = "Admin"
                    st.session_state.role = "admin"
                    st.session_state.page = "AdminPanel"
                    st.rerun()
                else:
                    st.error("Wrong credentials. Try: admin / admin123")
        else:
            email = st.text_input("Email or Mobile", placeholder="you@rayan.com")
            if st.button("Send OTP", use_container_width=True):
                if email:
                    st.session_state.otp_sent = True
                    st.toast(f"OTP sent! Use: 1234", icon="📱")
                else:
                    st.warning("Please enter your email.")

            if st.session_state.otp_sent:
                otp = st.text_input("Enter OTP", type="password", placeholder="1234")
                if st.button("Login & Shop Now", use_container_width=True):
                    if otp == "1234":
                        st.session_state.user = email.split("@")[0]
                        st.session_state.role = "customer"
                        st.session_state.page = "Store"
                        st.rerun()
                    else:
                        st.error("Wrong OTP. Use 1234.")

            st.markdown("---")
            if st.button("Continue as Guest", use_container_width=True):
                st.session_state.user = "Guest"
                st.session_state.role = "customer"
                st.session_state.page = "Store"
                st.rerun()

# ========================
# ADMIN PANEL
# ========================
elif st.session_state.page == "AdminPanel":
    st.markdown(f"""
    <div class="admin-bar">
        <div style="font-size:1.5rem;font-weight:900;color:#ff4444;letter-spacing:2px;">
            RAYAN ADMIN PANEL
        </div>
        <div style="color:#ccc;font-size:13px;">
            Logged in as <b style="color:#ff4444;">Admin</b> &nbsp;|&nbsp;
            {datetime.now().strftime("%d %b %Y, %H:%M")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown("#### Language / மொழி")
    lang_choice = st.sidebar.radio("", ["English", "Tamil"],
                                   index=0 if st.session_state.lang == "English" else 1,
                                   horizontal=True, key="admin_lang_pick")
    st.session_state.lang = lang_choice
    T = LANG[lang_choice]

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.markdown("### Admin Menu")
    admin_menu = st.sidebar.radio("", [
        "Dashboard Overview",
        "Order Database",
        "User Database",
        "Inventory Management",
        "Project Schema (MySQL)",
        "Analytics & Trends",
        "ML Research Results",
        "Feedback Logs",
    ])
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    # Simulated database records
    sim_orders = st.session_state.orders + [
        {"id":100001,"date":"23 Feb 2026, 09:15","total":62990, "items":[{"name":"Sony TV"}],         "status":"Delivered","pay_mode":"UPI / QR Code",       "coins_earned":1260},
        {"id":100002,"date":"22 Feb 2026, 14:30","total":16995, "items":[{"name":"Nike Jordan"}],     "status":"Shipped",  "pay_mode":"Credit/Debit Card",   "coins_earned":340},
        {"id":100003,"date":"21 Feb 2026, 11:00","total":2899,  "items":[{"name":"Levis Jeans"}],     "status":"Delivered","pay_mode":"Cash on Delivery",    "coins_earned":58},
        {"id":100004,"date":"20 Feb 2026, 18:45","total":129999,"items":[{"name":"Samsung S24"}],     "status":"Packed",   "pay_mode":"EMI",                 "coins_earned":2600},
        {"id":100005,"date":"19 Feb 2026, 10:20","total":8990,  "items":[{"name":"IKEA Chair"}],      "status":"Delivered","pay_mode":"Net Banking",         "coins_earned":180},
        {"id":100006,"date":"18 Feb 2026, 08:00","total":159900,"items":[{"name":"iPhone 15 Pro"}],   "status":"Delivered","pay_mode":"Credit/Debit Card",   "coins_earned":3198},
        {"id":100007,"date":"17 Feb 2026, 16:00","total":99900, "items":[{"name":"MacBook Air M2"}],  "status":"Shipped",  "pay_mode":"EMI",                 "coins_earned":1998},
    ]
    sim_users = [
        {"ID":1,"Username":st.session_state.user if st.session_state.user != "Admin" else "rayan_user",
         "Email":"rayan@gmail.com","SuperCoins":st.session_state.coins,"Orders":len(st.session_state.orders),"Role":"Customer","Status":"Active"},
        {"ID":2,"Username":"admin",          "Email":"admin@rayan.com",   "SuperCoins":9999,"Orders":150,"Role":"Admin",    "Status":"Active"},
        {"ID":3,"Username":"priya_sharma",   "Email":"priya@yahoo.com",   "SuperCoins":430, "Orders":7,  "Role":"Customer","Status":"Active"},
        {"ID":4,"Username":"arjun_kumar",    "Email":"arjun@hotmail.com", "SuperCoins":120, "Orders":3,  "Role":"Customer","Status":"Active"},
        {"ID":5,"Username":"meera_nair",     "Email":"meera@gmail.com",   "SuperCoins":890, "Orders":15, "Role":"Customer","Status":"Active"},
        {"ID":6,"Username":"rohan_verma",    "Email":"rohan@outlook.com", "SuperCoins":55,  "Orders":1,  "Role":"Customer","Status":"Inactive"},
    ]

    total_rev = sum(o["total"] for o in sim_orders)

    # ── DASHBOARD OVERVIEW ──
    if admin_menu == "Dashboard Overview":
        st.subheader("Store KPIs")
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="stat-card"><div class="stat-num">Rs.{total_rev:,.0f}</div><div class="stat-label">Total Revenue</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="stat-card"><div class="stat-num">{len(sim_orders)}</div><div class="stat-label">Total Orders</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="stat-card"><div class="stat-num">{len(sim_users)}</div><div class="stat-label">Registered Users</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="stat-card"><div class="stat-num">{len(CATALOG)}</div><div class="stat-label">Products Listed</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Recent Orders")
        df_recent = pd.DataFrame([{
            "Order ID": o["id"], "Date": o["date"],
            "Amount (Rs.)": f"{o['total']:,.0f}",
            "Status": o.get("status","N/A"),
            "Payment": o.get("pay_mode","N/A"),
        } for o in sim_orders[-5:]])
        st.dataframe(df_recent, use_container_width=True, hide_index=True)

    # ── ORDER DATABASE ──
    elif admin_menu == "Order Database":
        st.subheader(f"Order Table Reference ({len(sim_orders)} records)")
        df_orders = pd.DataFrame([{
            "Order ID":    o["id"],
            "Date":        o["date"],
            "Total (Rs.)": f"{o['total']:,.0f}",
            "Items":       len(o["items"]),
            "Payment":     o.get("pay_mode","N/A"),
            "Status":      o.get("status","Confirmed"),
            "Coins Earned":o.get("coins_earned",0),
        } for o in sim_orders])
        st.dataframe(df_orders, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Order Status Breakdown")
        status_df = df_orders["Status"].value_counts().reset_index()
        status_df.columns = ["Status","Count"]
        fig = plotly_dark_fig(px.pie(
            status_df, names="Status", values="Count", hole=0.45,
            color_discrete_sequence=["#cc0000","#ff4444","#ff7777","#ffaaaa","#660000"]
        ))
        st.plotly_chart(fig, use_container_width=True)

    # ── USER DATABASE ──
    elif admin_menu == "User Database":
        st.subheader(f"User Table Reference ({len(sim_users)} records)")
        st.dataframe(pd.DataFrame(sim_users), use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Preferred Payment Modes")
        pay_df = pd.DataFrame({
            "Mode": ["UPI/QR","Credit Card","Net Banking","EMI","Cash on Delivery"],
            "Count":[38, 29, 14, 12, 7]
        })
        fig2 = plotly_dark_fig(px.bar(
            pay_df, x="Mode", y="Count",
            color="Count", color_continuous_scale=["#660000","#cc0000","#ff4444"]
        ))
        st.plotly_chart(fig2, use_container_width=True)

    # ── INVENTORY MANAGEMENT ──
    elif admin_menu == "Inventory Management":
        st.subheader(f"Product Inventory ({len(CATALOG)} products)")
        inv_df = pd.DataFrame(CATALOG)[["id","name","cat","price","rating","stock"]]
        inv_df.columns = ["ID","Product","Category","Price (Rs.)","Rating","Stock"]
        st.dataframe(inv_df, use_container_width=True, hide_index=True)
        st.caption("Low stock (<10 units) items: " +
                   ", ".join([str(p["name"]) for p in CATALOG if int(p["stock"]) < 10]))

        cat_df = inv_df["Category"].value_counts().reset_index()
        cat_df.columns = ["Category","Count"]
        fig3 = plotly_dark_fig(px.pie(
            cat_df, names="Category", values="Count", hole=0.4,
            color_discrete_sequence=["#cc0000","#ff4444","#ff7777","#ffaaaa","#660000","#330000"]
        ))
        st.plotly_chart(fig3, use_container_width=True)

    # ── PROJECT SCHEMA ──
    elif admin_menu == "Project Schema (MySQL)":
        st.subheader("MySQL Database Design (ER Mapping)")
        st.markdown("""
        For the **Final Year Project report**, the following schema is used (Implemented via CSV DataFrame interfaces for portability):
        
        | Table | Primary Key | Description |
        | :--- | :--- | :--- |
        | **Users** | `user_id` | Stores customer credentials & profile |
        | **Products** | `product_id` | Textile inventory (Silk, Cotton, etc.) |
        | **Orders** | `order_id` | Transaction headers and totals |
        | **Order_Items** | `(order, product)` | Line items for each purchase |
        
        **SQL Reference:**
        ```sql
        CREATE TABLE Users (user_id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100));
        CREATE TABLE Products (product_id INT PRIMARY KEY, name VARCHAR(100), price FLOAT);
        ```
        """)
        st.image("https://dataedo.com/asset/img/kb/db-tools/mysql_workbench/output/mysql_workbench_sakila_diagram.png", caption="System Database Architecture", use_container_width=True)

    # ── ANALYTICS ──
    elif admin_menu == "Analytics & Trends":
        st.subheader("Textile Sales Trends")
        months  = ["Sep","Oct","Nov","Dec","Jan","Feb"]
        revenue = [85000,142000,230000,310000,180000,total_rev]
        fig4 = plotly_dark_fig(px.bar(
            pd.DataFrame({"Month":months,"Revenue":revenue}),
            x="Month", y="Revenue", title="Monthly Revenue Trend (Rs.)",
            color="Revenue", color_continuous_scale=["#330000","#cc0000","#ff4444"]
        ))
        st.plotly_chart(fig4, use_container_width=True)

        cat_rev = pd.DataFrame({
            "Category":["Silk Sarees","Cotton Wear","Ethnic Wear","Suits","Home Textiles"],
            "Revenue":  [520000,180000,95000,65000,40000]
        })
        fig5 = plotly_dark_fig(px.pie(
            cat_rev, names="Category", values="Revenue",
            title="Revenue by Category", hole=0.35,
            color_discrete_sequence=["#cc0000","#ff4444","#ff7777","#ff9999","#ffbbbb"]
        ))
        st.plotly_chart(fig5, use_container_width=True)

    # ── ML RESEARCH RESULTS ──
    elif admin_menu == "ML Research Results":
        import json
        from pathlib import Path
        st.subheader("ML Model Performance Metrics (CLV Analysis)")

        metrics_path = Path("models/model_metrics.json")
        if metrics_path.exists():
            with open(metrics_path) as f:
                metrics = json.load(f)

            best = metrics.get("best_model","N/A")
            trained = metrics.get("trained_at","N/A")

            st.markdown(f"#### Primary Algorithm: **{best}**")
            st.caption(f"Last Evaluation: {trained}")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Regression R2", f"{metrics.get('R2_Score',0):.4f}")
            c2.metric("CLV Value Accuracy", f"{metrics.get('Accuracy_MAPE',0)}%")
            c3.metric("Classification Acc", f"{metrics.get('Classification_Accuracy',0)}%")
            c4.metric("ROC AUC Score", f"{metrics.get('ROC_AUC',0):.4f}")

            st.divider()
            
            t1, t2 = st.tabs(["Performance Graphs", "Segment Analysis"])
            
            with t1:
                col1, col2 = st.columns(2)
                cm_path = Path("models/plots/confusion_matrix.png")
                roc_path = Path("models/plots/roc_curve.png")
                
                if cm_path.exists():
                    col1.image(str(cm_path), caption="Confusion Matrix (Value Segments)")
                if roc_path.exists():
                    col2.image(str(roc_path), caption="ROC Curve (High-Value Indicator)")
            
            with t2:
                seg_data = metrics.get("segments", {})
                st.write("**Customer Distribution by CLV Segment:**")
                st.bar_chart(seg_data, color="#cc0000")
        else:
            st.warning("No ML training data found. Please run 'scripts/train_models.py' first.")

    # ── FEEDBACK LOGS ──
    elif admin_menu == "Feedback Logs":
        st.subheader(T.get("fb_summary", "Feedback Analysis"))
        if not st.session_state.feedback:
            st.info("No customer feedback received yet.")
        else:
            fb_df = pd.DataFrame(st.session_state.feedback)
            avg_rating = fb_df["rating"].mean()
            st.metric("Average Customer Rating", f"{avg_rating:.2f} / 5.0")
            
            st.markdown("### Recent Reviews")
            for _, row in fb_df.iloc[::-1].iterrows():
                st.markdown(f"""
                <div style="background:#1a1a1a; padding:15px; border-radius:10px; border-left:4px solid #cc0000; margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between;">
                        <b style="color:#ff4444;">{row['user']}</b>
                        <span style="color:#999; font-size:12px;">{row['date']}</span>
                    </div>
                    <div style="color:#ffcc00; margin:5px 0;">{'★' * int(row['rating'])}{'☆' * (5-int(row['rating']))}</div>
                    <div style="color:#eee;">{row['comment']}</div>
                </div>
                """, unsafe_allow_html=True)

# ========================
# CUSTOMER STORE
# ========================
else:
    # Navbar
    st.markdown(f"""
    <div class="nav-bar">
        <div class="nav-brand">RAYAN <span>STORE</span></div>
        <div class="nav-info">
            <span>Hello, {st.session_state.user}</span>
            <span>Coins: {st.session_state.coins}</span>
            <span>Cart: {len(st.session_state.cart)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar nav
    st.sidebar.markdown("#### Language / மொழி")
    lang_choice = st.sidebar.radio("", ["English", "Tamil"],
                                   index=0 if st.session_state.lang == "English" else 1,
                                   horizontal=True, key="lang_pick")
    st.session_state.lang = lang_choice
    T = LANG[lang_choice]

    # Dynamic Clock
    st.sidebar.markdown(f"""
    <div style="background:#1a0000; padding:10px; border-radius:8px; border:1px solid #cc0000; text-align:center; margin-bottom:15px;">
        <div style="color:#ff4444; font-size:11px; font-weight:600; text-transform:uppercase;">Live Time</div>
        <div style="color:#fff; font-size:16px; font-weight:700;">{datetime.now().strftime("%I:%M:%S %p")}</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### {T['hello']}, {st.session_state.user}")
    st.sidebar.markdown(f"**{T['coins_label']}:** {st.session_state.coins}")
    choice = st.sidebar.radio(T["nav_store"],
                               [T["store"], T["wishlist"], T["orders"], T["ai"], T["feedback"]])
    st.sidebar.markdown("---")
    if st.sidebar.button(T["logout"], use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    # ── STORE ──
    if choice == T["store"]:
        st.markdown(f"""
        <div class="hero">
            <h1>{T['hero_h1']}</h1>
            <p>{T['hero_p']}</p>
        </div>
        """, unsafe_allow_html=True)

        fc, sc = st.columns([1, 2])
        with fc:
            cat_map = {
                T["cat_all"]: "All",
                T["cat_elec"]: "Silk Sarees",
                T["cat_fash"]: "Cotton Wear",
                T["cat_home"]: "Ethnic Wear",
                T["cat_beau"]: "Suits & Materials",
                T["cat_sport"]: "Home Textiles"
            }
            sel_cat_disp = st.selectbox(T["category"], list(cat_map.keys()))
            sel_cat = cat_map[sel_cat_disp]
        with sc:
            search = st.text_input(T["search"], placeholder="Silk, Cotton, Saree...")

        items = CATALOG
        if sel_cat != "All":
            items = [p for p in items if p["cat"] == sel_cat]
        if search:
            search_low = search.lower()
            items = [p for p in items if search_low in str(p["name"]).lower() or (p.get("name_ta") and search in str(p["name_ta"]))]

        st.caption(f"Showing **{len(items)}** products")

        cols = st.columns(4)
        for i, p in enumerate(items):
            with cols[i % 4]:
                # Show product name based on language
                disp_name = p.get("name_ta", p["name"]) if st.session_state.lang == "Tamil" else p["name"]
                st.markdown(f"""
                <div class="prod-card">
                    <img src="{p['img']}" class="prod-img" loading="lazy">
                    <div class="prod-name">{disp_name}</div>
                    <div style="font-size:10px;color:#666;margin-bottom:4px;">{p['name']}</div>
                    <div class="prod-rating">{chr(9733) * int(p['rating'])} {p['rating']}</div>
                    <div class="prod-price">Rs.{p['price']:,}</div>
                    <div class="prod-ship">{T['free_del']} | {T['stock']}: {p['stock']}</div>
                </div>
                """, unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                if c1.button(T["add"], key=f"add_{p['id']}"):
                    st.session_state.cart.append(p)
                    st.toast(f"Added: {p['name']}")
                if c2.button(T["save"], key=f"wish_{p['id']}"):
                    if p not in st.session_state.wishlist:
                        st.session_state.wishlist.append(p)
                        st.toast("Saved to wishlist!")

    # ── WISHLIST ──
    elif choice == T["wishlist"]:
        st.subheader("My Wishlist")
        if not st.session_state.wishlist:
            st.info("Wishlist is empty. Browse the store to save items!")
        else:
            for p in list(st.session_state.wishlist):
                with st.expander(f"{p['name']} — Rs.{p['price']:,}"):
                    a, b = st.columns([1, 3])
                    a.image(p['img'], width=100)
                    b.markdown(f"**{p['name']}**  \n{p['cat']} | Rating: {p['rating']}  \n**Rs.{p['price']:,}**")
                    if b.button("Move to Cart", key=f"wc_{p['id']}"):
                        st.session_state.cart.append(p)
                        st.session_state.wishlist.remove(p)
                        st.rerun()
                    if b.button("Remove", key=f"wr_{p['id']}"):
                        st.session_state.wishlist.remove(p)
                        st.rerun()

    # ── MY ORDERS ──
    elif choice == T["orders"]:
        st.subheader("My Orders & Tracking")
        if not st.session_state.orders:
            st.info("No orders yet. Time to shop!")
        else:
            for o in reversed(st.session_state.orders):
                with st.expander(f"Order #{o['id']}  |  {o['date']}  |  Rs.{o['total']:,.0f}  |  {o.get('status','Confirmed')}"):
                    for item in o["items"]:
                        st.markdown(f"- {item['name']} — Rs.{item['price']:,}")
                    st.markdown(f"**Payment:** {o.get('pay_mode','N/A')} | **Coins Earned:** {o.get('coins_earned',0)}")
                    st.markdown("""
                    <div class="tracker">
                        <div class="t-line"><div class="t-line-fill"></div></div>
                        <div class="t-step"><div class="t-dot"></div><br>Ordered</div>
                        <div class="t-step"><div class="t-dot"></div><br>Packed</div>
                        <div class="t-step"><div class="t-dot"></div><br>Shipped</div>
                        <div class="t-step"><div class="t-dot-off"></div><br>Delivered</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.success("Estimated Delivery: Today by 9 PM")

    # ── THREAD AI ──
    elif choice == T["ai"]:
        st.subheader("Thread AI — Your Shopping Assistant")
        st.caption("Ask me anything! Recommendations, price comparisons, order tracking, deals...")

        if not st.session_state.chat_history:
            st.session_state.chat_history = [("bot", "Hello! I am Fabric AI. How can I help you pick the perfect fabric today?")]

        for role, msg in st.session_state.chat_history:
            prefix = "Fabric AI:" if role == "bot" else "You:"
            color  = "#ff4444" if role == "bot" else "#f0f0f0"
            st.markdown(f"<span style='color:{color};font-weight:600;'>{prefix}</span> {msg}", unsafe_allow_html=True)

        q_input = st.text_input("Your question", placeholder="Best silk saree for wedding?", key="ai_q")
        if st.button("Send") and q_input:
            st.session_state.chat_history.append(("user", q_input))
            q = q_input.lower()
            if any(w in q for w in ["track","order","shipment"]):
                reply = f"You have {len(st.session_state.orders)} order(s). Check 'My Orders' for tracking."
            elif any(w in q for w in ["suggest","recommend","best","top"]):
                p = random.choice(CATALOG)
                reply = f"I recommend **{p['name']}** at Rs.{p['price']:,} — rated {p['rating']} stars!"
            elif "compare" in q:
                p1, p2 = random.sample(CATALOG, 2)
                reply = (f"{p1['name']} (Rs.{p1['price']:,}, {p1['rating']} stars) vs "
                         f"{p2['name']} (Rs.{p2['price']:,}, {p2['rating']} stars)")
            elif any(w in q for w in ["cheap","budget","under","affordable"]):
                all_items_sorted = sorted(CATALOG, key=lambda x: int(x["price"]))
                top3 = all_items_sorted[:3]
                reply = "Budget picks: " + " | ".join([f"{p['name']} Rs.{p['price']:,}" for p in top3])
            elif "coin" in q:
                reply = f"You have {st.session_state.coins} SuperCoins. Earn 2 coins per Rs.100 spent!"
            elif any(w in q for w in ["sale","offer","coupon","discount"]):
                reply = "Use coupon RAYAN10 for 10% off or FEST20 for 20% off your order!"
            else:
                reply = "I can help with recommendations, price comparison, order tracking, and deals. Ask away!"
            st.session_state.chat_history.append(("bot", reply))
            st.rerun()

    # ── FEEDBACK ──
    elif choice == T["feedback"]:
        st.subheader(T["feedback"])
        st.markdown("We value your input to serve you better!")
        with st.form("feedback_form"):
            rating = st.select_slider(T["rating"], options=[1, 2, 3, 4, 5], value=5)
            comment = st.text_area(T["comments"], placeholder="Share your experience with Rayan Textiles...")
            submit = st.form_submit_button(T["submit_fb"])
            if submit:
                st.session_state.feedback.append({
                    "user": st.session_state.user,
                    "rating": rating,
                    "comment": comment,
                    "date": datetime.now().strftime("%d %b %Y, %H:%M")
                })
                st.success(T["fb_thank_you"])

    # ── CART (SIDEBAR) ──
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### Cart ({len(st.session_state.cart)} items)")

    if not st.session_state.cart:
        st.sidebar.caption("Your cart is empty.")
    else:
        for idx, item in enumerate(st.session_state.cart):
            ca, cb = st.sidebar.columns([4, 1])
            ca.caption(f"{item['name'][:20]}...")
            if cb.button("X", key=f"rm_{idx}"):
                st.session_state.cart.pop(idx)
                st.rerun()

        st.sidebar.markdown("---")
        subtotal   = sum(i["price"] for i in st.session_state.cart)
        st.sidebar.metric("Subtotal", f"Rs.{subtotal:,}")

        code = st.sidebar.text_input("Coupon Code", placeholder="RAYAN10 or FEST20")
        disc = 0
        if code == "RAYAN10":
            disc = subtotal * 0.10
            st.sidebar.success("RAYAN10: -10% applied!")
        elif code == "FEST20":
            disc = subtotal * 0.20
            st.sidebar.success("FEST20: -20% applied!")

        final       = subtotal - disc
        coins_earn  = int(final / 100) * 2
        st.sidebar.metric("Total Payable", f"Rs.{final:,.0f}")
        st.sidebar.caption(f"You will earn {coins_earn} SuperCoins")

        st.sidebar.markdown("#### Payment Method")
        pay_mode = st.sidebar.radio("", [
            "UPI / QR Code", "Credit/Debit Card",
            "Net Banking", "EMI", "Cash on Delivery"
        ])

        if pay_mode == "UPI / QR Code":
            qr_data = f"upi://pay?pa=rayan@upi&pn=RayanShopping&am={final:.0f}&cu=INR"
            qr_url  = f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={qr_data}"
            st.sidebar.markdown(f'<div class="qr-box"><img src="{qr_url}" width="160"><br><small style="color:#333">Scan UPI QR | Rs.{final:,.0f}</small></div>', unsafe_allow_html=True)

        elif pay_mode == "Credit/Debit Card":
            st.sidebar.text_input("Card Number", placeholder="XXXX XXXX XXXX XXXX")
            x1, x2 = st.sidebar.columns(2)
            x1.text_input("MM/YY")
            x2.text_input("CVV", type="password")
            qr_data = f"PAY:CARD:RAYAN:{final:.0f}"
            qr_url  = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={qr_data}"
            st.sidebar.markdown(f'<div class="qr-box"><img src="{qr_url}" width="140"><br><small style="color:#333">Card Payment QR | Rs.{final:,.0f}</small></div>', unsafe_allow_html=True)

        elif pay_mode == "Net Banking":
            st.sidebar.selectbox("Select Bank", [
                "HDFC Bank","SBI","ICICI Bank","Axis Bank","Kotak","PNB"
            ])
            qr_data = f"NETBANKING:RAYAN:{final:.0f}"
            qr_url  = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={qr_data}"
            st.sidebar.markdown(f'<div class="qr-box"><img src="{qr_url}" width="140"><br><small style="color:#333">Net Banking Ref QR | Rs.{final:,.0f}</small></div>', unsafe_allow_html=True)

        elif pay_mode == "EMI":
            plan = st.sidebar.selectbox("EMI Plan", [
                "3 Months (No Cost)","6 Months","9 Months","12 Months"
            ])
            months = int(plan.split()[0])
            st.sidebar.caption(f"Monthly: Rs.{final/months:,.0f}/mo")
            qr_data = f"EMI:RAYAN:{months}M:{final:.0f}"
            qr_url  = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={qr_data}"
            st.sidebar.markdown(f'<div class="qr-box"><img src="{qr_url}" width="140"><br><small style="color:#333">EMI {months}M QR | Rs.{final/months:,.0f}/mo</small></div>', unsafe_allow_html=True)

        elif pay_mode == "Cash on Delivery":
            st.sidebar.info(f"Pay Rs.{final+50:,.0f} on delivery (+Rs.50 fee)")
            qr_data = f"COD:RAYAN:ORDER:{final:.0f}"
            qr_url  = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={qr_data}"
            st.sidebar.markdown(f'<div class="qr-box"><img src="{qr_url}" width="140"><br><small style="color:#333">COD Confirmation QR</small></div>', unsafe_allow_html=True)

        if st.sidebar.button("Confirm & Pay", use_container_width=True):
            oid = random.randint(100000, 999999)
            st.session_state.orders.append({
                "id":          oid,
                "date":        datetime.now().strftime("%d %b %Y, %H:%M"),
                "total":       final,
                "items":       list(st.session_state.cart),
                "status":      "Packed" if pay_mode != "Cash on Delivery" else "Confirmed",
                "pay_mode":    pay_mode,
                "coins_earned":coins_earn,
            })
            st.session_state.coins += coins_earn
            st.session_state.show_receipt = oid
            st.session_state.cart = []
            st.rerun()

    # ── RECEIPT ──
    if st.session_state.show_receipt:
        order = next((o for o in st.session_state.orders
                      if o["id"] == st.session_state.show_receipt), None)
        if order:
            T = LANG[st.session_state.lang]
            # Dynamic timestamp at moment of viewing
            view_time = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
            st.balloons()
            st.markdown(f"""
            <div class="receipt">
                <h2 style="text-align:center;color:#ff4444;margin:0 0 16px;">
                    {T['receipt_title']}
                </h2>
                <div style="text-align:center;color:#888;font-size:11px;margin-bottom:12px;">
                    Generated: {view_time}
                </div>
                <hr style="border-color:#cc0000;">
                <table style="width:100%;color:#f0f0f0;border-collapse:collapse;">
                    <tr><td style="padding:6px 0">{T['order_id']}</td><td align="right"><b>#{order['id']}</b></td></tr>
                    <tr><td style="padding:6px 0">{T['date']}</td><td align="right">{order['date']}</td></tr>
                    <tr><td style="padding:6px 0">{T['customer']}</td><td align="right">{st.session_state.user}</td></tr>
                    <tr><td style="padding:6px 0">{T['items']}</td><td align="right">{len(order['items'])}</td></tr>
                    <tr><td style="padding:6px 0">{T['payment']}</td><td align="right">{order['pay_mode']}</td></tr>
                    <tr><td style="padding:6px 0">{T['status']}</td><td align="right" style="color:#44ff88;">{order['status']}</td></tr>
                </table>
                <hr style="border-color:#cc0000;">
                <h2 style="text-align:center;color:#ff4444;">Rs.{order['total']:,.0f}</h2>
                <p style="text-align:center;color:#ff9900;">
                    {order['coins_earned']} {T['coins']}
                </p>
                <p style="text-align:center;color:#666;font-size:12px;">{T['thank_you']}</p>
            </div>
            """, unsafe_allow_html=True)

            # ── Build downloadable receipt text ──
            item_lines = "\n".join(
                [f"  - {it['name']}  Rs.{it['price']:,}" for it in order['items']]
            )
            receipt_text = f"""
================================================
  {T['receipt_title']}
================================================
{T['order_id']:<22}: #{order['id']}
{T['date']:<22}: {view_time}
{T['customer']:<22}: {st.session_state.user}
{T['payment']:<22}: {order['pay_mode']}
{T['status']:<22}: {order['status']}
------------------------------------------------
{T['items']}:
{item_lines}
------------------------------------------------
{T['total']:<22}: Rs.{order['total']:,.0f}
{T['coins']:<22}: {order['coins_earned']}
================================================
  {T['thank_you']}
================================================
"""
            st.download_button(
                label=T['download_receipt'],
                data=receipt_text.encode("utf-8"),
                file_name=f"Receipt_{order['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
            
            # PDF Download
            pdf_data = generate_pdf_receipt(order, T, st.session_state.user, view_time)
            st.download_button(
                label=T['download_pdf'],
                data=pdf_data,
                file_name=f"Receipt_{order['id']}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

            if st.button(T['close_receipt']):
                st.session_state.show_receipt = None
                st.rerun()

st.markdown("""
<div style="text-align:center;color:#333;font-size:12px;padding:20px;border-top:1px solid #2a2a2a;margin-top:40px;">
    &copy; 2026 Rayan Shopping Platform &nbsp;|&nbsp; All Rights Reserved
</div>
""", unsafe_allow_html=True)
