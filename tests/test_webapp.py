def test_index_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.template.name == 'index.html'
