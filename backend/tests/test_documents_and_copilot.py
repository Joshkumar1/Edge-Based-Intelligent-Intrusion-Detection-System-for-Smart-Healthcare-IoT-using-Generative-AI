import io
from fastapi.testclient import TestClient
from pypdf import PdfWriter
from app.main import app

client = TestClient(app)


def test_list_documents():
    response = client.get("/api/v1/documents/")
    assert response.status_code == 200
    docs = response.json()
    assert isinstance(docs, list)
    assert len(docs) >= 1
    # Check default IEEE paper is present
    ieee_doc = next((d for d in docs if d.get("is_default")), None)
    assert ieee_doc is not None
    assert "EdgeShield AI" in ieee_doc["title"]


def test_get_document_and_page():
    # 1. Get doc details
    response = client.get("/api/v1/documents/DOC-IEEE-EDGESHIELD-2026")
    assert response.status_code == 200
    doc = response.json()
    assert doc["id"] == "DOC-IEEE-EDGESHIELD-2026"
    assert doc["total_pages"] == 8

    # 2. Get specific page
    page_resp = client.get("/api/v1/documents/DOC-IEEE-EDGESHIELD-2026/page/3")
    assert page_resp.status_code == 200
    page_data = page_resp.json()
    assert page_data["page_number"] == 3
    assert "Isolation Forest" in str(page_data["sections"])


def test_search_document():
    response = client.get("/api/v1/documents/DOC-IEEE-EDGESHIELD-2026/search?q=Isolation+Forest")
    assert response.status_code == 200
    data = response.json()
    assert data["total_matches"] > 0
    assert any(m["page_number"] == 3 for m in data["results"])


def test_copilot_research_context():
    req = {
        "context_type": "research",
        "query": "What datasets were used for the intrusion detection experiments?",
        "context_id": "DOC-IEEE-EDGESHIELD-2026"
    }
    response = client.post("/api/v1/llm/copilot", json=req)
    assert response.status_code == 200
    res = response.json()
    assert "summary" in res
    assert "sources" in res
    assert len(res["sources"]) > 0
    assert res["page_reference"] is not None


def test_copilot_research_unavailable():
    req = {
        "context_type": "research",
        "query": "supercalifragilistic non-existent query completely irrelevant to cybersecurity x992",
        "context_id": "NON_EXISTENT_DOC"
    }
    response = client.post("/api/v1/llm/copilot", json=req)
    assert response.status_code == 200
    res = response.json()
    assert "Research document unavailable for AI context." in res["summary"]


def get_admin_auth_headers():
    login_resp = client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_device_isolation_and_reconnect():
    headers = get_admin_auth_headers()
    # Isolate DEV-ICU-101
    iso_resp = client.post("/api/v1/devices/DEV-ICU-101/isolate", headers=headers)
    assert iso_resp.status_code == 200
    data = iso_resp.json()
    assert data["status"] == "Isolated"
    assert data["enforcement_mode"] == "SIMULATION"
    assert data["enforcement_status"] == "SIMULATED"

    # Reconnect DEV-ICU-101
    rec_resp = client.post("/api/v1/devices/DEV-ICU-101/reconnect", headers=headers)
    assert rec_resp.status_code == 200
    rec_data = rec_resp.json()
    assert rec_data["status"] == "Active"
    assert rec_data["enforcement_status"] == "SIMULATED"


def test_pdf_upload():
    # Generate a real valid in-memory PDF using pypdf
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    pdf_bytes_io = io.BytesIO()
    writer.write(pdf_bytes_io)
    pdf_bytes = pdf_bytes_io.getvalue()

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("test_hospital_manual.pdf", pdf_bytes, "application/pdf")}
    )
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "SUCCESS"
    doc_id = res["document"]["id"]

    # Clean up by deleting uploaded document (requires auth)
    headers = get_admin_auth_headers()
    del_resp = client.delete(f"/api/v1/documents/{doc_id}", headers=headers)
    assert del_resp.status_code == 200
