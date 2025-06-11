import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import time

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Set page config
st.set_page_config(
    page_title='Interactive Prompt Playground',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Custom CSS with !important to override Streamlit defaults
st.markdown("""
<style>
/* Import formal fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+Pro:wght@400;600;700&display=swap');

/* Base styles */
html, body, [class*="css"] {
    color: #111827 !important;
    font-family: 'Source Serif Pro', Georgia, serif !important;
}

/* Main container */
.main .block-container {
    max-width: 1200px !important;
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    margin: 0 auto !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem !important;
    }
}

/* Background color */
.stApp {
    background-color: #F9FAFB !important;
}

/* Custom containers */
.output-container {
    background-color: white !important;
    padding: 20px !important;
    border-radius: 10px !important;
    margin: 10px 0 !important;
    border-left: 4px solid #2563EB !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
}

.result-card {
    border: 1px solid #e0e0e0 !important;
    padding: 20px !important;
    margin: 15px 0 !important;
    border-radius: 8px !important;
    background-color: white !important;
    border-left: 3px solid #10B981 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

.result-card:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
}

/* Buttons */
.stButton > button {
    background-color: #2563EB !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.01em !important;
}

.stButton > button:hover {
    background-color: #1d4ed8 !important;
    box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2) !important;
    transform: translateY(-1px) !important;
}

/* Headers */
.main-header {
    background: linear-gradient(90deg, #2563EB, #10B981) !important;
    background-clip: text !important;
    -webkit-background-clip: text !important;
    color: transparent !important;
    font-weight: 800 !important;
    font-size: 2.5rem !important;
    margin-bottom: 1rem !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.02em !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #111827 !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.01em !important;
}

/* Parameter cards */
.parameter-card {
    background-color: white !important;
    padding: 15px !important;
    border-radius: 8px !important;
    margin-bottom: 15px !important;
    border: 1px solid #e0e0e0 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}

/* Sidebar */
.css-1d391kg, .css-163ttbj, .css-1wrcr25 {
    background-color: #F9FAFB !important;
}

.sidebar-header {
    color: #10B981 !important;
    font-weight: 600 !important;
    margin-top: 1rem !important;
    margin-bottom: 1rem !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.01em !important;
}

/* Expander */
.stExpander {
    border-radius: 8px !important;
    border: 1px solid #e0e0e0 !important;
    overflow: hidden !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px !important;
}

.stTabs [data-baseweb="tab"] {
    background-color: #F9FAFB !important;
    border-radius: 4px 4px 0 0 !important;
    padding: 10px 16px !important;
    border: 1px solid #e0e0e0 !important;
    border-bottom: none !important;
}

.stTabs [aria-selected="true"] {
    background-color: white !important;
    border-bottom: 2px solid #2563EB !important;
}

/* Sliders */
.stSlider [data-baseweb="slider"] {
    margin-top: 1rem !important;
    margin-bottom: 1rem !important;
}

.stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
    background-color: #2563EB !important;
    color: white !important;
}

.stSlider [data-baseweb="slider"] [data-testid="stTickBar"] > div {
    background-color: #2563EB !important;
}

/* Select boxes */
.stSelectbox [data-baseweb="select"] {
    background-color: white !important;
    border-radius: 6px !important;
}

/* Dataframe */
.stDataFrame {
    border-radius: 8px !important;
    overflow: hidden !important;
    border: 1px solid #e0e0e0 !important;
}

/* Additional responsive adjustments */
@media (max-width: 640px) {
    .main-header {
        font-size: 2rem !important;
    }
    
    .parameter-card {
        padding: 10px !important;
    }
    
    .output-container {
        padding: 15px !important;
    }
    
    /* Adjust metric cards on small screens */
    div[data-testid="stVerticalBlock"] > div[style*="margin: 30px 0;"] div[style*="padding: 20px"] {
        padding: 12px !important;
    }
}

/* Form labels and inputs */
label, .stTextInput > div > div > input, .stTextArea > div > div > textarea {
    font-family: 'Inter', sans-serif !important;
}

.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    font-family: 'Source Serif Pro', Georgia, serif !important;
    font-size: 1rem !important;
}

/* Formal styling for selectbox */
.stSelectbox > div > div > div {
    font-family: 'Source Serif Pro', Georgia, serif !important;
}

/* Formal styling for tabs */
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)

# Title and description with hero section
st.markdown('''
<div style="text-align: center; padding: 2.5rem 0; background: linear-gradient(135deg, #f6f9fc, #eef3f9); border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
    <h1 class="main-header">🧠 Interactive Prompt Playground</h1>
    <p style="font-size: 1.2rem; margin: 1rem auto 1.5rem; max-width: 700px; color: #4b5563;">
        Craft perfect AI responses by experimenting with different models and parameters
    </p>
    <div style="display: inline-flex; gap: 10px; margin-top: 0.5rem;">
        <span style="background-color: #2563EB; color: white; padding: 5px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 500;">OpenAI API</span>
        <span style="background-color: #10B981; color: white; padding: 5px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 500;">GPT Models</span>
        <span style="background-color: #6366F1; color: white; padding: 5px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 500;">Parameter Testing</span>
    </div>
</div>
''', unsafe_allow_html=True)

# Sidebar for model and system settings with improved styling
with st.sidebar:
    st.markdown('''
    <div style="text-align: center; padding: 1rem 0 1.5rem;">
        <div style="background: linear-gradient(135deg, #2563EB, #6366F1); width: 90px; height: 90px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
            <img src="https://img.icons8.com/fluency/96/000000/chatbot.png" width="60" style="filter: brightness(0) invert(1);"/>
        </div>
        <p style="margin-top: 10px; font-weight: 600; color: #2563EB;">AI Prompt Assistant</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
    <div style="background-color: white; padding: 15px 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <h3 class="sidebar-header" style="margin-top: 0;">🤖 Model Settings</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    model = st.selectbox(
        'Select Model',
        ['gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo'],
        help='Choose the OpenAI model to use'
    )
    
    st.markdown('''
    <div style="background-color: white; padding: 15px 20px; border-radius: 12px; margin: 20px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <h3 class="sidebar-header" style="margin-top: 0;">⚙️ System Configuration</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 0.9rem; margin: -10px 0 5px; color: #6b7280;">Choose the AI\'s personality</p>', unsafe_allow_html=True)
    system_role = st.selectbox(
        'Assistant Role',
        ['Product Description Writer', 'Customer Support Agent', 'Technical Expert', 'Creative Writer', 'Custom'],
        help='Choose a predefined role or select Custom to write your own'
    )
    
    if system_role == 'Product Description Writer':
        system_prompt = "You are a skilled copywriter that creates compelling and detailed product descriptions that highlight key features and benefits."
    elif system_role == 'Customer Support Agent':
        system_prompt = "You are a helpful customer support agent who provides friendly, clear, and solution-oriented responses to customer inquiries."
    elif system_role == 'Technical Expert':
        system_prompt = "You are a technical expert who explains complex concepts in clear, precise language with relevant examples."
    elif system_role == 'Creative Writer':
        system_prompt = "You are a creative writer who crafts engaging, imaginative content with vivid descriptions and compelling narratives."
    else:
        system_prompt = st.text_area(
            'Custom System Prompt',
            'You are a helpful assistant that provides detailed and accurate information.',
            help='Define the AI\'s role and behavior'
        )

    st.markdown('<hr style="margin: 2rem 0 1rem;">', unsafe_allow_html=True)
    st.markdown('''
    <div style="text-align: center; padding: 1rem; background-color: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <p style="margin-bottom: 5px; font-size: 0.9rem;">Made with ❤️ by AI Enthusiasts</p>
        <div style="display: flex; justify-content: center; gap: 10px; margin-top: 8px;">
            <a href="https://openai.com/" target="_blank" style="color: #6b7280; text-decoration: none; font-size: 0.8rem;">OpenAI</a>
            <span style="color: #d1d5db;">•</span>
            <a href="https://streamlit.io/" target="_blank" style="color: #6b7280; text-decoration: none; font-size: 0.8rem;">Streamlit</a>
            <span style="color: #d1d5db;">•</span>
            <a href="https://github.com/" target="_blank" style="color: #6b7280; text-decoration: none; font-size: 0.8rem;">GitHub</a>
        </div>
    </div>
    ''', unsafe_allow_html=True)

# Main content area - improved tabs with custom styling
tab_style = """
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        padding: 0 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 8px 8px 0 0;
        gap: 6px;
        padding: 10px 16px;
        background-color: #f3f4f6 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        border-bottom: 2px solid #2563EB !important;
    }
</style>
"""
st.markdown(tab_style, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🎯 Single Generation", "🔄 Batch Testing"])

with tab1:
    st.markdown('''
    <div style="background-color: white; padding: 25px; border-radius: 12px; margin: 10px 0 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <h3 style="margin-top: 0; color: #111827; display: flex; align-items: center; gap: 8px;">
            <span style="background-color: #2563EB; color: white; width: 24px; height: 24px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.8rem;">1</span>
            Create Your Prompt
        </h3>
    </div>
    ''', unsafe_allow_html=True)
    
    prompt_templates = {
        "Product Description": "Write a detailed description for [product name]",
        "Compare Products": "Compare [product A] and [product B] highlighting their key differences",
        "Technical Explanation": "Explain how [technical concept] works in simple terms",
        "Custom": ""
    }
    
    template_choice = st.selectbox("Prompt Template", list(prompt_templates.keys()))
    
    if template_choice != "Custom":
        user_prompt = st.text_area(
            'Your Prompt',
            prompt_templates[template_choice],
            height=100,
            help='Enter your prompt here'
        )
    else:
        user_prompt = st.text_area(
            'Your Prompt',
            '',
            height=100,
            help='Enter your custom prompt here'
        )
    
    # Parameters section with numbered heading
    st.markdown('''
    <div style="background-color: white; padding: 25px; border-radius: 12px; margin: 30px 0 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <h3 style="margin-top: 0; color: #111827; display: flex; align-items: center; gap: 8px;">
            <span style="background-color: #2563EB; color: white; width: 24px; height: 24px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.8rem;">2</span>
            Adjust Parameters
        </h3>
        <p style="color: #6b7280; margin-bottom: 20px;">Fine-tune how the AI responds to your prompt</p>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('''
        <div class="parameter-card" style="border-left: 4px solid #2563EB;">
            <h4 style="margin-top: 0; display: flex; align-items: center; gap: 8px;">
                <span style="color: #2563EB;">⚙️</span> Primary Parameters
            </h4>
            <p style="color: #6b7280; font-size: 0.9rem; margin-bottom: 15px;">These have the biggest impact on output</p>
        </div>
        ''', unsafe_allow_html=True)
        temperature = st.slider(
            'Temperature',
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help='Controls randomness: 0 = deterministic, 2 = very random'
        )
        
        max_tokens = st.select_slider(
            'Max Tokens',
            options=[50, 150, 300, 500, 750, 1000, 1500, 2000],
            value=300,
            help='Maximum length of the generated response'
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Advanced parameters with improved styling
        st.markdown('''
        <div class="parameter-card" style="border-left: 4px solid #10B981;">
            <h4 style="margin-top: 0; display: flex; align-items: center; gap: 8px;">
                <span style="color: #10B981;">🔧</span> Advanced Parameters
            </h4>
            <p style="color: #6b7280; font-size: 0.9rem; margin-bottom: 15px;">Fine-tune for specialized outputs</p>
        </div>
        ''', unsafe_allow_html=True)
        presence_penalty = st.slider(
            'Presence Penalty',
            min_value=-2.0,
            max_value=2.0,
            value=0.0,
            step=0.1,
            help='Penalizes new tokens based on whether they appear in the text so far'
        )
        
        frequency_penalty = st.slider(
            'Frequency Penalty',
            min_value=-2.0,
            max_value=2.0,
            value=0.0,
            step=0.1,
            help='Penalizes new tokens based on their frequency in the text so far'
        )
        
        stop_sequence = st.text_input(
            'Stop Sequence',
            help='The API will stop generating further tokens when the stop sequence is generated'
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate button with section header and spinner
    st.markdown('''
    <div style="background-color: white; padding: 25px; border-radius: 12px; margin: 30px 0 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <h3 style="margin-top: 0; color: #111827; display: flex; align-items: center; gap: 8px;">
            <span style="background-color: #2563EB; color: white; width: 24px; height: 24px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.8rem;">3</span>
            Generate AI Response
        </h3>
        <p style="color: #6b7280; margin-bottom: 0;">Click the button below to generate your AI response</p>
    </div>
    ''', unsafe_allow_html=True)
    
    generate_col1, generate_col2, generate_col3 = st.columns([1, 1, 1])
    with generate_col2:
        if st.button('Generate Response 🚀', type='primary', key='generate_single', use_container_width=True):
            if not user_prompt.strip():
                st.error('Please enter a prompt before generating a response.')
            else:
                with st.spinner('🧠 AI is crafting your response...'):
                    try:
                        start_time = time.time()
                        
                        messages = [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ]
        
                        response = client.chat.completions.create(
                            model=model,
                            messages=messages,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            presence_penalty=presence_penalty,
                            frequency_penalty=frequency_penalty,
                            stop=[stop_sequence] if stop_sequence else None
                        )
                        
                        end_time = time.time()
                        
                        # Enhanced output container
                        st.markdown('''
                        <div style="background-color: white; padding: 25px; border-radius: 12px; margin: 30px 0 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.08);">
                            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                                <div style="background-color: #10B981; color: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                                    <span style="font-size: 18px;">✓</span>
                                </div>
                                <h3 style="margin: 0; color: #111827;">Generated Response</h3>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        with st.container():
                            st.markdown('''
                            <div class="output-container" style="background-color: white; padding: 25px; border-radius: 12px; margin: 0; border-left: 4px solid #2563EB; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                                <div style="color: #111827; font-family: 'Source Serif Pro', Georgia, serif; line-height: 1.6;">
                            ''', unsafe_allow_html=True)
                            st.markdown(response.choices[0].message.content)
                            st.markdown('</div></div>', unsafe_allow_html=True)
    
                        # Display enhanced metrics
                        st.markdown('<div style="margin: 30px 0;">', unsafe_allow_html=True)
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.markdown('''
                            <div style="background-color: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                                <p style="margin: 0 0 5px; color: #6b7280; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">Response Time</p>
                                <h3 style="margin: 0; font-size: 1.5rem; color: #2563EB; font-weight: 600;">
                            ''', unsafe_allow_html=True)
                            st.markdown(f"{(end_time - start_time):.2f}s", unsafe_allow_html=True)
                            st.markdown('</h3></div>', unsafe_allow_html=True)
                        with col_b:
                            st.markdown('''
                            <div style="background-color: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                                <p style="margin: 0 0 5px; color: #6b7280; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">Tokens Used</p>
                                <h3 style="margin: 0; font-size: 1.5rem; color: #10B981; font-weight: 600;">
                            ''', unsafe_allow_html=True)
                            st.markdown(f"{len(response.choices[0].message.content.split())} (est.)", unsafe_allow_html=True)
                            st.markdown('</h3></div>', unsafe_allow_html=True)
                        with col_c:
                            st.markdown('''
                            <div style="background-color: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                                <p style="margin: 0 0 5px; color: #6b7280; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">Model</p>
                                <h3 style="margin: 0; font-size: 1.5rem; color: #6366F1; font-weight: 600;">
                            ''', unsafe_allow_html=True)
                            st.markdown(f"{model}", unsafe_allow_html=True)
                            st.markdown('</h3></div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
    
                        # Display parameters used
                        with st.expander('Parameters Used'):
                            st.json({
                                'model': model,
                                'system_prompt': system_prompt,
                                'temperature': temperature,
                                'max_tokens': max_tokens,
                                'presence_penalty': presence_penalty,
                                'frequency_penalty': frequency_penalty,
                                'stop_sequence': stop_sequence if stop_sequence else None
                            })
    
                    except Exception as e:
                        st.error(f'Error: {str(e)}')

with tab2:
    st.markdown('<h3>Batch Testing Configuration</h3>', unsafe_allow_html=True)
    st.markdown('Test multiple parameter combinations at once to compare outputs')
    
    batch_prompt = st.text_area(
        'Prompt for Batch Testing',
        'Write a tagline for a new smartphone',
        height=80,
        help='Enter the prompt to use for all batch tests'
    )
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        temperatures = st.multiselect(
            'Test Temperatures',
            [0.0, 0.3, 0.7, 1.0, 1.5],
            default=[0.0, 0.7, 1.5]
        )
        
    with col4:
        max_tokens_list = st.multiselect(
            'Test Max Tokens',
            [50, 100, 150, 300, 500],
            default=[50, 150, 300]
        )
    
    with col5:
        models = st.multiselect(
            'Test Models',
            ['gpt-3.5-turbo', 'gpt-4'],
            default=['gpt-3.5-turbo']
        )
    
    with st.expander('Advanced Batch Parameters'):
        col6, col7 = st.columns(2)
        
        with col6:
            presence_penalties = st.multiselect(
                'Test Presence Penalties',
                [-1.0, 0.0, 1.0, 2.0],
                default=[0.0, 1.0]
            )
        
        with col7:
            frequency_penalties = st.multiselect(
                'Test Frequency Penalties',
                [-1.0, 0.0, 1.0, 2.0],
                default=[0.0, 1.0]
            )
    
    # Calculate total combinations
    total_combinations = len(temperatures) * len(max_tokens_list) * len(models) * len(presence_penalties) * len(frequency_penalties)
    st.info(f"This will generate {total_combinations} different outputs. Estimated time: {total_combinations * 2} seconds.")
    
    # Generate button with spinner
    if st.button('Run Batch Test', type='primary', key='run_batch'):
        if not batch_prompt.strip():
            st.error('Please enter a prompt before running batch tests.')
        elif total_combinations > 24:
            st.error('Too many combinations. Please reduce the number of parameters to test (maximum 24 combinations recommended).')
        else:
            with st.spinner(f'Running {total_combinations} tests...'):
                try:
                    results = []
                    progress_bar = st.progress(0)
                    
                    counter = 0
                    for model_choice in models:
                        for temp in temperatures:
                            for tokens in max_tokens_list:
                                for pres in presence_penalties:
                                    for freq in frequency_penalties:
                                        messages = [
                                            {"role": "system", "content": system_prompt},
                                            {"role": "user", "content": batch_prompt}
                                        ]
    
                                        response = client.chat.completions.create(
                                            model=model_choice,
                                            messages=messages,
                                            temperature=temp,
                                            max_tokens=tokens,
                                            presence_penalty=pres,
                                            frequency_penalty=freq,
                                            stop=[stop_sequence] if stop_sequence else None
                                        )
    
                                        results.append({
                                            'Model': model_choice,
                                            'Temperature': temp,
                                            'Max Tokens': tokens,
                                            'Presence Penalty': pres,
                                            'Frequency Penalty': freq,
                                            'Output': response.choices[0].message.content
                                        })
                                        
                                        counter += 1
                                        progress_bar.progress(counter / total_combinations)
    
                    # Display results in a table
                    st.markdown('### Batch Test Results')
                    df = pd.DataFrame(results)
                    
                    # Add column for output length
                    df['Output Length'] = df['Output'].apply(lambda x: len(x.split()))
                    
                    st.dataframe(df)
                    
                    # Option to download as CSV
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download Results as CSV",
                        data=csv,
                        file_name="batch_test_results.csv",
                        mime="text/csv",
                    )
    
                    # Display individual results
                    st.markdown('### Individual Results')
                    for idx, result in enumerate(results):
                        with st.expander(f'Result {idx + 1} - {result["Model"]} (Temp: {result["Temperature"]})'):
                            st.markdown(f"""
                            **Parameters:**
                            - Model: {result['Model']}
                            - Temperature: {result['Temperature']}
                            - Max Tokens: {result['Max Tokens']}
                            - Presence Penalty: {result['Presence Penalty']}
                            - Frequency Penalty: {result['Frequency Penalty']}
                            
                            **Output:**
                            """)
                            st.markdown(f'<div class="result-card">{result["Output"]}</div>', unsafe_allow_html=True)
    
                except Exception as e:
                    st.error(f'Error: {str(e)}')

# Add helpful information
st.markdown('---')
with st.expander('📚 Parameter Guide'):
    col8, col9 = st.columns(2)
    
    with col8:
        st.markdown("""
        ### Temperature
        - **0.0 - 0.3**: Focused, deterministic responses
        - **0.4 - 0.7**: Balanced creativity and coherence
        - **0.8 - 1.2**: More creative, varied outputs
        - **1.3 - 2.0**: Highly random, experimental results
        
        ### Max Tokens
        Controls the maximum length of the generated response:
        - **50-150**: Short responses, taglines
        - **300-500**: Paragraphs, short descriptions
        - **1000+**: Long-form content, detailed explanations
        """)
    
    with col9:
        st.markdown("""
        ### Presence & Frequency Penalty
        - **Negative values**: May repeat content more often
        - **0.0**: Neutral behavior
        - **Positive values**: Encourages variety, discourages repetition
        
        ### Models
        - **GPT-3.5-Turbo**: Faster, more economical
        - **GPT-4**: More capable, better reasoning, more expensive
        """)