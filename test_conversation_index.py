# test_conversation_index.py

"""
Test script for conversation history indexing
Run with: python test_conversation_index.py
"""

from modules.conversation_index import ConversationIndex, initialize_conversation_index
from pathlib import Path


def test_indexing():
    """Test conversation indexing"""
    print("=" * 60)
    print("TESTING CONVERSATION INDEXING")
    print("=" * 60)
    
    # Initialize index
    print("\n1. Initializing conversation index...")
    index = ConversationIndex()
    
    # Check if memory directory exists
    if not Path("memory").exists():
        print("⚠️ No memory directory found. Create some conversations first.")
        return
    
    # Index all conversations
    print("\n2. Indexing all conversations...")
    index.index_all_conversations(force=True)
    
    # Get stats
    print("\n3. Index Statistics:")
    stats = index.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test search
    print("\n4. Testing Search:")
    test_queries = [
        "What is the relationship between Gensol and Go-Auto?",
        "Tell me about DLF apartments",
        "What is artificial intelligence?",
    ]
    
    for query in test_queries:
        print(f"\n   Query: {query}")
        results = index.search(query)
        print(f"   Found {len(results)} relevant conversations:")
        for i, conv in enumerate(results, 1):
            print(f"      {i}. [{conv['date']}] {conv['query'][:60]}...")
            print(f"         Similarity: {conv['similarity_score']:.4f}")
    
    # Test context formatting
    print("\n5. Testing Context Formatting:")
    results = index.search("Gensol")
    context = index.format_context(results)
    print(context)


def test_integration():
    """Test integration with agent"""
    print("\n" + "=" * 60)
    print("TESTING INTEGRATION")
    print("=" * 60)
    
    print("\n1. Initialize with auto-indexing...")
    index = initialize_conversation_index(auto_index=True)
    
    print("\n2. Simulate agent query...")
    query = "What do you know about Gensol?"
    current_session = "2025/01/15/session-1736950000-test123"
    
    results = index.search(query, exclude_session=current_session)
    context = index.format_context(results)
    
    print(f"\n   Query: {query}")
    print(f"   Found {len(results)} relevant past conversations")
    print(f"\n   Context to provide to agent:")
    print(context)


def test_incremental_indexing():
    """Test incremental indexing (only new files)"""
    print("\n" + "=" * 60)
    print("TESTING INCREMENTAL INDEXING")
    print("=" * 60)
    
    index = ConversationIndex()
    
    print("\n1. First indexing (all files)...")
    index.index_all_conversations(force=False)
    
    print("\n2. Second indexing (should skip unchanged files)...")
    index.index_all_conversations(force=False)
    
    print("\n3. Force re-indexing (all files)...")
    index.index_all_conversations(force=True)


if __name__ == "__main__":
    print("\n🧪 CONVERSATION INDEX TEST SUITE\n")
    
    try:
        test_indexing()
        test_integration()
        test_incremental_indexing()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
