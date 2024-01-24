from google.cloud import speech

def transcribe_file_with_auto_punctuation(path: str) -> speech.RecognizeResponse:
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=path)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=8000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result()

    return response
