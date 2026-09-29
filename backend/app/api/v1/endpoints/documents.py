import os
import uuid
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.services.pdf_service import pdf_service, UPLOAD_DIR
from app.core.database import get_db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.api.deps import require_containment_privilege

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Uploads a PDF file, extracts pages, builds index, and makes it available to EdgeShield AI."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty PDF file uploaded.")
    if len(content) > 30 * 1024 * 1024:  # 30MB limit
        raise HTTPException(status_code=400, detail="File size exceeds 30MB maximum limit.")

    try:
        doc_meta = pdf_service.process_and_index_pdf(content, file.filename)
        return {
            "status": "SUCCESS",
            "message": f"Successfully processed and indexed {file.filename}",
            "document": doc_meta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")


@router.get("/")
def list_documents():
    """Lists all research papers and documents available in EdgeShield AI."""
    return pdf_service.list_documents()


@router.get("/{doc_id}")
def get_document(doc_id: str):
    """Returns full document metadata, pages, and table of contents."""
    doc = pdf_service.get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document with ID '{doc_id}' not found.")
    return doc


@router.get("/{doc_id}/page/{page_num}")
def get_document_page(doc_id: str, page_num: int):
    """Returns the text content and sections for a specific page."""
    page = pdf_service.get_page(doc_id, page_num)
    if not page:
        raise HTTPException(status_code=404, detail=f"Page {page_num} of document '{doc_id}' not found.")
    return page


@router.get("/{doc_id}/search")
def search_document(doc_id: str, q: str = Query(..., min_length=2)):
    """Performs full-text keyword search within the document with page numbers and snippets."""
    results = pdf_service.search_document(doc_id, q)
    return {
        "doc_id": doc_id,
        "query": q,
        "total_matches": len(results),
        "results": results
    }


@router.delete("/{doc_id}")
def delete_document(
    doc_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_containment_privilege)
):
    """Deletes an uploaded document from the library. Requires operator/admin privileges."""
    success = pdf_service.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=400, detail="Default IEEE research document cannot be deleted, or document was not found.")

    # Record audit log
    audit = AuditLog(
        audit_id=f"AUD-{uuid.uuid4().hex[:10].upper()}",
        actor_id=current_user.id,
        actor_username=current_user.username,
        actor_role=current_user.role,
        action_type="DOCUMENT_DELETE",
        target_entity_type="DOCUMENT",
        target_entity_id=doc_id,
        target_device_id=None,
        previous_state="INDEXED",
        new_state="DELETED",
        impact_assessment=f"Document '{doc_id}' removed from EdgeShield research library by {current_user.username}.",
        timestamp=datetime.now(timezone.utc),
        source_ip=None,
        enforcement_mode="N/A",
        enforcement_status="N/A",
        enforcement_result=None,
        success=True,
        failure_reason=None,
        correlation_id=None
    )
    db.add(audit)
    db.commit()

    return {"status": "SUCCESS", "message": f"Document '{doc_id}' deleted."}

