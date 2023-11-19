from selenium import webdriver
from selenium.webdriver.edge.service import Service
from PIL import Image
import time
import msvcrt
import os
import glob
import pyautogui
import io

def scroll_and_screenshot(driver, delay, screenshots):
    # 等一会儿
    time.sleep(delay)

    # 获取浏览器窗口的高度
    window_height = driver.execute_script("return window.innerHeight")

    # 第一次滚动和截图
    driver.save_screenshot(f'ScreenshotWebPage\output\screenshot_{len(screenshots)}.png')
    screenshots.append(Image.open(f'ScreenshotWebPage\output\screenshot_{len(screenshots)}.png'))
    # driver.execute_script(f"window.scrollBy(0, {window_height});")

    # 从第二次开始，滚动和截图的步长都为浏览器窗口高度的四分之三
    scroll_step = window_height * 3 / 4

    # 获取网页的高度
    # last_height = driver.execute_script("return document.body.scrollHeight")
    # flag = 0
    driver.execute_script(f"window.scrollBy(0, {scroll_step});")
    while True:
        # 获取滚动前的页面滚动高度
        last_scroll_height = driver.execute_script("return window.pageYOffset")
        # if flag == 0:
        #     screenshot = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
        #     cropped = screenshot.crop((0, screenshot.height / 4, screenshot.width, screenshot.height))
        #     cropped.save(f'ScreenshotWebPage\output\screenshot_{len(screenshots)}.png')
        #     screenshots.append(cropped)
        #     flag = 1

        # 截图并保存
        # driver.save_screenshot(f'ScreenshotWebPage\output\screenshot_{len(screenshots)}.png')
        # screenshots.append(Image.open(f'ScreenshotWebPage\output\screenshot_{len(screenshots)}.png'))

        # 截图并保存
        screenshot = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
        cropped = screenshot.crop((0, screenshot.height / 4, screenshot.width, screenshot.height))
        cropped.save(f'ScreenshotWebPage\output\screenshot_{len(screenshots)}.png')
        screenshots.append(cropped)

        # 滚动一段距离
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")

        # 等待页面加载
        time.sleep(delay)

        # 获取滚动后的页面滚动高度
        new_scroll_height = driver.execute_script("return window.pageYOffset")

        # 计算实际滚动的距离
        actual_scroll_step = new_scroll_height - last_scroll_height

        # 如果实际滚动的距离小于浏览器窗口的高度，那么我们就判断已经滚动到页面底部了
        # if actual_scroll_step < scroll_step:
        #     break

        # 如果实际滚动的距离小于浏览器窗口的高度，那么我们就判断已经滚动到页面底部了
        # if actual_scroll_step < scroll_step:
        #     # 等待一段时间
        #     time.sleep(delay)

        #     last_scroll_step = actual_scroll_step

        #     # 再滚动一次
        #     driver.execute_script(f"window.scrollBy(0, {scroll_step});")

        #     # 获取滚动后的页面滚动高度
        #     new_scroll_height = driver.execute_script("return window.pageYOffset")

        #     # 计算实际滚动的距离
        #     actual_scroll_step = new_scroll_height - last_scroll_height

        #     # 如果滚动的距离为0，那么我们就判断已经滚动到页面底部了
        #     if actual_scroll_step == 0:
        #         break

        # 如果滚动的距离为0，那么我们就判断已经滚动到页面底部了
        if actual_scroll_step == 0:
            break

        # 如果实际滚动的距离小于浏览器窗口的高度
        if actual_scroll_step < scroll_step:
            # 删除最后一张截图
            os.remove(f'ScreenshotWebPage\output\screenshot_{len(screenshots)-1}.png')
            screenshots.pop()

            # 以最后的滚动距离作为高进行最后一次截图
            screenshot = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
            cropped = screenshot.crop((0, screenshot.height - actual_scroll_step, screenshot.width, screenshot.height))
            cropped.save(f'ScreenshotWebPage\output\screenshot_{len(screenshots)}.png')
            screenshots.append(cropped)

        # 检查是否滚动到底部
        # new_height = driver.execute_script("return document.body.scrollHeight")
        # if new_height == last_height:
        #     break
        # last_height = new_height

        # 比较两次截图
        # if screenshots[-1] == screenshots[-2]:
        #     screenshots.pop()  # 删除最后一张截图
        #     break

        # 检查用户是否按下Esc
        if msvcrt.kbhit() and msvcrt.getch() == b'\x1b':
            break

if __name__ == "__main__":
    if os.path.exists('ScreenshotWebPage\output'):
        files = glob.glob('ScreenshotWebPage\output\*')
        for file in files:
            os.remove(file)
    # web_url = input('请输入完整的网址：')
    # delay = int(input('请输入延迟时间（秒）：'))
    # web_url = 'https://m.douban.com/movie/'
    # 从url.txt文件中读取所有的网页url
    with open(r'ScreenshotWebPage\url.txt', 'r') as file:
        web_urls = file.readlines()
    # 遍历所有的网页url
    for web_url in web_urls:
        if os.path.exists('ScreenshotWebPage\output'):
            files = glob.glob('ScreenshotWebPage\output\*')
            for file in files:
                os.remove(file)
        web_url = web_url.strip()  # 去除每行末尾的换行符
        # 其他的代码...
        # 获取显示器的高度
        screen_width, screen_height = pyautogui.size()
        driver = webdriver.Edge(service=Service('ScreenshotWebPage\msedgedriver.exe'))
        driver.get(web_url)
        driver.fullscreen_window()
        # 设置浏览器窗口的高度
        driver.set_window_size(driver.get_window_size()['width'], screen_height)
        screenshots = []
        scroll_and_screenshot(driver, 2, screenshots)
        driver.quit()

        # 合并截图
        total_height = sum([img.height for img in screenshots])
        merged = Image.new('RGB', (screenshots[0].width, total_height))
        y = 0
        for img in screenshots:
            merged.paste(img, (0, y))
            y += img.height
        merged.save('ScreenshotWebPage\output\merged.png')
        # 重命名merged.png文件，并移动到上一个目录
        os.rename('ScreenshotWebPage\output\merged.png', f'ScreenshotWebPage\{web_url.split("/")[-2]}.png')