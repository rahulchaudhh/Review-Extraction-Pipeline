from extractor import analyze_and_save_review, get_stored_reviews
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Review Analyzer API")


class ReviewInput(BaseModel):
    text: str


@app.post("/analyze")
def analyze(payload: ReviewInput):
    if not payload.text.strip():
        raise HTTPException(
            status_code=400, detail="Review text cannot be empty."
        )

    try:
        result = analyze_and_save_review(payload.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reviews")
def fetch_reviews():
    try:
        reviews = get_stored_reviews()
        return {"reviews": reviews, "count": len(reviews)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)