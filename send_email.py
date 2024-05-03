import argparse
import os
import tarfile

from gmail_sender import mail_sender


def make_tar_gz(target_dir):
    target_gz_file = target_dir + '.tar.gz'

    if os.path.exists(target_gz_file):
        print(f'압축파일 {target_gz_file}이 이미 존재합니다.')

    with tarfile.open(target_gz_file, 'w:gz') as tar:
        tar.add(target_dir, arcname=os.path.basename(target_dir))
        print(f'압축파일 {target_gz_file}이 생성되었습니다.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--target_dir", type=str, required=False, default='inference', help='이미지 분류 결과 디렉토리 경로')
    parser.add_argument("--sender_email", type=str, required=True, help='유효한 지메일 아이디')
    parser.add_argument("--sender_password", type=str, required=True, help='유효한 지메일 비밀번호')
    parser.add_argument("--receiver_email", type=str, required=True, help='결과를 보낼 이메일 주소')

    parsed, _ = parser.parse_known_args()

    make_tar_gz(target_dir=parsed.target_dir)
    sender = mail_sender(
        receiver_email=parsed.receiver_email,
        sender_email=parsed.sender_email,
        sender_password=parsed.sender_password
    )

    sender.send(parsed.target_dir + '.tar.gz')
