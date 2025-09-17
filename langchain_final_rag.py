"""
Final LangChain-based RAG Service for MIDC Land Bank Chatbot
This version combines the best of your final_rag_service.py with LangChain framework
"""

import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import numpy as np

# LangChain imports
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.memory import ConversationBufferMemory

# Direct imports for components
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from pinecone import Pinecone
from improved_query_handler import SmartQueryHandler

# Load environment variables
load_dotenv()

class LangChainFinalRAG:
    def __init__(self):
        """Initialize final LangChain RAG service with all improvements"""
        self.embeddings = None
        self.pinecone_index = None
        self.llm = None
        self.memory = None
        self.prompt_template = None
        self.query_handler = SmartQueryHandler()
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize all services"""
        try:
            print("🚀 Initializing Final LangChain RAG Service...")
            
            # 1. Initialize Embeddings (direct)
            self.embeddings = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
            print("✅ Sentence Transformer initialized")
            
            # 2. Initialize Pinecone (direct)
            pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
            index_name = os.getenv("PINECONE_INDEX_NAME", "midc-land-bank")
            self.pinecone_index = pc.Index(index_name)
            print("✅ Pinecone initialized")
            
            # 3. Initialize Google Gemini (direct)
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.llm = genai.GenerativeModel("gemini-2.5-flash")
            print("✅ Google Gemini initialized")
            
            # 4. Initialize LangChain Memory
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            print("✅ LangChain Memory initialized")
            
            # 5. Create LangChain Prompt Template with natural language
            self.prompt_template = self._create_prompt_template()
            print("✅ LangChain Prompt Template created")
            
            print("✅ Final LangChain RAG Service fully initialized!")
            
        except Exception as e:
            print(f"❌ Error initializing services: {e}")
            raise
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create a LangChain prompt template with natural language"""
        template = """You are a friendly and helpful real estate consultant for MIDC (Maharashtra Industrial Development Corporation) Land Bank. 
You speak in a natural, conversational way - like you're talking to a friend who's looking for property information.

Context Information from MIDC Land Bank Database:
{context}

User Question: {question}

{chat_history}

IMPORTANT INSTRUCTIONS:
- **CONTEXT AWARENESS**: If the user's current question is incomplete or refers to a previous question (like "i want only industrial plots" after asking about a location), use the chat history to understand the full context and provide a complete answer.
- **CRITICAL LANGUAGE DETECTION**: 
  * If the user's question contains ANY Devanagari script characters (like पुणे, भुसावळ, औद्योगिक, etc.), you MUST respond in Marathi.
  * If the user's question is in English, respond in English.
  * This is MANDATORY - always match the user's language exactly.
- **NATURAL CONVERSATIONAL STYLE**:
  * Provide detailed, helpful answers with context and explanations.
  * Include specific details like rates, units, and locations (e.g., "₹4840 प्रति चौ.मी." or "₹4840 per sq. meter").
  * Explain the significance of the information (e.g., "this is cheaper than other areas").
  * Offer comparisons between different options when relevant.
  * Use friendly, conversational language with greetings and closing remarks.
  * If the exact information is not found, suggest alternative options from the available data.
- Write in complete, flowing sentences that sound like natural speech.

RESPONSE STYLE EXAMPLES:

English: "Hi there! Great question! Looking for affordable plots in Mumbai area? Let me check what's available in our MIDC Land Bank database for you. I found some interesting options in the Mumbai region. In Addl. Ambernath, managed by RO Thane-II, there are 2 Industrial 4 plots available at ₹5090 per square meter, which is quite affordable compared to other Mumbai area locations. Additionally, in Kalyan-Bhiwandi, there are 2 Commercial 4 plots at ₹14520 per square meter. While this is higher than Ambernath, it's still more affordable than Thane area rates which start from ₹30800 per square meter for industrial plots."

Marathi: "नमस्कार! छान प्रश्न विचारलात. मुंबई परिसरात स्वस्त जमीन कुठे मिळेल ते पाहूया, मी तुमच्यासाठी MIDC लँड बँक डेटाबेसमधून काही माहिती शोधली आहे. तुम्हाला मुंबई परिसरात स्वस्त जागा हवी असेल, तर मला आमच्या नोंदीनुसार अंबरनाथ (Addl. Ambernath) मध्ये एक चांगला पर्याय दिसत आहे. RO ठाणे-II प्रादेशिक कार्यालयाअंतर्गत असलेल्या अंबरनाथ औद्योगिक क्षेत्रात सध्या 5090 रुपये प्रति चौरस मीटर या दराने औद्योगिक 4 श्रेणीतील 2 प्लॉट उपलब्ध आहेत. हा दर इतर ठिकाणांच्या तुलनेत खूपच कमी आहे."

**FINAL INSTRUCTION**: Look at the user's question carefully. If it contains Devanagari script (Marathi) or Marathi transliteration tokens, respond in Marathi. If it's in English, respond in English. ALWAYS use chat history to understand context - if the current question is incomplete, combine it with previous questions to provide a complete answer."""

        return PromptTemplate(
            template=template,
            input_variables=["context", "question", "chat_history"]
        )
    
    def _improve_query(self, query: str) -> str:
        """Improve query using smart query handler"""
        return self.query_handler.improve_query(query)
    
    def _semantic_search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Perform semantic search using direct Pinecone with improved metadata mapping"""
        try:
            # Improve query
            improved_query = self._improve_query(query)
            
            # Generate embedding
            query_embedding = self.embeddings.encode(improved_query).tolist()
            
            # Search in Pinecone
            search_results = self.pinecone_index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Process results with IMPROVED metadata field mapping
            results = []
            for match in search_results.matches:
                # LOWER the similarity threshold to get more results
                if match.score >= 0.3:  # Lowered threshold for better coverage
                    # Construct text from ACTUAL metadata fields
                    metadata = match.metadata
                    text_parts = []
                    
                    # Map to actual MIDC data fields with better handling
                    if metadata.get('Regional Office'):
                        text_parts.append(f"Regional Office: {metadata['Regional Office']}")
                    
                    if metadata.get('Industrial Area'):
                        text_parts.append(f"Industrial Area: {metadata['Industrial Area']}")
                    
                    # Better handling of numeric fields
                    total_plots = metadata.get('Total Plots Available', 0)
                    if total_plots and total_plots != 0 and not (isinstance(total_plots, float) and np.isnan(total_plots)):
                        text_parts.append(f"Total Plots Available: {int(total_plots)}")
                    
                    current_rate = metadata.get('Current Rate (Rs/sq meter)', 0)
                    if current_rate and current_rate != 0 and not (isinstance(current_rate, float) and np.isnan(current_rate)):
                        text_parts.append(f"Current Rate: {current_rate} Rs per square meter")
                    
                    if metadata.get('Sheet_Name'):
                        text_parts.append(f"Category: {metadata['Sheet_Name']}")
                    
                    # Add source file info for context
                    if metadata.get('source_file'):
                        text_parts.append(f"Source: {metadata['source_file']}")
                    
                    # Only add if we have meaningful content
                    if text_parts:
                        constructed_text = " | ".join(text_parts)
                        
                        results.append({
                            'id': match.id,
                            'score': match.score,
                            'metadata': match.metadata,
                            'text': constructed_text
                        })
            
            return results
            
        except Exception as e:
            print(f"❌ Error in semantic search: {e}")
            return []
    
    def _is_greeting(self, query: str) -> bool:
        """Check if the query is a greeting"""
        query_lower = query.lower().strip()
        greetings = ['hey', 'hello', 'hi', 'good morning', 'good afternoon', 'good evening']
        casual_questions = ['how are you', 'how are you doing', 'what\'s up', 'how do you do']
        
        # Check for pure greetings
        if any(greeting in query_lower for greeting in greetings):
            for greeting in greetings:
                if greeting in query_lower:
                    after_greeting = query_lower.split(greeting, 1)[1].strip()
                    after_greeting = after_greeting.replace(',', '').replace('.', '').replace('!', '').strip()
                    if len(after_greeting) < 3:  # Just greeting, no question
                        return True
                    break
        
        # Check for casual questions
        if any(casual in query_lower for casual in casual_questions):
            return True
            
        return False
    
    def _handle_greeting(self) -> str:
        """Handle greeting queries with natural language"""
        return "Hi there! I'm your friendly MIDC Land Bank AI Assistant powered by LangChain. I'm here to help you find information about land plots, industrial areas, and property details. What can I help you discover today?"
    
    def query(self, user_question: str) -> Dict[str, Any]:
        """Main query method using LangChain components with natural language"""
        try:
            # Check if it's a greeting
            if self._is_greeting(user_question):
                return {
                    'answer': self._handle_greeting(),
                    'sources': [],
                    'confidence': 0.9,
                    'chat_history': [],
                    'is_greeting': True
                }
            
            # Perform semantic search with MORE results
            context_docs = self._semantic_search(user_question, top_k=10)
            
            # Prepare context
            context_text = ""
            for i, doc in enumerate(context_docs, 1):
                context_text += f"Document {i} (Relevance Score: {doc['score']:.3f}):\n"
                context_text += f"{doc['text']}\n\n"
            
            # Get chat history from LangChain memory and format it properly for context
            chat_history = self.memory.chat_memory.messages if hasattr(self.memory, 'chat_memory') else []
            if chat_history:
                chat_history_text = "Previous conversation:\n"
                for msg in chat_history[-4:]:  # Last 4 messages
                    if msg.type == "human":
                        chat_history_text += f"User: {msg.content}\n"
                    elif msg.type == "ai":
                        chat_history_text += f"Assistant: {msg.content}\n"
                chat_history_text += "\nIMPORTANT: If the current question is incomplete or refers to previous context, combine it with the chat history above.\n"
            else:
                chat_history_text = ""
            
            # Format prompt using LangChain template
            formatted_prompt = self.prompt_template.format(
                context=context_text,
                question=user_question,
                chat_history=chat_history_text
            )
            
            # Generate response using Gemini
            response = self.llm.generate_content(formatted_prompt)
            answer = response.text
            
            # Save to LangChain memory
            self.memory.chat_memory.add_user_message(user_question)
            self.memory.chat_memory.add_ai_message(answer)
            
            # Calculate confidence
            confidence = self._calculate_confidence(context_docs)
            
            return {
                'answer': answer,
                'sources': context_docs,
                'confidence': confidence,
                'chat_history': [f"User: {user_question}", f"Assistant: {answer}"],
                'is_greeting': False
            }
                
        except Exception as e:
            print(f"❌ Error in query: {e}")
            return {
                'answer': "I apologize, but I encountered an error while processing your question. Please try again.",
                'sources': [],
                'confidence': 0.0,
                'chat_history': [],
                'is_greeting': False
            }
    
    def _calculate_confidence(self, source_documents: List[Dict[str, Any]]) -> float:
        """Calculate confidence based on source documents"""
        if not source_documents:
            return 0.3
        
        # Simple confidence calculation based on number of sources
        num_sources = len(source_documents)
        if num_sources >= 5:
            return 0.9
        elif num_sources >= 3:
            return 0.7
        elif num_sources >= 1:
            return 0.5
        else:
            return 0.3
    
    def clear_memory(self):
        """Clear conversation memory"""
        if self.memory:
            self.memory.clear()
            print("✅ Conversation memory cleared")
    
    def get_memory_summary(self) -> str:
        """Get summary of conversation memory"""
        if self.memory and hasattr(self.memory, 'chat_memory'):
            return str(self.memory.chat_memory)
        return "No conversation history"

# Test function to verify the RAG service
def test_rag_service():
    """Test the RAG service with sample queries"""
    try:
        rag = LangChainFinalRAG()
        
        # Test queries that were failing
        test_queries = [
            "plots available in pune",
            "industrial plot in mumbai", 
            "commercial plots",
            "Show me commercial plots in Mumbai",
            "What are the cheapest industrial plots?",
            "What plots are available in Addl. Nandurbar (Bhaler)?"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing Query: '{query}'")
            result = rag.query(query)
            print(f"📝 Response: {result['answer'][:200]}...")
            print(f"📊 Context Docs Found: {len(result['sources'])}")
            print(f"🎯 Confidence: {result['confidence']:.3f}")
            if result['sources']:
                print(f"📋 Top Result Score: {result['sources'][0]['score']:.3f}")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

# Sample questions for the frontend
SAMPLE_QUESTIONS = [
    "What are the available industrial plots in Pune?",
    "Show me all plots in MIDC Aurangabad",
    "What is the largest plot available in the database?",
    "How many plots are there in each regional office?",
    "What are the different property types available?",
    "Show me plots with area more than 5000 sq meters",
    "What industrial areas are available in Mumbai region?",
    "How many commercial plots are available?",
    "What is the smallest plot size available?",
    "Show me all plots in MIDC Nagpur"
]

if __name__ == "__main__":
    test_rag_service()
