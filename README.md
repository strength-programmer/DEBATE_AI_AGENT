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

## 🎨 Customization

### Styling
- Modify `style.css` to customize the appearance
- Update color variables in `:root` section
- Adjust animations and transitions

### Debate Topics
- Edit example topics in `debate.py`
- Modify the topic suggestions section

### Agent Behavior
- Update agent instructions in `debate.py`
- Customize debate parameters like number of rounds

## 🔒 Security

- API keys are stored in session state
- Keys are not persisted between sessions
- Use environment variables for production deployment

## 🚧 Troubleshooting

Common issues and solutions:

1. **API Key Issues**
   - Ensure key starts with 'sk-'
   - Check OpenAI account status
   - Verify API key permissions

2. **Copy Functionality**
   - Enable JavaScript in browser
   - Check browser permissions
   - Try using the clipboard fallback

3. **Style Issues**
   - Clear browser cache
   - Check CSS file loading
   - Verify file paths

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Open a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for the API
- Streamlit for the framework
- Contributors and testers

## 📞 Support

For issues and feature requests:
1. Check existing issues
2. Create a new issue with details
3. Follow the issue template

---

Built with ❤️ using Streamlit and OpenAI
