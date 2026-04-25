from fastapi import APIRouter, HTTPException
from schemas import TextRequest, TextAnalysisResponse
from service import analyze_text

router = APIRouter(prefix="/text", tags=["text"])


@router.post("/analyze", response_model=TextAnalysisResponse)
def analyze(data: TextRequest):
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Текст не может быть пустым")
    result = analyze_text(data.text)
    return result
