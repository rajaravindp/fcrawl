import boto3
import os
import json
import ssl
import urllib3
import requests

from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

from langchain_aws import ChatBedrockConverse
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter

from prompt_template import get_prompt_template
from override_tokenizer import override_tokenizer

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

# Configure requests to ignore SSL verification
old_merge_environment_settings = requests.Session.merge_environment_settings

def merge_environment_settings(self, url, proxies, stream, verify, cert):
    settings = old_merge_environment_settings(self, url, proxies, stream, verify, cert)
    settings['verify'] = False
    return settings

requests.Session.merge_environment_settings = merge_environment_settings

def get_llm_response(text: str) -> Dict[str, Any]:
    """
    Generate a summarized response from a large language model (LLM) using LangChain utilities.

    Args:
        text (str): The input text to be summarized.

    Returns:
        Dict[str, Any]: A dictionary containing the summarized text or an error message.
    """
    try:
        # Override the tokenizer
        override_tokenizer()

        # Load environment variables
        load_dotenv()

        # Initialize AWS Bedrock client
        session = boto3.Session()
        bedrock = session.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("REGION_NAME"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            verify=False
        )

        # Initialize the LLM with Bedrock client
        llm = ChatBedrockConverse(
            model_id=os.getenv("MODEL_ID"),
            client=bedrock,
            max_tokens=None,
            temperature=0.5,
        )

        # Split the input text into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n"], chunk_size=10, chunk_overlap=5
        )
        docs: List[Dict[str, str]] = text_splitter.create_documents([text])

        # Load the summarization chain
        summary_chain = load_summarize_chain(
            llm=llm,
            chain_type="map_reduce",
            verbose=True,
            map_prompt=get_prompt_template(),
            combine_prompt=get_prompt_template()
        )

        # Generate the summary
        return {"summary": summary_chain.invoke(docs)['output_text']}

    except boto3.exceptions.Boto3Error as e:
        # Handle AWS Boto3-related errors
        print(f"Boto3 error: {e}")
        return {"error": f"Boto3 error: {str(e)}"}
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print(f"JSON decode error: {e}")
        return {"error": f"JSON decode error: {str(e)}"}
    except KeyError as e:
        # Handle missing environment variable errors
        print(f"Key error: {e}")
        return {"error": f"Key error: {str(e)}"}
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e}")
        return {"error": f"Unexpected error: {str(e)}"}