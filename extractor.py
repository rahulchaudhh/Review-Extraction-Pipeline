import os
from typing import Literal, Optional, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from pymongo import MongoClient
import certifi

load_dotenv()

# Setup MongoDB
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=2000
)

db = mongo_client["review_analyzer"]
collection = db["reviews"]


class Review(BaseModel):
    key_themes: List[str] = Field(
        default_factory=list,
        description="Write down all the key themes discussed in the review"
    )
    summary: str = Field(description="A brief summary of the review")
    sentiment: Literal["pos", "neg", "neutral"] = Field(
        description="Return sentiment of the review as pos, neg, or neutral"
    )
    pros: Optional[List[str]] = Field(
        default=None, description="List of pros"
    )
    cons: Optional[List[str]] = Field(
        default=None, description="List of cons"
    )
    name: Optional[str] = Field(
        default=None, description="Name of the reviewer"
    )


# Initialize Model with Native Structured Output
model = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)
structured_llm = model.with_structured_output(Review)


def analyze_and_save_review(review_text: str) -> dict:
    # A. Run LLM extraction natively
    extracted_review: Review = structured_llm.invoke(review_text)
    
    # B. Convert to dict & attach raw text
    review_dict = extracted_review.model_dump()
    review_dict["raw_text"] = review_text
    
    # C. Save to DB (fallback if Atlas IP is not whitelisted)
    try:
        result = collection.insert_one(review_dict)
        review_dict["_id"] = str(result.inserted_id)
    except Exception as e:
        review_dict["_id"] = "local_demo_id"
        review_dict["db_status"] = "Analyzed successfully (MongoDB Atlas offline or IP blocked)"
    
    return review_dict


def get_stored_reviews(limit: int = 50) -> List[dict]:
    try:
        docs = list(collection.find().sort("_id", -1).limit(limit))
        for doc in docs:
            doc["_id"] = str(doc["_id"])
        return docs
    except Exception:
        return []