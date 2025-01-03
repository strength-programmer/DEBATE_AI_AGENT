import streamlit as st
from swarm import Swarm, Agent
from openai import OpenAI
import time
import base64
import os
import json
from fpdf import FPDF
import io
from datetime import datetime

#function for fpdf
def generate_debate_pdf(debate_topic, debate_history):
    pdf = FPDF()
    pdf.add_page()
    
    # Use default font instead of Poppins to avoid font loading issues
    # Title
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 20, 'AI vs Traditional Teaching Methods Debate', 0, 1, 'C')
    
    # Date and Topic
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Date: {datetime.now().strftime("%B %d, %Y")}', 0, 1, 'R')
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Debate Topic:', 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, debate_topic)
    pdf.ln(10)
    
    # Debate Content
    for i, entry in enumerate(debate_history):
        # Round number
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f'Round {i//2 + 1}', 0, 1)
        
        # Speaker
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 8, entry['agent'], 0, 1)
        
        # Message
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(0, 8, entry['message'])
        pdf.ln(5)
    
    return pdf.output(dest='S').encode('latin1')

# Set up page config
st.set_page_config(page_title="AI Teaching Methods Debate", layout="wide")

# Add after page config
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        
        .stApp {
            font-family: 'Poppins', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Load custom CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state for API key and authentication
if 'api_key' not in st.session_state:
    st.session_state.api_key = None
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
if 'debate_history' not in st.session_state:
    st.session_state.debate_history = []
if 'current_turn' not in st.session_state:
    st.session_state.current_turn = 0

# API Key authentication page
if not st.session_state.is_authenticated:
    st.title("🔑 Welcome to AI Teaching Methods Debate")
    st.markdown("Please enter your OpenAI API key to continue")
    
    api_key = st.text_input("Enter your OpenAI API key:", type="password")
    if st.button("Submit"):
        if api_key.startswith('sk-'):
            st.session_state.api_key = api_key
            st.session_state.is_authenticated = True
            st.experimental_rerun()
        else:
            st.error("Please enter a valid OpenAI API key")
    
    st.markdown("---")
    st.markdown("""
    ### How to get your API key:
    1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
    2. Create a new API key
    3. Copy and paste it here
    """)

else:
    # Initialize OpenAI client with the provided API key
    api = OpenAI(api_key=st.session_state.api_key)
    client = Swarm(api)

    # Agents setup
    traditional = Agent(
        name="Traditional Professor",
        instructions="""You are a passionate debater advocating for traditional teaching methods without AI tools.
        Your position:
        - Defend human-centered, traditional teaching approaches
        - Argue against over-reliance on AI and technology in education
        - Emphasize the irreplaceable human elements of teaching
        - Highlight potential risks and drawbacks of AI in education
        Present your arguments professionally but firmly, supporting them with relevant examples and evidence. Debate with Modern Professor and counter their arguments (if they have taken their turn).
        
        *IMPORTANT: Your response should be super concise, straight to the point and direct. It should be in paragraph form and should have at most 2 sentences to ENSURE conciseness and being direct to the point. 
        
        *ADDITIONAL NOTE: When responding, be straightforward and just state your argument, no need to specify what agent are you (Ex: Traditional Professor: <Argument>). 
        
        Style:
        - Keep tone conversational rather than overly formal
        - Maintain professionalism while being approachable
        - Respond as if having a natural discussion between colleagues

        I REPEAT, in your response, ALWAYS skip agent identification headers! NEVER STATE your AGENT NAME BEFORE ARGUMENT! for example, "Traditional:"
        """,
    )

    modern = Agent(
        name="Modern Professor",
        instructions="""You are a passionate debater advocating for the integration of AI tools in modern teaching.
        Your position:
        - Champion the benefits of AI-enhanced education
        - Argue for the necessity of adapting to technological advancement
        - Emphasize how AI can augment and improve teaching effectiveness
        - Address common concerns about AI while highlighting its advantages
        Present your arguments professionally but firmly, supporting them with relevant examples and evidence. Debate with Traditional Professor and counter their arguments (if they have taken their turn).
        
        *IMPORTANT: Your response should be super concise, straight to the point and direct. It should be in paragraph form and should have at most 2 sentences to ENSURE conciseness and being direct to the point. 
        
        *ADDITIONAL NOTE: When responding, be straightforward and just state your argument, no need to specify what agent are you (Ex: Modern Professor: <Argument>). 
        
        Style:
        - Keep tone conversational rather than overly formal
        - Maintain professionalism while being approachable
        - Respond as if having a natural discussion between colleagues

        I REPEAT, in your response, ALWAYS skip agent identification headers! NEVER STATE your AGENT NAME BEFORE ARGUMENT! for example, "Modern:"
    """,
    )

    # Page Header
    st.markdown("""
        <div class="main-header">
            <h1>🎓 AI vs Traditional Teaching Methods Debate</h1>
            <p>Watch two professors debate about the future of education</p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("Debate Controls")
        debate_topic = st.text_input("Enter Debate Topic:", 
                                    placeholder="What is the best teaching style to make students learn?",
                                    key="topic")
        num_rounds = st.slider("Number of Rounds:", min_value=1, max_value=20, value=2)
        start_debate = st.button("Start New Debate")
        
        st.markdown("---")
        st.markdown("### How it works")
        st.markdown("""
        1. Enter a debate topic
        2. Select number of rounds
        3. Click 'Start New Debate'
        4. Watch the professors debate!
        """)

        st.markdown("---")
        if st.button("Logout"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()

        st.markdown('<div class="debate-controls">', unsafe_allow_html=True)

    # Main debate area
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="professor-card traditional-card">
                <h2>👨‍🏫 Traditional Professor</h2>
                <p><em>Advocates for traditional teaching methods</em></p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="professor-card modern-card">
                <h2>🤖 Modern Professor</h2>
                <p><em>Advocates for AI-enhanced teaching</em></p>
            </div>
        """, unsafe_allow_html=True)

    # Start new debate
    if start_debate:
        st.session_state.debate_history = []
        st.session_state.current_turn = 0
        struct = [{"role": "user", "content": debate_topic}]
        
        with st.spinner("Debate in progress..."):
            for turn in range(num_rounds * 2):
                current_agent = traditional if turn % 2 == 0 else modern
                response = client.run(agent=current_agent, messages=struct)
                message = str(response.messages[-1]["content"])
                struct.append({"role": "assistant", "content": f"{current_agent.name}: {message}"})
                st.session_state.debate_history.append({
                    "agent": current_agent.name,
                    "message": message
                })

    # Display debate history
    if st.session_state.debate_history:
        st.markdown('<div class="debate-stage">', unsafe_allow_html=True)
        st.markdown('<h2 class="debate-title">Debate Transcript</h2>', unsafe_allow_html=True)
        
        for i, entry in enumerate(st.session_state.debate_history):
            is_traditional = entry["agent"] == "Traditional Professor"
            col = col1 if is_traditional else col2
            
            with col:
                st.markdown(f"""
                    <div class="debate-message {'traditional-card' if is_traditional else 'modern-card'}"
                         data-message-index="{i}">
                        <div class="round-badge">Round {i//2 + 1}</div>
                        <div class="status-indicator {'status-active' if i == len(st.session_state.debate_history)-1 else ''}"></div>
                        <p><em>{entry['message']}</em></p>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Add a download button for PDF
        st.markdown("""
            <div class="download-section">
                <h3>📥 Download Debate Transcript</h3>
            </div>
        """, unsafe_allow_html=True)
        
        try:
            pdf_bytes = generate_debate_pdf(debate_topic, st.session_state.debate_history)
            st.download_button(
                label="Download as PDF",
                data=pdf_bytes,
                file_name=f"debate_transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")

    else:
        st.info("Enter a topic and click 'Start New Debate' to begin!")

    # Update the initial info message with suggestions
    if not st.session_state.debate_history:
        st.markdown("""
            <div class="topic-suggestions">
                <h3>🤔 Example Debate Topics:</h3>
                <div class="topic-group">
                    <div class="topic-item" data-topic="Should AI completely replace traditional teaching methods in schools?">
                        <span class="topic-text">Should AI completely replace traditional teaching methods in schools?</span>
                        <button class="copy-button" onclick="copyToClipboard(this.parentElement)">📋</button>
                    </div>
                    <div class="topic-item" data-topic="Are digital textbooks better than physical textbooks for learning?">
                        <span class="topic-text">Are digital textbooks better than physical textbooks for learning?</span>
                        <button class="copy-button" onclick="copyToClipboard(this.parentElement)">📋</button>
                    </div>
                    <div class="topic-item" data-topic="Should coding be mandatory in elementary education?">
                        <span class="topic-text">Should coding be mandatory in elementary education?</span>
                        <button class="copy-button" onclick="copyToClipboard(this.parentElement)">📋</button>
                    </div>
                    <div class="topic-item" data-topic="Is personalized AI-driven learning more effective than standardized education?">
                        <span class="topic-text">Is personalized AI-driven learning more effective than standardized education?</span>
                        <button class="copy-button" onclick="copyToClipboard(this.parentElement)">📋</button>
                    </div>
                    <div class="topic-item" data-topic="Should smartphones be allowed in classrooms as learning tools?">
                        <span class="topic-text">Should smartphones be allowed in classrooms as learning tools?</span>
                        <button class="copy-button" onclick="copyToClipboard(this.parentElement)">📋</button>
                    </div>
                </div>
            </div>
            <script>
                async function copyToClipboard(element) {
                    const text = element.getAttribute('data-topic');
                    try {
                        await navigator.clipboard.writeText(text);
                        const button = element.querySelector('.copy-button');
                        button.textContent = '✅';
                        setTimeout(() => button.textContent = '📋', 1500);
                        
                        // Update Streamlit input
                        const input = document.querySelector('input[aria-label="Enter Debate Topic:"]');
                        if (input) {
                            input.value = text;
                            input.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                    } catch (err) {
                        console.error('Copy failed:', err);
                        // Fallback for older browsers
                        const textarea = document.createElement('textarea');
                        textarea.value = text;
                        textarea.style.position = 'fixed';
                        textarea.style.opacity = '0';
                        document.body.appendChild(textarea);
                        textarea.select();
                        try {
                            document.execCommand('copy');
                            const button = element.querySelector('.copy-button');
                            button.textContent = '✅';
                            setTimeout(() => button.textContent = '📋', 1500);
                        } catch (e) {
                            console.error('Fallback copy failed:', e);
                            const button = element.querySelector('.copy-button');
                            button.textContent = '❌';
                            setTimeout(() => button.textContent = '📋', 1500);
                        }
                        document.body.removeChild(textarea);
                    }
                }
            </script>
        """, unsafe_allow_html=True)

# Add after the imports
st.markdown("""
    <script>
        function loadScript() {
            const existingScript = document.querySelector('script[src*="script.js"]');
            if (!existingScript) {
                const script = document.createElement('script');
                script.src = 'static/script.js';
                script.type = 'text/javascript';
                document.head.appendChild(script);
            }
        }

        // Try to load immediately
        loadScript();
        
        // Also try after window load (backup)
        window.addEventListener('load', loadScript);
        
        // Ensure the script runs after Streamlit's rerun
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length) {
                    loadScript();
                }
            });
        });
        
        observer.observe(document.body, { childList: true, subtree: true });
    </script>
""", unsafe_allow_html=True)

# Add this function after the imports
def load_static_file(filename):
    try:
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        with open(os.path.join(static_dir, filename), 'r') as f:
            return f.read()
    except Exception as e:
        st.error(f"Error loading static file: {e}")
        return ""

# Move this function to the top, right after the imports and before st.set_page_config
