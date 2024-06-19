# Spectropic API Interaction and Webhook Handler

This project provides a Python script to interact with the Spectropic API for transcribing audio files. It includes
functionality to handle webhooks using Flask.

## Requirements

- Python 3.7+
- `requests` library
- `flask` library

## Setup

1. **Install Dependencies**:
   ```sh
   pip install requests flask
   ```

2. **Store API Key**:
   Store your Spectropic API key in macOS Keychain:
   ```sh
   security add-generic-password -a "$USER" -s "spectropic_api_key" -w "YOUR_API_KEY"
   ```

3. **Expose Local Server with ngrok**:
   ```sh
   ngrok http 5000
   ```
   Copy the generated ngrok URL (e.g., `http://<ngrok_id>.ngrok.io`) to use as the webhook URL.

## Usage

### Run Webhook Server

```sh
python spectropic_api.py server --port 5000
```

### Create Transcript

```sh
python spectropic_api.py post --file_path <path_to_file> --webhook_url <ngrok_url>/webhook --num_speakers <number_of_speakers> --language <language_code> --vocabulary <custom_vocabulary>
```

### Test Webhook

```sh
python spectropic_api.py test --webhook_url <ngrok_url>/webhook
```

## Script Details

### Webhook Handler

The Flask server handles incoming POST requests to the `/webhook` endpoint.

### Creating Transcripts

Uploads a local audio file to the Spectropic API and triggers a transcription, with results sent to the specified
webhook URL.

### Testing Webhooks

Sends a test request to the specified webhook URL to verify its configuration.

## Example

1. **Run ngrok**:
   ```sh
   ngrok http 5000
   ```
   Use the generated ngrok URL for the webhook.

2. **Run Webhook Server**:
   ```sh
   python spectropic_api.py server --port 5000
   ```

3. **Create Transcript**:
   ```sh
   python spectropic_api.py post --file_path example.wav --webhook_url http://<ngrok_id>.ngrok.io/webhook --num_speakers 2 --language en --vocabulary "Spectropic, AI, LLama, Mistral, Whisper."
   ```

4. **Test Webhook**:
   ```sh
   python spectropic_api.py test --webhook_url http://<ngrok_id>.ngrok.io/webhook
   ```

This script helps interact with the Spectropic API securely using macOS Keychain for API key management and provides an
easy way to handle webhooks for transcript results.