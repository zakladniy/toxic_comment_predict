import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.application import main
from fastapi.testclient import TestClient


client = TestClient(main.app)


def test_server_for_correct_response() -> None:
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
