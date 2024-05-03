# 🎓졸환회 사진 분류기

---
이 프로젝트는 졸업식 환송회 행사에서 전달 할 졸업생들의 사진을 분류하는 분류기입니다

사진 분류는 총 `두 가지 과정`으로 진행된다

1. 네이버 카페 메뉴 카테고리에 있는 모든 게시글의 사진을 크롤링
2. 여러 장의 사진 중에서 찾으려는 사람을 필터링

### 1. 크롤링

---
크롤링을 하기 위해서는 유효한 네이버 계정이 필요하다

유효한 네이버 계정이란 [폴리포니 카페](https://cafe.naver.com/cbnupolyphony) 에 가입되어 있는 계정이어야 한다.

| 파라미터 명     | 설명                  | 필수 파라미터 여부     |
|------------|---------------------|----------------|
| --menu_id  | 네이버 카페 메뉴 고유 번호     | O              |
| --naver_id | 유효한 네이버 아이디         | O              |
| --naver_pw | 유효한 네이버 비밀번호        | O              |
| --debug    | `True`일경우, 크롤링 창 실행 | X(기본값 `False`) |

#### 실행 예시

```bash
python crawling.py \
--menu_id=네이버 메뉴 아이디 \ 
--naver_id=네이버 아이디 \
--naver_pw=네이버 비밀번호  \
--debug=True 
```

#### 결과물

실행 된 결과물은 `output` 디렉토리에 게시물 별로 저장된다
output 하위 디렉토리의 명명 규칙은 `게시물 명.게시물 고유 번호`로 저장된다
> 게시물 제목이 중복일 경우 덮어씌워지는 이슈를 막기 위함

예시

```bash
├── output
│   ├── 23년 PP인의밤.2019
│   ├── 23년 졸환회.2020
│   └── 23년도 하계수련회 콩쿨.2069
```

### 2. 필터링

`1번 과정`에서 크롤링한 사진들을 [Amazon Rekognition](https://aws.amazon.com/ko/rekognition/)을 사용하여 특정 인물을 필터링한다.

`source_image_path`은 필터링할 인물의 사진이다.

`target_directory_path`는 `1번 과정`에서 크롤링한 사진들을 모아놓은 디렉토리 위치이다. 별도로 지정할 수 있으며 default값은 `output`이다.

`AWS Access Key`와 관련된
정보는 [해당 링크](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html?icmpid=docs_iam_console#Using_CreateAccessKey)
를 참조

| 파라미터 명                  | 설명                                 | 필수 파라미터 여부 |
|-------------------------|------------------------------------|------------|
| --aws_access_key_id     | AWS Access Key                     | O          |
| --aws_secret_access_key | AWS Secret Access Key              | O          |
| --source_image_path     | 기준 이미지 경로                          | O          |
| --target_directory_path | 필터링 대상 이미지 디렉토리 경로(default output) | X          |

#### 실행 예시

```bash
python compare_face.py \
--aws_access_key_id=ACCESS KEY ID \
--aws_secret_access_key=SECRET ACCESS KEY \
--target_directory_path=output 
--source_image_path=source.jpg
```

#### 결과물

실행 된 결과물은 `inference` 디렉토리 하위에 `negative`, `positive`로 나뉘어 저장된다.

negative는 특정 인물이 포함되지 않은 이미지를 분류한 것이고 positive는 특정 인물이 포함됐다고 판단한 이미지들이다.

예시

```bash
├── inference
│   ├── negative
│   └── positive
```

### [성능 평가](https://github.com/sukkyun2/graduation-farewell-reception/wiki/%EC%84%B1%EB%8A%A5-%ED%8F%89%EA%B0%80)
