# modules/conversation_index.py

"""
Conversation History Indexing System
Indexes past conversations and provides relevant context to the agent
"""

import os
import json
import faiss
import numpy as np
import requests
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import hashlib


class ConversationIndex:
    """
    Indexes historical conversations and provides semantic search
    for retrieving relevant past context
    """
    
    def __init__(
        self,
        memory_dir: str = "memory",
        index_dir: str = "conversation_index",
        embed_url: str = "http://localhost:11434/api/embeddings",
        embed_model: str = "nomic-embed-text",
        top_k: int = 3
    ):
        self.memory_dir = Path(memory_dir)
        self.index_dir = Path(index_dir)
        self.embed_url = embed_url
        self.embed_model = embed_model
        self.top_k = top_k
        
        # Create index directory
        self.index_dir.mkdir(exist_ok=True)
        
        # File paths
        self.index_file = self.index_dir / "conversations.index"
        self.metadata_file = self.index_dir / "conversations_metadata.json"
        self.cache_file = self.index_dir / "index_cache.json"
        
        # Load or initialize
        self.index = None
        self.metadata = []
        self.cache = {}
        
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        """Load existing index or create new one"""
        if self.index_file.exists() and self.metadata_file.exists():
            try:
                self.index = faiss.read_index(str(self.index_file))
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
                if self.cache_file.exists():
                    with open(self.cache_file, 'r') as f:
                        self.cache = json.load(f)
                print(f"✅ Loaded conversation index with {len(self.metadata)} entries")
            except Exception as e:
                print(f"⚠️ Error loading index: {e}. Creating new index.")
                self._create_new_index()
        else:
            self._create_new_index()
    
    def _create_new_index(self):
        """Create a new empty index"""
        self.index = None
        self.metadata = []
        self.cache = {}
        print("📝 Created new conversation index")
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """Get embedding vector for text"""
        try:
            response = requests.post(
                self.embed_url,
                json={"model": self.embed_model, "prompt": text},
                timeout=10
            )
            response.raise_for_status()
            embedding = response.json()["embedding"]
            return np.array(embedding, dtype=np.float32)
        except Exception as e:
            print(f"⚠️ Embedding error: {e}")
            # Return zero vector as fallback
            return np.zeros(768, dtype=np.float32)
    
    def _file_hash(self, filepath: Path) -> str:
        """Calculate hash of file for change detection"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""
    
    def index_all_conversations(self, force: bool = False):
        """
        Index all conversations from memory directory
        
        Args:
            force: If True, re-index all files even if unchanged
        """
        print("🔍 Scanning conversation history...")
        
        if not self.memory_dir.exists():
            print("⚠️ Memory directory not found")
            return
        
        indexed_count = 0
        skipped_count = 0
        
        # Find all session JSON files
        session_files = list(self.memory_dir.rglob("session-*.json"))
        
        for session_file in session_files:
            file_hash = self._file_hash(session_file)
            
            # Skip if already indexed and unchanged
            if not force and str(session_file) in self.cache:
                if self.cache[str(session_file)] == file_hash:
                    skipped_count += 1
                    continue
            
            # Index this session
            if self._index_session_file(session_file):
                self.cache[str(session_file)] = file_hash
                indexed_count += 1
        
        # Save index
        if indexed_count > 0:
            self._save_index()
            print(f"✅ Indexed {indexed_count} conversations, skipped {skipped_count}")
        else:
            print(f"ℹ️ No new conversations to index (skipped {skipped_count})")
    
    def _index_session_file(self, filepath: Path) -> bool:
        """Index a single session file"""
        try:
            with open(filepath, 'r') as f:
                session_data = json.load(f)
            
            # Extract relevant conversations
            conversations = self._extract_conversations(session_data, filepath)
            
            if not conversations:
                return False
            
            # Generate embeddings and add to index
            for conv in conversations:
                embedding = self._get_embedding(conv['text'])
                
                # Initialize index if needed
                if self.index is None:
                    dim = len(embedding)
                    self.index = faiss.IndexFlatL2(dim)
                
                # Add to index
                self.index.add(embedding.reshape(1, -1))
                self.metadata.append(conv)
            
            return True
            
        except Exception as e:
            print(f"⚠️ Error indexing {filepath}: {e}")
            return False
    
    def _extract_conversations(self, session_data: List[Dict], filepath: Path) -> List[Dict]:
        """Extract meaningful conversations from session data"""
        conversations = []
        
        # Extract session ID from filepath
        session_id = filepath.stem  # e.g., "session-2025-01-15-1736950000-abc123"
        
        # Group by user query and final answer
        current_query = None
        current_answer = None
        
        for item in session_data:
            item_type = item.get('type', '')
            
            # Track user queries
            if item_type == 'run_metadata':
                text = item.get('text', '')
                if 'Started new session with input:' in text:
                    current_query = text.split('Started new session with input:')[1].strip()
            
            # Track final answers
            if item_type == 'tool_output':
                tool_result = item.get('tool_result', {})
                result_text = tool_result.get('result', '')
                
                if 'FINAL_ANSWER:' in result_text:
                    current_answer = result_text.split('FINAL_ANSWER:')[1].strip()
                    
                    # Create conversation entry
                    if current_query and current_answer:
                        # Create searchable text
                        searchable_text = f"Query: {current_query}\nAnswer: {current_answer}"
                        
                        conversations.append({
                            'text': searchable_text,
                            'query': current_query,
                            'answer': current_answer,
                            'session_id': session_id,
                            'timestamp': item.get('timestamp', 0),
                            'date': datetime.fromtimestamp(item.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')
                        })
                        
                        # Reset for next conversation
                        current_query = None
                        current_answer = None
        
        return conversations
    
    def _save_index(self):
        """Save index, metadata, and cache to disk"""
        try:
            if self.index is not None:
                faiss.write_index(self.index, str(self.index_file))
            
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
            
            print(f"💾 Saved conversation index ({len(self.metadata)} entries)")
        except Exception as e:
            print(f"⚠️ Error saving index: {e}")
    
    def search(self, query: str, exclude_session: Optional[str] = None) -> List[Dict]:
        """
        Search for relevant past conversations
        
        Args:
            query: Current user query
            exclude_session: Session ID to exclude (current session)
        
        Returns:
            List of relevant past conversations
        """
        if self.index is None or len(self.metadata) == 0:
            return []
        
        try:
            # Get query embedding
            query_embedding = self._get_embedding(query)
            
            # Search index
            distances, indices = self.index.search(
                query_embedding.reshape(1, -1),
                min(self.top_k * 2, len(self.metadata))  # Get more to filter
            )
            
            # Collect results
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx < len(self.metadata):
                    conv = self.metadata[idx].copy()
                    conv['similarity_score'] = float(distance)
                    
                    # Exclude current session
                    if exclude_session and conv['session_id'] == exclude_session:
                        continue
                    
                    results.append(conv)
                    
                    if len(results) >= self.top_k:
                        break
            
            return results
            
        except Exception as e:
            print(f"⚠️ Search error: {e}")
            return []
    
    def format_context(self, conversations: List[Dict]) -> str:
        """Format conversations as context for the agent"""
        if not conversations:
            return ""
        
        context_parts = ["📚 Relevant Past Conversations:\n"]
        
        for i, conv in enumerate(conversations, 1):
            context_parts.append(f"\n{i}. [{conv['date']}]")
            context_parts.append(f"   Query: {conv['query']}")
            context_parts.append(f"   Answer: {conv['answer'][:200]}...")  # Truncate long answers
        
        context_parts.append("\n---\n")
        return "\n".join(context_parts)
    
    def get_stats(self) -> Dict:
        """Get index statistics"""
        return {
            'total_conversations': len(self.metadata),
            'index_size': self.index.ntotal if self.index else 0,
            'cached_files': len(self.cache),
            'index_file_exists': self.index_file.exists(),
            'metadata_file_exists': self.metadata_file.exists(),
        }


# Convenience functions
def initialize_conversation_index(auto_index: bool = True) -> ConversationIndex:
    """
    Initialize conversation index
    
    Args:
        auto_index: If True, automatically index all conversations on startup
    
    Returns:
        ConversationIndex instance
    """
    index = ConversationIndex()
    
    if auto_index:
        index.index_all_conversations()
    
    return index


def search_past_conversations(
    index: ConversationIndex,
    query: str,
    current_session: Optional[str] = None
) -> Tuple[List[Dict], str]:
    """
    Search past conversations and format as context
    
    Args:
        index: ConversationIndex instance
        query: Current user query
        current_session: Current session ID to exclude
    
    Returns:
        Tuple of (conversations list, formatted context string)
    """
    conversations = index.search(query, exclude_session=current_session)
    context = index.format_context(conversations)
    return conversations, context
