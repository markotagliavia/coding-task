import json
from flask import Flask, jsonify, request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import requests
from selenium import webdriver
  
app = Flask(__name__)

def get_prices(aurora_tokens) :
    return look_up_prices([element["id"] for element in aurora_tokens]);

def look_up_prices(id_array) :
  prices = {}
  s = requests.Session()
  for id_chunk in id_array :   
    res = s.get('https://api.coingecko.com/api/v3/simple/price?ids=' + id_chunk + '&vs_currencies=usd')
    data = res.json()
    if data[id_chunk]["usd"] :
        prices[id_chunk] = data[id_chunk]["usd"];

  return prices

  
@app.route('/hello', methods=['GET'])
def helloworld():
    if(request.method == 'GET'):
        data = {"data": "Hello World"}
        return jsonify(data)

@app.route('/prices', methods=['GET'])
def prices():
    if(request.method == 'GET'): 
        aurora_tokens = [
            { "id": "weth", "symbol": "WETH", "contract": "0xC9BdeEd33CD01541e1eeD10f90519d2C06Fe3feB"},
            { "id": "wrapped-near", "symbol": "WNEAR", "contract": "0xC42C30aC6Cc15faC9bD938618BcaA1a1FaE8501d"},
            { "id": "polaris-token", "symbol": "PLRS", "contract": "0xD93d770C123a419D4c48206F201Ed755dEa3037B"},
            { "id": "terra-luna", "symbol": "LUNA", "contract": "0xC4bdd27c33ec7daa6fcfd8532ddB524Bf4038096"},
            { "id": "frax", "symbol": "FRAX", "contract": "0xDA2585430fEf327aD8ee44Af8F1f989a2A91A3d2"},
            { "id": "rose", "symbol": "ROSE", "contract": "0xdcd6d4e2b3e1d1e1e6fa8c21c8a323dcbecff970"},
            { "id": "nearpad", "symbol": "PAD", "contract": "0x885f8CF6E45bdd3fdcDc644efdcd0AC93880c781"},
            { "id": "usd-coin", "symbol": "USDC", "contract": "0xb12bfca5a55806aaf64e99521918a4bf0fc40802"},
            { "id": "dai", "symbol": "DAI", "contract": "0xe3520349f477a5f6eb06107066048508498a291b"},
            { "id": "dai", "symbol": "DAI", "contract": "0x53810e4c71bc89d39df76754c069680b26b20c3d"},
            { "id": "terrausd", "symbol": "UST", "contract": "0x5ce9F0B6AFb36135b5ddBF11705cEB65E634A9dC"},
            { "id": "mimatic", "symbol": "MIMATIC", "contract": "0xdFA46478F9e5EA86d57387849598dbFB2e964b02"},
            { "id": "mimatic", "symbol": "MIMATIC", "contract": "0xdFA46478F9e5EA86d57387849598dbFB2e964b02"}
        ];
        prices = get_prices(aurora_tokens);
        data = {"data": prices}
        return jsonify(data)       

@app.route('/apr', methods=['GET'])
def apr():
    if(request.method == 'GET'):

        driver_path = "./chromedriver.exe"
        packed_meta_mask_extension_path = './10.13.0_0.crx'
        connect_wallet_text = '[CONNECT WALLET]'
        pool_link_text = '[NEAR]-[WETH] Uni LP'
        log_text = 'log'
        apr_text = 'APR: '
        timeout_interval = 120

        url = "https://vfat.tools/aurora/auroraswap/"
        options = webdriver.ChromeOptions()
        options.add_extension(packed_meta_mask_extension_path) 
        driver = webdriver.Chrome(driver_path, options=options)
        driver.get(url)
        connect_button = driver.find_element_by_link_text(connect_wallet_text)
        connect_button.click()
        
        #Waiting interval for MetaMask wallet to connect.
        WebDriverWait(driver, timeout_interval).until(EC.visibility_of_element_located((By.LINK_TEXT, pool_link_text)))
        
        log_element = driver.find_element_by_id(log_text)
        lines = log_element.text.splitlines()
        cnt = 0
        for line in lines:
            if line.startswith(apr_text):
                cnt = cnt + 1
                if cnt == 2:
                    return line
                    #For just yearly percent -> 
                    # return line[line.find('Yearly'):]

        return ''

if __name__ == '__main__':
    app.run(debug=True)