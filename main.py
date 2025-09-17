from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import os
from langchain_final_rag import LangChainFinalRAG, SAMPLE_QUESTIONS

# Initialize FastAPI app
app = FastAPI(
    title="MIDC Land Bank RAG Chatbot",
    description="AI-powered chatbot for MIDC land bank data using RAG (Retrieval Augmented Generation)",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Final LangChain RAG service
rag_service = LangChainFinalRAG()

# Pydantic models
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    confidence: float
    timestamp: str
    chat_history: List[str] = []

class SampleQuestionsResponse(BaseModel):
    questions: List[str]

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main chatbot interface"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Static files not found. Please ensure static/index.html exists.</h1>")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    """Handle chat messages and return RAG-generated responses"""
    try:
        if not chat_message.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get response from RAG service
        result = rag_service.query(chat_message.message)
        
        # Add timestamp
        from datetime import datetime
        result['timestamp'] = datetime.now().isoformat()
        
        return ChatResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")

@app.get("/api/sample-questions", response_model=SampleQuestionsResponse)
async def get_sample_questions():
    """Get sample questions for the chatbot"""
    return SampleQuestionsResponse(questions=SAMPLE_QUESTIONS)

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "MIDC Land Bank RAG Chatbot",
        "version": "1.0.0"
    }

@app.get("/api/stats")
async def get_stats():
    """Get basic statistics about the service"""
    try:
        # This would require additional implementation to get actual stats
        return {
            "total_questions_answered": "N/A",
            "service_uptime": "N/A",
            "vector_database_status": "Connected",
            "embedding_model": "sentence-transformers/all-mpnet-base-v2",
            "generation_model": "gemini-2.5-flash",
            "framework": "LangChain"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

@app.post("/api/clear-memory")
async def clear_memory():
    """Clear conversation memory"""
    try:
        rag_service.clear_memory()
        return {"message": "Conversation memory cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing memory: {str(e)}")

@app.get("/api/memory-summary")
async def get_memory_summary():
    """Get conversation memory summary"""
    try:
        summary = rag_service.get_memory_summary()
        return {"memory_summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting memory summary: {str(e)}")

@app.post("/api/clear-memory")
async def clear_memory():
    """Clear the conversation memory"""
    try:
        rag_service.clear_memory()
        return {"message": "Memory cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing memory: {str(e)}")

if __name__ == "__main__":
    # Create static directory if it doesn't exist
    os.makedirs("static", exist_ok=True)
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
