"""
Chat Service - TEMPLATE FOR CANDIDATES TO IMPLEMENT

TODO: Implement this service to:
1. Use retrieval service to find relevant chunks
2. Build context from search results
3. Generate intelligent responses using an LLM
4. Cite sources clearly in responses

Key considerations:
- Choose an appropriate LLM (OpenAI, Anthropic, Cohere, etc.)
- Build effective prompts with retrieved context
- Handle conversation history
- Implement proper source attribution
"""

from typing import List
from ..types import ChatRequest, ChatResponse, SearchRequest
from .retrieval_service import retrieval_service


class ChatService:
    """
    Service responsible for handling chat interactions with context from Google Drive.

    Candidates should implement:
    - LLM client initialization
    - Context building from search results
    - Prompt engineering for accurate responses
    - Source attribution in responses
    """

    def __init__(self):
        # TODO: Initialize your LLM client here
        # Examples:
        # - OpenAI: self.llm = openai.ChatCompletion
        # - Anthropic: self.llm = anthropic.Anthropic()
        # - Cohere: self.llm = cohere.Client()

        self.llm = None  # Replace with your LLM client

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Process a chat message and return a response with sources.

        TODO: Implement the following steps:
        1. Use retrieval_service to find relevant chunks
        2. Build context from retrieved chunks
        3. Construct prompt with context and conversation history
        4. Generate response using LLM
        5. Format response with source citations
        6. Return ChatResponse with message and sources

        Args:
            request: ChatRequest with message and optional context

        Returns:
            ChatResponse with generated message and source citations

        Consider:
        - Including conversation history for context
        - Limiting context size to fit LLM token limits
        - Instructing LLM to cite sources in response
        - Handling cases where no relevant documents are found
        - Making responses concise and accurate
        """
        # TODO: Implement chat logic
        raise NotImplementedError("Candidates must implement chat")

        # Example structure:
        # # Step 1: Retrieve relevant documents
        # search_request = SearchRequest(
        #     query=request.message,
        #     folderId=request.folder_id,
        #     fileId=request.file_id,
        #     limit=5
        # )
        # sources = await retrieval_service.search(search_request)
        #
        # # Step 2: Build context
        # context = self._build_context(sources)
        #
        # # Step 3: Generate response
        # response_text = await self._generate_response(
        #     message=request.message,
        #     context=context,
        #     history=request.conversation_history
        # )
        #
        # # Step 4: Return with sources
        # return ChatResponse(
        #     message=response_text,
        #     sources=sources
        # )

    def _build_context(self, sources: List) -> str:
        """
        Build context string from search results.

        TODO: Implement context building:
        - Combine relevant chunks into coherent context
        - Include source attribution for each chunk
        - Format for LLM prompt
        - Handle context length limits

        Args:
            sources: List of SearchResult objects

        Returns:
            Formatted context string
        """
        # TODO: Implement context building
        raise NotImplementedError("Candidates must implement _build_context")

        # Example format:
        # context_parts = []
        # for i, source in enumerate(sources, 1):
        #     context_parts.append(
        #         f"[Source {i}] From '{source.file.name}' ({source.file.path}):\n"
        #         f"{source.snippet}\n"
        #     )
        # return "\n\n".join(context_parts)

    async def _generate_response(self, message: str, context: str, history: List = None) -> str:
        """
        Generate LLM response given message, context, and history.

        TODO: Implement LLM response generation:
        1. Build system prompt with instructions
        2. Include context from retrieved documents
        3. Add conversation history if provided
        4. Call LLM API
        5. Extract and return response text

        Args:
            message: User's question
            context: Context from retrieved documents
            history: Optional conversation history

        Returns:
            Generated response text

        Consider:
        - Crafting a system prompt that encourages:
          * Accurate answers based only on provided context
          * Clear source citations
          * Admitting when information isn't available
        - Managing token limits
        - Handling API errors gracefully
        """
        # TODO: Implement LLM response generation
        raise NotImplementedError("Candidates must implement _generate_response")

        # Example with OpenAI:
        # system_prompt = """You are a helpful assistant that answers questions about
        # documents in a Google Drive. Use the provided context to answer questions
        # accurately. Always cite your sources by mentioning the document name.
        # If the answer isn't in the context, say so."""
        #
        # messages = [{"role": "system", "content": system_prompt}]
        #
        # if history:
        #     for msg in history:
        #         messages.append({"role": msg.role, "content": msg.content})
        #
        # messages.append({
        #     "role": "user",
        #     "content": f"Context:\n{context}\n\nQuestion: {message}"
        # })
        #
        # response = await self.llm.create(
        #     model="gpt-4",
        #     messages=messages,
        #     temperature=0.7,
        #     max_tokens=500
        # )
        #
        # return response.choices[0].message.content


# Global instance
chat_service = ChatService()
