"""
test_memory.py
"""
import pytest
import shutil
import os
from datetime import datetime
from models import Memory
from memory_stream import MemoryStream
import config

# Use a temporary directory for testing
TEST_CHROMA_DIR = os.path.join(os.getcwd(), "tests", "chroma_db")

@pytest.fixture
def memory_stream():
    # Setup
    original_path = config.CHROMA_PERSIST_DIR
    config.CHROMA_PERSIST_DIR = TEST_CHROMA_DIR
    
    stream = MemoryStream("TestAgent")
    
    yield stream
    
    # Teardown
    config.CHROMA_PERSIST_DIR = original_path
    if os.path.exists(TEST_CHROMA_DIR):
        shutil.rmtree(TEST_CHROMA_DIR)

def test_add_and_retrieve(memory_stream):
    mem = Memory(
        content="Important secret",
        memory_type="observation",
        importance=10,
        tags=["secret"]
    )
    memory_stream.add_memory(mem)
    
    # Query
    results = memory_stream.retrieve("secret", k=1)
    assert len(results) == 1
    assert results[0].memory.content == "Important secret"
    assert results[0].final_score > 0
