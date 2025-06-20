import boto3
import json
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Request model
class EmbedRequest(BaseModel):
    text: str
    dimensions: int = 1024
    normalize: bool = True
    model_id: str = "amazon.titan-embed-text-v2:0"
    region: str = "eu-north-1"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/help")
def help():
    return {
        "description": "This service generates embeddings using Amazon Titan Embedding v2.",
        "input_format": {
            "text": "The text string to embed.",
            "dimensions": "(Optional) Integer. Embedding dimensions. Default: 1024.",
            "normalize": "(Optional) Boolean. Normalize output. Default: True.",
            "model_id": "(Optional) The full model ID (default: amazon.titan-embed-text-v2:0).",
            "region": "(Optional) AWS region (default: eu-north-1)."
        },
        "output_format": {
            "embedding": "List of float values representing the embedding."
        }
    }

@app.post("/embed")
async def embed(request: Request):
    try:
        data = await request.json()
        input_data = EmbedRequest(**data)

        # Load AWS credentials from environment variables
        AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
        AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

        if not AWS_ACCESS_KEY or not AWS_SECRET_KEY:
            raise HTTPException(status_code=500, detail="AWS credentials not set in environment variables.")

        # Create Bedrock client dynamically based on input region
        bedrock_client = boto3.client(
            "bedrock-runtime",
            region_name=input_data.region,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

        payload = {
            "inputText": input_data.text,
            "dimensions": input_data.dimensions,
            "normalize": input_data.normalize
        }

        response = bedrock_client.invoke_model(
            modelId=input_data.model_id,
            body=json.dumps(payload)
        )

        result = json.loads(response['body'].read().decode())
        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run: uvicorn filename:app --reload
