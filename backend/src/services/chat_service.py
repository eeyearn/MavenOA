"""
Chat Service - Handles chat interactions with RAG (Retrieval Augmented Generation)

This service:
1. Uses search tool to find relevant chunks
2. Builds context from search results
3. Generates intelligent responses using an LLM
4. Cites sources clearly in responses
"""

from typing import List, Optional
import os
from dotenv import load_dotenv
from openai import OpenAI
from ..types import ChatRequest, ChatResponse, SearchRequest, SearchResult
from ..tools.search_tool import search_documents

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ChatService:
    """
    Service responsible for handling chat interactions with context from Google Drive.
    
    Uses RAG (Retrieval Augmented Generation) to provide accurate, cited responses.
    """

    def __init__(self):
        self.llm = openai_client
        # Model configuration
        self.model = "gpt-4o-mini"  # Good balance of quality and cost
        self.max_tokens = 1000
        self.temperature = 0.7

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Process a chat message and return a response with sources.
        
        Steps:
        1. Use search tool to find relevant chunks
        2. Build context from retrieved chunks
        3. Construct prompt with context and conversation history
        4. Generate response using LLM
        5. Format response with source citations
        6. Return ChatResponse with message and sources
        """
        try:
            # Step 1: Retrieve relevant documents
            print(f"Searching for: {request.message}")
            sources = await search_documents(
                query=request.message,
                folder_id=request.folder_id,
                file_id=request.file_id,
                limit=5  # Get top 5 most relevant chunks
            )
            
            print(f"Found {len(sources)} relevant sources")
            
            if not sources:
                response_text = "I couldn't find any relevant information in your Google Drive to answer that question."
                return ChatResponse(message=response_text, sources=[])
            
            # Step 2: Build context from sources
            context = self._build_context(sources)
            
            # Step 3: Generate response using LLM
            response_text = await self._generate_response(
                message=request.message,
                context=context,
                history=request.conversation_history
            )
            
            # Step 4: Return with sources
            return ChatResponse(
                message=response_text,
                sources=sources
            )
            
        except Exception as e:
            print(f"Error in chat: {str(e)}")
            # Return error message with no sources
            return ChatResponse(
                message=f"I'm sorry, I encountered an error while processing your request: {str(e)}",
                sources=[]
            )

    def _build_context(self, sources: List[SearchResult]) -> str:
        """
        Build context string from search results.
        
        Combines relevant chunks into coherent context with source attribution.
        """
        context = ""
        for i, source in enumerate(sources):
            context += f"Source {i+1} (File: {source.metadata.get('file_name', 'Unknown')}, Link: {source.metadata.get('web_view_link', '#')}):\n"
            context += f"```{source.text}```\n\n"
        return context

    async def _generate_response(
        self, 
        message: str, 
        context: str, 
        history: Optional[List] = None
    ) -> str:
        """
        Generate LLM response given message, context, and history.
        
        Uses OpenAI's chat completion API with carefully crafted prompts
        to ensure accurate, cited responses.
        """
        # System prompt - instructions for the LLM
        system_prompt = """You are a helpful AI assistant that helps users find and understand information from their Google Drive documents.

Your responsibilities:
1. Answer questions accurately based ONLY on the provided context from Google Drive documents
2. Always cite your sources by mentioning the document name when you use information from it
3. If the answer is not in the provided context, clearly say so - don't make up information
4. Be concise but thorough in your responses
5. When multiple documents contain relevant information, synthesize it clearly

Remember: Only use information from the provided sources. If you're not sure, say so."""

        # Build messages for the API
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history if provided (for context continuity)
        if history and len(history) > 0:
            for msg in history[-5:]:  # Only include last 5 messages to manage token limits
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Add the current user message with context
        user_message = f"""Based on the following documents from Google Drive:

{context}

Question: {message}

Please provide a helpful answer based on the information above. Remember to cite which document(s) you're getting the information from."""

        messages.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Call OpenAI API
            response = self.llm.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error calling LLM: {str(e)}")
            return f"I encountered an error generating a response: {str(e)}"


# Global instance
chat_service = ChatService()
