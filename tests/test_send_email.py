import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_send_email_success(client):
    response = client.post("/send_email", json={
        "to": "test@example.com",
        "subject": "Test Subject",
        "message": "Test Message"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Email sent successfully"}


def test_send_email_invalid_address(client):
    response = client.post("/send_email", json={
        "to": "",
        "subject": "Test Subject",
        "message": "Test Message"
    })
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid email address"}


def test_send_email_server_error(client, monkeypatch):
    def mock_sendmail(username, to, message):
        raise Exception("SMTP server error")

    monkeypatch.setattr("smtplib.SMTP.sendmail", mock_sendmail)

    response = client.post("/send_email", json={
        "to": "test@example.com",
        "subject": "Test Subject",
        "message": "Test Message"
    })
    assert response.status_code == 500
    assert response.json() == {"detail": "SMTP server error"}
