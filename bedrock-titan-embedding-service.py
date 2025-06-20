import boto3
import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load AWS credentials from .env
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

app = FastAPI(
    title="Titan Embedding Service",
    description="Simple FastAPI service that wraps Amazon Bedrock Titan Embedding v2 model.",
    version="1.0.0"
)

class EmbedRequest(BaseModel):
    text: str = Field(..., description="The input text to embed")
    dimensions: int = Field(1024, description="Number of embedding dimensions", example=1024)
    normalize: bool = Field(True, description="Whether to normalize the embedding vector")
    model_id: str = Field("amazon.titan-embed-text-v2:0", description="Bedrock model ID")
    region: str = Field("eu-north-1", description="AWS region where Bedrock is deployed")

class EmbedResponse(BaseModel):
    embedding: list = Field(..., description="The resulting embedding vector")

@app.post("/embed", response_model=EmbedResponse)
def generate_embedding(request: EmbedRequest):
    try:
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name=request.region,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        payload = {
            "inputText": request.text,
            "dimensions": request.dimensions,
            "normalize": request.normalize
        }

        response = client.invoke_model(
            modelId=request.model_id,
            body=json.dumps(payload)
        )

        body = response['body'].read().decode()
        result = json.loads(body)

        # Always return the simplified embedding field
        return EmbedResponse(embedding=result.get("embedding"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/help")
def help():
    return {
        "title": "Titan Embedding Service",
        "description": "POST /embed with text, dimensions, normalize, model_id, region to get embedding.",
        "example_request": {
            "text": "The quick brown fox jumps over the lazy dog.",
            "dimensions": 1024,
            "normalize": True,
            "model_id": "amazon.titan-embed-text-v2:0",
            "region": "eu-north-1"
        }
    }
