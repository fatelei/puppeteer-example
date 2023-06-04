import asyncio
from pyppeteer import launch


async def handle_response(response):
    if response.url == "https://m.jf.10086.cn/cmcc-h5-shop/ware/detailPage":
        data = await response.json()
        print(data)


async def intercept_request():
    browser = await launch(headless=True,
                           handleSIGINT=False,
                           handleSIGTERM=False,
                           handleSIGHUP=False,
                           args=[
                               '--disable-gpu',
                               '--disable-dev-shm-usage',
                               '--disable-setuid-sandbox',
                               '--no-first-run',
                               '--no-sandbox',
                               '--no-zygote',
                               '--deterministic-fetch',
                               '--disable-features=IsolateOrigins',
                               '--disable-site-isolation-trials'])
    page = await browser.newPage()
    # await page.setRequestInterception(True)
    page.on("response", lambda response: asyncio.ensure_future(handle_response(response)))
    await page.goto(
        "https://m.jf.10086.cn/#/modules/pages/goodsDetail/goodsDetail?skuWareCode=11538956&groupId=&shareLocation=03&shareUserId=",
        waitUntil=["networkidle2"])
    await browser.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(intercept_request())
