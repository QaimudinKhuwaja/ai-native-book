from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock
import pytest

client = TestClient(app)

@pytest.fixture
def mock_cohere_client():
    with patch("app.api.chat.co") as mock_cohere:
        mock_cohere.embed.return_value = MagicMock(embeddings=[[0.1] * 1024])
        mock_cohere.generate.return_value = MagicMock(generations=[MagicMock(text="Mocked answer")])
        yield mock_cohere

@pytest.fixture
def mock_qdrant_service():
    with patch("app.api.chat.qdrant_service") as mock_qdrant:
        mock_qdrant.search.return_value = [
            {'id': 1, 'score': 0.9, 'payload': {'source': '/docs/intro', 'chunk_index': 0, 'content': 'Content of chunk 1'}},
            {'id': 2, 'score': 0.8, 'payload': {'source': '/docs/chapter1', 'chunk_index': 1, 'content': 'Content of chunk 2'}},
        ]
        yield mock_qdrant

def test_chat_endpoint_global_book(mock_cohere_client, mock_qdrant_service):
    response = client.post(
        "/api/v1/chat",
        json={"query": "What is physical AI?", "mode": "global-book"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert data["answer"] == "Mocked answer"
    assert len(data["sources"]) == 2
    assert data["sources"][0]["source"] == "/docs/intro"
    assert data["sources"][0]["content"] == "Content of chunk 1"

def test_chat_endpoint_selected_text_only(mock_cohere_client, mock_qdrant_service):
    response = client.post(
        "/api/v1/chat",
        json={"query": "Explain this concept.", "mode": "selected-text-only", "selected_text": "This is the selected text."}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert data["answer"] == "Mocked answer"
    # For selected-text-only mode, the retrieved chunks might still be from Qdrant,
    # but the prompt construction logic would need to prioritize selected_text.
    # The current mock simulates retrieval from Qdrant.
    assert len(data["sources"]) == 2

def test_chat_endpoint_missing_selected_text():
    response = client.post(
        "/api/v1/chat",
        json={"query": "Explain this concept.", "mode": "selected-text-only"}
    )
    assert response.status_code == 422 # Unprocessable Entity due to missing selected_text
