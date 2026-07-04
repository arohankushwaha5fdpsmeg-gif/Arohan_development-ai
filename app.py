# AROHAN ENGINE: HIGH-DENSITY PRODUCTION CORE MATRICES
import os, sqlite3, random, stripe, gradio as gr
from datetime import datetime, timedelta

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_51Tke3WRsVgVw9kTXB7nWOrvb1jGUnCuTAqwgcX5OA7r7hxVh534pcyg5Y0D989GwT4CQmwsfN9SezJyb8gEdjXDF00OEi2JoDS")
os.makedirs("data", exist_ok=True)
DB_PATH = "data/arohan_global_production.db"

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("CREATE TABLE IF NOT EXISTS server_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, prompt TEXT, generated_code TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
        c.execute("CREATE TABLE IF NOT EXISTS cloud_users (username TEXT PRIMARY KEY, password TEXT, tokens_remaining INTEGER, is_premium INTEGER DEFAULT 0, last_exhausted_time TEXT)")
init_db()

def auth_sync(user, pwd, is_reg=False):
    user, pwd = user.strip().lower(), pwd.strip()
    if not user or not pwd: return "🔴 Boundary Violation", "<h3>Inputs cannot be null</h3>", gr.update(visible=False), "", gr.update(visible=True)
    with sqlite3.connect(DB_PATH) as c:
        if is_reg:
            if "guest_" in user: return "❌ Layout Restricted", "<h3>Illegal namespace prefix</h3>", gr.update(visible=False), "", gr.update(visible=True)
            try: c.execute("INSERT INTO cloud_users VALUES (?, ?, 15, 0, NULL)", (user, pwd))
            except sqlite3.IntegrityError: return "❌ Vector Collision", "<h3>Identity key duplication</h3>", gr.update(visible=False), "", gr.update(visible=True)
            return "🍏 Active Schema", f"<h3>Registration successful for node: {user}</h3>", gr.update(visible=False), "", gr.update(visible=True)
        prof = c.execute("SELECT tokens_remaining, is_premium, last_exhausted_time FROM cloud_users WHERE username=? AND password=?", (user, pwd)).fetchone()
        if not prof: return "❌ Access Denied", "<h3>Invalid cryptographic identity keys</h3>", gr.update(visible=False), "", gr.update(visible=True)
        tk, prem, exh = prof
        if prem == 0 and tk == 0 and exh:
            if (datetime.now() - datetime.strptime(exh, "%Y-%m-%d %H:%M:%S")) >= timedelta(hours=24):
                tk = 15
                c.execute("UPDATE cloud_users SET tokens_remaining=15, last_exhausted_time=NULL WHERE username=?", (user,))
    return ("👑 Premium Node" if prem == 1 else f"🍏 Metrics: {tk}/15 Units", f"<h3 style='color:#4F46E5;'>✅ Connection Active: Synchronized node {user}</h3>", gr.update(visible=True), user, gr.update(visible=False))

def guest_proxy():
    pid = f"guest_{random.randint(100000, 999999)}"
    with sqlite3.connect(DB_PATH) as c: c.execute("INSERT INTO cloud_users VALUES (?, 'proxy', 15, 0, NULL)", (pid,))
    return f"🍏 Allocation: 15/15 Units", f"<h3 style='color:#059669;'>🚪 Ephemeral Tunnel Initialized: {pid}</h3>", gr.update(visible=True), pid, gr.update(visible=False)

def compile_inference(prompt, user):
    if not user: return "# LOCKOUT", "Handshake missing", "<h3>Terminal Fault</h3>", "🔴 Encrypted"
    with sqlite3.connect(DB_PATH) as c:
        tk, prem = c.execute("SELECT tokens_remaining, is_premium FROM cloud_users WHERE username=?", (user,)).fetchone()
        if prem == 0 and tk <= 0:
            return "# CONSTRAINTS EXCEEDED", "Resource exhaustion.", f"<div style='background:#FEF2F2; padding:15px;'><h3>🛑 Vector Quota Exhausted</h3></div>", "🔴 Fault"
        val = "Unlimited" if prem == 1 else tk - 1
        ts = f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'" if val == 0 else "NULL"
        if prem == 0: c.execute(f"UPDATE cloud_users SET tokens_remaining={val}, last_exhausted_time={ts} WHERE username='{user}'")
        out = f"# Compilation Pipeline Successful\\ndef arohan_matrix():\\n    # Node Task Matrix: {prompt}\\n    return True"
        c.execute("INSERT INTO server_logs (username, prompt, generated_code) VALUES (?, ?, ?)", (user, prompt, out))
    return out, "Matrix execution clean.", "<h3>Inference Resolved</h3>", f"👑 Active" if val == "Unlimited" else f"🍏 Remaining: {val} Units"

with gr.Blocks(title="Arohan Engine", head='<meta name="description" content="Arohan Code Generator Matrix Engine."><meta name="keywords" content="Arohan Global, AI Code Generator">', theme=gr.themes.Soft()) as demo:
    ust = gr.State("")
    gr.Markdown("# 🚀 AROHAN GLOBAL DEVELOPMENT ENGINE")
    with gr.Row() as ap:
        with gr.Tab("Sign In"):
            u, p = gr.Textbox(label="Username"), gr.Textbox(label="Password", type="password")
            li = gr.Button("Authenticate Core Node")
        with gr.Tab("Register"):
            ru, rp = gr.Textbox(label="Node Namespace"), gr.Textbox(label="Node Security Key", type="password")
            reg = gr.Button("Provision New Schema")
            ro = gr.HTML()
        with gr.Column():
            gt = gr.Button("Deploy Ephemeral Guest Tunnel", variant="secondary")
    wb, gst = gr.HTML("<h3>Core Locked</h3>"), gr.Label(value="🔴 Offline Matrix")
    with gr.Column(visible=False) as ws:
        pi = gr.Textbox(label="Instruction Prompt Vector")
        ex = gr.Button("Execute Core Pipeline", variant="primary")
        with gr.Row():
            co, lo = gr.Code(label="Output Stream", language="python"), gr.Textbox(label="Diagnostic Log Stream")
        po = gr.HTML()
    reg.click(lambda u, p: auth_sync(u, p, True), [ru, rp], [ro])
    li.click(auth_sync, [u, p], [gst, wb, ws, ust, ap])
    gt.click(guest_proxy, [], [gst, wb, ws, ust, ap])
    ex.click(compile_inference, [pi, ust], [co, lo, po, gst])

if __name__ == "__main__":
    os.environ["GRADIO_SERVER_NAME"] = "0.0.0.0"
    demo.queue().launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)), inline=False, share=False)
