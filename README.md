# DEBATE_AI_AGENT
# AI Teaching Methods Debate Platform

A Streamlit-based web application that facilitates debates between traditional and AI-enhanced teaching methods using AI agents.

## 🌟 Features

- Interactive debate platform with AI agents
- Real-time topic suggestions with copy functionality
- PDF export of debate transcripts
- Customizable number of debate rounds
- Modern, responsive UI with animations
- Secure API key management
  
## THE AGENTS
# AI Teaching Debate Agents

## Traditional Professor 🎓
An AI agent that defends traditional teaching methods, emphasizing human interaction and proven classroom techniques. Opposes excessive technology use in education and argues for maintaining the human element in teaching.

## Modern Professor 🤖
An AI agent that advocates for AI-enhanced education and technological innovation in teaching. Champions data-driven, personalized learning approaches and argues for modernizing educational methods.

## How They Work
The agents engage in a structured debate, taking turns to present concise arguments (max 2 sentences) about their respective teaching philosophies. Their interaction creates an engaging discussion about the future of education, balancing tradition with innovation. 
## 🚀 Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key

### Installation Steps

1. Clone the repository:
2. Create and activate a virtual environment:
3. Install required packages:
4. Set up OpenAI API key:
- Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
- Create a new API key
- Keep it secure for use in the application


### Project Structure

## 🎮 Running the Application

1. Navigate to the project directory
2. Run the Streamlit application:
```bash
python -m streamlit run debate_app.py
```
3. Enter your OpenAI API key when prompted

## 🛠️ Configuration

### OpenAI Swarm Setup

The application uses the Swarm library to manage AI agents. Here's how to configure it:

1. Install Swarm:
```bash
pip install git+https://github.com/openai/swarm.git
```
2. Configure agents in `debate.py`:
```python
from swarm import Swarm, Agent
Initialize Swarm with OpenAI client
client = Swarm(api)
Configure Traditional Professor agent
traditional = Agent(
name="Traditional Professor",
instructions="""Your custom instructions here"""
)
Configure Modern Professor agent
modern = Agent(
name="Modern Professor",
instructions="""Your custom instructions here"""
)
```


## 📞 Support

For issues and feature requests:
1. Check existing issues
2. Create a new issue with details
3. Follow the issue template

---

Built with ❤️ using Streamlit and OpenAI
