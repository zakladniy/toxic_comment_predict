from fastapi.testclient import TestClient

from src.application import main

client = TestClient(main.app)


def test_server_for_correct_response() -> None:
    """Tests for correct response fields and model prediction."""
    params = {
        'text': 'как дела',
    }
    response = client.get(
        url='/api/toxic_predict',
        params=params,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert 'label' in response.json()['data']
    assert 'proba_of_toxic' in response.json()['data']
    assert response.json()['data']['label'] == 'Non toxic'
    assert round(response.json()['data']['proba_of_toxic']) == 0.0
