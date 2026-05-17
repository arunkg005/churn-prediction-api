import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread


PROJECT_ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = PROJECT_ROOT / 'frontend'
BACKEND_HOST = '127.0.0.1'
BACKEND_PORT = 5000
FRONTEND_PORT = 3000


def start_backend():
    from backend.app import app as backend_app

    print(f'Backend API running at http://{BACKEND_HOST}:{BACKEND_PORT}')
    backend_app.run(debug=True, host=BACKEND_HOST, port=BACKEND_PORT, use_reloader=False)


def start_frontend():
    handler = partial(SimpleHTTPRequestHandler, directory=str(FRONTEND_DIR))
    server = ThreadingHTTPServer((BACKEND_HOST, FRONTEND_PORT), handler)

    print(f'Frontend running at http://{BACKEND_HOST}:{FRONTEND_PORT}')
    print(f'API URL: http://{BACKEND_HOST}:{BACKEND_PORT}')
    server.serve_forever()


def start_all():
    backend_thread = Thread(target=start_backend, daemon=True)
    backend_thread.start()
    start_frontend()


def parse_args():
    parser = argparse.ArgumentParser(description='Run the churn prediction project.')
    parser.add_argument(
        'mode',
        nargs='?',
        choices=('backend', 'frontend', 'all'),
        default='all',
        help='Choose whether to run the backend API, the frontend UI, or both.',
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if args.mode == 'backend':
        start_backend()
    elif args.mode == 'frontend':
        start_frontend()
    else:
        start_all()