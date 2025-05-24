import pytest
from unittest.mock import patch

def test_health_check(client):
    with patch('redis.Redis.ping') as mock_ping:
        mock_ping.return_value = True
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert all(component == "healthy" for component in data["components"].values())

def test_health_check_redis_failure(client):
    with patch('redis.Redis.ping') as mock_ping:
        mock_ping.side_effect = Exception("Redis connection failed")
        response = client.get("/api/v1/health")
        assert response.status_code == 503
        data = response.json()
        assert data["detail"] == "Service Unavailable"
        assert response.headers.get("X-Health-Check") == "failed"

def test_health_check_db_failure(client):
    with patch('sqlalchemy.orm.Session.execute') as mock_execute:
        mock_execute.side_effect = Exception("Database connection failed")
        response = client.get("/api/v1/health")
        assert response.status_code == 503
        data = response.json()
        assert data["detail"] == "Service Unavailable"
        assert response.headers.get("X-Health-Check") == "failed" 