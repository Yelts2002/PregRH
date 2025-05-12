# Preguntas/drive_utils.py

from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def subir_archivo_a_drive(nombre_archivo, ruta_archivo_local):
    """
    Sube un archivo a la carpeta de Drive configurada y devuelve su ID.
    """
    creds = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': nombre_archivo,
        'parents': [settings.GOOGLE_DRIVE_FOLDER_ID],
    }
    media = MediaFileUpload(ruta_archivo_local, resumable=True)
    drive_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return drive_file.get('id')
