"""
Google Drive Service - Handles authentication and file operations
"""

from typing import List, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import os
from google.auth.transport.requests import Request
import google_auth_httplib2
import httplib2


class DriveService:
    """Service for interacting with Google Drive API"""

    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    TOKEN_FILE = 'token.json'

    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
        self.credentials: Optional[Credentials] = None
        self._load_credentials()

    def _load_credentials(self):
        """Loads credentials from token.json if it exists."""
        try:
            if os.path.exists(self.TOKEN_FILE):
                print("Found token.json, attempting to load credentials...")
                creds = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES)
                if creds and creds.valid:
                    # Refresh token if necessary
                    if creds.expired and creds.refresh_token:
                        print("Credentials expired, attempting to refresh...")
                        creds.refresh(Request())
                        print("Credentials successfully refreshed.")
                    self.credentials = creds
                    print("Successfully loaded credentials from token.json.")
                else:
                    print("Loaded token is invalid. Deleting token.json.")
                    os.remove(self.TOKEN_FILE)
        except Exception as e:
            print(f"Error loading credentials from token.json: {e}")
            print("Deleting corrupted token.json file.")
            if os.path.exists(self.TOKEN_FILE):
                os.remove(self.TOKEN_FILE)

    def _save_credentials(self):
        """Saves credentials to token.json."""
        if self.credentials:
            with open(self.TOKEN_FILE, 'w') as token:
                token.write(self.credentials.to_json())
            print("Saved credentials to token.json")

    def get_auth_url(self) -> str:
        """Generate Google OAuth authorization URL"""
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri],
                }
            },
            scopes=self.SCOPES,
            redirect_uri=self.redirect_uri
        )

        auth_url, _ = flow.authorization_url(
            access_type='offline',
            prompt='consent',  # Force prompt for consent to ensure refresh_token is issued
            include_granted_scopes='true'
        )

        return auth_url

    def handle_callback(self, code: str) -> Credentials:
        """Handle OAuth callback and exchange code for credentials"""
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri],
                }
            },
            scopes=self.SCOPES,
            redirect_uri=self.redirect_uri
        )

        flow.fetch_token(code=code)
        self.credentials = flow.credentials
        self._save_credentials()
        return self.credentials

    def list_files(self, folder_id: Optional[str] = None, page_size: int = 100) -> List[dict]:
        """List all files in Drive or in a specific folder"""
        if not self.credentials:
            raise ValueError("Not authenticated. Call handle_callback first.")

        # Create an authorized http object with a timeout
        authed_http = google_auth_httplib2.AuthorizedHttp(self.credentials, http=httplib2.Http(timeout=60))
        service = build('drive', 'v3', http=authed_http)

        query = "trashed=false"
        if folder_id:
            query += f" and '{folder_id}' in parents"

        results = []
        page_token = None
        previous_page_token = ""  # Sentinel value to detect duplicate tokens

        while True:
            try:
                print(f"Requesting files from Drive API... (Page token: {page_token})")
                response = service.files().list(
                    q=query,
                    pageSize=page_size,
                    fields="nextPageToken, files(id, name, mimeType, modifiedTime, size, webViewLink, parents)",
                    pageToken=page_token
                ).execute()

                results.extend(response.get('files', []))
                print(f"Fetched {len(results)} total files so far...")

                previous_page_token = page_token
                page_token = response.get('nextPageToken')

                if not page_token:
                    print("No more pages from Drive API. Finished listing files.")
                    break
                
                # Safety break to prevent infinite loops from the API
                if page_token == previous_page_token:
                    print("Received a duplicate page token from Drive API. Breaking loop.")
                    break

            except Exception as e:
                print(f"Error calling Drive API in list_files: {e}")
                # Break the loop on error to prevent hanging
                break

        return results

    def get_file_metadata(self, file_id: str) -> dict:
        """Get metadata for a specific file"""
        if not self.credentials:
            raise ValueError("Not authenticated")

        authed_http = google_auth_httplib2.AuthorizedHttp(self.credentials, http=httplib2.Http(timeout=60))
        service = build('drive', 'v3', http=authed_http)
        return service.files().get(
            fileId=file_id,
            fields="id, name, mimeType, modifiedTime, size, webViewLink, parents"
        ).execute()

    def download_file(self, file_id: str) -> bytes:
        """Download file content"""
        if not self.credentials:
            raise ValueError("Not authenticated")

        authed_http = google_auth_httplib2.AuthorizedHttp(self.credentials, http=httplib2.Http(timeout=60))
        service = build('drive', 'v3', http=authed_http)
        request = service.files().get_media(fileId=file_id)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        return fh.getvalue()

    def export_google_doc(self, file_id: str, mime_type: str = 'text/plain') -> bytes:
        """Export Google Docs/Sheets/Slides to a downloadable format"""
        if not self.credentials:
            raise ValueError("Not authenticated")

        authed_http = google_auth_httplib2.AuthorizedHttp(self.credentials, http=httplib2.Http(timeout=60))
        service = build('drive', 'v3', http=authed_http)
        request = service.files().export_media(fileId=file_id, mimeType=mime_type)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        return fh.getvalue()

    def build_file_path(self, file_id: str, file_name: str, parents: Optional[List[str]] = None) -> str:
        """Build the full path of a file by traversing parent folders"""
        if not parents or not self.credentials:
            return f"/{file_name}"

        authed_http = google_auth_httplib2.AuthorizedHttp(self.credentials, http=httplib2.Http(timeout=60))
        service = build('drive', 'v3', http=authed_http)
        path_parts = [file_name]

        current_parent = parents[0] if parents else None

        while current_parent:
            try:
                parent_metadata = service.files().get(
                    fileId=current_parent,
                    fields="id, name, parents"
                ).execute()

                path_parts.insert(0, parent_metadata['name'])
                current_parent = parent_metadata.get('parents', [None])[0]
            except:
                break

        return "/" + "/".join(path_parts)

    def is_authenticated(self) -> bool:
        """Check if user is authenticated with valid credentials"""
        return self.credentials is not None and self.credentials.valid


# Global instance
drive_service = DriveService()
