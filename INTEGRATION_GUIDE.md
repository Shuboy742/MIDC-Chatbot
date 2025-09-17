# MIDC Land Bank Chatbot Widget - Integration Guide

## 🎯 Overview
This is a pure HTML/CSS/JS chatbot widget designed for government websites. No backend server required - it can be embedded directly into any website.

## 📁 Files Created
- `midc_chatbot_widget.html` - **Main widget file** (use this one)
- `chatbot_widget.html` - Alternative version
- `INTEGRATION_GUIDE.md` - This guide

## 🚀 Quick Integration

### Method 1: Direct Embedding
```html
<!-- Add this to your government website's HTML -->
<iframe src="midc_chatbot_widget.html" 
        width="500" 
        height="800" 
        frameborder="0"
        style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">
</iframe>
```

### Method 2: Copy & Paste (Recommended)
1. Copy the entire content from `midc_chatbot_widget.html`
2. Paste it into your website's HTML
3. The widget will appear as a floating button

## 🎨 Customization Options

### Colors
The widget uses a professional blue color scheme suitable for government websites:
- **Primary**: `#1e3c72` (Dark Blue)
- **Secondary**: `#2a5298` (Light Blue)
- **Accent**: `#e3f2fd` (Light Blue Background)

### Size
- **Width**: 480px (increased from reference)
- **Height**: 750px (increased from reference)
- **Mobile**: Full screen on mobile devices

### Sample Questions
The widget includes 12 sample questions based on your MIDC data:
- English questions about plots, rates, locations
- Marathi questions for bilingual support
- Questions about specific areas like Bhusaval, Pune, Mumbai

## 🔧 Features

### ✅ What's Included
- **Floating Chat Button** - Appears on bottom right
- **Responsive Design** - Works on desktop and mobile
- **Bilingual Support** - English and Marathi
- **Sample Questions** - 12 pre-loaded questions
- **Typing Indicators** - Shows when assistant is "thinking"
- **Smooth Animations** - Professional transitions
- **Auto-scroll** - Chat area scrolls automatically
- **Keyboard Support** - Enter key to send messages

### 🎯 Sample Questions Included
1. "Plots in Bhusaval"
2. "Commercial plots in Pune"
3. "Cheapest industrial plots"
4. "भुसावळ मध्ये औद्योगिक प्लॉट" (Marathi)
5. "पुणे मध्ये कॉमर्शियल प्लॉट दाखवा" (Marathi)
6. "Plots in Mumbai"
7. "Residential plots"
8. "Current rates"
9. "सर्वात स्वस्त प्लॉट कोणते?" (Marathi)
10. "Industrial areas in Maharashtra"
11. "RO Jalgaon plots available"
12. "मुंबई मध्ये कॉमर्शियल प्लॉट" (Marathi)

## 🔌 API Integration

### Current Status
The widget currently shows mock responses. To connect to your RAG service:

1. **Replace the `generateMIDCResponse()` function** in the JavaScript
2. **Add API call** to your FastAPI backend
3. **Handle real responses** from your RAG service

### Example API Integration
```javascript
async function generateMIDCResponse(userMessage) {
    try {
        const response = await fetch('http://your-api-url/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage })
        });
        
        const data = await response.json();
        addMIDCMessage(data.answer, 'assistant');
    } catch (error) {
        addMIDCMessage('Sorry, I encountered an error. Please try again.', 'assistant');
    }
}
```

## 📱 Mobile Responsive
- **Desktop**: 480x750px floating widget
- **Mobile**: Full screen overlay
- **Touch-friendly**: Large buttons and inputs
- **Swipe gestures**: Smooth interactions

## 🎨 Styling Customization

### Change Colors
```css
/* Primary color (header, buttons) */
background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);

/* Message bubbles */
.midc-message.assistant {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
}

/* Sample question hover */
.midc-sample-question:hover {
    background: #1e3c72;
}
```

### Change Size
```css
.midc-chatbot-container {
    width: 500px;  /* Increase width */
    height: 800px; /* Increase height */
}
```

## 🔒 Security Considerations
- **No external dependencies** - Pure HTML/CSS/JS
- **No data collection** - All data stays local
- **CORS ready** - Can be embedded in any domain
- **Government compliant** - Professional design suitable for official websites

## 📞 Support
For customization or integration help, refer to the code comments in `midc_chatbot_widget.html`.

## 🎯 Next Steps
1. **Test the widget** by opening `midc_chatbot_widget.html` in a browser
2. **Customize colors** if needed
3. **Add more sample questions** based on your data
4. **Integrate with your RAG API** for real responses
5. **Embed in your government website**

---

**Ready to use!** 🚀
