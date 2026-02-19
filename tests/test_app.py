import pytest
from app import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.psycopg2.connect')
def test_register_success(mock_connect, client):
    # Mock database connection and cursor
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully'
    mock_cur.execute.assert_called()
    mock_conn.commit.assert_called()

@patch('app.psycopg2.connect')
def test_login_success(mock_connect, client):
    # Mock database connection and cursor
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Mock fetchone to return a user record
    mock_cur.fetchone.return_value = (1, 'testuser', 'password123', 'test@example.com')
    
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Login successful'
    assert response.get_json()['user']['username'] == 'testuser'

@patch('app.psycopg2.connect')
def test_login_failure(mock_connect, client):
    # Mock database connection and cursor
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Mock fetchone to return None (user not found)
    mock_cur.fetchone.return_value = None
    
    response = client.post('/login', json={
        'username': 'wronguser',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Invalid credentials'
