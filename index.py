from flask import Flask, request, jsonify
from selenium import webdriver
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def scrape_me(url):
    # Set up Selenium webdriver
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
    # options.add_argument('--disable-gpu')  # Disable GPU acceleration (not needed in headless mode but recommended)
    driver = webdriver.Chrome(options=options)
    # URL of the webpage to scrape

    # Open the webpage
    driver.get(url)

    # Wait for the page to load
    time.sleep(4)

    try:
        # Find all div elements with class name "elfjS"
        div_elements = driver.find_elements(By.XPATH, "//div[@class='elfjS']")

        # Extract the text from each div element
        text_list = [element.text for element in div_elements]


        # Close the webdriver
        driver.quit()

        return text_list
    except Exception as e:
        # Close the webdriver in case of exception
        driver.quit()
        raise e



def scrape_data(url):
    try:
        # Set up WebDriver
        
        answer = scrape_me(url)
        print(answer)

        return {"title": answer}
    except Exception as e:
        return {'error': str(e)}


@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required in JSON format'}), 400

    url = data['url']

    result = scrape_data(url)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')#(debug=False,host='0.0.0.0')
