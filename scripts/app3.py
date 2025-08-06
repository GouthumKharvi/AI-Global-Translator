import streamlit as st
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import tempfile
import os
import base64
import fitz  # PyMuPDF
import docx
from PIL import Image
import datetime
import io
import time

AudioSegment.converter = "ffmpeg"

# Advanced Page Configuration
st.set_page_config(
    page_title="🌍 AI Translator APP", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS with 3D animations and futuristic design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');
    
    /* Global Variables */
    :root {
        --primary-glow: #00d4ff;
        --secondary-glow: #ff006e;
        --accent-glow: #8338ec;
        --success-glow: #06ffa5;
        --bg-dark: #0a0a0a;
        --bg-card: rgba(15, 15, 23, 0.95);
        --text-primary: #ffffff;
        --text-secondary: #b8b8b8;
    }
    
    /* Advanced Background */
    .main {
        background: linear-gradient(45deg, #0a0a0a, #1a1a2e, #16213e);
        position: relative;
        overflow: hidden;
    }
    
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 0, 110, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(131, 56, 236, 0.1) 0%, transparent 50%);
        animation: backgroundShift 20s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes backgroundShift {
        0%, 100% { opacity: 1; transform: scale(1) rotate(0deg); }
        50% { opacity: 0.8; transform: scale(1.1) rotate(2deg); }
    }
    
    /* Floating particles animation */
    .main::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, rgba(0, 212, 255, 0.3), transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255, 0, 110, 0.3), transparent),
            radial-gradient(1px 1px at 90px 40px, rgba(131, 56, 236, 0.3), transparent);
        background-repeat: repeat;
        background-size: 150px 150px;
        animation: particleFloat 30s linear infinite;
        z-index: -1;
    }
    
    @keyframes particleFloat {
        0% { transform: translateY(0px) translateX(0px); }
        100% { transform: translateY(-100px) translateX(50px); }
    }
    
    /* Advanced Header with 3D effects - Moved Higher */
    .futuristic-header {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(255, 0, 110, 0.15));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 25px;
        padding: 2rem 2rem;
        margin: 0.5rem 0 1.5rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 20px 50px rgba(0, 212, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transform-style: preserve-3d;
        animation: headerFloat 6s ease-in-out infinite;
    }
    
    @keyframes headerFloat {
        0%, 100% { transform: translateY(0px) rotateX(0deg); }
        50% { transform: translateY(-10px) rotateX(2deg); }
    }
    
    .futuristic-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(transparent, rgba(0, 212, 255, 0.1), transparent 30%);
        animation: headerRotate 8s linear infinite;
        z-index: -1;
    }
    
    @keyframes headerRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .futuristic-header h1 {
        font-family: 'Orbitron', monospace;
        font-size: 4rem;
        font-weight: 900;
        color: var(--text-primary);
        margin: 0;
        text-shadow: 
            0 0 20px var(--primary-glow),
            0 0 40px rgba(0, 212, 255, 0.5),
            0 0 60px rgba(0, 212, 255, 0.3);
        animation: textGlow 3s ease-in-out infinite alternate;
        transform: translateZ(20px);
    }
    
    @keyframes textGlow {
        0% { text-shadow: 0 0 20px var(--primary-glow), 0 0 40px rgba(0, 212, 255, 0.5); }
        100% { text-shadow: 0 0 30px var(--primary-glow), 0 0 60px rgba(0, 212, 255, 0.8); }
    }
    
    .futuristic-header p {
        font-family: 'Exo 2', sans-serif;
        font-size: 1.3rem;
        color: var(--text-secondary);
        margin: 1rem 0 0 0;
        transform: translateZ(10px);
    }
    
    /* Advanced Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(15, 15, 23, 0.95), rgba(26, 26, 46, 0.95));
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    /* Holographic Cards */
    .holo-card {
        background: rgba(15, 15, 23, 0.7);
        backdrop-filter: blur(25px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(0, 212, 255, 0.3);
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 15px 35px rgba(0, 0, 0, 0.3),
            0 5px 15px rgba(0, 212, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transform: translateZ(0);
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
    }
    
    .holo-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .holo-card:hover {
        transform: translateY(-10px) rotateX(5deg);
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.4),
            0 10px 25px rgba(0, 212, 255, 0.2);
        border-color: rgba(0, 212, 255, 0.6);
    }
    
    .holo-card:hover::before {
        left: 100%;
    }
    
    /* Language Selection Container */
    .language-container {
        background: rgba(15, 15, 23, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(131, 56, 236, 0.4);
        position: relative;
        box-shadow: 
            0 10px 30px rgba(131, 56, 236, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    
    /* Quantum Buttons */
    .stButton > button {
        background: linear-gradient(45deg, rgba(0, 212, 255, 0.8), rgba(131, 56, 236, 0.8));
        color: var(--text-primary);
        border: 1px solid rgba(0, 212, 255, 0.5);
        border-radius: 15px;
        padding: 1rem 2rem;
        font-family: 'Exo 2', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
        box-shadow: 
            0 5px 15px rgba(0, 212, 255, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transform: translateZ(0);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 
            0 15px 30px rgba(0, 212, 255, 0.4),
            0 5px 15px rgba(131, 56, 236, 0.3);
        background: linear-gradient(45deg, rgba(0, 212, 255, 1), rgba(131, 56, 236, 1));
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02);
    }
    
    /* Enhanced Swap Button */
    .swap-button {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 2.5rem;
    }
    
    .swap-btn {
        background: radial-gradient(circle, rgba(255, 0, 110, 0.9), rgba(0, 212, 255, 0.9)) !important;
        border: 3px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 50% !important;
        width: 80px !important;
        height: 80px !important;
        font-size: 2rem !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        animation: swapPulse 2s ease-in-out infinite !important;
        box-shadow: 
            0 0 25px rgba(255, 0, 110, 0.6),
            0 0 50px rgba(0, 212, 255, 0.4),
            inset 0 2px 0 rgba(255, 255, 255, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1) !important;
    }
    
    .swap-btn:hover {
        transform: scale(1.1) rotate(180deg) !important;
        box-shadow: 
            0 0 35px rgba(255, 0, 110, 0.8),
            0 0 70px rgba(0, 212, 255, 0.6) !important;
    }
    
    @keyframes swapPulse {
        0%, 100% { transform: scale(1) rotate(0deg); box-shadow: 0 0 25px rgba(255, 0, 110, 0.6), 0 0 50px rgba(0, 212, 255, 0.4); }
        50% { transform: scale(1.05) rotate(10deg); box-shadow: 0 0 35px rgba(255, 0, 110, 0.8), 0 0 70px rgba(0, 212, 255, 0.6); }
    }
    
    /* Center Translate Button */
    .center-translate-button {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
        position: relative;
    }
    
    .center-translate-button .stButton > button {
        background: linear-gradient(45deg, rgba(255, 0, 110, 0.9), rgba(0, 212, 255, 0.9)) !important;
        font-size: 1.2rem !important;
        padding: 1.5rem 3rem !important;
        border-radius: 25px !important;
        box-shadow: 
            0 10px 30px rgba(255, 0, 110, 0.4),
            0 0 40px rgba(0, 212, 255, 0.3) !important;
        animation: translatePulse 3s ease-in-out infinite !important;
    }
    
    @keyframes translatePulse {
        0%, 100% { 
            box-shadow: 0 10px 30px rgba(255, 0, 110, 0.4), 0 0 40px rgba(0, 212, 255, 0.3);
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 15px 40px rgba(255, 0, 110, 0.6), 0 0 60px rgba(0, 212, 255, 0.5);
            transform: scale(1.02);
        }
    }
    
    /* Live Translation Indicator */
    .live-indicator {
        position: absolute;
        top: 10px;
        right: 15px;
        background: linear-gradient(45deg, rgba(6, 255, 165, 0.8), rgba(0, 212, 255, 0.8));
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        animation: livePulse 1.5s ease-in-out infinite;
        box-shadow: 0 0 15px rgba(6, 255, 165, 0.5);
    }
    
    @keyframes livePulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(0.95); }
    }
    
    /* Advanced Text Areas */
    .stTextArea > div > div > textarea {
        background: rgba(15, 15, 23, 0.9);
        border: 2px solid rgba(0, 212, 255, 0.3);
        border-radius: 15px;
        color: var(--text-primary);
        font-family: 'Exo 2', sans-serif;
        font-size: 1.1rem;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-glow);
        box-shadow: 
            inset 0 2px 10px rgba(0, 0, 0, 0.3),
            0 0 20px rgba(0, 212, 255, 0.3);
        outline: none;
    }
    
    /* Advanced Select Boxes */
    .stSelectbox > div > div {
        background: rgba(15, 15, 23, 0.9);
        border: 2px solid rgba(131, 56, 236, 0.3);
        border-radius: 15px;
        color: var(--text-primary);
        backdrop-filter: blur(10px);
        font-family: 'Exo 2', sans-serif;
    }
    
    /* Page Headers with Holographic Effect */
    .page-header {
        background: linear-gradient(45deg, rgba(0, 212, 255, 0.1), rgba(255, 0, 110, 0.1));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 255, 0.4);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        animation: headerShimmer 4s ease-in-out infinite;
    }
    
    @keyframes headerShimmer {
        0%, 100% { box-shadow: 0 5px 25px rgba(0, 212, 255, 0.2); }
        50% { box-shadow: 0 5px 25px rgba(255, 0, 110, 0.2); }
    }
    
    .page-header h2 {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
        text-shadow: 0 0 20px var(--primary-glow);
    }
    
    /* Advanced History Cards */
    .history-item {
        background: rgba(15, 15, 23, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid var(--primary-glow);
        position: relative;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .history-item:hover {
        transform: translateX(10px);
        border-left-color: var(--secondary-glow);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    
    .history-timestamp {
        color: #00d4ff;
        font-family: 'Orbitron', monospace;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .history-original {
    color: #ffffff;
    margin-bottom: 0.5rem;
    word-wrap: break-word;
}

.history-translation {
    color: #ffffff;
    word-wrap: break-word;
}
    
    .history-label-original {
        color: #8338ec;
        font-weight: bold;
        word-wrap: break-word;
    }
    
    .history-label-translation {
        color: #ff006e;
        font-weight: bold;
        word-wrap: break-word;
    }
    
    /* File Upload Area */
    .uploadedFile {
        background: rgba(15, 15, 23, 0.8);
        border: 2px dashed rgba(0, 212, 255, 0.5);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        transition: all 0.3s ease;
    }
    
    .uploadedFile:hover {
        border-color: var(--success-glow);
        box-shadow: 0 0 20px rgba(6, 255, 165, 0.2);
    }
    
    /* Status Messages */
    .stSuccess {
        background: rgba(6, 255, 165, 0.1);
        border: 1px solid rgba(6, 255, 165, 0.3);
        border-radius: 10px;
        backdrop-filter: blur(10px);
        color: var(--success-glow);
    }
    
    .stInfo {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 10px;
        backdrop-filter: blur(10px);
        color: var(--primary-glow);
    }
    
    .stError {
        background: rgba(255, 0, 110, 0.1);
        border: 1px solid rgba(255, 0, 110, 0.3);
        border-radius: 10px;
        backdrop-filter: blur(10px);
        color: var(--secondary-glow);
    }
    
    /* Navigation Enhancement */
    .stRadio > div {
        background: rgba(15, 15, 23, 0.6);
        border-radius: 15px;
        padding: 1rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    /* Footer Enhancement */
    .futuristic-footer {
        background: rgba(15, 15, 23, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(131, 56, 236, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 3rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .futuristic-footer::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(131, 56, 236, 0.05), transparent);
        animation: footerGlow 6s linear infinite;
    }
    
    @keyframes footerGlow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .futuristic-header h1 { font-size: 2.5rem; }
        .page-header h2 { font-size: 2rem; }
        .holo-card { padding: 1.5rem; }
        .swap-btn { width: 60px !important; height: 60px !important; font-size: 1.5rem !important; }
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 15, 23, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, var(--primary-glow), var(--accent-glow));
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, var(--secondary-glow), var(--primary-glow));
    }
</style>
""", unsafe_allow_html=True)

# Futuristic Main Header - Moved Higher
st.markdown("""
<div class="futuristic-header">
    <h1>🌍 AI GLOBAL LANGUAGE TRANSLATOR</h1>
    <p>Experience the future of global langauge translation with advanced AI technology</p>
</div>
""", unsafe_allow_html=True)

# Enhanced Sidebar Navigation
st.sidebar.markdown("""
<div style="text-align: center; padding: 1.5rem; background: linear-gradient(45deg, rgba(0, 212, 255, 0.1), rgba(131, 56, 236, 0.1)); border-radius: 20px; margin-bottom: 2rem; backdrop-filter: blur(20px); border: 1px solid rgba(0, 212, 255, 0.3);">
    <h2 style="color: #ffffff; margin: 0; font-family: 'Orbitron', monospace; text-shadow: 0 0 15px #00d4ff;">🤖Menu</h2>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio("Go to", [
    "📝 Text Translator", 
    "🎙️ Speech Translator", 
    "📁 File Translator", 
    "📜 History"
])

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; padding: 1.5rem; background: rgba(15, 15, 23, 0.8); border-radius: 20px; backdrop-filter: blur(20px); border: 1px solid rgba(255, 0, 110, 0.3);">
    <h3 style="color: #ffffff; margin-bottom: 1rem; font-family: 'Orbitron', monospace;">👤 Connect with Me</h3>
""", unsafe_allow_html=True)

st.sidebar.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-GouthumKharvi-blue?logo=linkedin&style=for-the-badge)](https://www.linkedin.com/in/gouthum-kharvi-2366a6219/)")
st.sidebar.markdown("[![GitHub](https://img.shields.io/badge/GitHub-GouthumKharvi-black?logo=github&style=for-the-badge)](https://github.com/GouthumKharvi)")

st.sidebar.markdown("</div>", unsafe_allow_html=True)

translator = Translator()

# Initialize session state variables
if 'history' not in st.session_state:
    st.session_state.history = []

if 'source_lang' not in st.session_state:
    st.session_state.source_lang = 'English'

if 'target_lang' not in st.session_state:
    st.session_state.target_lang = 'Kannada'

if 'live_translation_enabled' not in st.session_state:
    st.session_state.live_translation_enabled = True

LANGUAGES = {
    'English': 'en', 'Kannada': 'kn', 'Hindi': 'hi', 'Telugu': 'te',
    'Tamil': 'ta', 'Malayalam': 'ml', 'French': 'fr', 'German': 'de', 'Spanish': 'es',
    'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar', 'Armenian': 'hy',
    'Azerbaijani': 'az', 'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bosnian': 'bs',
    'Bulgarian': 'bg', 'Burmese': 'my', 'Catalan': 'ca', 'Cebuano': 'ceb', 'Chichewa': 'ny',
    'Chinese (Simplified)': 'zh-CN', 'Chinese (Traditional)': 'zh-TW', 'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs',
    'Danish': 'da', 'Dutch': 'nl', 'Esperanto': 'eo', 'Estonian': 'et', 'Filipino': 'tl',
    'Finnish': 'fi', 'Galician': 'gl', 'Georgian': 'ka', 'Greek': 'el', 'Gujarati': 'gu',
    'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'iw', 'Hmong': 'hmn',
    'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig', 'Indonesian': 'id', 'Irish': 'ga',
    'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jw', 'Kazakh': 'kk', 'Khmer': 'km',
    'Kinyarwanda': 'rw', 'Korean': 'ko', 'Kurdish (Kurmanji)': 'ku', 'Kyrgyz': 'ky', 'Lao': 'lo',
    'Latin': 'la', 'Latvian': 'lv', 'Lithuanian': 'lt', 'Luxembourgish': 'lb', 'Macedonian': 'mk',
    'Malagasy': 'mg', 'Malay': 'ms', 'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr',
    'Mongolian': 'mn', 'Nepali': 'ne', 'Norwegian': 'no', 'Odia': 'or', 'Pashto': 'ps',
    'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt', 'Punjabi': 'pa', 'Romanian': 'ro',
    'Russian': 'ru', 'Samoan': 'sm', 'Scots Gaelic': 'gd', 'Serbian': 'sr', 'Sesotho': 'st',
    'Shona': 'sn', 'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk', 'Slovenian': 'sl',
    'Somali': 'so', 'Sundanese': 'su', 'Swahili': 'sw', 'Swedish': 'sv', 'Tajik': 'tg',
    'Thai': 'th', 'Turkish': 'tr', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uyghur': 'ug',
    'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh', 'Yiddish': 'yi',
    'Yoruba': 'yo', 'Zulu': 'zu', 'Tatar': 'tt', 'Uighur': 'ug', 'Tsonga': 'ts'
}

def swap_languages():
    """Swap source and target languages"""
    temp_source = st.session_state.source_lang
    st.session_state.source_lang = st.session_state.target_lang
    st.session_state.target_lang = temp_source

def live_translate(text, source_lang, target_lang):
    """Perform live translation with error handling"""
    if not text or not text.strip():
        return ""
    
    try:
        result = translator.translate(
            text,
            src=LANGUAGES[source_lang],
            dest=LANGUAGES[target_lang]
        )
        return result.text
    except Exception as e:
        return f"Translation error: {str(e)}"

# Enhanced Language Selection UI
st.markdown('<div class="language-container">', unsafe_allow_html=True)
with st.container():
    col1, col_swap, col2 = st.columns([4, 2, 4])
    with col1:
        source_lang = st.selectbox(
            "🌐 Source Language", 
            list(LANGUAGES.keys()), 
            index=list(LANGUAGES.keys()).index(st.session_state.source_lang),
            key="source_language_selector"
        )
        st.session_state.source_lang = source_lang
    
    with col_swap:
        st.markdown('<div class="swap-button">', unsafe_allow_html=True)
        if st.button("⇄", key="swap_languages", help="Quantum Language Swap", use_container_width=True):
            swap_languages()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        target_lang = st.selectbox(
            "🎯 Target Language", 
            list(LANGUAGES.keys()), 
            index=list(LANGUAGES.keys()).index(st.session_state.target_lang),
            key="target_language_selector"
        )
        st.session_state.target_lang = target_lang

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------
# PAGE: Text Translator
# ----------------------------------------
if page == "📝 Text Translator":
    st.markdown("""
    <div class="page-header">
        <h2>📝 TEXT TO TEXT TRANSLATOR</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Live Translation Toggle
    st.markdown('<div class="holo-card">', unsafe_allow_html=True)
    col_toggle1, col_toggle2 = st.columns([1, 4])
    with col_toggle1:
        live_enabled = st.checkbox("🔴 Live Translation", value=st.session_state.live_translation_enabled, key="live_toggle")
        st.session_state.live_translation_enabled = live_enabled
    with col_toggle2:
        if live_enabled:
            st.success("⚡ Live translation is ACTIVE")
        else:
            st.info("💤 Live translation is OFF - use 'Translate' button")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="holo-card" style="position: relative;">', unsafe_allow_html=True)
        if live_enabled:
            st.markdown('<div class="live-indicator">🔴 LIVE</div>', unsafe_allow_html=True)
        st.markdown("### ✍️ Original Input")
        
        source_text = st.text_area(
            "", 
            height=300, 
            label_visibility="collapsed", 
            key="live_text_input",
            placeholder="Start typing here for instant translation..." if live_enabled else "Enter text and click 'Translate' button"
        )
        
        if source_text and st.button("🔊 Listen Original Audio", key="listen_original"):
            try:
                tts = gTTS(source_text, lang=LANGUAGES[st.session_state.source_lang])
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name)
            except Exception as e:
                st.error(f"Audio synthesis error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Center Translate Button
    if not live_enabled:
        st.markdown('<div class="center-translate-button">', unsafe_allow_html=True)
        if st.button("🔮 TRANSLATE", key="manual_translate", use_container_width=False):
            if source_text and source_text.strip():
                with st.spinner("🔮 Translating..."):
                    translated = live_translate(source_text, st.session_state.source_lang, st.session_state.target_lang)
                    st.session_state.manual_translation = translated
                    st.success("✅ Translation completed!")
            else:
                st.warning("⚠️ Please enter some text to translate")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="holo-card" style="position: relative;">', unsafe_allow_html=True)
        if live_enabled:
            st.markdown('<div class="live-indicator">⚡ AUTO</div>', unsafe_allow_html=True)
        st.markdown("### 🔤 Translated Output")
        
        # Determine what translation to show
        display_translation = ""
        
        if live_enabled and source_text and source_text.strip():
            # Live translation mode
            display_translation = live_translate(source_text, st.session_state.source_lang, st.session_state.target_lang)
        elif not live_enabled and 'manual_translation' in st.session_state:
            # Manual translation mode
            display_translation = st.session_state.manual_translation
        
        st.text_area(
            "", 
            value=display_translation, 
            height=300, 
            disabled=True, 
            label_visibility="collapsed",
            placeholder="Translation will appear here..." if live_enabled else "Click 'Translate' button to see results",
            key="translated_output_display"
        )
        
        if display_translation and st.button("🔊 Listen Translated Audio", key="listen_translated"):
            try:
                tts = gTTS(display_translation, lang=LANGUAGES[st.session_state.target_lang])
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name)
            except Exception as e:
                st.error(f"Audio synthesis error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Auto-save to history when translation is complete
    if source_text and display_translation and len(source_text.strip()) > 0 and len(display_translation.strip()) > 0:
        # Check if this translation is already in history
        existing_translation = False
        for item in st.session_state.history:
            if (item['source'] == source_text and 
                item['translated'] == display_translation and 
                item['source_lang'] == st.session_state.source_lang and 
                item['target_lang'] == st.session_state.target_lang):
                existing_translation = True
                break
        
        if not existing_translation:
            st.session_state.history.append({
                'timestamp': datetime.datetime.now(),
                'source': source_text,
                'translated': display_translation,
                'source_lang': st.session_state.source_lang,
                'target_lang': st.session_state.target_lang
            })

# ----------------------------------------
# PAGE: Speech Translator
# ----------------------------------------
elif page == "🎙️ Speech Translator":
    st.markdown("""
    <div class="page-header">
        <h2>🎙️ AUDIO TO TEXT TRANSLATOR</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="holo-card">', unsafe_allow_html=True)
    st.markdown("### 🎧 Advanced Voice Recognition")
    st.markdown("Activate quantum microphone and speak clearly for AI processing")
    
    if st.button("🎧 ACTIVATE NEURAL LISTENING", key="start_speech_listening"):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("🔮 Neural networks listening... Speak now!")
                audio = r.listen(source, phrase_time_limit=5)
            
            with st.spinner("🧠 AI processing speech patterns..."):
                speech = r.recognize_google(audio, language=LANGUAGES[st.session_state.source_lang])
                st.success(f"✅ Neural network detected: {speech}")
                translated = translator.translate(
                    speech, 
                    src=LANGUAGES[st.session_state.source_lang], 
                    dest=LANGUAGES[st.session_state.target_lang]
                ).text

            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="holo-card">', unsafe_allow_html=True)
                st.markdown("#### 🗣️ Voice Input Analysis")
                st.text_area("", value=speech, height=200, disabled=True, label_visibility="collapsed")
                if st.button("🔊 Replay Neural Audio", key="listen_speech_input"):
                    try:
                        tts = gTTS(speech, lang=LANGUAGES[st.session_state.source_lang])
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                            tts.save(fp.name)
                            st.audio(fp.name)
                    except Exception as e:
                        st.error(f"Audio synthesis error: {e}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="holo-card">', unsafe_allow_html=True)
                st.markdown("#### 🔤 Quantum Translation")
                st.text_area("", value=translated, height=200, disabled=True, label_visibility="collapsed")
                if st.button("🔊 AI Voice Synthesis", key="listen_speech_translation"):
                    try:
                        tts = gTTS(translated, lang=LANGUAGES[st.session_state.target_lang])
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                            tts.save(fp.name)
                            st.audio(fp.name)
                    except Exception as e:
                        st.error(f"Audio synthesis error: {e}")
                st.markdown('</div>', unsafe_allow_html=True)

            st.session_state.history.append({
                'timestamp': datetime.datetime.now(),
                'source': speech,
                'translated': translated,
                'source_lang': st.session_state.source_lang,
                'target_lang': st.session_state.target_lang
            })
        except Exception as e:
            st.error(f"❌ Neural processing error: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------
# PAGE: File Translator
# ----------------------------------------
elif page == "📁 File Translator":
    st.markdown("""
    <div class="page-header">
        <h2>📁 NEAURAL MULTIMODAL TRANSLATOR</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="holo-card">', unsafe_allow_html=True)
    st.markdown("### 📤 Advanced File Analysis")
    st.markdown("Upload any document for AI-powered content extraction and translation")
    
    uploaded_file = st.file_uploader("", type=[
        "pdf", "docx", "txt", "png", "jpg", "jpeg", "mp3", "wav", "mp4", "flac", "ogg", "m4a"
    ], label_visibility="collapsed")
    
    if uploaded_file:
        st.success(f"✅ Quantum file detected: {uploaded_file.name}")
        ext = uploaded_file.name.split('.')[-1].lower()
        content = ""

        with st.spinner(f"🔮 AI analyzing {ext.upper()} structure..."):
            try:
                if ext == "pdf":
                    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                    for page in doc:
                        content += page.get_text()
                elif ext == "docx":
                    doc = docx.Document(io.BytesIO(uploaded_file.read()))
                    for para in doc.paragraphs:
                        content += para.text + "\n"
                elif ext == "txt":
                    content = uploaded_file.read().decode("utf-8")
                elif ext in ["png", "jpg", "jpeg"]:
                    try:
                        import pytesseract
                        img = Image.open(uploaded_file)
                        content = pytesseract.image_to_string(img)
                    except ImportError:
                        st.error("❌ OCR functionality requires pytesseract. Please install it.")
                elif ext in ["mp3", "wav", "flac", "ogg", "m4a"]:
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                            audio_segment = AudioSegment.from_file(uploaded_file)
                            audio_segment.export(temp_audio.name, format="wav")
                            recognizer = sr.Recognizer()
                            with sr.AudioFile(temp_audio.name) as source:
                                audio = recognizer.record(source)
                                content = recognizer.recognize_google(audio, language=LANGUAGES[st.session_state.source_lang])
                    except Exception as e:
                        st.error(f"❌ Neural audio processing failed: {e}")
            except Exception as e:
                st.error(f"❌ File processing error: {e}")

        if content.strip():
            with st.spinner("🧠 Quantum translation processing..."):
                try:
                    translated = translator.translate(
                        content, 
                        src=LANGUAGES[st.session_state.source_lang], 
                        dest=LANGUAGES[st.session_state.target_lang]
                    ).text
                except Exception as e:
                    st.error(f"❌ Translation error: {e}")
                    translated = ""
            
            if translated:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="holo-card">', unsafe_allow_html=True)
                    st.markdown("#### 📄 Extracted Content")
                    st.text_area("", value=content, height=300, label_visibility="collapsed")
                    if st.button("🔊 Listen Source Audio", key="listen_file_source"):
                        try:
                            tts = gTTS(content, lang=LANGUAGES[st.session_state.source_lang])
                            # Create audio bytes in memory instead of temporary file
                            audio_buffer = io.BytesIO()
                            tts.write_to_fp(audio_buffer)
                            audio_buffer.seek(0)
                            st.audio(audio_buffer.read())
                        except Exception as e:
                            st.error(f"Audio synthesis error: {e}")
                    st.markdown('</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="holo-card">', unsafe_allow_html=True)
                    st.markdown("#### 🔤 Quantum Translation")
                    st.text_area("", value=translated, height=300, label_visibility="collapsed")
                    if st.button("🔊 Listen Target Audio", key="listen_file_target"):
                        try:
                            tts = gTTS(translated, lang=LANGUAGES[st.session_state.target_lang])
                            # Create audio bytes in memory instead of temporary file
                            audio_buffer = io.BytesIO()
                            tts.write_to_fp(audio_buffer)
                            audio_buffer.seek(0)
                            st.audio(audio_buffer.read())
                        except Exception as e:
                            st.error(f"Audio synthesis error: {e}")
                    st.markdown('</div>', unsafe_allow_html=True)

                st.session_state.history.append({
                    'timestamp': datetime.datetime.now(),
                    'source': content,
                    'translated': translated,
                    'source_lang': st.session_state.source_lang,
                    'target_lang': st.session_state.target_lang
                })
                
                st.success("✅ Quantum file processing completed successfully!")
        else:
            st.warning("⚠️ No content could be extracted from the file.")
    
    st.markdown('</div>', unsafe_allow_html=True)
# ----------------------------------------
# PAGE: History
# ----------------------------------------
elif page == "📜 History":
    st.markdown("""
    <div class="page-header">
        <h2>📜 NEURAL MEMORY BANK</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.history:
        st.markdown(f"""
        <div class="holo-card" style="text-align: center; margin-bottom: 2rem;">
            <h3 style="color: #00d4ff; font-family: 'Orbitron', monospace;">📊 Total Neural Translations: {len(st.session_state.history)}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Clear history button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🗑️ CLEAR NEURAL MEMORY", key="clear_neural_history"):
                st.session_state.history = []
                st.success("✅ Neural memory bank cleared!")
                st.rerun()
        
        # Display history items with proper HTML formatting
        for i, h in enumerate(reversed(st.session_state.history[-10:])):  # Show last 10
            timestamp_str = h['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            source_text = h['source'][:150] + ('...' if len(h['source']) > 150 else '')
            translated_text = h['translated'][:150] + ('...' if len(h['translated']) > 150 else '')
            
            # Escape HTML characters to prevent rendering issues
            source_text = source_text.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
            translated_text = translated_text.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
            
            st.markdown(f"""
            <div class="history-item">
                <div class="history-timestamp">🕒 {timestamp_str} | {h['source_lang']} ➡️ {h['target_lang']}</div>
                <div class="history-original">
                    <span class="history-label-original">Original:</span> {source_text}
                </div>
                <div class="history-translation">
                    <span class="history-label-translation">Translation:</span> {translated_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="holo-card" style="text-align: center;">', unsafe_allow_html=True)
        if st.button("💾 DOWNLOAD NEURAL DATABASE", key="download_neural_history"):
            try:
                import pandas as pd
                df = pd.DataFrame(st.session_state.history)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Export Quantum Data", 
                    csv, 
                    "neural_translation_history.csv", 
                    "text/csv",
                    key="download_history_csv"
                )
            except ImportError:
                st.error("❌ Pandas library required for CSV export. Please install pandas.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="holo-card" style="text-align: center; padding: 4rem;">
            <h3 style="color: #00d4ff; font-family: 'Orbitron', monospace; margin-bottom: 1rem;">🧠 Neural Memory Bank Empty</h3>
            <p style="color: #b8b8b8; font-size: 1.2rem;">Initialize translation processes to populate the quantum database</p>
            <div style="margin-top: 2rem;">
                <span style="font-size: 3rem; opacity: 0.3;">🔮</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Futuristic Footer
st.markdown("---")
st.markdown("""
<div class="futuristic-footer">
    <h4 style="color: #ffffff; margin: 0; font-family: 'Orbitron', monospace; font-size: 1.5rem;">🌍 AI GLOBAL LANGUAGE TRANSLATOR</h4>
    <p style="color: #b8b8b8; margin: 0.5rem 0 0 0; font-family: 'Exo 2', sans-serif;">
        Built by Advanced Neural Machine Translation AI & Deep Translator(Google)
    </p>
    <div style="margin-top: 1rem; opacity: 0.6;">
        <span style="color: #00d4ff;">●</span>
        <span style="color: #ff006e;">●</span>
        <span style="color: #8338ec;">●</span>
        <span style="color: #06ffa5;">●</span>
    </div>
</div>
""", unsafe_allow_html=True)