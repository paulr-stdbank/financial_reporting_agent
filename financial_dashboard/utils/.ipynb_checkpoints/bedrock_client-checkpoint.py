import boto3, json, os

# Re-use credentials in ~/.aws/credentials or AWS_PROFILE
brt = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))

MODEL_ID = os.getenv("BEDROCK_MODEL", "anthropic.claude-3-sonnet")  # example

def llm_complete(prompt: str, *, temperature: float = 0.2, max_tokens: int = 500) -> str:
    body = json.dumps({
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "inferenceConfig": {"maxTokens": max_tokens, "temperature": temperature}
    })
    resp = brt.converse(modelId=MODEL_ID, messages=json.loads(body)["messages"])
    return resp["output"]["message"]["content"][0]["text"]
