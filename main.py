from functools import lru_cache
import numpy as np
import whisper
import os
from datetime import timedelta
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from tempfile import NamedTemporaryFile
from typing import List
import torch


class Whisper:
    def __init__(self, audio, whisper_model, task):
        """
        Initialize a Whisper object.

        Parameters:
        - audio: Path or data of the audio file to be transcribed.
        - whisper_model: The Whisper ASR model to be used.
        - task: The task to perform, either 'transcribe' or 'translation'.
        """
        self.audio = audio
        self.whisper_model = whisper_model
        self.model = None
        self.task = task

    def _load_whisper_model(self):
        """
        Load the whisper model from the cache or download it if it doesn't exist.

        This function uses the LRU (Least Recently Used) cache to store the loaded
        whisper model. If the model is not present in the cache, it loads the model
        using the specified whisper_model parameter.
        """

        if self.model is None:
            # Load whisper model
            self.model = whisper.load_model(self.whisper_model)

    def transcribe(self, task='transcribe'):
        """
        Perform either transcription or translation on the audio file using the Whisper model.

        Returns:
        - If task is 'transcribe': A string representing the transcribed text.
        - If task is 'translation': A string representing the translated text.
        """
        # Load whisper model if not already loaded
        self._load_whisper_model()

        # Transcribe
        transcript = self.model.transcribe(self.audio, task=self.task, fp16=False)

        return transcript['text']

    def generate_webvtt(self):
        """
        Generate WebVTT subtitles for the audio file using the Whisper model.

        Returns:
        A list representing the WebVTT subtitles.
        """
        # Load whisper model if not already loaded
        self._load_whisper_model()

        transcript = self.model.transcribe(self.audio)

        vtt_list = []

        for i in range(len(transcript["segments"])):
            start_time = transcript["segments"][i]["start"]
            end_time = transcript["segments"][i]["end"]
            text = transcript["segments"][i]["text"]

            # Format time in HH:MM:SS.sss
            start_time_formatted = f"{int(start_time // 3600):02d}:{int((start_time % 3600) // 60):02d}:{start_time % 60:06.3f}"
            end_time_formatted = f"{int(end_time // 3600):02d}:{int((end_time % 3600) // 60):02d}:{end_time % 60:06.3f}"

            # Add subtitle entry to WebVTT
            vtt_entry = f"[{start_time_formatted} --> {end_time_formatted}]: {text}"
            vtt_list.append(vtt_entry)

        return vtt_list





# Checking if NVIDIA GPU is available
torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

app = FastAPI()


class WhisperHandler:
    def init(self):
        pass

    @staticmethod
    def process_audio(audio_np, task):
        try:
            whisper_model = Whisper(audio_np, 'large', task)
            if task in ["transcribe", "translation"]:
                result = whisper_model.transcribe(task)
            elif task == "WebVTT":
                result = whisper_model.generate_webvtt()
        except Exception as e:
            return {"error": str(e)}

        return result

    def handle_upload(self, func_name: str, files: UploadFile):
        if files is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Bad Request, bad file"
            )

        #if not files:
            #raise HTTPException(status_code=400, detail="No files were provided")
        
        # For each file, let's store the results in a list of dictionaries.
        results = []

        #for file in files:
            # Create a temporary file.
        with NamedTemporaryFile(delete=True) as temp:
            # Write the user's uploaded file to the temporary file.
            with open(temp.name, "wb") as temp_file:
                temp_file.write(files.file.read())

            # Let's get the transcript of the temporary file.
            result = self.process_audio(temp.name, func_name)

            # Now we can store the result object for this file.
            results.append({
                'result': result,
            })

        return JSONResponse(content={'results': results})


whisper_handler = WhisperHandler()


@app.post("/whisper/")
async def handler(func_name: str, files: UploadFile = File(...)):
    return whisper_handler.handle_upload(func_name, files)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
