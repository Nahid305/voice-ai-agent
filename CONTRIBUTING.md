# Contributing to Voice-Based AI IT Support Agent

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Git
- A Groq API key (free at [console.groq.com](https://console.groq.com/))
- Microphone for testing

### Fork & Clone
1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/YOUR_USERNAME/voice-ai-agent.git
cd voice-ai-agent
```

### Setup Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install black flake8 pytest
```

### Configure Local Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=gsk_your_key_here
```

---

## 📋 Development Workflow

### Creating a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
# or
git checkout -b docs/your-documentation
```

### Making Changes
1. Edit files as needed
2. Keep changes focused and small
3. Follow Python style guidelines (see below)
4. Test your changes locally

### Code Quality
Always run these before committing:

```bash
# Format code with Black
black utils/ app.py

# Check for linting issues
flake8 utils/ app.py

# Run tests (if any)
pytest
```

### Commit Messages
Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add: Support for multiple audio input devices"
git commit -m "Fix: Audio playback lag on Windows"
git commit -m "Docs: Update installation instructions"

# Avoid
git commit -m "Update"
git commit -m "Fix bug"
git commit -m "asdf"
```

Format: `[Type]: [Description]`
- `Add` - New feature
- `Fix` - Bug fix
- `Docs` - Documentation
- `Refactor` - Code refactoring
- `Test` - Test additions

### Push & Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:
- Clear title describing the change
- Description of what changed and why
- Reference any related issues (#123)

---

## 💻 Code Style Guidelines

### Python Style
Follow PEP 8 with these tools:
```bash
black --line-length 88 file.py
flake8 file.py
```

### Function Documentation
```python
def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio file to text using faster-whisper.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Transcribed text as string
        
    Raises:
        FileNotFoundError: If audio file not found
        ValueError: If audio format is invalid
    """
    pass
```

### Variable Naming
- Variables: `snake_case` (e.g., `audio_data`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_DURATION`)
- Classes: `PascalCase` (e.g., `AudioRecorder`)
- Private: Prefix with `_` (e.g., `_internal_method`)

---

## 🧪 Testing

### Running Tests
```bash
pytest
pytest tests/test_audio_recorder.py
pytest -v  # Verbose output
```

### Writing Tests
```python
# tests/test_audio_recorder.py
import pytest
from utils.audio_recorder import record_audio

def test_record_audio_creates_file():
    """Test that record_audio creates a valid file."""
    file_path = record_audio(duration=1)
    assert os.path.exists(file_path)
    os.remove(file_path)

def test_record_audio_requires_microphone():
    """Test that record_audio fails without microphone."""
    with pytest.raises(RuntimeError):
        record_audio(duration=1)
```

---

## 🐛 Bug Reports

### Before Reporting
- Check existing issues to avoid duplicates
- Test with latest code from main branch
- Try removing .streamlit cache: `streamlit cache clear`

### Bug Report Format
```markdown
## Bug Description
Clear description of the bug.

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Windows/Mac/Linux
- Python: 3.9/3.10/3.11
- faster-whisper: version
- error logs/screenshots

## Additional Context
Any other relevant information
```

---

## 💡 Feature Requests

### Proposing Features
Before starting work on a major feature, please open an issue to discuss:
- What problem it solves
- How it would work
- Potential implementation approach

### Feature Request Template
```markdown
## Feature Description
What is the feature and why would it be useful?

## Use Case
Who would use this and how?

## Proposed Solution
How should this work?

## Alternatives Considered
Other approaches you considered

## Additional Context
Screenshots, mockups, or references
```

---

## 📚 Documentation

### README Updates
When adding features, update README.md:
- Add feature to 🌟 Features section
- Update 📁 Project Structure if new files added
- Add usage examples if user-facing

### Code Comments
Add comments for complex logic:
```python
# Use VAD to detect speech end (silence > 2 seconds)
while len(audio_chunk) > 0:
    # Process chunk...
    pass
```

### Docstrings
All functions should have docstrings:
```python
def function(param1: str) -> bool:
    """One-line description.
    
    More detailed explanation if needed.
    
    Args:
        param1: Description of param1
        
    Returns:
        Description of return value
    """
```

---

## 🔄 Pull Request Process

1. **Create PR**: 
   - Title format: `[Type] Short description`
   - Link related issues with `Fixes #123`
   - Describe changes clearly

2. **Code Review**:
   - Address feedback from reviewers
   - Keep commits clean and logical
   - Update PR description if needed

3. **Checks**:
   - All CI/CD checks must pass
   - Code quality standards met
   - Tests pass locally and in CI

4. **Merge**:
   - Use "Squash and merge" for clean history
   - Your branch is automatically deleted

---

## 📝 Areas for Contribution

### 🌟 High Priority
- [ ] Multi-language support
- [ ] Conversation export (PDF/JSON)
- [ ] Docker containerization
- [ ] Performance optimization

### 🎨 Medium Priority
- [ ] UI/UX improvements
- [ ] Custom system prompts
- [ ] Additional audio formats
- [ ] Error handling improvements

### 📚 Low Priority
- [ ] Documentation updates
- [ ] Comment improvements
- [ ] Test coverage increase
- [ ] Example configurations

---

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome all experience levels
- Provide constructive feedback
- No harassment or discrimination
- Assume good intent

---

## 📬 Communication

- **Issues**: For bugs and feature discussions
- **Pull Requests**: For code changes
- **Discussions**: For general questions
- **Email**: For sensitive matters

---

## 📄 Licensing

By contributing, you agree your code will be licensed under MIT License. See LICENSE file.

---

## ✨ Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Thanked in release notes
- Recognized in README

---

## 🎓 Additional Resources

- [Git Guide](https://git-scm.com/book/en/v2)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Black Formatter](https://black.readthedocs.io/)

---

Thank you for contributing! 🙏
