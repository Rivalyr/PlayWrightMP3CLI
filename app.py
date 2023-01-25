from playwright.async_api import async_playwright
import requests
import asyncio
import time
import os


async def run(playwright):
    global songnamefinal
    os.system('cls')
    # or "firefox" or "webkit".
    chromium = playwright.chromium
    browser = await chromium.launch()

    # create a new incognito. El contexto va antes de la pagina
    context = await browser.new_context(is_mobile=False)
    page = await browser.new_page(accept_downloads=True)

    await page.set_viewport_size({'width': 1920, 'height': 1080})
    await page.goto('https://getn.topsandtees.space/')
    namesong = input(str('Youtube link or song name please :D\n here: '))
    songnameinput = page.locator('//input[@placeholder="Enter YouTube url or search phrase"]')
    time.sleep(0.500)
    # Envia un click, envia un texto y presiona enter
    await songnameinput.click()
    await page.keyboard.insert_text(f'{namesong}')
    await page.keyboard.press('Enter')
    await asyncio.sleep(1)

    # Espera que la página cargue, le da al boton de descarga y espera
    await page.wait_for_selector('//div[@class="container"]//div[1]//div[1]//div[1]//a[1]', timeout=20000)
    dwnbtn = page.locator('//div[@class="container"]//div[1]//div[1]//div[1]//a[1]')
    await dwnbtn.click()
    dwnbtn_final = await page.wait_for_selector('//span[@class="search-item__download dl_progress_finished btn_clck_spec"]', timeout=12000)
    url = await dwnbtn_final.get_attribute('data-href')

    # Busca el h1, consigue el txt y por ultimo agrega .mp3 al nombre para tener el nombre del archivo
    songname1 = page.locator('h1'); songname2 = await songname1.inner_text()
    songname3 = songname2 + ".mp3"

    # el mismo script anterior para solucionar el problema de compatibilidad con algunos nombres de canciones
    songname = songname3
    char_i = ["\\", "/", "|", "-", ":", "*", "?", "\"", "<", ">"]

    for char in char_i:
        if char in songname:
            songnamefinal = songname.replace(char, '-')
            print(songname)
            break
    await page.screenshot(path='Foto.png')
    await browser.close()

    r = requests.get(url)
    with open(songnamefinal, "wb") as f:
        f.write(r.content)
    print('Cancion descargada con exito')


async def main():
    # Tambien se puede hacer esto en una variable pero aqui se hace mas controlado ya que simplemente
    # tengo que invocar la funcion
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == "__main__":
    # asyncio.run(main())
    asyncio.get_event_loop().run_until_complete(main())
