// Global variables
let isTyping = false;
let chatHistory = [];

// DOM elements
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');
const chatContainer = document.getElementById('chatContainer');
const welcomeSection = document.getElementById('welcomeSection');
const typingIndicator = document.getElementById('typingIndicator');
const loadingOverlay = document.getElementById('loadingOverlay');
const sampleQuestionsModal = document.getElementById('sampleQuestionsModal');
const sampleQuestionsList = document.getElementById('sampleQuestionsList');
const closeModal = document.getElementById('closeModal');
const showSampleQuestions = document.getElementById('showSampleQuestions');
const clearChat = document.getElementById('clearChat');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadSampleQuestions();
});

// Initialize the application
async function initializeApp() {
    try {
        // Show loading overlay
        loadingOverlay.style.display = 'flex';
        
        // Check if the API is healthy
        const response = await fetch('/api/health');
        if (response.ok) {
            console.log('✅ API is healthy');
        } else {
            throw new Error('API health check failed');
        }
        
        // Hide loading overlay after a short delay
        setTimeout(() => {
            loadingOverlay.style.display = 'none';
        }, 1500);
        
    } catch (error) {
        console.error('❌ Error initializing app:', error);
        loadingOverlay.style.display = 'none';
        showErrorMessage('Failed to connect to the AI assistant. Please refresh the page and try again.');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Send message on button click
    sendButton.addEventListener('click', sendMessage);
    
    // Send message on Enter key press
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Show sample questions modal
    showSampleQuestions.addEventListener('click', function() {
        sampleQuestionsModal.classList.add('show');
    });
    
    // Close sample questions modal
    closeModal.addEventListener('click', function() {
        sampleQuestionsModal.classList.remove('show');
    });
    
    // Close modal when clicking outside
    sampleQuestionsModal.addEventListener('click', function(e) {
        if (e.target === sampleQuestionsModal) {
            sampleQuestionsModal.classList.remove('show');
        }
    });
    
    // Clear chat
    clearChat.addEventListener('click', function() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            clearChatHistory();
        }
    });
    
    // Auto-resize input
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
}

// Load sample questions
async function loadSampleQuestions() {
    try {
        const response = await fetch('/api/sample-questions');
        const data = await response.json();
        
        sampleQuestionsList.innerHTML = '';
        data.questions.forEach((question, index) => {
            const questionElement = document.createElement('div');
            questionElement.className = 'sample-question';
            questionElement.innerHTML = `
                <i class="fas fa-question-circle"></i>
                ${question}
            `;
            questionElement.addEventListener('click', function() {
                messageInput.value = question;
                sampleQuestionsModal.classList.remove('show');
                sendMessage();
            });
            sampleQuestionsList.appendChild(questionElement);
        });
    } catch (error) {
        console.error('Error loading sample questions:', error);
    }
}

// Send message function
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isTyping) return;
    
    // Hide welcome section and show chat
    if (welcomeSection.style.display !== 'none') {
        welcomeSection.style.display = 'none';
        chatContainer.style.display = 'flex';
    }
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Disable input and show typing indicator
    setTypingState(true);
    
    try {
        // Send message to API
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Add assistant response to chat
        addMessage(data.answer, 'assistant', data.sources, data.confidence);
        
        // Store in chat history
        chatHistory.push({
            user: message,
            assistant: data.answer,
            timestamp: data.timestamp,
            sources: data.sources,
            confidence: data.confidence
        });
        
    } catch (error) {
        console.error('Error sending message:', error);
        addMessage('Sorry, I encountered an error while processing your request. Please try again.', 'assistant');
    } finally {
        setTypingState(false);
    }
}

// Add message to chat
function addMessage(content, sender, sources = null, confidence = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    // Format content with proper line breaks and bullet points
    if (sender === 'assistant') {
        // For assistant messages, format with HTML to preserve line breaks
        let formattedContent = content
            .replace(/\n/g, '<br>')  // Convert newlines to <br>
            .replace(/\* /g, '• ')   // Convert * to bullet points
            .replace(/• /g, '<br>• '); // Add line break before each bullet point
        
        // Remove the first <br> if it exists at the beginning
        if (formattedContent.startsWith('<br>')) {
            formattedContent = formattedContent.substring(4);
        }
        
        messageContent.innerHTML = formattedContent;
    } else {
        // For user messages, keep as plain text
        messageContent.textContent = content;
    }
    
    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = new Date().toLocaleTimeString();
    
    messageDiv.appendChild(messageContent);
    
    // Sources are now hidden from the frontend for better user experience
    
    // Confidence score is now hidden for cleaner user experience
    
    messageDiv.appendChild(messageTime);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Set typing state
function setTypingState(typing) {
    isTyping = typing;
    sendButton.disabled = typing;
    messageInput.disabled = typing;
    
    if (typing) {
        typingIndicator.style.display = 'flex';
    } else {
        typingIndicator.style.display = 'none';
    }
}

// Clear chat history
function clearChatHistory() {
    chatMessages.innerHTML = '';
    chatHistory = [];
    welcomeSection.style.display = 'block';
    chatContainer.style.display = 'none';
}

// Show error message
function showErrorMessage(message) {
    addMessage(message, 'assistant');
}

// Utility function to format text
function formatText(text) {
    // Convert line breaks to HTML
    return text.replace(/\n/g, '<br>');
}

// Handle API errors
function handleApiError(error) {
    console.error('API Error:', error);
    let errorMessage = 'An unexpected error occurred. Please try again.';
    
    if (error.message.includes('Failed to fetch')) {
        errorMessage = 'Unable to connect to the server. Please check your internet connection.';
    } else if (error.message.includes('500')) {
        errorMessage = 'Server error occurred. Please try again later.';
    } else if (error.message.includes('400')) {
        errorMessage = 'Invalid request. Please check your input and try again.';
    }
    
    showErrorMessage(errorMessage);
}

// Add smooth scrolling
function smoothScrollToBottom() {
    chatMessages.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: 'smooth'
    });
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        messageInput.focus();
    }
    
    // Escape to close modal
    if (e.key === 'Escape') {
        sampleQuestionsModal.classList.remove('show');
    }
});

// Add loading animation for better UX
function showLoadingAnimation() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant';
    loadingDiv.innerHTML = `
        <div class="message-content">
            <div class="typing-indicator">
                <i class="fas fa-circle"></i>
                <i class="fas fa-circle"></i>
                <i class="fas fa-circle"></i>
                AI is thinking...
            </div>
        </div>
    `;
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return loadingDiv;
}

// Remove loading animation
function removeLoadingAnimation(loadingDiv) {
    if (loadingDiv && loadingDiv.parentNode) {
        loadingDiv.parentNode.removeChild(loadingDiv);
    }
}

// Add message validation
function validateMessage(message) {
    if (!message || message.trim().length === 0) {
        return { valid: false, error: 'Please enter a message.' };
    }
    
    if (message.length > 1000) {
        return { valid: false, error: 'Message is too long. Please keep it under 1000 characters.' };
    }
    
    return { valid: true };
}

// Enhanced send message with validation
async function sendMessage() {
    const message = messageInput.value.trim();
    const validation = validateMessage(message);
    
    if (!validation.valid) {
        showErrorMessage(validation.error);
        return;
    }
    
    if (isTyping) return;
    
    // Hide welcome section and show chat
    if (welcomeSection.style.display !== 'none') {
        welcomeSection.style.display = 'none';
        chatContainer.style.display = 'flex';
    }
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Show loading animation
    const loadingDiv = showLoadingAnimation();
    
    // Disable input
    setTypingState(true);
    
    try {
        // Send message to API
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Remove loading animation
        removeLoadingAnimation(loadingDiv);
        
        // Add assistant response to chat
        addMessage(data.answer, 'assistant', data.sources, data.confidence);
        
        // Store in chat history
        chatHistory.push({
            user: message,
            assistant: data.answer,
            timestamp: data.timestamp,
            sources: data.sources,
            confidence: data.confidence
        });
        
    } catch (error) {
        console.error('Error sending message:', error);
        removeLoadingAnimation(loadingDiv);
        handleApiError(error);
    } finally {
        setTypingState(false);
    }
}
