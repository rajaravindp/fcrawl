import os
import boto3
from typing import IO

def tts(text: str, voice_id: str = 'Ivy', output_format: str = 'mp3', language_code: str = 'en-US') -> IO[bytes]:
    """
    Convert text to speech using Amazon Polly.

    :param text: The text to convert to speech.
    :param voice_id: The voice ID to use for the conversion.
    :param output_format: The format of the output audio file.
    :param language_code: The language code for the voice.
    :return: The audio stream of the converted speech.
    """
    session = boto3.Session()
    polly_client = session.client(
        service_name='polly',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('REGION_NAME'),
        verify=False)

    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id,
        LanguageCode=language_code
    )

    return response['AudioStream']