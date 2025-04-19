import uvicorn
from app.server import app  # Assuming `app/server.py` contains FastAPI app

if __name__ == "__main__":
	import os
	port = int(os.environ.get("PORT", 5050))
	uvicorn.run(app, host="0.0.0.0", port=port)