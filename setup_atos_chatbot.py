#!/usr/bin/env python3
"""
Atos Chatbot Deployment Automation Script
Automates the complete setup of React app with Copilot Studio integration
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_status(message, color=Colors.BLUE):
    print(f"{color}{Colors.BOLD}🚀 {message}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}{Colors.BOLD}✅ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}{Colors.BOLD}❌ {message}{Colors.END}")

def run_command(command, cwd=None, shell=True):
    """Run a command and return success status"""
    try:
        print_status(f"Running: {command}")
        result = subprocess.run(command, shell=shell, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print_error(f"Command failed: {result.stderr}")
            return False
        else:
            print_success(f"Command completed successfully")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        return True
    except Exception as e:
        print_error(f"Error running command: {str(e)}")
        return False

def check_prerequisites():
    """Check if required tools are installed"""
    print_status("Checking prerequisites...")
    
    required_tools = ['node', 'npm', 'git']
    missing_tools = []
    
    for tool in required_tools:
        try:
            result = subprocess.run([tool, '--version'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print_success(f"{tool} is installed")
            else:
                missing_tools.append(tool)
                print_error(f"{tool} is not installed")
        except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
            missing_tools.append(tool)
            print_error(f"{tool} is not installed (Error: {str(e)})")
    
    if missing_tools:
        print_error(f"Please install missing tools: {', '.join(missing_tools)}")
        sys.exit(1)

def create_folder_structure():
    """Create the required folder structure"""
    print_status("Creating folder structure...")
    
    folders = [
        'src/components',
        'public',
        '.github/workflows',
        'deployment'
    ]
    
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print_success(f"Created folder: {folder}")

def create_package_json():
    """Create package.json with required dependencies"""
    print_status("Creating package.json...")
    
    package_json = {
        "name": "atos-chatbot",
        "version": "1.0.0",
        "description": "Atos AI Assistant Chatbot with Copilot Studio integration",
        "private": True,
        "dependencies": {
            "@testing-library/jest-dom": "^5.16.4",
            "@testing-library/react": "^13.3.0",
            "@testing-library/user-event": "^13.5.0",
            "lucide-react": "^0.263.1",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "web-vitals": "^2.1.4"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject",
            "deploy": "npm run build && gh-pages -d build"
        },
        "eslintConfig": {
            "extends": [
                "react-app",
                "react-app/jest"
            ]
        },
        "browserslist": {
            "production": [
                ">0.2%",
                "not dead",
                "not op_mini all"
            ],
            "development": [
                "last 1 chrome version",
                "last 1 firefox version",
                "last 1 safari version"
            ]
        },
        "devDependencies": {
            "autoprefixer": "^10.4.14",
            "gh-pages": "^5.0.0",
            "postcss": "^8.4.24",
            "tailwindcss": "^3.3.0"
        }
    }
    
    with open('package.json', 'w', encoding='utf-8') as f:
        json.dump(package_json, f, indent=2)
    print_success("package.json created")

def create_react_component():
    """Create the main React component"""
    print_status("Creating React component...")
    
    component_code = '''import React, { useState, useRef, useEffect } from 'react';
import { Send, Search, Bot, User } from 'lucide-react';

const AtosChatbot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: 'Hello! I\\'m your Atos AI Assistant. I can help you search the web and answer your questions. What would you like to know today?',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue;
    setInputValue('');
    setIsLoading(true);

    try {
      // TODO: Replace with your actual Copilot Studio Agent API endpoint
      const API_ENDPOINT = process.env.REACT_APP_COPILOT_API_ENDPOINT || 'YOUR_COPILOT_STUDIO_ENDPOINT_HERE';
      
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add any required headers for Copilot Studio API
          // 'Authorization': `Bearer ${process.env.REACT_APP_API_KEY}`,
          // 'Ocp-Apim-Subscription-Key': process.env.REACT_APP_SUBSCRIPTION_KEY,
        },
        body: JSON.stringify({
          message: currentInput,
          // Add other required parameters for Copilot Studio
          sessionId: `session-${Date.now()}`, // Generate or maintain session ID
          // userId: 'user-id', // If required
          // channelId: 'web-chat', // If required
        })
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      
      // Extract response content - adjust based on Copilot Studio response format
      const botResponse = data.message || data.response || data.content || 'I apologize, but I received an unexpected response format.';

      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: botResponse,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('API Error:', error);
      
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: `I apologize, but I'm currently experiencing technical difficulties. Please try again later.\\n\\nError: ${error.message}`,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-4 shadow-lg">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="bg-white/20 p-2 rounded-lg">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold">Atos AI Assistant</h1>
            <p className="text-blue-100 text-sm">Powered by Web Search & AI</p>
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex items-start gap-3 ${
                message.type === 'user' ? 'flex-row-reverse' : 'flex-row'
              }`}
            >
              {/* Avatar */}
              <div className={`p-2 rounded-full ${
                message.type === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-white shadow-md text-blue-600'
              }`}>
                {message.type === 'user' ? (
                  <User className="w-5 h-5" />
                ) : (
                  <Bot className="w-5 h-5" />
                )}
              </div>

              {/* Message Bubble */}
              <div className={`max-w-3xl ${
                message.type === 'user' ? 'text-right' : 'text-left'
              }`}>
                <div className={`inline-block p-4 rounded-2xl shadow-sm ${
                  message.type === 'user'
                    ? 'bg-blue-600 text-white rounded-tr-md'
                    : 'bg-white text-gray-800 rounded-tl-md border border-blue-100'
                }`}>
                  <div className="whitespace-pre-wrap">{message.content}</div>
                </div>
                <div className={`text-xs text-gray-500 mt-1 ${
                  message.type === 'user' ? 'text-right' : 'text-left'
                }`}>
                  {formatTime(message.timestamp)}
                </div>
              </div>
            </div>
          ))}

          {/* Loading indicator */}
          {isLoading && (
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-full bg-white shadow-md text-blue-600">
                <Bot className="w-5 h-5" />
              </div>
              <div className="bg-white p-4 rounded-2xl rounded-tl-md shadow-sm border border-blue-100">
                <div className="flex items-center gap-2">
                  <Search className="w-4 h-4 text-blue-600 animate-spin" />
                  <span className="text-gray-600">Searching and analyzing...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-white border-t border-blue-200">
          <div className="flex gap-3 items-end">
            <div className="flex-1 relative">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me anything... I'll search the web and provide you with comprehensive answers."
                className="w-full p-4 pr-12 border border-blue-200 rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent min-h-[60px] max-h-32"
                rows={1}
                style={{ 
                  height: 'auto',
                  minHeight: '60px'
                }}
                onInput={(e) => {
                  e.target.style.height = 'auto';
                  e.target.style.height = Math.min(e.target.scrollHeight, 128) + 'px';
                }}
                disabled={isLoading}
              />
            </div>
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isLoading}
              className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 disabled:from-gray-400 disabled:to-gray-500 text-white p-4 rounded-2xl transition-all duration-200 shadow-lg hover:shadow-xl disabled:shadow-md"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          
          {/* Footer */}
          <div className="text-center mt-3 text-xs text-gray-500">
            Powered by Atos AI • Web Search Enhanced • 
            <span className="text-blue-600 font-medium"> Always Learning</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AtosChatbot;'''

    with open('src/components/AtosChatbot.js', 'w', encoding='utf-8') as f:
        f.write(component_code)
    print_success("React component created")

def create_config_files():
    """Create all configuration files"""
    print_status("Creating configuration files...")
    
    # Create App.js
    app_js = '''import React from 'react';
import AtosChatbot from './components/AtosChatbot';
import './App.css';

function App() {
  return (
    <div className="App">
      <AtosChatbot />
    </div>
  );
}

export default App;'''
    
    with open('src/App.js', 'w', encoding='utf-8') as f:
        f.write(app_js)
    
    # Create App.css
    app_css = '''@tailwind base;
@tailwind components;
@tailwind utilities;

.App {
  height: 100vh;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

* {
  box-sizing: border-box;
}'''
    
    with open('src/App.css', 'w', encoding='utf-8') as f:
        f.write(app_css)
    
    # Create index.js
    index_js = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './App.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);'''
    
    with open('src/index.js', 'w', encoding='utf-8') as f:
        f.write(index_js)
    
    # Create public/index.html
    index_html = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#2563eb" />
    <meta name="description" content="Atos AI Assistant - Web Search Enhanced Chatbot" />
    <title>Atos AI Assistant</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>'''
    
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    # Create tailwind.config.js
    tailwind_config = '''module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'atos-blue': {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af'
        }
      }
    },
  },
  plugins: [],
}'''
    
    with open('tailwind.config.js', 'w', encoding='utf-8') as f:
        f.write(tailwind_config)
    
    # Create postcss.config.js
    postcss_config = '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}'''
    
    with open('postcss.config.js', 'w', encoding='utf-8') as f:
        f.write(postcss_config)
    
    print_success("Configuration files created")

def create_environment_files():
    """Create environment configuration files"""
    print_status("Creating environment files...")
    
    env_example = '''# Copilot Studio API Configuration
REACT_APP_COPILOT_API_ENDPOINT=https://your-copilot-studio-endpoint.com/api/chat
REACT_APP_API_KEY=your-api-key-here
REACT_APP_SUBSCRIPTION_KEY=your-subscription-key-here

# Optional: Application Configuration
REACT_APP_APP_NAME=Atos AI Assistant
REACT_APP_VERSION=1.0.0'''
    
    with open('.env.example', 'w', encoding='utf-8') as f:
        f.write(env_example)
    
    env_local = '''# Copilot Studio API Configuration
REACT_APP_COPILOT_API_ENDPOINT=YOUR_COPILOT_STUDIO_ENDPOINT_HERE
REACT_APP_API_KEY=your-actual-api-key
REACT_APP_SUBSCRIPTION_KEY=your-actual-subscription-key

# Optional: Application Configuration
REACT_APP_APP_NAME=Atos AI Assistant
REACT_APP_VERSION=1.0.0'''
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_local)
    
    print_success("Environment files created")

def create_github_workflows():
    """Create GitHub Actions workflows"""
    print_status("Creating GitHub Actions workflows...")
    
    # GitHub Pages deployment
    github_pages_workflow = '''name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4
      
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        
    - name: Install dependencies
      run: npm ci
      
    - name: Build
      run: npm run build
      env:
        REACT_APP_COPILOT_API_ENDPOINT: ${{ secrets.REACT_APP_COPILOT_API_ENDPOINT }}
        REACT_APP_API_KEY: ${{ secrets.REACT_APP_API_KEY }}
        REACT_APP_SUBSCRIPTION_KEY: ${{ secrets.REACT_APP_SUBSCRIPTION_KEY }}
        
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      if: github.ref == 'refs/heads/main'
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./build'''
    
    with open('.github/workflows/deploy.yml', 'w', encoding='utf-8') as f:
        f.write(github_pages_workflow)
    
    # Azure Static Web Apps workflow
    azure_workflow = '''name: Azure Static Web Apps CI/CD

on:
  push:
    branches:
      - main
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches:
      - main

jobs:
  build_and_deploy_job:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    name: Build and Deploy Job
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
      - name: Build And Deploy
        id: builddeploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "/"
          build_location: "build"
          output_location: "build"
          
  close_pull_request_job:
    if: github.event_name == 'pull_request' && github.event.action == 'closed'
    runs-on: ubuntu-latest
    name: Close Pull Request Job
    steps:
      - name: Close Pull Request
        id: closepullrequest
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          action: "close"'''
    
    with open('.github/workflows/azure-static-web-apps.yml', 'w', encoding='utf-8') as f:
        f.write(azure_workflow)
    
    print_success("GitHub workflows created")

def create_gitignore():
    """Create .gitignore file"""
    print_status("Creating .gitignore...")
    
    gitignore_content = '''# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Production build
build/
dist/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs
*.log

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# nyc test coverage
.nyc_output

# ESLint cache
.eslintcache

# Optional npm cache directory
.npm

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# parcel-bundler cache (https://parceljs.org/)
.cache
.parcel-cache

# next.js build output
.next

# nuxt.js build output
.nuxt

# vuepress build output
.vuepress/dist

# Serverless directories
.serverless

# Editor directories and files
.idea
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?'''
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print_success(".gitignore created")

def create_readme():
    """Create comprehensive README.md"""
    print_status("Creating README.md...")
    
    readme_content = '''# Atos AI Assistant Chatbot

A modern, responsive chatbot application built with React and integrated with Microsoft Copilot Studio for intelligent web search and AI-powered responses.

## 🚀 Features

- **Modern Chat Interface**: Clean, responsive design with Atos branding
- **Web Search Integration**: Powered by Copilot Studio Agent API
- **Real-time Responses**: Instant AI-powered answers to user queries
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- **Professional UI**: Atos color scheme (royal blue and light blue)

## 🛠️ Technology Stack

- **Frontend**: React 18, Tailwind CSS, Lucide React Icons
- **Backend**: Microsoft Copilot Studio Agent API
- **Deployment**: GitHub Pages / Azure Static Web Apps
- **Styling**: Tailwind CSS with custom Atos theme

## 📋 Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Git
- Microsoft Copilot Studio access

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/IN-PUN-COAONE-AUTOMATNSA/copilot-websearch.git
cd copilot-websearch
npm install
```

### 2. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your Copilot Studio API credentials
```

### 3. Development
```bash
npm start
# Opens on http://localhost:3000
```

### 4. Production Build
```bash
npm run build
npm run deploy
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
REACT_APP_COPILOT_API_ENDPOINT=https://your-copilot-studio-endpoint.com/api/chat
REACT_APP_API_KEY=your-api-key-here
REACT_APP_SUBSCRIPTION_KEY=your-subscription-key-here
```

### Copilot Studio Integration

The application is designed to work with Microsoft Copilot Studio Agent APIs. Update the API endpoint and authentication headers in the environment variables.

## 🚀 Deployment

### GitHub Pages
The application automatically deploys to GitHub Pages when you push to the main branch.

### Azure Static Web Apps
Configure Azure Static Web Apps for enterprise deployment with the included workflow.

## 🎨 Customization

### Branding
- Colors: Defined in `tailwind.config.js`
- Logo: Update in the header component
- Messaging: Modify initial greeting and placeholder text

### API Integration
- Endpoint configuration: `.env` file
- Request/response format: `src/components/AtosChatbot.js`

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is proprietary to Atos.

## 🆘 Support

For technical support, please contact the development team or raise an issue in the repository.

---

**Powered by Atos AI • Web Search Enhanced • Always Learning**'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print_success("README.md created")

def main():
    """Main automation function"""
    print_status("🎯 Atos Chatbot Deployment Automation Starting...")
    print_status("Current directory: " + os.getcwd())
    
    # Check prerequisites
    check_prerequisites()
    
    # Create folder structure
    create_folder_structure()
    
    # Create package.json
    create_package_json()
    
    # Install dependencies
    print_status("Installing npm dependencies...")
    if not run_command("npm install"):
        print_error("Failed to install npm dependencies")
        sys.exit(1)
    
    # Install Tailwind CSS
    print_status("Installing Tailwind CSS...")
    if not run_command("npm install -D tailwindcss postcss autoprefixer"):
        print_warning("Failed to install Tailwind CSS via npm")
    
    if not run_command("npx tailwindcss init -p"):
        print_warning("Failed to initialize Tailwind CSS")
    
    # Install additional dependencies
    print_status("Installing additional dependencies...")
    if not run_command("npm install lucide-react"):
        print_warning("Failed to install lucide-react")
    
    if not run_command("npm install gh-pages --save-dev"):
        print_warning("Failed to install gh-pages")
    
    # Create all files
    create_react_component()
    create_config_files()
    create_environment_files()
    create_github_workflows()
    create_gitignore()
    create_readme()
    
    # Git setup
    print_status("Setting up Git...")
    run_command("git add .")
    run_command('git commit -m "Initial commit: Atos Chatbot with Copilot Studio integration"')
    
    # Final build test
    print_status("Testing build...")
    if run_command("npm run build"):
        print_success("Build successful!")
    else:
        print_warning("Build failed - check for errors")
    
    # Final instructions
    print_success("🎉 Deployment automation completed successfully!")
    print("")
    print_status("📋 Next Steps:")
    print(f"{Colors.YELLOW}1. Update .env file with your Copilot Studio API credentials{Colors.END}")
    print(f"{Colors.YELLOW}2. Test locally: npm start{Colors.END}")
    print(f"{Colors.YELLOW}3. Push to GitHub: git push origin main{Colors.END}")
    print(f"{Colors.YELLOW}4. Enable GitHub Pages in repository settings{Colors.END}")
    print("")
    print_status("🔗 Your app will be available at:")
    print(f"{Colors.GREEN}https://in-pun-coaone-automatnsa.github.io/copilot-websearch/{Colors.END}")
    
    print("")
    print_status("🛠️ Development Commands:")
    print(f"{Colors.BLUE}npm start          {Colors.END}# Start development server")
    print(f"{Colors.BLUE}npm run build      {Colors.END}# Create production build")
    print(f"{Colors.BLUE}npm run deploy     {Colors.END}# Deploy to GitHub Pages")
    print(f"{Colors.BLUE}npm test           {Colors.END}# Run tests")

if __name__ == "__main__":
    main()