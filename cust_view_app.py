import gradio as gr
from supabase import create_client, Client
import pandas as pd
import requests

# --- 1. CONFIGURATION & BRAND ASSETS ---
SUPABASE_URL = "https://kcfpghyachxjhjkzkacw.supabase.co"
SUPABASE_KEY = "sb_publishable_A1CVqjhltmtBybZOzJsdfA_H0ABTC3c"

# Direct RAW URLs for GitHub assets to ensure 200 OK status
LOGO_URL = "https://raw.githubusercontent.com/ankitashri03/mishtee-logo.png/main/misTee_logo.png"
CSS_RAW_URL = "https://raw.githubusercontent.com/ankitashri03/mishtee-logo.png/main/style.py"

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch Custom Brand CSS with Resilient Fallback
try:
    response = requests.get(CSS_RAW_URL, timeout=5)
    if response.status_code == 200:
        raw_content = response.text
        # Extract string if wrapped in triple quotes in your GitHub file
        mishtee_css = raw_content.split('"""')[1] if '"""' in raw_content else raw_content
    else:
        raise Exception("CSS Not Found")
except Exception:
    # High-end Minimalist Fallback Style
    mishtee_css = """
    .gradio-container { background-color: #FAF9F6 !important; font-family: 'Serif'; }
    button.primary { background: #C06C5C !important; color: white !important; border: none !important; border-radius: 0px !important; }
    * { border-radius: 0px !important; box-shadow: none !important; }
    table { font-family: sans-serif !important; }
    """

# --- 2. CORE BACKEND FUNCTIONS ---

def get_trending_products():
    """Retrieves top 4 products by total quantity sold."""
    try:
        res = supabase.table("orders").select("qty_kg, products(sweet_name, variant_type)").execute()
        if not res.data:
            return pd.DataFrame(columns=["Artisanal Sweet", "Variant", "Total Sold (kg)"])
        
        raw_data = []
        for r in res.data:
            if r.get('products'):
                raw_data.append({
                    "Product": r['products']['sweet_name'], 
                    "Variant": r['products']['variant_type'], 
                    "Qty": r['qty_kg']
                })
        
        df = pd.DataFrame(raw_data)
        trending_df = df.groupby(["Product", "Variant"])["Qty"].sum().reset_index()
        trending_df = trending_df.sort_values(by="Qty", ascending=False).head(4)
        trending_df.columns = ["Artisanal Sweet", "Variant", "Total Sold (kg)"]
        return trending_df
    except Exception:
        return pd.DataFrame(columns=["Artisanal Sweet", "Variant", "Total Sold (kg)"])

def handle_login(phone_number):
    """Handles personalized greetings and historical data retrieval."""
    if not phone_number or not phone_number.startswith('9') or len(phone_number) != 10:
        return "⚠️ Please enter a valid 10-digit number starting with 9.", pd.DataFrame(), get_trending_products()

    try:
        # Fetch Customer Profile
        cust_res = supabase.table("customers").select("full_name").eq("phone", phone_number).execute()
        if not cust_res.data:
            return "Welcome! Profile not found. Please visit our store to register.", pd.DataFrame(), get_trending_products()
        
        name = cust_res.data[0]['full_name']
        greeting = f"## Namaste, {name} ji! \n*Your artisanal journey continues here.*"

        # Fetch Order History with Join
        order_res = supabase.table("orders").select(
            "order_date, qty_kg, order_value_inr, status, products(sweet_name)"
        ).eq("cust_phone", phone_number).order("order_date", desc=True).execute()

        df_data = [
            {
                "Date": row['order_date'],
                "Item": row['products']['sweet_name'] if row.get('products') else "MishTee Delight",
                "Qty (kg)": row['qty_kg'],
                "Value (₹)": row['order_value_inr'],
                "Status": row['status']
            } for row in order_res.data
        ]
        
        return greeting, pd.DataFrame(df_data), get_trending_products()
    except Exception as e:
        return f"System Error: {str(e)}", pd.DataFrame(), get_trending_products()

# --- 3. UI LAYOUT (Vertical Stack) ---

with gr.Blocks(css=mishtee_css, title="MishTee-Magic") as demo:
    # 1. Header & Logo
    with gr.Column(elem_id="header_container"):
        gr.Image(LOGO_URL, show_label=False, width=350, interactive=False, container=False)
        gr.Markdown("<center><h3>Purity Reimagined. Heritage Refined.</h3></center>")
        gr.HTML("<hr style='border: 0; border-top: 1px solid #D1CDC7;'>")

    # 2. Welcome Logic (Login)
    with gr.Row():
        with gr.Column(scale=2):
            phone_input = gr.Textbox(label="Enter Registered Phone (+91)", placeholder="98XXXXXXXX")
            login_btn = gr.Button("ACCESS YOUR VAULT", variant="primary")
        with gr.Column(scale=3):
            greeting_output = gr.Markdown("### Welcome to MishTee-Magic\n*Enter your credentials to reveal your artisanal history.*")

    gr.HTML("<br>")

    # 3. Data Presentation (Tabs)
    with gr.Tabs():
        with gr.TabItem("MY ORDER HISTORY"):
            history_table = gr.DataFrame(
                headers=["Date", "Item", "Qty (kg)", "Value (₹)", "Status"], 
                interactive=False
            )
        
        with gr.TabItem("TRENDING TODAY"):
            trending_table = gr.DataFrame(
                value=get_trending_products(), 
                interactive=False
            )

    # Event binding
    login_btn.click(
        fn=handle_login,
        inputs=[phone_input],
        outputs=[greeting_output, history_table, trending_table]
    )

    # Footer
    gr.Markdown("<center><small>MishTee-Magic | Artisanal Indian Sweets | A2 Milk & Organic Ingredients</small></center>")

# --- 4. LAUNCH ---
if __name__ == "__main__":
    # Keeping css in Blocks() to avoid TypeError in current Gradio versions
    demo.launch(debug=True)
