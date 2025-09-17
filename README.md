# 🏭 MIDC Land Bank RAG Chatbot

A sophisticated AI-powered chatbot for the Maharashtra Industrial Development Corporation (MIDC) Land Bank, built using Retrieval-Augmented Generation (RAG) technology. This chatbot provides intelligent responses about land plots, industrial areas, and property details by leveraging vector database search and advanced language models.

## 🌟 Features

- **🤖 Intelligent Chatbot**: Natural language processing with context-aware responses
- **🔍 Semantic Search**: Advanced vector-based search using Pinecone
- **🌐 Multilingual Support**: Responds in English and Marathi based on user input
- **💬 Real-time Chat**: Live typing indicators and smooth chat experience
- **📱 Responsive Design**: Beautiful, mobile-friendly interface
- **🏢 Government Integration**: Ready for embedding in government websites
- **🧠 Smart Query Processing**: Handles spelling mistakes, location variations, and semantic understanding
- **📊 Comprehensive Data**: Covers all MIDC land bank information

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **LangChain**: Framework for developing applications powered by language models
- **Google Gemini 2.5 Flash**: Advanced language model for response generation
- **Pinecone**: Vector database for semantic search
- **Sentence Transformers**: Embedding model (`all-mpnet-base-v2`)
- **Python 3.11+**: Core programming language

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript (ES6+)**: Interactive functionality
- **Responsive Design**: Mobile-first approach

### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **NLTK**: Natural language processing
- **Regex**: Pattern matching and text processing

### Infrastructure
- **Uvicorn**: ASGI server for FastAPI
- **CORS**: Cross-origin resource sharing
- **Environment Variables**: Secure configuration management

## 📋 Prerequisites

### System Requirements
- **Python**: 3.11 or higher
- **Operating System**: Windows 10/11, Linux (Ubuntu 20.04+), or macOS
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 2GB free space

### API Keys Required
1. **Pinecone API Key**: For vector database access
2. **Google Gemini API Key**: For language model access

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd MIDC-Local
```

### 2. Quick Access (If Already Set Up)
If the project is already configured and running:
- **Backend**: http://localhost:8000
- **Chatbot**: **http://localhost:8080/midc_chatbot_widget.html**

### 3. Environment Setup

#### Create Virtual Environment
```bash
# Windows
python -m venv rag_env
rag_env\Scripts\activate

# Linux/macOS
python3 -m venv rag_env
source rag_env/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration

#### Create Environment File
Create a `.env` file in the project root:

```env
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=midc-land-bank

# Google Gemini Configuration
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

#### Get API Keys

**Pinecone API Key:**
1. Visit [Pinecone Console](https://app.pinecone.io/)
2. Sign up/Login to your account
3. Go to API Keys section
4. Copy your API key

**Google Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the generated key

### 5. Run the Application

#### Start Backend Server
```bash
# Windows
rag_env\Scripts\activate
python main.py

# Linux/macOS
source rag_env/bin/activate
python main.py
```

The backend will start on `http://localhost:8000`

#### Access the Chatbot
Open `midc_chatbot_widget.html` in your web browser or serve it using a local server:

```bash
# Using Python's built-in server
python -m http.server 8080
```

Then visit: **http://localhost:8080/midc_chatbot_widget.html**

> **Note**: Make sure both the backend server (port 8000) and frontend server (port 8080) are running simultaneously for the chatbot to work properly.

## 📁 Project Structure

```
MIDC-Local/
├── 📄 main.py                          # FastAPI backend server
├── 📄 langchain_final_rag.py           # Core RAG implementation
├── 📄 improved_query_handler.py        # Smart query processing
├── 📄 config.py                        # Configuration settings
├── 📄 requirements.txt                 # Python dependencies
├── 📄 start.sh                         # Linux startup script
├── 📄 .env                             # Environment variables (create this)
├── 📄 README.md                        # This file
├── 📄 INTEGRATION_GUIDE.md             # Website integration guide
├── 📄 midc_chatbot_widget.html         # Main chatbot interface
├── 📄 chatbot_widget.html              # Alternative interface
├── 📁 image/
│   └── 📄 MIDC.jpg                     # MIDC logo
├── 📁 static/                          # Static web assets
│   ├── 📄 index.html
│   ├── 📄 script.js
│   └── 📄 style.css
├── 📁 rag_env/                         # Python virtual environment
└── 📁 __pycache__/                     # Python cache files
```

## 🔧 Detailed Setup Instructions

### Windows Setup

#### 1. Install Python
1. Download Python 3.11+ from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation: `python --version`

#### 2. Setup Project
```cmd
# Navigate to project directory
cd C:\path\to\MIDC-Local

# Create virtual environment
python -m venv rag_env

# Activate virtual environment
rag_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure Environment
Create `.env` file with your API keys (see Configuration section above)

#### 4. Run Application
```cmd
# Activate environment (if not already active)
rag_env\Scripts\activate

# Start backend
python main.py

# In another terminal, serve frontend
python -m http.server 8080
```

#### 5. Access the Chatbot
Open your web browser and visit: **http://localhost:8080/midc_chatbot_widget.html**

### Linux Setup

#### 1. Install Python and Dependencies
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# CentOS/RHEL
sudo yum install python3.11 python3.11-venv python3-pip

# Verify installation
python3 --version
```

#### 2. Setup Project
```bash
# Navigate to project directory
cd /path/to/MIDC-Local

# Create virtual environment
python3 -m venv rag_env

# Activate virtual environment
source rag_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure Environment
Create `.env` file with your API keys

#### 4. Run Application
```bash
# Make startup script executable
chmod +x start.sh

# Start application
./start.sh

# Or manually:
source rag_env/bin/activate
python main.py

# In another terminal, serve frontend
python3 -m http.server 8080
```

#### 5. Access the Chatbot
Open your web browser and visit: **http://localhost:8080/midc_chatbot_widget.html**

## 🎯 Usage

### Basic Usage
1. **Open the Chatbot**: Visit **http://localhost:8080/midc_chatbot_widget.html** in your browser
2. **Ask Questions**: Type queries about land plots, industrial areas, or property details
3. **Get Responses**: Receive intelligent, data-driven answers from the MIDC database

### Sample Questions
- "What are the cheapest industrial plots?"
- "Show me commercial plots in Pune"
- "Plots in Bhusaval"
- "मुंबई मध्ये कॉमर्शियल प्लॉट" (Marathi)
- "Punyat kuthlya jaga ahet?" (Marathi transliteration)

### Features
- **Multilingual**: Automatically detects and responds in English or Marathi
- **Smart Search**: Handles spelling mistakes and location variations
- **Context Awareness**: Maintains conversation history
- **Real-time**: Live typing indicators and instant responses

## 🔌 API Endpoints

### Backend API (FastAPI)
- `POST /api/chat` - Send chat messages
- `POST /api/clear-memory` - Clear conversation history
- `GET /health` - Health check endpoint

### Request Format
```json
{
  "message": "What are the cheapest industrial plots?",
  "chat_history": []
}
```

### Response Format
```json
{
  "answer": "Based on our MIDC Land Bank database...",
  "sources": ["relevant_data_sources"]
}
```

## 🌐 Website Integration

The chatbot is designed to be embedded in government websites. See `INTEGRATION_GUIDE.md` for detailed integration instructions.

### Quick Integration
1. Copy `midc_chatbot_widget.html` to your website
2. Ensure the backend is running on your server
3. Update the API endpoint URL in the JavaScript
4. Customize styling to match your website theme

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Solution: Ensure virtual environment is activated
source rag_env/bin/activate  # Linux/macOS
rag_env\Scripts\activate     # Windows
```

#### 2. API Key Errors
```bash
# Solution: Check .env file exists and contains valid keys
cat .env  # Linux/macOS
type .env # Windows
```

#### 3. Port Already in Use
```bash
# Solution: Kill existing processes or use different port
pkill -f "python main.py"
# Or change port in main.py
```

#### 4. Pinecone Connection Issues
- Verify API key is correct
- Check internet connection
- Ensure Pinecone index exists and is accessible

#### 5. Frontend Not Loading
- Check if backend is running on port 8000
- Verify CORS settings in main.py
- Check browser console for errors

### Debug Mode
Enable debug logging by setting environment variable:
```bash
export DEBUG=1  # Linux/macOS
set DEBUG=1     # Windows
```

## 📊 Performance Optimization

### Backend Optimization
- Use production ASGI server (Gunicorn with Uvicorn workers)
- Implement Redis caching for frequent queries
- Optimize vector search parameters
- Use connection pooling for database connections

### Frontend Optimization
- Minify CSS and JavaScript
- Implement lazy loading for images
- Use CDN for static assets
- Enable browser caching

## 🔒 Security Considerations

### API Security
- Use HTTPS in production
- Implement rate limiting
- Validate and sanitize all inputs
- Use environment variables for sensitive data

### Data Privacy
- No user data is permanently stored
- Chat history is cleared on session end
- API keys are kept secure in environment variables

## 🚀 Deployment

### Production Deployment
1. **Server Setup**: Use a production server (AWS, GCP, Azure)
2. **Environment**: Set up production environment variables
3. **Process Management**: Use PM2 or systemd for process management
4. **Reverse Proxy**: Configure Nginx or Apache as reverse proxy
5. **SSL Certificate**: Install SSL certificate for HTTPS
6. **Monitoring**: Set up logging and monitoring

### Docker Deployment (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is developed for the Maharashtra Industrial Development Corporation (MIDC) and is intended for government use.

## 📞 Support

For technical support or questions:
- Check the troubleshooting section above
- Review the integration guide
- Contact the development team

## 🔄 Version History

- **v1.0.0**: Initial release with basic RAG functionality
- **v1.1.0**: Added multilingual support (English/Marathi)
- **v1.2.0**: Enhanced query processing and smart search
- **v1.3.0**: Improved UI/UX with typing indicators
- **v1.4.0**: Added MIDC branding and logo integration

---

**Built with ❤️ for MIDC Land Bank Services**
