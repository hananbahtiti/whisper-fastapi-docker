# whisper-fastapi-docker
## Description:
This repository provides an API for converting speech to text and translating speech to English using Whisper, all implemented with FastAPI and Docker. The output is formatted as WebVTT for easy integration with video and audio applications.

### Features

- Speech-to-Text: Convert audio input to text using Whisper.
- Translation to English: Automatically translate recognized speech to English.
- WebVTT Output: Generate WebVTT files for subtitles and captions.

### Technologies Used

- Whisper: For speech recognition and translation.
- FastAPI: To build the web API.
- Docker: For containerizing the application, ensuring consistent deployment across environments.

## Getting Started 

### Prerequisites 

- Docker
- Git

### Installation 
1. Clone the repository:
   ```bash
   git clone https://github.com/hananbahtiti/whisper-fastapi-docker.git
   cd whisper-fastapi-docker

2. Build the Docker image:
   ```bash
   docker build -t whisper-api .

3. Run the Docker container:
   ```bash
   docker run -p 2000:2000 whisper-api
