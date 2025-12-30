mishtee_css = """
/* Import high-end fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Inter:wght@300;400&display=swap');

/* Global Container and Background */
.gradio-container {
    background-color: #FAF9F6 !important;
    font-family: 'Inter', sans-serif;
    color: #333333;
}

/* Headings: Elegant Serif Style */
h1, h2, h3, .section-header {
    font-family: 'Playfair Display', serif !important;
    letter-spacing: 0.05em;
    font-weight: 400 !important;
    color: #333333;
    margin-bottom: 1.5rem !important;
}

/* Typography for Tables and Data */
table, .gr-table, .gr-dataframe {
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    font-size: 0.95rem;
    border-collapse: collapse !important;
}

/* Remove Shadows and Enforce Sharp Lines */
* {
    box-shadow: none !important;
    border-radius: 0px !important;
}

/* High-End Padding and Border Styling */
.block, .form, .gr-box {
    padding: 2rem !important;
    border: 1px solid #D1CDC7 !important;
    background-color: transparent !important;
    margin-bottom: 2rem !important;
}

/* Button: Sober Terracotta */
button.primary, .gr-button-lg, #submit-btn {
    background: #C06C5C !important;
    color: #FFFFFF !important;
    border: 1px solid #C06C5C !important;
    padding: 0.8rem 2rem !important;
    font-family: 'Inter', sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

button.primary:hover {
    background: #A65D4F !important;
    border-color: #A65D4F !important;
}

/* Input Fields */
input, textarea, .gr-input {
    background-color: transparent !important;
    border: 1px solid #D1CDC7 !important;
    padding: 0.6rem !important;
}

/* Horizontal Rule for Visual Separation */
hr {
    border: 0;
    border-top: 1px solid #D1CDC7;
    margin: 3rem 0;
}
"""
