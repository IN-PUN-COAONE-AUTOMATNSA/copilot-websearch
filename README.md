# Atos AI Assistant Chatbot

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

**Powered by Atos AI • Web Search Enhanced • Always Learning**