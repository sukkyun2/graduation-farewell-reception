import boto3
import shutil
import os


def copy_image(source_path, destination_path):
    image_name = os.path.basename(source_path)

    destination_file_path = os.path.join(destination_path, image_name)
    shutil.copyfile(source_path, destination_file_path)


class Rekognition:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name='ap-northeast-2'):
        assert aws_secret_access_key != ''
        assert aws_access_key_id != ''

        self.rekognition = boto3.client('rekognition',
                                        region_name=region_name,
                                        aws_access_key_id=aws_access_key_id,
                                        aws_secret_access_key=aws_secret_access_key)

    def detect_labels(self, image_path):
        # 이미지 파일에서 레이블 검출
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()

        response = self.rekognition.detect_labels(Image={'Bytes': image_bytes})

        # 검출된 레이블 출력
        labels = [label['Name'] for label in response['Labels']]
        print("Detected labels:", labels)

        return labels

    def compare_faces(self, source_image_path, target_image_path, similarity_threshold=20.0):
        positive_path = 'inference/positive'
        negtive_path = 'inference/negative'

        with open(source_image_path, 'rb') as source_image_file, open(target_image_path, 'rb') as target_image_file:
            source_image_bytes = source_image_file.read()
            target_image_bytes = target_image_file.read()

        response = self.rekognition.compare_faces(SourceImage={'Bytes': source_image_bytes},
                                                  TargetImage={'Bytes': target_image_bytes},
                                                  SimilarityThreshold=similarity_threshold)
        # 얼굴 비교 결과 출력
        if response['FaceMatches']:
            print(f"Face match found! File Name : {os.path.basename(target_image_path)}")
            for match in response['FaceMatches']:
                similarity = match['Similarity']
                print(f"Similarity: {similarity}%")

                copy_image(target_image_path, positive_path)
        else:
            print(f"No face match found. File Name : {os.path.basename(target_image_path)}")

            copy_image(target_image_path, negtive_path)
