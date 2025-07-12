from app import app

if __name__ == "__main__":
    # For development only. For production, use Gunicorn or another WSGI server.
    app.run(host="0.0.0.0", port=5080, debug=False)
