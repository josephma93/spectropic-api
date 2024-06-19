import argparse
import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Handles incoming POST requests to the webhook."""
    data = request.json
    print("Received data:", data)
    return jsonify(success=True), 200

def run_server(port):
    """Runs the Flask server on the specified port."""
    app.run(port=port, debug=True)

def create_transcript(api_key, args):
    """Creates a new transcript by uploading a local file."""
    url = "https://api.spectropic.ai/v1/transcribe"
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    files = {
        'file': (os.path.basename(args.file_path), open(args.file_path, 'rb'), 'multipart/form-data')
    }
    data = {
        "webhook": args.webhook_url,
        "numSpeakers": args.num_speakers,
        "language": args.language,
        "vocabulary": args.vocabulary
    }
    # Filter out None values and prepare the data part of the multipart request
    data = {k: (None, str(v)) for k, v in data.items() if v is not None}

    response = requests.post(url, headers=headers, files=files, data=data)
    print(response.json())

def test_webhook(api_key, args):
    """Tests the webhook configuration using POST request."""
    url = "https://api.spectropic.ai/v1/test"
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    data = {"webhook": args.webhook_url}
    response = requests.post(url, headers=headers, json=data)
    print(response.json())

def main():
    load_dotenv()
    api_key = os.getenv("SPECTROPIC_API_KEY")

    parser = argparse.ArgumentParser(description="Interact with Spectropic API and handle webhooks.")
    subparsers = parser.add_subparsers(title='commands', help='available commands', dest='command')
    subparsers.required = True

    # Sub-command for running the webhook server
    parser_server = subparsers.add_parser('server', help='Run the webhook server')
    parser_server.add_argument("--port", type=int, default=5000, help="Port to run the webhook server on")
    parser_server.set_defaults(func=lambda args: run_server(args.port))

    # Sub-command for posting a new transcript
    parser_post = subparsers.add_parser('post', help='Create a new transcript from a local file')
    parser_post.add_argument("--file_path", type=str, required=True, help="Local path to the file to transcribe")
    parser_post.add_argument("--webhook_url", type=str, required=True, help="Webhook URL for sending the transcript")
    parser_post.add_argument("--num_speakers", type=int, help="Number of speakers in the transcript")
    parser_post.add_argument("--language", type=str, help="Language of the transcript")
    parser_post.add_argument("--vocabulary", type=str, help="Custom vocabulary for the transcript")
    parser_post.set_defaults(func=lambda args: create_transcript(api_key, args))

    # Sub-command for testing the webhook
    parser_test = subparsers.add_parser('test', help='Test the webhook URL')
    parser_test.add_argument("--webhook_url", type=str, required=True, help="Webhook URL to test")
    parser_test.set_defaults(func=lambda args: test_webhook(api_key, args))

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
