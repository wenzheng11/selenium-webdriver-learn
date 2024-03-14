from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
# 加入异步模块
import asyncio
import concurrent.futures
import requests
import random
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import re
from bs4 import BeautifulSoup
import yaml

# 需要的第三方包 ： bs4 ， selenium ，requests
with open('config.yaml', 'r', encoding='utf-8') as file:
    # 解压yaml 文件
    data = yaml.safe_load(file)
# 日志存储位置
log_file = data['Logging']['log_file']
# 遍历的URL
urls = [
    "https://developer.aliyun.com/?spm=a2c6h.27063436.J_6978680750.2.46d34f46yWj5e2",
    "https://developer.aliyun.com/group/networking/ask",
    "https://developer.aliyun.com/group/aliyun_linux/?spm=a2c6h.28340001.J_7035175860.1.22c91a97nM7IWo",
    "https://developer.aliyun.com/group/yunxiao/",
    "https://developer.aliyun.com/group/viapi/",
    "https://developer.aliyun.com/yitian/",

    "https://developer.aliyun.com/cloudnative/?spm=a2c6h.12873639.article-detail.10.5ab636f0SAEUqp",
    "https://developer.aliyun.com/iot/?spm=a2c6h.12873639.article-detail.15.5ab636f0SAEUqp",
    "https://developer.aliyun.com/polardb/?spm=a2c6h.12873639.article-detail.16.5ab636f0SAEUqp",
    "https://developer.aliyun.com/modelscope/?spm=a2c6h.12873639.article-detail.8.5ab636f0CRjDDi",
    "https://developer.aliyun.com/bigdata/?spm=a2c6h.12873639.article-detail.9.5ab636f0SAEUqp",
    "https://developer.aliyun.com/computenest/?spm=a2c6h.12873639.article-detail.11.5ab636f0SAEUqp",
    "https://developer.aliyun.com/database/?spm=a2c6h.12873639.article-detail.12.5ab636f0SAEUqp",
    "https://developer.aliyun.com/ecs/?spm=a2c6h.12873639.article-detail.13.5ab636f0dnhhzy",
    "https://developer.aliyun.com/storage/?spm=a2c6h.12873639.article-detail.14.5ab636f0dnhhzy",

]

"""

"""
# 运行的账号
accounts = [{'name': acc['name'], 'password': acc['password']} for acc in data['Database']['accounts']]

pinlun = [
    '这篇文章真的是非常优秀的。作者不仅提供了深入的分析和解释，而且还包含了很多实用的建议和技巧。我特别欣赏他们对于技术问题的热情和执着，这种精神值得我们学习和推崇。总之，我会把这篇文章推荐给我的同事和朋友，因为它对于我们学习和发展技能非常有帮助。',
    '我觉得这篇文章非常出色，因为作者提供了非常详细、深入的分析和解释。我从文章中学到了很多新知识和技巧，这对于我的工作和职业发展非常有帮助。同时，作者的写作风格非常吸引人，让我一直保持着专注并受益匪浅。总之，我认为这是一篇非常优秀的技术文章，值得我们认真阅读和学习。',
    '这篇文章真的是太棒了！作者提供了非常详细、深入的分析和解释，让读者能够完全理解技术问题的复杂性。我非常欣赏作者的专业知识和经验，这些对于技术人员来说是非常宝贵的资源。同时，作者还提供了很多实用的技巧和建议，这些都可以帮助我们更好地应对工作中遇到的挑战。总之，我认为这篇文章是一篇非常优秀的技术文章，值得我们深入研究和学习。',
    '我觉得这篇文章非常出色，因为作者提供了非常深入、详尽的分析和解释。他们的专业知识和经验非常令人印象深刻，而且他们的写作风格也非常吸引人。我从文章中学到了很多新知识和技巧，这些对于我的工作和职业发展非常有帮助。总之，我认为这是一篇非常优秀的技术文章，值得我们认真阅读和学习。',
    '这篇文章非常出色，因为作者提供了非常详细、深入的分析和解释。他们的专业知识和经验非常宝贵，让我感受到了科技行业的魅力和广阔前景。同时，作者的写作风格也非常吸引人，让读者容易理解技术问题的复杂性。总之，我认为这篇文章是一篇非常优秀的技术文章，可以帮助我们更好地理解和应对工作中的技术挑战。',
    '这篇文章非常出色，因为作者提供了非常详细、深入的分析和解释，让读者能够完全理解技术问题的复杂性。他们的专业知识和经验非常令人印象深刻，为我们提供了广阔的视野和深入的思考。同时，作者还提供了很多实用的技巧和建议，可以帮助我们更好地应对工作中的挑战。总之，我认为这篇文章是一篇非常优秀的技术文章，值得我们认真研究和学习。',
    '我觉得这篇文章非常出色，因为作者提供了非常详尽、深入的分析和解释，让读者能够更好地理解技术问题的本质和复杂性。他们的专业知识和经验非常宝贵，为我们提供了许多有用的思路和方法。同时，作者的写作风格也非常吸引人，让读者容易理解和掌握技术问题。总之，我认为这篇文章是一篇非常优秀的技术文章，可以帮助我们更好地应对日常工作中的挑战。',
    '这篇文章真的是太棒了！作者提供了非常详尽、深入的分析和解释，让读者能够充分理解技术问题的本质和复杂性。他们的专业知识和经验非常令人钦佩，为我们提供了深刻的思考和启示。同时，作者还提供了很多实用的技巧和建议，可以帮助我们更好地应对工作中的挑战。总之，我认为这篇文章是一篇非常优秀的技术文章，值得我们认真学习和探究。',
    '这篇文章真的是太出色了！作者提供了非常详细、深入的分析和解释，让读者能够完全理解技术问题的复杂性。他们的专业知识和经验非常宝贵，为我们提供了广阔的视野和深入的思考。同时，作者还提供了很多实用的技巧和建议，可以帮助我们更好地应对日常工作中的挑战。总之，我认为这篇文章是一篇非常优秀的技术文章，可以帮助我们不断提升自己的能力和水平。',
    '我觉得这篇文章真的是太好了！作者提供了非常深入、详尽的分析和解释，让读者能够完全理解技术问题的复杂性。他们的专业知识和经验非常令人印象深刻，为我们提供了广阔的思路和深入的思考。同时，作者提供了很多实用的技巧和建议，让我们能够更好地应对工作中的挑战。总之，我认为这篇文章是一篇非常优秀的技术文章，值得我们认真学习和探究',
    '这篇文章让我深受启发，作者提供了非常有价值的见解和经验，让我对技术领域有了更深入的理解。他们的分析和解释非常详细和透彻，同时还结合了实际案例和经验，使我能够更好地应用这些知识到实际工作中。',
    '我认为这篇文章非常出色，因为作者提供了非常有用和实用的技术知识和建议。他们的专业知识和经验非常宝贵，为我们提供了很多有关技术领域的洞察和启示。同时，作者的写作风格也非常吸引人，使我一直专注并从中受益匪浅。',
    '这篇文章真的是太棒了！作者提供了非常深入、详细的分析和解释，让读者能够更好地理解技术问题的本质和复杂性。他们的专业知识和经验非常丰富，为我们提供了很多实用的技巧和建议，可以帮助我们更好地应对工作中的挑战。',
    '我对这篇文章印象非常深刻，作者提供了非常有价值的技术知识和经验。他们的分析和解释非常透彻，同时还提供了很多实际案例和应用方案，使我能够更好地应用这些知识到实际工作中。总之，我认为这篇文章是一篇非常出色的技术文章，值得我们认真学习和借鉴。',
    '我觉得这篇文章非常出色，因为作者提供了非常详尽、深入的技术分析和解释，让读者能够更好地理解和应用这些知识。他们的专业知识和经验非常丰富，为我们提供了很多有关技术领域的见解和思考。同时，作者还提供了很多实用的技巧和建议，可以帮助我们更好地应对工作中的挑战。',
    '我觉得这篇文章非常出色，因为作者提供了非常详尽、深入的分析和解释，让读者能够更好地理解技术问题的本质和复杂性。他们的专业知识和经验非常丰富，为我们提供了很多有关技术领域的见解和思考。同时，作者还提供了很多实用的技巧和建议，可以帮助我们更好地应对工作中的挑战。总之，我认为这篇文章是一篇非常出色的技术文章，值得我们认真阅读和学习。',
    '作者提供了非常详尽、深入的分析和解释，使读者能够全面理解技术问题的复杂性和挑战。他们的专业知识和经验非常宝贵，为我们提供了很多实际操作的建议和技巧。同时，作者的写作风格也非常吸引人，使我能够保持兴趣并从中受益匪浅。总之，我认为这篇文章是一篇非常出色的技术文章，值得我们认真学习和借鉴。',
    '因为作者提供了非常详尽、深入的分析和解释，让读者能够更好地理解技术问题的本质和复杂性。他们的专业知识和经验非常丰富，为我们提供了很多有关技术领域的见解和思考。同时，作者还提供了实用的技巧和建议，可以帮助我们更好地应对工作中的挑战。总之，我认为这是一篇非常出色的技术文章，值得我们认真阅读和学习。',
    '这篇文章真是令人印象深刻！作者提供了非常详尽和深入的分析，让读者能够更好地理解和应用技术知识。他们的专业知识和经验非常宝贵，为我们提供了很多有益的思考和启示。同时，作者的写作风格也非常吸引人，保持了读者的兴趣并从中受益匪浅。总之，我觉得这篇文章是一篇非常出色的技术文章，值得我们认真学习和借鉴。',
    ]

# 一次启动多少个账号，取决电脑性能
max_run = data['Database']['max_run']
# 签到完成后，等待系统缓冲时间(用于一键领取积分)
buffer_sleep = data['Database']['buffer_sleep']
# 是否开启浏览器UI界面显示（开启后将显示运行画面，关闭后只在后台运行不显示画面）True 开启，False 关闭
is_show = data['Database']['is_show']
# 服务器ip地址
IP = data['Database']['IP']

# 需要运行的项目
is_qiandao = bool(data['Database']['is_qiandao'])  # 签到
is_guankan = bool(data['Database']['is_guankan'])  # 观看视频
is_wenzhang = bool(data['Database']['is_wenzhang'])  # 发布文章
is_sanlian = bool(data['Database']['is_sanlian'])  # 一键三联

#######################################################################################
logging.basicConfig(filename=log_file, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# 获取当前日期和时间
current_date = datetime.datetime.now()
# 获取当前日期的星期几（0代表星期一，6代表星期日）
weekday = current_date.weekday()
weekday = weekday + 1
logging.info("##########################-------开始执行--------############################")
logging.info("获取到今天是星期%s,开始执行脚本" % weekday)


def article(user, driver):

    # 打开网页--- 使用在当前窗口新增网页的操作
    driver.execute_script("window.open('https://chat18.aichatos.xyz/#/chat/1705027883227', '_blank');")
    # 切换到新开的标签页
    driver.switch_to.window(driver.window_handles[-1])
    sleep(4)
    # 当没有远程服务器时，手动控制文章主题
    if not bool(data['Database']['is_connect']):
        a_title = data['Database']['theme']
    else:
        # 标题来自接口获取
        params = {'user': user}
        response = requests.get(IP + 'getTitle', params=params)
        data1 = response.json()

        if data1['code'] == '200':
            a_title = data1['message']
        else:
            print("当前数据库中没有可以使用的主题了")
            return None
    # 每次循环时都重新生成窗口
    driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/div/div/aside/div[1]/div/main/div[1]/button').click()
    wait = WebDriverWait(driver, 6)
    input_box = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div[1]/div/div/div/div/div/div/footer/div/div[3]/div/div[1]/div[1]/textarea')))
    sleep(0.5)
    input_box.send_keys(
        '帮我写一篇文章，包含 标题，摘要，正文 。文章主题是自拟（可以是前端，后端，java，python，C，数据库，等多种类型的技术性文章） 。需要你自己拟标题和文字内容。关联主题即可，是技术性文章即可,摘要部分要和常规的不一样，你不需要包含其他内容，只要 标题，摘要，正文 ')
    sleep(2.5)
    input_box.send_keys(Keys.RETURN)
    # 提交表单并等待网页加载完成
    sleep(70)

    # 不同的循环获取的ip不一致


    # 获取结果
    result = driver.find_element(By.XPATH, '//*[@id="image-wrapper"]/div[2]/div[2]/div/div[1]')

    texts = result.text
    # 提取标题
    title_match = re.search(r"标题：(.*?)摘要", texts, re.DOTALL)
    if title_match:
        title = title_match.group(1)
    else:
        title = None

    # 提取摘要
    summary_match = re.search(r"摘要：(.*?)正文", texts, re.DOTALL)
    if summary_match:
        summary = summary_match.group(1)
    else:
        summary = None

    # 提取正文
    content_match = re.search(r"正文：\n(.*)", texts, re.DOTALL)
    if content_match:
        content = content_match.group(1).strip()
    else:
        content = None
    driver.close()
    # 切换回原窗口
    driver.switch_to.window(driver.window_handles[0])
    return title, summary, content


# 读取cookie的方法，暂时弃用
def get_cookies(driver):
    # 添加cookie
    data = "cna=gxDvHGcjxxQCAasPEH386Thl; currentRegionId=cn-hangzhou; aliyun_lang=zh; cnaui=1801981649879990; aui=1801981649879990; _samesite_flag_=true; cookie2=160eb70adbb657a4e6118e923244a726; munb=2211925078222; login_aliyunid_pk=1576522702724354; login_current_pk=1576522702724354; _tb_token_=eebeeb37f9e13; yunpk=1576522702724354; atpsida=8934ecfd6ac2c4c007e155cc_1698668964_1; sca=2426df8e; aliyun_choice=CN; login_disaster=master; csg=440b4d84; t=30c209eb33aebc299078ef7a14fb873a; login_aliyunid_ticket=GxRigm2Cb4fGaCdBZWIzmgdHq6sXXZQg4KFWufyvpeV*0*Cm58slMT1tJw3_7$$2a_COp3VtgLJEGhROm8Kwn7KE64FCcsRFcnxhJyUpVof_BNpwU_TOTNChZBoeM1KJexdfb9zhYnsN5Zos6qISCr7t0; login_aliyunid_csrf=_csrf_tk_1449998832524584; hssid=CN-SPLIT-ARCEByIOc2Vzc2lvbl90aWNrZXQyAQE4use80rgxQAFKEMhSlIkgjw8PBQ3SY6r-PYQpbkS8Sx-JCcc66RDl4qyoIOF9bg; hsite=6; aliyun_country=CN; aliyun_site=CN; login_aliyunid_pks=BG+iTppNl48RFhGNh+yLRuTGbuoe7JilprVY0KswOKTC/8=; login_aliyunid=%E6%96%B0%E7%9A%84%E8%B4%A6%E5%8F%B7001; isg=BAUFcNcbzMZTg-moDzGC4cnXFEE_wrlUsklkBQdqzTxLniUQzxE1JR7vqsJo3tEM; l=fBIfhd6eNyIa_Sd5BOfwPurza77OSIRAguPzaNbMi9fPOm1B5w7dW1F40cL6C3GVFs_6R3RpoAReBeYBq7F-nxvtGwBLE8DmndLHR35..; tfstk=dZeeb0NvE9BU_-0CMXDrQokpdVMKexQbt8gSquqoA20HdpTu_zagAHiQV5uzSPuHdk1KZ04bVXVQVJ6zarMnwWgSR4kz2rS1lt6bvkH-nZ_fh5J8vYK1x3NlhkEKeYbflt6XUf3RuT-xbCxeEXQ0DV2pUYw_dazx7LvyDDlnot3wEL2ZYlucQnL-j4i7e8BJZXmtbqsNbY1kz_1.."
    # data = "cna=gxDvHGcjxxQCAasPEH386Thl;currentRegionId=cn-hangzhou;"
    # 当存在有多个cookie时
    # 将数据以分号进行拆分
    items = data.split('; ')
    print(items)
    # 创建一个字典存储结果
    result = {}
    # 遍历每个键值对并添加到字典中
    for item in items:
        key, value = item.split('=', 1)
        result[key] = value
        cookie = {'name': key, 'value': value}
        driver.add_cookie(cookie)
    print("添加内容完成")
    logging.info("添加cookie信息完成")
    # 刷新页面，使添加的 Cookie 生效
    driver.refresh()
    sleep(2)


def huadong(driver):
    # 滑动方法-当前可以弃用
    # 当某次循环点击过时，后续的应该不在点击了
    try:
        # 应该判断是否有ifame，存在ifame时才点击，不存在时不进入
        # 当不存在的时候不需要再次切换ifame
        # 等待并判断 iframe 是否存在
        iframe = WebDriverWait(driver, 0.3).until(
            EC.presence_of_element_located((By.ID, "baxia-dialog-content"))
        )
        logging.info("元素存在，开始滑动")

        driver.switch_to.frame('baxia-dialog-content')

        slider = driver.find_element(By.XPATH, '//*[@id="nc_1_n1z"]')
        sleep(2)
        action = ActionChains(driver)
        action.click_and_hold(on_element=slider).perform()
        action.move_by_offset(xoffset=298, yoffset=0).perform()
        action.pause(2).release().perform()
        driver.switch_to.parent_frame()
        logging.info("滑动结束")
        return True
    except Exception as e:
        # logging.info(e)
        logging.info("元素不存在，不需要滑动")
        return False


def logon(user, driver):
    # 登录脚本
    logging.info("开始登录")
    driver.get('https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fwww.aliyun.com%2Fnotfound%2F')
    sleep(1)
    # 切换进入ifame表单
    driver.switch_to.frame('alibaba-login-box')
    driver.find_element(By.XPATH, '//*[@id="fm-login-id"]').send_keys(user["name"])
    driver.find_element(By.XPATH, '//*[@id="fm-login-password"]').send_keys(user["password"])
    sleep(1)
    x = 0
    if huadong(driver):
        x = 1
    # 点击登录
    driver.find_element(By.XPATH, '//*[@id="login-form"]/div[6]/button').click()
    sleep(1)
    if x == 0:
        # 如果当前登录识别成功过，就不再执行
        huadong(driver)
    driver.switch_to.default_content()
    logging.info("登录成功，执行签到")


def chrome():
    # 浏览器初始化
    # 设置Chrome浏览器的选项--启动无头模式
    chrome_options = Options()
    if (not is_show):
        chrome_options.add_argument('--headless')  # 启用Headless模式
        chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
        chrome_options.add_argument('--no-sandbox')  # 以沙盒模式运行

    # 初始化Chrome浏览器实例
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
                """
    })
    driver.implicitly_wait(2)
    driver.maximize_window()

    # 设置等待时间为10秒
    wait = WebDriverWait(driver, 10)
    return driver, wait


# 每日任务
def sign_in(driver):
    # 签到
    for i, url in enumerate(urls):

        driver.get(url)
        sleep(2)
        # 在第一个url 时做处理
        # if i == 0:
        #     get_cookies(driver)
        # 点击签到
        # print("开始等待")
        # sleep(15800)
        # print("等待结束")

        # 判断是星期5

        logging.info("点击签到,当前第%s个任务" % str(i + 1))
        try:
            if i == 0:
                driver.find_element(By.XPATH,
                                    '//*[@id="J_SignUpButton"]/div/div/div[2]/div[' + str(weekday) + ']').click()
            else:
                driver.find_element(By.XPATH, '//*[@id="sign-box"]/div/div[2]/div[' + str(weekday) + ']').click()
            logging.info("签到成功")
            sleep(2)
        except Exception as e:
            logging.info("已签到，无需签到")


def scene_experience(driver):
    # 场景过于苛刻-去除
    # 场景体验获取积分
    url = 'https://developer.aliyun.com/adc/scenario/410e5b6a852f4b4b88bf74bf4c197a57?spm=a2c6h.13858375.devcloud-scene-list.3.1d594090Zd9Ets'
    driver.get(url)
    sleep(3)
    # 点击立即开始
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[2]/div/div/div/div[4]/button').click()
    sleep(2)
    # 选择公用资源
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/section/article/section/div[2]/div[1]/div[1]/div[4]/div/div[1]/div[1]').click()
    sleep(1)
    # 同意协议-- 默认勾选协议了
    # driver.find_element(By.XPATH,'//*[@id="root"]/div/section/article/section/div[2]/div[1]/div[1]/div[4]/div/div[2]/div/label/span[1]/input').click()
    sleep(0.6)
    # 开始实验
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/section/article/section/div[2]/div[1]/div[1]/div[4]/div/div[2]/button').click()
    # 等待实验开启
    sleep(58)
    print("开始点击")
    driver.find_element(By.XPATH, '//*[@id="exp-btn"]/div/button[2]').click()
    # 关闭实验
    driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[3]/button[1]').click()
    print("实验任务结束")
    # 实验结束后需要新开网页，不然无法跳转
    driver.get("https://developer.aliyun.com/score")
    alert = driver.switch_to.alert
    # 接受弹窗
    alert.accept()
    # 结束


def watch_video(driver):
    # 观看视频
    url = "https://developer.aliyun.com/live/252899?spm=a2c6h.12873587.live-index.9.617f21a0ulcf6f"
    driver.get(url)
    sleep(5)
    try:
        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/div[5]').click()
    except:
        print("没有找到观看视频元素")
    # 等待几秒后再次点击
    sleep(3)
    try:
        e1 = driver.find_elements(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/div[5]/div')
        if len(e1) > 0:
            e1[0].click()
    except:
        print("已经点击过了，不需要点击了")
    sleep(61)


def like_article(driver):
    # 5次点赞文章+ 5次收藏+ 1次分享文章+1次评论 = 20积分
    # 进入推荐阅读页面，随机进行点赞评论等操作
    url = 'https://developer.aliyun.com/indexFeed/?spm=a2c6h.13528211.index-feed.152.129331e2PqJWyl'
    driver.get(url)
    # 获取推荐的文章内容，解析a标签
    # 定义目标div
    div_element = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]')
    # 获取div内的html源码
    div_html = div_element.get_attribute('innerHTML')
    # 解析div内的HTML
    soup = BeautifulSoup(div_html, 'html.parser')
    # 获取所有的a 标签
    a_tags = soup.find_all('a')
    # 提取所有的链接
    links = [a['href'] for a in a_tags]
    # 去重链接，处理链接
    article_list = [item for item in links if item.startswith('/article/')]
    set_li = list(set(article_list))

    sleep(5)
    # 进行5次操作
    for i in range(5):
        random_item = random.sample(set_li, 1)[0]
        # 进入任意的一个链接中
        driver.get('https://developer.aliyun.com' + random_item)
        # 单次移除链接
        set_li.remove(random_item)

        # 点赞
        driver.find_element(By.XPATH, '//*[@id="action-btns"]/div[3]/div[1]').click()
        sleep(0.5)
        # 收藏
        driver.find_element(By.XPATH, '//*[@id="action-btns"]/div[2]/div[1]').click()
        sleep(1)
        # 有关注就点击关注，没有的话就不处理
        e1 = driver.find_elements(By.XPATH, '//*[@id="focus-dialog-mask"]/div/div/div[3]')
        if len(e1) > 0:
            e1[0].click()
        if i == 0:
            # 分享
            driver.find_element(By.XPATH, '//*[@id="action-btns"]/div[6]/div').click()
            sleep(0.3)
            driver.find_element(By.XPATH, '//*[@id="share-dialog-mask"]/div/div/div[1]').click()
            sleep(0.3)
            # 评论
            driver.find_element(By.XPATH, '//*[@id="action-btns"]/div[4]').click()
            # 等待缓冲
            sleep(3)
            # 判断是否进行了实名认证
            e2 = driver.find_elements(By.XPATH, "//a[contains(text(), '实名认证')]")
            if len(e2) > 0:
                print("当前账号没有实名认证哦")
                sleep(5)
                continue
            sleep(2)
            try:
                driver.find_element(By.XPATH, '//*[@id="comment"]/div/div/div[1]/div[2]/textarea').send_keys(
                    random.choice(pinlun))
            except:
                print("当前账号无法评论")
                continue
            print("进入了评论页面")
            sleep(3)
            # 点击评论
            driver.find_element(By.XPATH, '//*[@id="comment"]/div/div/div[1]/div[2]/div/button').click()
            sleep(1)
        logging.info("一键三联完成")
        sleep(2)


def like_answer(driver):
    # 点赞回答
    # 需要判断当前问答是否被点赞过，如果被点赞了，则换下一条，当下一条没有之时就换下一个问答
    pass


def scoring(driver):
    # 电子书打分
    # 循环遍历的进行找电子书，当电子书被评分过则跳过当前，进行评分其他的   可能还需要进行爬虫获取到所有的电子书信息
    # 随机生成数字
    while True:
        random_number = random.randint(1, 7963)
        url = 'https://developer.aliyun.com/ebook/' + str(random_number)

        driver.get(url)
        sleep(1)
        driver.find_element(By.XPATH, '//*[@id="ebook-detail"]/div[2]/div/div[1]/div[1]/div[2]/div[8]/a[2]').click()
        # 切换新窗口
        driver.maximize_window()
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])
        sleep(2)
        # 点击评价
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[1]/div/div[3]/span[1]').click()

        # 判断是否已评价,已评价则不评价
        e1 = driver.find_elements(By.XPATH,
                                  '//*[@id="ebook-view"]/div/div/div/div[1]/div/div[3]/div/div[1]/div/div[3]/button')
        if len(e1) == 0:
            # 没有找到提交按钮，换链接
            continue
        sleep(0.3)
        # 5星好评
        driver.find_element(By.XPATH,
                            '//*[@id="ebook-view"]/div/div/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[1]/span[5]/i').click()
        driver.find_element(By.XPATH,
                            '//*[@id="ebook-view"]/div/div/div/div[1]/div/div[3]/div/div[1]/div/div[3]/button').click()
        break


def publish_article(driver, user):
    # 发布文章
    url = 'https://developer.aliyun.com/article/new?spm=a2c6h.27120161.J_7073166060.4.a5511721nNGoHw#/'
    driver.get(url)
    # 判断是否能够发布文章，当账号无法发布文章时，结束方法
    e1 = driver.find_elements(By.XPATH, '/html/body/div[2]/div[2]/p/a')
    if len(e1) > 0:
        print("当前账号没有实名认证，无法发布文章")
        logging.info("当前账号没有实名认证，无法发布文章")
        return None
    title = None
    summary = None
    content = None
    for i in range(4):
        if title is None or summary is None or content is None:
            # 判空-任意为空- 进入方法进行获取，当没有获取到时，重新加载
            result = article(user, driver)
            if result is None:
                return
            title, summary, content = result
        else:
            print("执行到这里了")
            break
    sleep(1)
    try:
        driver.find_element(By.XPATH, '//*[@id="title"]').send_keys(title)
    except:
        # 若无法写入，则结束
        return
    sleep(1)
    print("获取到了摘要内容", title, summary, content)
    driver.find_element(By.XPATH, '//*[@id="abstractContent"]').send_keys(summary)
    sleep(2)
    driver.find_element(By.XPATH,
                        '//*[@id="publish-article"]/div/form/div[3]/div/div[2]/div/div[2]/div[1]/textarea').send_keys(
        content)
    # 点击发布，随机等待
    wait_time = random.uniform(1, 10)  # 生成0.5~3.0秒之间的浮点数
    sleep(wait_time)

    driver.find_element(By.XPATH, '//*[@id="publish-article"]/div/div[2]/div/div/div/button[2]').click()
    sleep(1)
    # 处理滑块验证码
    slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]')
    sleep(2)
    action = ActionChains(driver)
    action.click_and_hold(on_element=slider).perform()
    action.move_by_offset(xoffset=298, yoffset=0).perform()
    action.pause(2).release().perform()
    driver.switch_to.parent_frame()
    logging.info("滑动结束")
    # 发布文章
    driver.find_element(By.XPATH, '//*[@id="dialog-footer-2"]/span/button[1]').click()
    logging.info("发布文章执行一次完成")

    return 1


# 每日任务--结束

def run(account):
    # 启动浏览器
    driver, wait = chrome()
    # 先登录
    logon(account, driver)

    # 发布文章内容
    if is_wenzhang:
        for i in range(1, 4):
            retuen_jieguo = publish_article(driver, account['name'])
            if retuen_jieguo is None:
                break
            sleep(3)

    # 执行签到
    if weekday == 5:
        # 如果是星期五，则执行俩次脚本
        for i in range(2):
            if is_qiandao:
                sign_in(driver)
    else:
        if is_qiandao:
            sign_in(driver)
    # 观看视频
    if is_guankan:
        watch_video(driver)

    # 场景流程制作
    # scene_experience(driver)

    # 一键3连
    if is_sanlian:
        like_article(driver)

    # 电子书打分
    if bool(data['Database']['is_dianzishu']):
        scoring(driver)

    print("脚本执行结束 ")
    # 进入总页面，统一领取积分
    logging.info("开始一键领取积分,等待时间")
    sleep(buffer_sleep)
    driver.get("https://developer.aliyun.com/score")
    sleep(3)
    logging.info("点击领取")
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '一键领取')]")))
    element.click()
    sleep(4)
    # 清除当前登录信息
    # logging.info("退出登录")
    # driver.delete_all_cookies()
    # 关闭浏览器
    driver.quit()
    logging.info("账号%s执行完成" % account["name"])


async def process_accounts(accounts):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 创建任务列表
        tasks = [executor.submit(run, account) for account in accounts]

        # 等待完成并处理结果
        for future in concurrent.futures.as_completed(tasks):
            await asyncio.wrap_future(future)


async def main():
    # 分组账号
    grouped_accounts = [accounts[i:i + max_run] for i in range(0, len(accounts), max_run)]

    # 循环处理每组账号
    for group in grouped_accounts:
        await process_accounts(group)


# 创建事件循环并运行主程序
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
