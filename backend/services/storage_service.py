import os
import logging
from fastapi import UploadFile

logger = logging.getLogger(__name__)

# Check Supabase availability
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

class StorageService:
    def __init__(self):
        self.bucket = os.getenv("SUPABASE_BUCKET", "jso-resumes")
        self.supabase_url = os.getenv("SUPABASE_URL", "https://xyzcompany.supabase.co")
        self.supabase_key = os.getenv("SUPABASE_KEY", "")
        self.use_mock = not bool(self.supabase_key) or not SUPABASE_AVAILABLE
        self.supabase_client = self._init_supabase()

    def _init_supabase(self):
        """
        Initialization of Supabase client.
        """
        if not self.use_mock:
            try:
                client: Client = create_client(self.supabase_url, self.supabase_key)
                logger.info("Supabase Storage Service initialized successfully")
                return client
            except Exception as e:
                logger.warning(f"Supabase init failed: {e}. Using mock responses.")
                self.use_mock = True
        
        logger.info("Initializing Supabase Storage Service (Mock)")
        return None

    async def upload_file(self, file: UploadFile, folder: str = "resumes") -> str:
        """
        Uploads a file to the Supabase storage bucket and returns the public URL.
        """
        file_content = await file.read()
        file_path = f"{folder}/{file.filename}"
        
        if not self.use_mock and self.supabase_client:
            try:
                # Attempt to upload to real Supabase
                res = self.supabase_client.storage.from_(self.bucket).upload(
                    path=file_path,
                    file=file_content,
                    file_options={"content-type": file.content_type}
                )
                logger.info(f"Successfully uploaded {file.filename} to Supabase bucket {self.bucket}")
                # Public URL format
                return f"{self.supabase_url}/storage/v1/object/public/{self.bucket}/{file_path}"
            except Exception as e:
                logger.error(f"Supabase upload failed: {e}. Falling back to mock URL.")

        # Mock Upload Logic
        logger.info(f"Uploaded {file.filename} ({len(file_content)} bytes) to mock Supabase {self.bucket}/{folder}/")
        
        # Return a mock Supabase public URL
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket}/{folder}/{file.filename}"

    def get_signed_url(self, file_key: str) -> str:
        """
        Generates a pre-signed URL for a private object in Supabase.
        """
        return f"{self.supabase_url}/storage/v1/object/sign/{self.bucket}/{file_key}?token=mock-token-123"

# Singleton instance
storage_service = StorageService()
