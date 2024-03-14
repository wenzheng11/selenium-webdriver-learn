const { Builder, By, Key, until, Origin, ActionSequence, Button } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const path = require('path');
const configObj = require('./config.js');
const { Database } = configObj;

const { accounts, is_wenzhang, is_qiandao, db_qiandao, buffer_sleep } = Database;

// 创建一个新的Date对象，它代表当前的日期和时间  
const today = new Date();

// 使用getDay()方法获取今天的星期几（0-6）  
const dayOfWeek = today.getDay();

// 创建一个数组，包含星期几的字符串表示  
const weekdays = ['7', '1', '2', '3', '4', '5', '6'];

// 根据getDay()方法返回的数字，从数组中获取对应的星期几字符串  
const weekday = weekdays[dayOfWeek];

// 遍历的URL
const urls = [
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

function sleep(driver, s) {
    if (driver && typeof driver === 'object') {
        return driver.sleep((s || 0) * 1000);
    }
    return new Promise(resolve => setTimeout(resolve, (s || 0) * 1000));
}

function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
}

async function huadong(driver) {
    return new Promise(async function (resolve) {
        // 滑动方法-当前可以弃用
        // 当某次循环点击过时，后续的应该不在点击了
        try {
            // 应该判断是否有ifame，存在ifame时才点击，不存在时不进入
            // 当不存在的时候不需要再次切换ifame
            // 等待并判断 iframe 是否存在
            // 等待直到某个元素加载完成  
            let iframe = await driver.wait(until.elementLocated(By.id('baxia-dialog-content')), 300);

            console.info("元素存在，开始滑动")

            await driver.switchTo().frame('baxia-dialog-content')
            const track = await driver.findElement(By.xpath('//*[@id="nc_1_wrapper"]'))
            const slider = await driver.findElement(By.xpath('//*[@id="nc_1_n1z"]'))
            // 计算滑动的距离（这通常需要根据实际情况来确定）  
            let trackWidth = await track.getRect().then(size => size.width);
            let sliderWidth = await slider.getRect().then(size => size.width);
            let moveDistance = trackWidth - sliderWidth; // 假设需要滑动到最右边  
            await sleep(driver, 2)

            let action = driver.actions({ bridge: true });
            // let action = new ActionSequence(driver, { bridge: true });
            // 按住鼠标左键  这个方法包含2个操作，首先将光标移动到被操作元素的正中心，然后按下鼠标左键不松开。 这对于聚焦一个特殊元素很有用：
            await action.move({ origin: slider }).press().perform();
            // 执行滑动操作（这里使用了一个简化的方法，实际情况可能需要更复杂的逻辑） 滑块验证通常会有各种反自动化机制  
            //   await driver.executeScript(`  
            //   arguments[0].style.transform = 'translateX(' + arguments[1] + 'px)';  
            //   arguments[0].dispatchEvent(new Event('change')); // 触发滑动结束事件，这取决于具体的实现方式  
            // `, slider, moveDistance);

            // 从当前光标位置（原点）偏移
            // 这个方法是指光标位于当前位置（原点），然后通过偏移量进行光标相对原点的偏移。 如果之前没有移动过光标位置，则这个位置是视窗左上角（原点）。 注意当页面发生滚动后光标位置不会发生变化。
            // 注意第一个参数指定为正数时向右移动，第二个参数指定为正数时向下移动。所以 moveByOffset(298, 0) 是指从当前光标位置向右移动298个像素位置和向上移动0个像素位置。
            // .perform(); // 执行动作链
            await action.move({ x: moveDistance, y: 0, origin: Origin.POINTER }).perform()
            await action.pause(2).release(Button.FORWARD).perform()
            // 切换回父框架  
            await driver.switchTo().parentFrame()
            console.info("滑动结束")
            resolve(true)
        } catch (error) {
            console.log(error, 'error')
            console.info("元素不存在，不需要滑动")
            resolve(false)
        }
    })

}

async function login(user, driver) {
    return new Promise(async function (resolve) {
        console.log("开始登录");
        // 导航到目标网页  
        await driver.get('https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fwww.aliyun.com%2Fnotfound%2F');
        await sleep(driver, 1);
        // 切换进入ifame表单
        await driver.switchTo().frame('alibaba-login-box')
        // // 等待元素加载（可选，取决于元素是否动态加载）  
        // await driver.wait(async function () {
        // })
        //  List<WebElement> listOfElements = driver.findElements(By.xpath("//div"));
        const element = await driver.findElement(By.id('fm-login-id'))
        // sendKeys(...keys: string[]): 模拟在元素上键入一系列键。这通常用于在输入框中填写文本。
        await element.sendKeys(user.name, Key.RETURN)
        await driver.findElement(By.xpath('//*[@id="fm-login-password"]')).sendKeys(user.password);
        await sleep(driver, 1);
        // 点击登录
        await driver.findElement(By.xpath('//*[@id="login-form"]/div[6]/button')).click();
        await sleep(driver, 1)
        const isTrue = await huadong(driver)
        if(isTrue) {
            await sleep(driver, 1)
            await driver.findElement(By.xpath('//*[@id="login-form"]/div[6]/button')).click();
        }
        await sleep(driver, 1)
        await driver.switchTo().defaultContent()
        console.info("登录成功，执行签到")
        resolve();

    })
}

// 验证码滑动
async function yzmhuadong(driver) {
    return new Promise(async function (resolve) {
        try {
            const captchaInput = await driver.findElements(By.id('nc_1_nocaptcha')); // 验证码输入框有一个特定的ID 
            // const isDisplayed = await captchaInput.isDisplayed();
            if (captchaInput.length) {  
                console.info("验证码滑块元素存在，开始滑动")
                // await driver.switchTo().frame('baxia-dialog-content')
                const track = await driver.findElement(By.xpath('//*[@id="nc_1_wrapper"]'))
                const slider = await driver.findElement(By.xpath('//*[@id="nc_1_n1z"]'))
                // 计算滑动的距离（这通常需要根据实际情况来确定）  
                let trackWidth = await track.getRect().then(size => size.width);
                let sliderWidth = await slider.getRect().then(size => size.width);
                let moveDistance = trackWidth - sliderWidth; // 假设需要滑动到最右边  
                await sleep(driver, 2)
    
                let action = driver.actions({ bridge: true });
                // let action = new ActionSequence(driver, { bridge: true });
                // 按住鼠标左键  这个方法包含2个操作，首先将光标移动到被操作元素的正中心，然后按下鼠标左键不松开。 这对于聚焦一个特殊元素很有用：
                await action.move({ origin: slider }).press().perform();
                // 从当前光标位置（原点）偏移
                // 这个方法是指光标位于当前位置（原点），然后通过偏移量进行光标相对原点的偏移。 如果之前没有移动过光标位置，则这个位置是视窗左上角（原点）。 注意当页面发生滚动后光标位置不会发生变化。
                // 注意第一个参数指定为正数时向右移动，第二个参数指定为正数时向下移动。所以 moveByOffset(298, 0) 是指从当前光标位置向右移动298个像素位置和向上移动0个像素位置。
                // .perform(); // 执行动作链
                await action.move({ x: moveDistance, y: 0, origin: Origin.POINTER }).perform()
                await action.pause(2).release(Button.FORWARD).perform()
                console.info("滑动结束")

                // 等待元素加载  
                const errorEl = await driver.wait(function() {  
                    return  driver.findElement(By.xpath('//*[@id="nc_1_refresh1"]')); 
                }, 5000); // 等待时间，例如 5000 毫秒  

                if (captchaInput.isDisplayed()) {
                    // 获取元素的文本内容  
                    element.getText().then(async function(text) {  
                        if (text.includes('请刷新页面重试(error:')) {  
                            console.log(text);  
                            // 刷新当前页面  
                            await driver.navigate().refresh();
                            const isResolve = await yzmhuadong();
                            if(isResolve) {
                                resolve(true)
                            }
                        } else {  
                            resolve(true)
                        }  
                    });
                }else {
                    resolve(true)
                }
                // // 切换回父框架  
                // await driver.switchTo().parentFrame()
            } else {  
                console.log('未出现验证码拦截');  
                resolve(true)
            }

            // 使用 WebDriver 的等待机制（如 WebDriverWait），等待验证码元素出现。如果在设定的超时时间内元素出现了，则可以判断为出现了验证码拦截。
            // var wait = new webdriver.promise.ControlFlow().wait;  
            // var captchaInput = wait(driver.findElement(By.id('captchaInputId')), 5000); // 等待5秒  
            // if (captchaInput) {  
            //     console.log('出现验证码拦截');  
            // } else {  
            //     console.log('未出现验证码拦截');  
            // }
        } catch (error) {
            console.log(error, 'error')
            console.info("元素不存在，不需要滑动")
            resolve(true)
        }
    })

}

// 每日任务
async function sign_in(driver, account) {
    return new Promise(async function (resolve) {
        // 签到
        for (const i in urls) {
            if (Object.hasOwnProperty.call(urls, i)) {
                const url = urls[i];
                await driver.get(url);
                await sleep(driver, 2);
                /**
                 * # 在第一个url 时做处理
                  # if i == 0:
                  #     get_cookies(driver)
                  # 点击签到
                  # print("开始等待")
                  # sleep(driver,15800)
                  # print("等待结束")
                 */
                console.info(`${account.name}：每日任务,点击签到,当前第${Number(i) + 1}个任务`);
                // 校验是否出了验证码
                await yzmhuadong(driver);
                try {
                    let el = null;
                    if (i == 0) {
                        el = await driver.findElement(By.xpath('//*[@id="J_SignUpButton"]/div/div/div[2]/div[' + weekday + ']'));
                    } else {
                        el = await driver.findElement(By.xpath('//*[@id="sign-box"]/div/div[2]/div[' + weekday + ']'));
                    }
                    const text = await el.getText();
                    if(text.includes('已打卡') || text.includes('已签到')) {
                        console.info("已签到成功")
                    }else {
                        await el.click();
                        await sleep(2);
                        // 尝试查找包含特定文本的元素  
                        const isExit = await driver.findElements(By.xpath('//*[contains(text(), "打卡成功")]'));
                        if(isExit) {
                            console.info("签到成功")
                        }else {
                            // 校验是否出了验证码
                            await yzmhuadong(driver);
                            if (i == 0) {
                                await el.click();
                            } else {
                                await el.click();
                            } 
                        }
                    }
                    
                } catch (error) {
                    console.info(error)
                    // 校验是否出了验证码
                    await yzmhuadong(driver);
                    if (i == 0) {
                        const el = await driver.findElement(By.xpath('//*[@id="J_SignUpButton"]/div/div/div[2]/div[' + weekday + ']'));
                        // 判断元素是否可以点击
                        await el.click();
                    } else {
                        const el = await driver.findElement(By.xpath('//*[@id="sign-box"]/div/div[2]/div[' + weekday + ']'));
                        await el.click();
                    }
                }
            }
        }
        resolve();
    })

}

async function qiandao(driver, num, account) {
    for (const key in new Array(num || 1).fill('1')) {
        await sign_in(driver, account)
    }
}

async function runFirstScript(account) {
    return new Promise(async function (resolve) {
        const options = new chrome.Options();
        options.addArguments('--window-size=1280,1696'); // 设置窗口大小（可选）  
        options.addArguments('--disable-gpu'); // 在无头模式下禁用GPU加速（对于某些系统可能需要）  
        options.addArguments('--no-sandbox'); // 禁用沙盒模式（在某些环境中可能需要）  
        options.addArguments('--disable-blink-features=AutomationControlled'); // 在启动Chrome浏览器时，可以使用--disable-blink-features=AutomationControlled标志来禁用navigator.webdriver属性的设置。这可以在一定程度上隐藏WebDriver的使用，但请注意，这并非完美的解决方案，因为有些网站可能有其他方法来检测自动化工具。
        // 创建 WebDriver 实例  
        const driver = new Builder().forBrowser('chrome')
            .setChromeOptions(options)
            .build();

        // 执行一段 JavaScript 代码来获取 ChromeDriver 的版本  
        const version = await driver.executeScript(() => {
            return navigator.webdriver; // 这将返回一个包含 ChromeDriver 信息的对象  
        });

        // 打印 ChromeDriver 的版本  
        console.log('ChromeDriver version:', version.version);

        // 设置隐式等待时间为 10 秒  
        await driver.manage().setTimeouts({ implicit: 10000 });

        // 最大化浏览器窗口  
        await driver.manage().window().maximize();

        try {
            // 设置隐式等待时间（以毫秒为单位）    
            // await driver.manage().timeouts().implicitlyWait(2000); // 2000毫秒等于2秒 
            await sleep(null, 2);
            // 先登录
            await login(account, driver);

            if (is_qiandao) {
                await qiandao(driver, db_qiandao ? 2 : weekday == 5 ? 2 : 1, account);
            }
            await sleep(driver, 4)

            console.info("开始一键领取积分,等待时间")
            await sleep(driver, buffer_sleep)
            driver.get("https://developer.aliyun.com/score")
            await sleep(driver, 3)
            console.info("点击领取")
            const element = await driver.wait(until.elementLocated(By.xpath("//*[contains(text(), '一键领取')]")), 300);
            if (element) {
                await driver.findElement(By.xpath("//*[contains(text(), '一键领取')]")).click();
            }
            await sleep(driver, 4)
            console.info("账号%s执行完成" % account["name"])
            if (driver) {
                await driver.quit();
            }
            resolve();
        } catch (error) {
            if (driver) {
                await driver.quit();
            }
            console.log(error, 'error');
            resolve();
        }
    })

}

async function process_accounts(arr) {
    return new Promise(async function (resolve) {
        for (const key in arr) {
            if (Object.hasOwnProperty.call(arr, key)) {
                const element = arr[key];
                await runFirstScript(element);
            }
        }
        resolve();
    })
}


async function main() {
    try {
        //分组账号
        const grouped_accounts = accounts
        //  [accounts[i:i + max_run] for i in range(0, len(accounts), max_run)]

        // 循环处理每组账号
        for (const group in grouped_accounts) {
            if (Object.hasOwnProperty.call(grouped_accounts, group)) {
                // await sleep(null, 10);
                const element = grouped_accounts[group];
                await process_accounts([element])
            }
        }
    } catch (error) {
        console.error(error);
    }
}

main();