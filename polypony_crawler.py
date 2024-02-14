import os
import time
from urllib.parse import quote

import pyperclip
import urllib3
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class PolyponyTargetCrawler:
    def __init__(self, driver: WebDriver, menu_id: int):
        self.driver = driver
        self.menu_id = menu_id
        self.board_type = 'L'
        self.list_url = "https://cafe.naver.com/cbnupolyphony" \
                        "?iframe_url=/ArticleList.nhn" \
                        f"%3Fsearch.clubid=29044951%26search.menuid={self.menu_id}%26search.boardtype={self.board_type}"

    def crawling(self):
        page_urls = self.crawling_pages()
        board_no_list = []
        for page_url in page_urls:
            board_no_list += self.crawling_board_no(page_url)
            time.sleep(2)

        print('crawling done :)')
        print(f"total : {len(board_no_list)}")

        return board_no_list

    def crawling_pages(self):
        def convert_page_url(page_element: WebElement):
            page_no = page_element.text
            additional_query_string = quote('&search.page') + '=' + page_no

            return self.list_url + additional_query_string

        self.driver.get(self.list_url)
        self.__switch_iframe__()

        # div.prev-next 클래스를 가진 div 엘리먼트 찾기
        div_element = self.driver.find_element(By.CSS_SELECTOR, 'div.prev-next')

        # div 엘리먼트 내부에서 a 태그 찾기
        page_elements = div_element.find_elements(By.TAG_NAME, 'a')
        return list(map(convert_page_url, page_elements))

    def crawling_board_no(self, page_url):
        self.driver.get(page_url)
        self.__switch_iframe__()

        board_no_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.inner_number')
        return list(map(lambda e: e.text, board_no_elements))

    def __switch_iframe__(self):
        iframe_element = self.driver.find_element(By.CSS_SELECTOR, 'iframe#cafe_main')
        self.driver.switch_to.frame(iframe_element)


class PolyponyPhotoCrawler:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.title = None
        self.images = []

    def crawling(self, board_no):
        self.__extract_image__(board_no)
        self.__download_images__(board_no)

        print('crawling done :)')
        print(f"total : {len(self.images)}")

    def login(self, nid, npw):
        naver_login_url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com'
        self.driver.get(naver_login_url)

        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, '#id')
        pyperclip.copy(nid)
        self.driver.find_element(By.CSS_SELECTOR, '#id').send_keys(Keys.CONTROL + 'v')

        time.sleep(1)
        pyperclip.copy(npw)

        # 비밀번호 보안을위해 클립보드에 blank저장
        secure = 'blank'
        self.driver.find_element(By.CSS_SELECTOR, '#pw').send_keys(Keys.CONTROL + 'v')
        pyperclip.copy(secure)
        self.driver.find_element(By.XPATH, '//*[@id="log.login"]').click()

    def __extract_image__(self, board_no):
        detail_url = f"https://cafe.naver.com/cbnupolyphony/{board_no}"

        self.driver.get(detail_url)
        time.sleep(3)

        # iframe으로 스위치
        iframe_element = self.driver.find_element(By.CSS_SELECTOR, 'iframe#cafe_main')
        self.driver.switch_to.frame(iframe_element)

        img_elements = self.__find_element_old_version__() + self.__find_element_new_version__()
        title = self.driver.find_element(By.CSS_SELECTOR, 'h3.title_text').text
        images = list(map(lambda e: Image(title, e), img_elements))

        self.title = title
        self.images = images

    def __find_element_old_version__(self):
        return self.driver.find_elements(By.CSS_SELECTOR, 'img.article_img.ATTACH_IMAGE')

    def __find_element_new_version__(self):
        div_element = self.driver.find_element(By.CSS_SELECTOR, 'div.content.CafeViewer')
        img_elements = div_element.find_elements(By.CSS_SELECTOR, 'img.se-image-resource')

        # old version과 규격을 맞추기 위함
        for index, img_element in enumerate(img_elements):
            self.driver.execute_script(f"arguments[0].setAttribute('data-index', '{index}')", img_element)

        return img_elements

    def __download_images__(self, board_no):
        output_dir_path = f"./output/{self.title}.{board_no}"

        def make_dir():
            if not os.path.exists(output_dir_path):
                os.makedirs(output_dir_path)
                print(f"Directory has been created: {output_dir_path}")

        def download_image(image: Image):
            http = urllib3.PoolManager()

            response = http.request('GET', image.src)

            if response.status == 200:
                destination = f"{output_dir_path}/{image.file_name()}"
                with open(destination, 'wb') as f:
                    f.write(response.data)
                print(f"Image downloaded successfully: {image.file_name()}")
            else:
                print(f"Failed to download image. Status code: {response.status}")

        make_dir()
        for image in self.images:
            download_image(image)


class Image:
    def __init__(self, title: str, image_element: WebElement):
        if image_element is None:
            AssertionError('image element is not none!')

        self.name = f"{title}-{image_element.get_attribute('data-index')}"
        self.src = image_element.get_attribute('src')

    def file_name(self):
        return self.name + '.jpg'
