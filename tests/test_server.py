from fastapi.testclient import TestClient

from src.application import main

client = TestClient(main.app)


def test_server_for_correct_response() -> None:
    """Tests for correct response fields and model prediction."""
    payload = {
        "comments": [
            "Привет, как дела?",
        ]
    }
    response = client.post(
        url="/api/toxic_predict",
        json=payload,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "input_text" in response.json()["data"][0]
    assert "class" in response.json()["data"][0]
    assert "toxic_proba" in response.json()["data"][0]
    assert response.json()["data"][0]["class"] == "Not toxic"
    assert round(response.json()["data"][0]["toxic_proba"]) == 0.0
