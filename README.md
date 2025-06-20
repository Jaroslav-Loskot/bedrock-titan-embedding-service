# Titan Embedding Service

A simple FastAPI-based microservice that wraps Amazon Bedrock Titan Embedding v2 model to generate text embeddings via HTTP API.

## Features

* Accepts JSON requests to generate embeddings
* Dynamically configurable model ID and AWS region
* Uses environment variables to securely load AWS credentials
* Includes `/health` and `/help` endpoints
* Dockerized for easy deployment

---

## Requirements

* Python 3.9+ (if running locally)
* Docker (if running containerized)
* AWS account with Bedrock access and permissions to invoke Titan Embedding v2
* AWS credentials with Bedrock permissions

---

## Installation (local, without Docker)

1. Clone the repository and navigate into the project directory.

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # (Linux/Mac)
.venv\Scripts\activate     # (Windows)
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

**Your `requirements.txt`:**

```
fastapi
uvicorn
boto3
python-dotenv
pydantic
```

4. Create a `.env` file in the root directory with your AWS credentials:

```bash
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

> **Note:** Never commit your credentials to version control.

---

## Running the service (local)

Start the server with:

```bash
uvicorn your_python_file:app --reload
```

Replace `your_python_file` with your actual filename (without `.py` extension).

Example:

```bash
uvicorn bedrock_embed_service:app --reload
```

---

## Running the service with Docker

### 1. Build the Docker image

```bash
docker build -t titan-embedding-service .
```

### 2. Run the Docker container

```bash
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  titan-embedding-service
```

The `.env` file will provide the AWS credentials inside the container.

### 3. Test it

You can test it as before:

```bash
curl -X POST http://127.0.0.1:8000/embed \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The quick brown fox jumps over the lazy dog.",
    "dimensions": 1024,
    "normalize": true
  }'
```

---

## Endpoints

### `POST /embed`

Generate embedding from input text.

**Request JSON Format:**

```json
{
  "text": "Your text to embed.",
  "dimensions": 1024,
  "normalize": true,
  "model_id": "amazon.titan-embed-text-v2:0",
  "region": "eu-north-1"
}
```

> `dimensions`, `normalize`, `model_id`, and `region` are optional. Defaults will be used if omitted.

**Response Example:**

```json
{
  "embedding": [0.123, -0.456, ...]
}
```

### `GET /health`

Simple health check. Returns:

```json
{ "status": "ok" }
```

### `GET /help`

Returns full API usage documentation.

---

## Notes

* Make sure Bedrock is enabled in your AWS account.
* Ensure your IAM role has permissions to invoke the model.
* Confirm that you have requested and been granted access to the Titan Embedding v2 model.

---

## License

MIT License
