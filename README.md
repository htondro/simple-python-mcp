# Model Context Protocol (MCP) Implementation

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A robust implementation of the Model Context Protocol (MCP) that enables AI models to interact with external tools and services through a standardized protocol.

[Installation](#installation) •
[Usage](#usage) •
[How It Works](#how-it-works) •
[Contributing](#contributing)

</div>

## 🌟 Features

- 🚀 Implementation of the Model Context Protocol (MCP)
- 🤖 Integration with Anthropic's Claude AI model
- 🛠️ Tool execution system with JSON-RPC communication
- 🔐 Environment variable configuration for API keys
- ⏰ Example tool implementation (get_current_time)

## 📋 Prerequisites

- Python 3.11 or higher
- Anthropic API key
- pip (Python package installer)

## 🚀 Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Anthropic API key:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

## 📁 Project Structure

```
.
├── chatbot.py          # Main client implementation
├── mcp_server.py      # Server implementation
├── requirements.txt   # Python dependencies
└── .env              # API key configuration (not in repo)
```

## 💻 Usage

1. Start the chatbot:
```bash
python chatbot.py
```

2. Interact with the chatbot in the terminal:
   - Ask questions that might require tool usage
   - Type "exit" to quit the program

## 📝 Example Interaction

```bash
User: What time is it?
Assistant: Let me check the current time for you.
Found 1 tool calls
Tool get_current_time result: 2024-03-26 15:30:45
Assistant: The current time is 2024-03-26 15:30:45.
```

## 🔧 How It Works

1. The `MCPClient` class manages communication with the MCP server using JSON-RPC
2. When a user sends a message, it's processed by Claude
3. If Claude determines a tool is needed, it makes a tool call
4. The tool call is executed by the MCP server
5. The result is sent back to Claude for final response generation

## 🔒 Security

- 🔑 API keys are stored in `.env` file and not committed to the repository
- 🚫 The `.env` file is included in `.gitignore` to prevent accidental commits

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Anthropic for the Claude AI model
- The Model Context Protocol specification

---

<div align="center">
Made with ❤️ by [htondro](https://linkedin.com/in/htondro)
</div> 