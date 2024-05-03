import argparse
import os
import tarfile

import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def make_tar_gz(target_dir: str):
    target_gz_file = target_dir + '.tar.gz'

    if os.path.exists(target_gz_file):
        print(f'압축파일 {target_gz_file}이 이미 존재합니다.')
        return

    with tarfile.open(target_gz_file, 'w:gz') as tar:
        tar.add(target_dir, arcname=os.path.basename(target_dir))
        print(f'압축파일 {target_gz_file}이 생성되었습니다.')


def upload_file_to_drive(file_path: str, google_drive_dir_id: str):
    creds, _ = google.auth.default()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': file_path.replace('/', '_'),
        'parents': [google_drive_dir_id]
    }

    media = MediaFileUpload(file_path, mimetype='application/gzip')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f'파일이 업로드되었습니다. 파일 ID: {file.get("id")}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, default='inference/positive', help='업로드할 output 디렉토리 경로')
    parser.add_argument("--google_drive_dir_id", type=str, required=True, help='드라이브에 업로드할 디렉토리 경로')

    parsed, _ = parser.parse_known_args()

    make_tar_gz(parsed.target_dir)
    upload_file_to_drive(parsed.target_dir + '.tar.gz', parsed.google_drive_dir_id)
