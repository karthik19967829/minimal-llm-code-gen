# LLM Code Generator & Repository Manager

A comprehensive Python application that uses Large Language Models to generate code and perform advanced repository-level operations on remote Git repositories.

## 🚀 Features

### 💻 Basic Code Generation
- Generate Python code using LLM APIs (OpenAI GPT-5, Claude, Gemini)
- Execute generated code safely in isolated environment
- Configuration-based API key management
- Support for multiple LLM providers

### 🏗️ Advanced Repository Operations
- **Clone & Analyze** - Clone remote Git repositories and analyze structure
- **AI-Powered Summaries** - Generate comprehensive project overviews
- **Smart Improvements** - Get targeted suggestions for code quality, security, performance
- **Feature Implementation** - Implement new features across multiple files automatically
- **Issue Resolution** - Fix bugs and issues with AI-generated solutions
- **Branch Management** - Create feature branches and prepare pull requests
- **Multi-file Operations** - Make changes across entire codebases intelligently

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/karthik19967829/minimal-llm-code-gen.git
   cd minimal-llm-code-gen
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install requests
   ```

4. **Configure API keys**
   Edit `config.json` and add your API keys:
   ```json
   {
     "models": {
       "openai": {
         "api_key": "your-openai-api-key-here",
         "model_name": "gpt-5"
       },
       "claude": {
         "api_key": "your-anthropic-api-key-here",
         "model_name": "claude-3-sonnet-20240229"
       },
       "gemini": {
         "api_key": "your-google-api-key-here",
         "model_name": "gemini-pro"
       }
     }
   }
   ```

## 🎯 Usage

### Basic Code Generation

**Generate and execute code:**
```bash
python llm_code_generator.py "Create a Python program that sorts a list using quicksort"
```

**Generate code without execution:**
```bash
python llm_code_generator.py "Create a REST API server" --no-execute
```

**Use different model:**
```bash
python llm_code_generator.py "Create a machine learning model" --model claude
```

### Repository Operations

#### 📊 Repository Analysis
```bash
# Get detailed repository statistics
python repo_cli.py analyze https://github.com/user/project.git

# Analyze specific branch
python repo_cli.py analyze https://github.com/user/project.git --branch develop
```

**Output includes:**
- File count and structure
- Programming languages used
- Repository size and metrics
- Git branch information

#### 📝 AI-Generated Repository Summary
```bash
# Generate comprehensive project overview
python repo_cli.py summary https://github.com/facebook/react.git

# Use different AI model
python repo_cli.py summary https://github.com/user/project.git --model claude
```

**AI analyzes and provides:**
- Project purpose and architecture
- Technology stack overview
- Key components and relationships
- Development patterns and structure

#### 🔧 Smart Improvement Suggestions
```bash
# General improvements
python repo_cli.py improve https://github.com/user/webapp.git

# Focus on specific areas
python repo_cli.py improve https://github.com/user/api.git --focus security
python repo_cli.py improve https://github.com/user/app.git --focus performance
python repo_cli.py improve https://github.com/user/lib.git --focus testing
```

**AI provides targeted suggestions for:**
- Code quality and best practices
- Security vulnerabilities and fixes
- Performance optimizations
- Testing improvements
- Documentation enhancements

#### ⚡ Feature Implementation
```bash
# Implement new feature across multiple files
python repo_cli.py feature https://github.com/user/project.git "Add user authentication system"

# Create feature branch for pull request
python repo_cli.py feature https://github.com/user/app.git "Add real-time notifications" --create-pr

# Work on specific branch
python repo_cli.py feature https://github.com/user/project.git "Add API rate limiting" --branch develop --create-pr
```

**AI automatically:**
- Analyzes existing codebase structure
- Creates implementation plan
- Generates code for multiple files
- Handles file creation and modification
- Creates feature branch (with `--create-pr`)
- Commits changes with detailed messages

#### 🐛 Issue Resolution
```bash
# Fix bugs and issues
python repo_cli.py fix https://github.com/user/project.git "Fix memory leaks in data processing"

# Create fix branch for pull request
python repo_cli.py fix https://github.com/user/app.git "Resolve SQL injection vulnerabilities" --create-pr

# Use specific AI model
python repo_cli.py fix https://github.com/user/project.git "Fix race conditions" --model claude --create-pr
```

**AI automatically:**
- Identifies root causes of issues
- Generates targeted fixes
- Modifies affected files
- Creates fix branch (with `--create-pr`)
- Commits with detailed fix descriptions

## 🛠️ Command Reference

### Repository Commands

| Command | Description | Options |
|---------|-------------|---------|
| `analyze` | Analyze repository structure and statistics | `--branch`, `--model` |
| `summary` | Generate AI-powered project summary | `--branch`, `--model` |
| `improve` | Get targeted improvement suggestions | `--focus`, `--branch`, `--model` |
| `feature` | Implement new features across multiple files | `--create-pr`, `--branch`, `--model` |
| `fix` | Fix issues with AI-generated solutions | `--create-pr`, `--branch`, `--model` |

### Global Options

| Option | Description | Values |
|--------|-------------|--------|
| `--branch` | Specify Git branch to work with | Branch name (default: `main`) |
| `--model` | Choose AI model provider | `openai`, `claude`, `gemini` |
| `--create-pr` | Create new branch for pull request | Flag (no value) |
| `--focus` | Focus improvement suggestions | `security`, `performance`, `testing`, etc. |

## 📁 Project Structure

```
minimal-llm-code-gen/
├── config.json                 # API keys and model configuration
├── config_reader.py            # Configuration management
├── llm_code_generator.py       # Basic code generation
├── repo_manager.py             # Git repository operations
├── repo_code_generator.py      # Repository-level AI operations
├── repo_cli.py                 # Command-line interface
├── README.md                   # This file
└── venv/                       # Virtual environment
```

### Core Components

**Basic Code Generation:**
- `llm_code_generator.py` - Single-file code generation and execution
- `config_reader.py` - API key and model configuration management

**Repository Operations:**
- `repo_manager.py` - Git operations (clone, branch, commit, push)
- `repo_code_generator.py` - AI-powered repository analysis and modification
- `repo_cli.py` - Command-line interface for all repository features

## 🔒 Security & Best Practices

### Security Features
- **API Key Protection** - Never commit API keys to version control
- **Isolated Execution** - Generated code runs in subprocess isolation
- **Temporary Workspaces** - Repository operations use temporary directories
- **Automatic Cleanup** - Cloned repositories are automatically cleaned up
- **Branch Isolation** - Changes are made in separate branches

### Configuration Security
```json
{
  "models": {
    "openai": {
      "api_key": "",  // ← Keep empty in version control
      // Set via environment variable: OPENAI_API_KEY
    }
  }
}
```

### Best Practices
- Always use `--create-pr` for repository modifications
- Review AI-generated changes before merging
- Test generated code in isolated environments
- Use focused improvement suggestions for better results
- Configure appropriate execution timeouts

## 🌟 Examples

### Analyze a Popular Open Source Project
```bash
python repo_cli.py analyze https://github.com/django/django.git
```

### Get Security Improvements for Your Web App
```bash
python repo_cli.py improve https://github.com/youruser/webapp.git --focus security
```

### Add Comprehensive Logging to a Project
```bash
python repo_cli.py feature https://github.com/youruser/api.git "Add structured logging with log levels and rotation" --create-pr
```

### Fix Performance Issues
```bash
python repo_cli.py fix https://github.com/youruser/service.git "Optimize database queries and reduce memory usage" --create-pr
```

### Generate Project Summary for Documentation
```bash
python repo_cli.py summary https://github.com/youruser/library.git --model claude
```

## 🚨 Limitations

- Requires valid API keys for LLM providers
- Large repositories may hit token limits
- Generated code should be reviewed before production use
- Git operations require proper permissions
- Some LLM models have usage restrictions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. See the repository for license details.

---

**Made with ❤️ using AI-powered code generation**