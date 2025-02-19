from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os
import requests
from requests.exceptions import RequestException
import time
from lxml import etree
import pyautogui
import uuid
import datetime
import hashlib
from PIL import ImageGrab
import ddddocr
from PIL import Image
import cv2


def randomCode_ocr(randomCode_x1, randomCode_y1, randomCode_x2, randomCode_y2):  # 获取登录验证码
    randomCode_x1 = int(randomCode_x1)
    randomCode_y1 = int(randomCode_y1)
    randomCode_x2 = int(randomCode_x2)
    randomCode_y2 = int(randomCode_y2)
    bbox = (randomCode_x1, randomCode_y1, randomCode_x2, randomCode_y2)
    im = ImageGrab.grab(bbox)
    a = im.transpose(Image.ROTATE_90)
    a.save('as1.png')
    img = Image.open('as1.png')
    img = img.transpose(Image.ROTATE_270)  # 将图片旋转90度
    img.save("as1.png")
    ocr = ddddocr.DdddOcr()
    with open('as1.png', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    os.remove('as1.png')
    return res


def open_new_tap(browser, url):  # 在已打开的浏览器中用新建标签页打开网址
    browser.get(url)
    # do something with the driver object


def get_mac_address():  # 获取本计算机的mac地址
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
    mac_address = "-".join([mac[e:e + 2] for e in range(0, 11, 2)])
    return mac_address


def encrypt_program():  # 对程序进行加密，返回系统计算出的授权码
    mac_address = get_mac_address()
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    local_information = str(mac_address) + '-' + str(year) + '-' + str(month) + '-' + '2022年11月6日14:05:55'
    authorization_code = encrypt_method(local_information)
    return authorization_code


def encrypt_method(local_information):  # 加密方式
    md5 = hashlib.md5(local_information.encode()).hexdigest()
    sha1 = hashlib.sha1(md5.encode()).hexdigest()
    sha256 = hashlib.sha256(sha1.encode()).hexdigest()

    return sha256

def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def make_new_lesson_codings(names):
    # 对原列表进行遍历
    for name in names:
        new_name = name[8: 24]
        # 把当前变量保存在新列表中
        new_names.append(new_name)

    return new_names  # 返回新列表


def make_lesson_urls(url, codes):
    for code in codes:
        genuine_url = url[0: 32] + 'playkpoint' + url[39: 56] + '?kpointId=' + code
        genuine_urls.append(genuine_url)

    return genuine_urls


def parse_one_page(html):
    # html.encoding = 'utf-8'
    selecter = etree.HTML(html)
    old_lesson_codings = selecter.xpath(
        '//*[@id="aCoursesList"]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li/@onclick')
    lesson_codings = make_new_lesson_codings(old_lesson_codings)
    lesson_urls = make_lesson_urls(lessons_url, lesson_codings)
    lesson_types = selecter.xpath(
        '/html/body/div[1]/div[1]/div[4]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li/div/a[2]/@title')
    lesson_times = selecter.xpath(
        '/html/body/div[1]/div[1]/div[4]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li/div/a[2]/small/text()')
    return lesson_urls, lesson_types, lesson_times


def lesson_times_analyze(lesson_times):  # 获得每个课时所需要的时间，秒为单位
    for lesson_time in lesson_times:
        if lesson_time[1].isdigit():
            if lesson_time[2].isdigit():
                lesson_time_minute = lesson_time[0:3]
            else:
                lesson_time_minute = lesson_time[0:2]
        else:
            lesson_time_minute = lesson_time[0]

        lesson_time_second = (int(lesson_time_minute) + int(2)) * int(60)
        lesson_time_seconds.append(lesson_time_second)
    return lesson_time_seconds

def main(browser,url, play_button_coordinate_x, play_button_coordinate_y, photo_button_coordinate_x, photo_button_coordinate_y):
    print('开始学习课程：' + url)
    html = get_one_page(url)
    lesson_sourse = parse_one_page(html)
    lesson_urls = lesson_sourse[0]
    lesson_types = lesson_sourse[1]
    lesson_times = lesson_times_analyze(lesson_sourse[2])
    lesson_quantity = len(lesson_urls)  # 获取课时数量
    for i in range(0, lesson_quantity):
        open_new_tap(browser,lesson_urls[i])
        time.sleep(10)
        if lesson_types[i] == '视频播放':
            pyautogui.moveTo(int(play_button_coordinate_x), int(play_button_coordinate_y), duration=1)
            time.sleep(1)
            pyautogui.click()
            time.sleep(lesson_times[i])
            # 选择点击播放按钮
            # 选择sleep lesson_times[i]
        else:
            pyautogui.moveTo(int(photo_button_coordinate_x), int(photo_button_coordinate_y), duration=1)
            pyautogui.scroll(-9999999)
            time.sleep(5)

        time.sleep(4)
        print('已经学完第' + str(int(i) + int(1)) + '课时')
    print('本课程已经学完')


if __name__ == '__main__':
    test_first = input("这是测试信息")
    print('你的本机mac地址为：' + get_mac_address())
    user_authorization_code = input('请输入授权码，可告知向开发者mac地址，询问授权码：')
    if user_authorization_code == encrypt_program():
        print('授权码正确，可以继续使用。为更好运行程序，请学习时不要操作电脑。')

        # 查看浏览器坐标信息
        print('请在打开的浏览器中查看验证码区域坐标，并手动登录，查看播放按钮和图文滚动坐标，并进行记录。')
        print('记录完成后，打开本程序窗口，输入任意数字，进行下一步：')
        time.sleep(10)

        test_browser = browser = webdriver.Edge(executable_path='msedgedriver.exe')
        test_browser.maximize_window()
        test_browser.get('https://www.sxgbxx.gov.cn/login')
        test_browser_canshu = input('请输入任意内容并回车，进行下一步操作。')
        test_browser.quit()
        time.sleep(3)

        # 输入所有初始信息
        randomCode_x1 = input('请输入验证码左上角的x坐标：')
        randomCode_y1 = input('请输入验证码左上角的y坐标：')
        randomCode_x2 = input('请输入验证码右下角的x坐标：')
        randomCode_y2 = input('请输入验证码右下角的y坐标：')
        play_button_coordinate_x = input('请输入播放按钮x坐标：')
        play_button_coordinate_y = input('请输入播放按钮y坐标：')
        photo_button_coordinate_x = input('请输入图文课程滚动x坐标：')
        photo_button_coordinate_y = input('请输入图文课程滚动x坐标：')

        usernames_list = input('输入需要学习的账户名，空格隔开：')
        passwords_list = input('请输对应账户的密码，空格隔开：')
        lessons_urls_list = input('请输入课程网址，多个课程之间空格隔开：')
        usernames = usernames_list.split(' ')
        passwords = passwords_list.split(' ')
        lessons_urls = lessons_urls_list.split(' ')
        usernames_number = range(len(usernames))  # 查看有几个账号

        # 开始一个账户的学习
        for i in usernames_number:
            username = usernames[i]
            password = passwords[i]

            browser = webdriver.Edge(executable_path='msedgedriver.exe')
            browser.maximize_window()
            browser.get('https://www.sxgbxx.gov.cn/login')
            time.sleep(3)

            code = randomCode_ocr(randomCode_x1, randomCode_y1, randomCode_x2, randomCode_y2)
            print(code)

            # 定位用户名和密码输入框，并输入相应的信息
            browser.find_element_by_xpath('//*[@id="userEmail"]').send_keys(username)
            browser.find_element_by_xpath('//*[@id="userPassword"]').send_keys(password)
            browser.find_element_by_xpath('//*[@id="randomCode"]').send_keys(code)
            time.sleep(2)
            browser.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div[4]/section/div/article/section/section/div[2]/a').click()
            time.sleep(3)

            for lessons_url in lessons_urls:
                new_names = []
                genuine_urls = []
                lesson_time_seconds = []
                main(browser, lessons_url, play_button_coordinate_x, play_button_coordinate_y,
                     photo_button_coordinate_x, photo_button_coordinate_y)

            print('账户' + username + '所有课程以学习完成')
            time.sleep(2)
            browser.close()
            time.sleep(4)

        print('所有账户学习完毕')

    else:
        print('授权码不正确或授权码到期，授权码请询问开发者。')

    input('程序已经运行完毕，可以关闭了！')
