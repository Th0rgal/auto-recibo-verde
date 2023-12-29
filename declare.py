from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import traceback
import random
import time
import re

from info import NIF, PASSWORD, DATE, COMPANY_NAME, COMPANY_COUNTRY, INVOICE_DESCRIPTION, AMOUNT

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('disable-infobars')

def login():
    nif_btn = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#content-area > div > div > label:nth-child(4)"))
    )
    nif_btn.click()
    # Wait for the input email field to load
    nif_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Nº de Contribuinte"]'))
    )
    nif_input.send_keys(NIF)
    password_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Senha de acesso"]'))
    )
    password_input.send_keys(PASSWORD)
    login_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#sbmtLogin"))
        )
    login_btn.click()


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://irs.portaldasfinancas.gov.pt/recibos/portal/")
login()
create_btn = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content > div > section > div > div > div:nth-child(1) > div.col-xs-12 > a"))
)
create_btn.click()

invoice_receipt_btn = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content > div > section > div > div:nth-child(1) > div:nth-child(1) > a > h4"))
)
invoice_receipt_btn.click()

tx_date_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content > div > div > emitir-documentos-app-v2 > emitir-documentos-form-v2 > div.code-fixed-header > div.row.margin-top-lg > div > div > div > div.panel-body > div > div.col-md-3.col-xs-12 > lf-date > div > div.input-group.input-group-sm.date > input"))
    )
tx_date_input.send_keys(DATE)

invoice_type_select = Select(WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content > div > div > emitir-documentos-app-v2 > emitir-documentos-form-v2 > div.code-fixed-header > div.row.margin-top-lg > div > div > div > div.panel-body > div > div.col-md-4.col-xs-12 > lf-dropdown > div > select"))
    ))
# Fatura-Recibo Ato Isolado
invoice_type_select.select_by_visible_text("Fatura-Recibo")

emitir_btn = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content > div > div > emitir-documentos-app-v2 > emitir-documentos-form-v2 > div.code-fixed-header > div.row.margin-top-lg > div > div > div > div.panel-body > div > div.col-xs-4.text-right.margin-top > button"))
    )
body_element = driver.find_element(By.TAG_NAME, 'body')
body_element.click()
emitir_btn.click()

# no_btn = WebDriverWait(driver, 15).until(
#         EC.presence_of_element_located((By.XPATH, '//*[@id="decisaoTipoEmissaoAIModal"]/div/div/div[3]/div/button[1]'))
#     )
# time.sleep(1)
# no_btn.click()

country_select = Select(WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content > div > div > emitir-app > emitir-form > div.code-fixed-header > div.row.margin-top-lg > div > dados-adquirente > div > div.panel-body > div:nth-child(1) > div.col-md-3.col-xs-12 > lf-dropdown > div > select"))
    ))
country_select.select_by_visible_text(COMPANY_COUNTRY)


# subsistema_saude_select = Select(WebDriverWait(driver, 15).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content > div > div > emitir-app > emitir-form > div.code-fixed-header > div.row.margin-top-lg > div > dados-adquirente > div > div.panel-body > div:nth-child(4) > div:nth-child(1) > lf-dropdown > div > select"))
# ))
# time.sleep(100)
# subsistema_saude_select.select_by_visible_text("NÃO APLICÁVEL")

company_name_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#main-content > div > div > emitir-app > emitir-form > div.code-fixed-header > div.row.margin-top-lg > div > dados-adquirente > div > div.panel-body > div:nth-child(2) > div > lf-text > div > input'))
    )
company_name_input.send_keys(COMPANY_NAME)

# biens ou services
paiement_type = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#main-content > div > div > emitir-app > emitir-form > div.code-fixed-header > div.row.margin-top-lg > div > dados-transmissao > div > div.panel-body > div.col-md-12 > pf-radio > div > div:nth-child(2) > label > input'))
    )
paiement_type.click()

description_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#main-content > div > div > emitir-app > emitir-form > div.code-fixed-header > div.row.margin-top-lg > div > dados-transmissao > div > div.panel-body > div:nth-child(2) > div > textarea'))
    )
description_input.send_keys(INVOICE_DESCRIPTION)

regime_iva_select = Select(WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#main-content > div > div > emitir-app > emitir-form > div.code-fixed-header > div.row.margin-top-lg > div > dados-transmissao > div > div.panel-body > div:nth-child(6) > div > div:nth-child(1) > lf-dropdown > div > select'))
    ))
regime_iva_select.select_by_visible_text("Regras de localização - art.º 6.º [regras especificas]")

base_incidencia_irs_select = Select(WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#main-content > div > div > emitir-app > emitir-form > div.code-fixed-header > div.row.margin-top-lg > div > dados-transmissao > div > div.panel-body > div:nth-child(7) > div:nth-child(1) > div > lf-dropdown > div > select'))
))
base_incidencia_irs_select.select_by_visible_text("Sem retenção - Não residente sem estabelecimento")

base_amount_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#main-content > div > div > emitir-app > emitir-form > div.code-fixed-header > div.row.margin-top-lg > div > dados-transmissao > div > div.panel-body > div:nth-child(4) > div > div > div > input')
        ))
base_amount_input.send_keys(AMOUNT)

imposto_do_solo = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#main-content > div > div > emitir-app > emitir-form > div.code-fixed-header > div.row.margin-top-lg > div > dados-transmissao > div > div.panel-body > div.row.ng-scope > div > div > div > input')
        ))
imposto_do_solo.send_keys("0,00")

emitir_btn = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div/div/emitir-app/emitir-form/div[1]/div[1]/div[1]/div[1]/div[4]/div/button[1]')
        ))
emitir_btn.click()

# confirm_emitir_btn = WebDriverWait(driver, 15).until(
#         EC.presence_of_element_located((By.XPATH, '//*[@id="emitirModal"]/div/div/div[3]/button[2]')
#         ))
# confirm_emitir_btn.click()


time.sleep(1000)
driver.close()
