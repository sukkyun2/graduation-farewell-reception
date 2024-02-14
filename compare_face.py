import argparse
import os

import botocore.errorfactory

from rekognition import Rekognition


def get_image_paths(root_dir_path):
    image_paths = []

    sub_dir_list = os.listdir(root_dir_path)

    for sub_dir_path in sub_dir_list:
        dir_path = os.path.join(root_dir_path, sub_dir_path)
        for file_name in os.listdir(dir_path):
            image_paths.append(os.path.join(dir_path, file_name))

    return image_paths


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--aws_access_key_id", type=str, required=True)
    parser.add_argument("--aws_secret_access_key", type=str, required=True)
    parser.add_argument("--source_image_path", type=str, required=True, help='기준 이미지 경로')
    parser.add_argument("--target_directory_path", type=str, default='output', help='필터링 대상 이미지 디렉토리 경로')

    parsed, _ = parser.parse_known_args()

    target_image_paths = get_image_paths(parsed.target_directory_path)

    rekognition = Rekognition(parsed.aws_access_key_id, parsed.aws_secret_access_key)
    for target_image_path in target_image_paths:
        try:
            rekognition.compare_faces(parsed.source_image_path, target_image_path)
        except botocore.errorfactory.ClientError:
            print(f"Amazon Rekognition API Error!! Pass Image : {target_image_path}")
