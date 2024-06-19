import argparse
import os
import requests
import subprocess
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    logger.info(f"Received data: {data}")
    return jsonify(success=True), 200


def run_server(port, debug):
    app.run(port=port, debug=debug)


def get_api_key():
    try:
        user = os.getenv("USER")
        result = subprocess.run(
            ["security", "find-generic-password", "-a", user, "-s", "spectropic_api_key", "-w"],
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        logger.error("API key not found in the Keychain.")
        logger.error('Add it using: security add-generic-password -a "$USER" -s "spectropic_api_key" -w "YOUR_API_KEY"')
        exit(1)


def create_transcript(api_key, args):
    url = "https://api.spectropic.ai/v1/transcribe"
    headers = {'Authorization': f'Bearer {api_key}'}
    files = {'file': (os.path.basename(args.file_path), open(args.file_path, 'rb'), 'multipart/form-data')}
    data = {
        "webhook": args.webhook_url,
        "numSpeakers": args.num_speakers,
        "language": args.language,
        "vocabulary": args.vocabulary
    }
    data = {k: (None, str(v)) for k, v in data.items() if v is not None}

    logger.debug(f"Sending request to {url} with headers {headers} and data {data}")
    response = requests.post(url, headers=headers, files=files, data=data)
    logger.info(f"API Response: {response.json()}")


def test_webhook(api_key, args):
    url = "https://api.spectropic.ai/v1/test"
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    data = {"webhook": args.webhook_url}

    logger.debug(f"Testing webhook with URL {url} and data {data}")
    response = requests.post(url, headers=headers, json=data)
    logger.info(f"API Response: {response.json()}")


def main():
    parser = argparse.ArgumentParser(description="Interact with Spectropic API and handle webhooks.")
    parser.add_argument("--log", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO",
                        help="Set the logging level")
    subparsers = parser.add_subparsers(title='commands', help='available commands', dest='command')
    subparsers.required = True

    parser_server = subparsers.add_parser('server', help='Run the webhook server')
    parser_server.add_argument("--port", type=int, default=5000, help="Port to run the webhook server on")
    parser_server.add_argument("--debug", action='store_true', help="Run the server in debug mode")
    parser_server.set_defaults(func=lambda args: run_server(args.port, args.debug))

    parser_post = subparsers.add_parser('post', help='Create a new transcript from a local file')
    parser_post.add_argument("--file_path", type=str, required=True, help="Local path to the file to transcribe")
    parser_post.add_argument("--webhook_url", type=str, required=True, help="Webhook URL for sending the transcript")
    parser_post.add_argument("--num_speakers", type=int, help="Number of speakers in the transcript")
    parser_post.add_argument("--language", type=str, help="Language of the transcript")
    parser_post.add_argument("--vocabulary", type=str, help="Custom vocabulary for the transcript")
    parser_post.set_defaults(func=lambda args: create_transcript(api_key, args))

    parser_test = subparsers.add_parser('test', help='Test the webhook URL')
    parser_test.add_argument("--webhook_url", type=str, required=True, help="Webhook URL to test")
    parser_test.set_defaults(func=lambda args: test_webhook(api_key, args))

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log))
    logger.setLevel(getattr(logging, args.log))

    api_key = get_api_key()
    args.func(args)


if __name__ == "__main__":
    main()
