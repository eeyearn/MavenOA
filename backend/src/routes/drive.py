"""
Drive Routes 
Handles file and folder listing from Google Drive
"""

import asyncio
from typing import Optional, List

from fastapi import APIRouter, HTTPException
from ..services.drive_service import drive_service
from ..types import DriveFile, DriveFolder

router = APIRouter(prefix="/drive", tags=["drive"])


@router.get("/files")
async def get_files(folderId: Optional[str] = None):
    """Returns a list of all files in the user's Drive, optionally filtered by folder."""
    try:
        files = await asyncio.to_thread(drive_service.list_files, folder_id=folderId)
        # Filter out folders from the general file list
        files = [f for f in files if f['mimeType'] != 'application/vnd.google-apps.folder']
        return sorted(files, key=lambda f: f['name'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/folders")
async def get_folders():
    """Returns a list of all folders in the user's Drive."""
    try:
        # We get all files and then filter for folders.
        # This can be optimized if needed.
        all_files = await asyncio.to_thread(drive_service.list_files)
        folders = [
            f for f in all_files
            if f['mimeType'] == 'application/vnd.google-apps.folder'
        ]
        return sorted(folders, key=lambda f: f['name'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/folders/{folder_id}", response_model=DriveFolder)
async def get_folder(folder_id: str):
    """
    Get details about a specific folder.
    """
    try:
        folder_metadata = drive_service.get_file_metadata(folder_id)

        if folder_metadata['mimeType'] != 'application/vnd.google-apps.folder':
            raise HTTPException(status_code=400, detail="File is not a folder")

        # Count files in folder
        files_in_folder = drive_service.list_files(folder_id=folder_id)
        file_count = len([f for f in files_in_folder if f['mimeType'] != 'application/vnd.google-apps.folder'])

        path = drive_service.build_file_path(
            folder_metadata['id'],
            folder_metadata['name'],
            folder_metadata.get('parents')
        )

        return DriveFolder(
            id=folder_metadata['id'],
            name=folder_metadata['name'],
            path=path,
            fileCount=file_count
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
