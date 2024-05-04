export MENU_ID= #TODO ex)53
export NAVER_ID= #TODO
export NAVER_PW= #TODO
export AWS_ACCESS_KEY_ID= #TODO ex)AKIDKANDRJUR
export AWS_SECRET_ACCESS_KEY= #TODO ex)ciqT36zmZosask59
export SOURCE_IMAGE_PATH= #TODO ex)source/source1.jpg
export GOOGLE_DRIVE_DIR_ID= #TODO ex)1rv9aH7DE1QA18PaatrDa
export GOOGLE_APPLICATION_CREDENTIALS= #TODO ex)service_account.json

all: crawling rekognition upload

crawling:
	python crawling.py --menu_id=$(MENU_ID) --naver_id=$(NAVER_ID) --naver_pw=$(NAVER_PW)
rekognition:
	python compare_face.py --aws_access_key_id=$(AWS_ACCESS_KEY_ID) --aws_secret_access_key=$(AWS_SECRET_ACCESS_KEY) --source_image_path=$(SOURCE_IMAGE_PATH)
upload:
	python upload_drive.py --google_drive_dir_id=$(GOOGLE_DRIVE_DIR_ID)
