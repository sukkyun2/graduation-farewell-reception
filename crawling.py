from selenium import webdriver

from polypony_crawler import PolyponyTargetCrawler, PolyponyPhotoCrawler
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--menu_id", type=int, required=True, help='네이버 카페 메뉴 고유 번호')
    parser.add_argument("--naver_id", type=str, required=True, help='유효한 네이버 아이디')
    parser.add_argument("--naver_pw", type=str, required=True, help='유효한 네이버 비밀번호')
    parser.add_argument("--debug", type=bool, default=False)

    parsed, _ = parser.parse_known_args()

    options = webdriver.ChromeOptions()
    if not parsed.debug:
        options.add_argument('headless')  # 창을 띄우지 않고 실행
    driver = webdriver.Chrome(options=options)

    target_crawler = PolyponyTargetCrawler(driver, parsed.menu_id)
    board_no_list = target_crawler.crawling()

    photo_crawler = PolyponyPhotoCrawler(driver)
    photo_crawler.login(parsed.naver_id, parsed.naver_pw)

    for board_no in board_no_list:
        photo_crawler.crawling(board_no)