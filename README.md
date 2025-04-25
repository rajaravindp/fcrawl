Extract webpage content, generate concise summary using AWS Bedrock, and convert text-to-speech using Amazon Polly.

# Features
- Web scraping with Firecrawl API
- Text summarization using AWS Bedrock LLMs
- Text-to-speech conversion with Amazon Polly
- Simple command-line interface

# Prerequisites
- Python 3.8+
- AWS account with access to Bedrock and Polly services
- Boto3 and Botocore
- Firecrawl API key
- Tiktokken/ Accelerate

# Env vars
Add these to your <code>.env</code> file
<code>
FIRECRAWL_API_KEY=your_firecrawl_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
REGION_NAME=your_aws_region
MODEL_ID=your_bedrock_model_id
</code>
