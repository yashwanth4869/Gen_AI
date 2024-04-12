import os

def create_faiss_db_directory(self):
    relative_path = "FAISS_DB"
    current_directory = os.getcwd()
    absolute_path = os.path.join(current_directory, relative_path)
    os.makedirs(absolute_path, exist_ok=True)

def create_uploads_directory(self):
    relative_path = "uploads"
    current_directory = os.getcwd()
    absolute_path = os.path.join(current_directory,relative_path)
    os.makedirs(absolute_path, exist_ok=True)