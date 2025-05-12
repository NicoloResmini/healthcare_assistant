import pytest
from api.app import create_app
import json

@pytest.fixture(scope='module')
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_patient_endpoint(client):
    # Create
    res = client.post('/api/patients', json={
        'first_name':'Test','last_name':'User','email':'t@u.com','date_of_birth':None
    })
    assert res.status_code == 201
    data = res.get_json()
    pid = data['id']
    # Read
    res2 = client.get(f'/api/patients/{pid}')
    assert res2.status_code == 200
    # Update
    res3 = client.put(f'/api/patients/{pid}', json={'first_name':'New'})
    assert res3.get_json()['first_name'] == 'New'
    # Delete
    res4 = client.delete(f'/api/patients/{pid}')
    assert res4.status_code == 204

def test_chat_endpoint(client, monkeypatch):
    # Patch retriever and generator
    from api.routes.chat import retriever, generator
    monkeypatch.setattr(retriever, 'retrieve', lambda q: ["ctx"])
    monkeypatch.setattr(generator, 'generate', lambda question, context_docs: "risposta finta")
    # Call
    res = client.post('/api/chat/message', json={'patient_id':1, 'message':'ciao'})
    data = res.get_json()
    assert res.status_code == 200
    assert data['response'] == 'fake response'