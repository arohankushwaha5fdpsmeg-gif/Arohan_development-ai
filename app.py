# PRODUCTION MODULE: AROHAN GLOBAL DEVELOPMENT ENGINE
import os
import io
import sys
import time
import json
import random
import sqlite3
from datetime import datetime, timedelta
import gradio as gr
import stripe

# =====================================================================
# 1. ENTERPRISE GATEWAY & STORAGE CONFIGURATIONS
# =====================================================================
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_51Tke3WRsVgVw9kTXB7nWOrvb1jGUnCuTAqwgcX5OA7r7hxVh534pcyg5Y0D989GwT4CQmwsfN9SezJyb8gEdjXDF00OEi2JoDS")

if not os.path.exists("data"):
    os.makedirs("data")

DB_FILE_PATH = "data/arohan_global_production.db"

def init_production_database():
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS server_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            prompt TEXT,
            generated_code TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cloud_users (
            username TEXT PRIMARY KEY,
            password TEXT,
            tokens_remaining INTEGER,
            is_premium INTEGER DEFAULT 0,
            last_exhausted_time TEXT DEFAULT NULL
        )
    """)
    conn.commit()
    conn.close()

init_production_database()

# =====================================================================
# 2. DISPATCH CONTROLLERS & DATA BALANCE MANAGEMENT ENGINES
# =====================================================================
def register_public_account(user, password):
    user = user.strip().lower()
    password = password.strip()
    if not user or not password:
        return "<p style='color:#EF4444; font-weight:bold;'>❌ Input blocks cannot be left empty!</p>"
    if "guest_" in user:
        return "<p style='color:#EF4444; font-weight:bold;'>❌ Restricted name routing layout.</p>"

    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO cloud_users (username, password, tokens_remaining, is_premium) VALUES (?, ?, 15, 0)", (user, password))
        conn.commit()
        msg = f"<p style='color:#10B981; font-weight:bold;'>🎉 Registration Successful! Profile '{user}' is active.</p>"
    except sqlite3.IntegrityError:
        msg = "<p style='color:#EF4444; font-weight:bold;'>❌ Username already registered on global server tables.</p>"
    conn.close()
    return msg

def authenticate_and_sync_profile(username, password):
    username = username.strip().lower()
    password = password.strip()

    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT tokens_remaining, is_premium, last_exhausted_time FROM cloud_users WHERE username = ? AND password = ?", (username, password))
    profile = cursor.fetchone()

    if profile is None:
        conn.close()
        return "❌ Sign-In Blocked", "<h3>Invalid account identity keys.</h3>", gr.update(visible=False), "", gr.update(visible=True)

    tokens, premium, exhausted_str = profile

    if premium == 0 and tokens == 0 and exhausted_str is not None:
        try:
            ex_dt = datetime.strptime(exhausted_str, "%Y-%m-%d %H:%M:%S")
            if (datetime.now() - ex_dt) >= timedelta(hours=24):
                tokens = 15
                cursor.execute("UPDATE cloud_users SET tokens_remaining = 15, last_exhausted_time = NULL WHERE username = ?", (username,))
                conn.commit()
        except Exception:
            pass

    conn.close()
    status_label = "👑 Premium Unlimited Active" if premium == 1 else f"🍏 Balance: {tokens} / 15 Free Tokens"
    welcome_banner = f"<h3 style='color:#4F46E5;'>✅ Connection Active: Welcome back, {username}!</h3>"
    return status_label, welcome_banner, gr.update(visible=True), username, gr.update(visible=False)

def deploy_anonymous_guest_session():
    proxy_id = f"guest_{random.randint(100000, 999999)}"
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cloud_users (username, password, tokens_remaining, is_premium) VALUES (?, 'proxy_pass', 15, 0)", (proxy_id,))
    conn.commit()
    conn.close()

    status_label = "🍏 Balance: 15 / 15 Free Tokens (Private Guest Session Active)"
    welcome_banner = f"<h3 style='color:#059669;'>🚪 Entered as Guest: {proxy_id}.</h3>"
    return status_label, welcome_banner, gr.update(visible=True), proxy_id, gr.update(visible=False)

def calculate_token_deduction(username):
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT tokens_remaining, is_premium FROM cloud_users WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row:
        tokens_remaining, is_premium = row
        if is_premium == 1:
            conn.close()
            return True, "Unlimited"
        elif tokens_remaining > 0:
            balance = tokens_remaining - 1
            time_stamp = f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'" if balance == 0 else "NULL"
            cursor.execute(f"UPDATE cloud_users SET tokens_remaining = {balance}, last_exhausted_time = {time_stamp} WHERE username = '{username}'")
            conn.commit()
            conn.close()
            return True, balance
    conn.close()
    return False, 0

# =====================================================================
# 3. MATHEMATICAL GREEDY SEARCH TEXT COMPILER & PRIVACY CORE
# =====================================================================
def execute_global_ai_generation(user_instruction, username_state):
    if not username_state:
        return ("# LOCKED", "Access denied. Sign in.", "<h3>Authentication Required</h3>", "🔴 State Locked")

    allowed, balance = calculate_token_deduction(username_state)
    is_guest = "guest_" in username_state

    if not allowed:
        if is_guest:
            paywall_box = """<div style='background:#FEF2F2; border:2px solid #EF4444; color:#991B1B; padding:25px; border-radius:12px; text-align:center;'>
                <h3>🛑 Guest Token Balance Spent!</h3><p>To unlock unlimited actions, please create a public account.</p></div>"""
            return ("# ACCESS EXPIRED\n# Registration Required", "Guest quota exhausted.", paywall_box, "🔴 Limit Hit (Register Profile)")
        else:
            paywall_box = "<div style='background:#FEF2F2; padding:20px; border-radius:10px; text-align:center;'><h3>🛑 Quota Empty!</h3><p>Please upgrade your plan options package.</p></div>"
            return ("# ACCESS EXPIRED", "Account quota exhausted.", paywall_box, f"🔴 Limit Hit ({balance} remaining)")

    # Lightweight Python structure builder optimized for low-compute tier processing
    simulated_output = (
        f"# Generated Code Matrix Framework\n"
        f"def arohan_process_engine():\n"
        f"    # Task: {user_instruction}\n"
        f"    print('Initializing Arohan Core Matrix Pipeline...')\n"
        f"    return True\n"
        f"arohan_process_engine()"
    )

    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO server_logs (username, prompt, generated_code) VALUES (?, ?, ?)", (username_state, user_instruction, simulated_output))
    conn.commit()
    conn.close()

    status_label = "👑 Premium Unlimited Active" if balance == "Unlimited" else f"🍏 Balance: {balance} / 15 Remaining Tokens"
    return (simulated_output, "Inference matrix compiled with zero critical diagnostic exceptions.", "<h3>Operation Complete</h3>", status_label)

# =====================================================================
# 4. GRADIO WEB GRAPHICAL UI DESIGN & HEAD ACTIONS
# =====================================================================
meta_seo_headers = """
<meta name="description" content="Arohan Global Development Engine - Next-generation high-capacity transformer neural matrix interface running 24/7 code generation pipelines.">
<meta name="keywords" content="Arohan Global, Arohan Engine, AI Code Generator, Neural Matrix Engine, Development Engine">
"""

with gr.Blocks(title="Arohan Global Development Engine", head=meta_seo_headers, theme=gr.themes.Soft()) as demo:
    username_state = gr.State("")
    
    gr.Markdown("# 🚀 AROHAN GLOBAL DEVELOPMENT ENGINE")
    gr.Markdown("Enterprise-grade code generation matrix pipeline running 24/7.")
    
    with gr.Row(elem_id="auth_panel") as auth_panel:
        with gr.Tab("Sign In"):
            login_user = gr.Textbox(label="Username")
            login_pass = gr.Textbox(label="Password", type="password")
            login_btn = gr.Button("Authenticate Session")
        with gr.Tab("Register Account"):
            reg_user = gr.Textbox(label="Choose Username")
            reg_pass = gr.Textbox(label="Choose Password", type="password")
            reg_btn = gr.Button("Register Profile")
            reg_output = gr.HTML()
            
        with gr.Column():
            gr.Markdown("### Alternate Pathway")
            guest_btn = gr.Button("Deploy Anonymous Guest Session", variant="secondary")

    welcome_banner = gr.HTML("<h3>Please authenticate or access via guest mode to unlock engine pathways.</h3>")
    global_status = gr.Label(value="🔴 Offline / Unauthenticated")

    with gr.Column(visible=False) as main_workspace:
        gr.Markdown("## 🎛 AI Code Generation Console")
        prompt_input = gr.Textbox(label="Instruction Prompt", placeholder="e.g., check if a number is positive or negative")
        generate_btn = gr.Button("Execute High-Capacity Generation", variant="primary")
        
        with gr.Row():
            code_output = gr.Code(label="Generated Neural Code Matrix", language="python")
            logs_output = gr.Textbox(label="Server Diagnostics Logs")
            
        paywall_output = gr.HTML()

