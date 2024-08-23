import uvicorn
from routes import app, history_file_path 
import os 


if __name__ == "__main__":
    if not os.path.exists(history_file_path):
        os.makedirs(history_file_path)
    uvicorn.run(app, host="0.0.0.0", port=634)