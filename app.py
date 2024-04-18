from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen
import logging

logging.basicConfig(filename="scrapper.log", level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def homepage():
    return render_template("index.html")

@app.route("/Product", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/" + searchString
            urlclient = urlopen(url)
            test_page = urlclient.read()
            urlclient.close()
            test_page_html = bs(test_page, 'html.parser')
            bigbox = test_page_html.find_all("div", class_="col-md-4 col-xl-4 col-lg-4")

            filename = searchString + ".csv"
            fw = open(filename, "w", encoding="utf-8")
            headers = "Name,Description,Reviews,Prices\n"
            fw.write(headers)
            product_Detail = []

            for element in bigbox:
                try:
                    name = element.find("a", class_="title").text.strip()
                    print(name)
                except AttributeError as e:
                    name = 'No name'
                    logging.error(f"Error in finding name: {e}")

                try:
                    description = element.find("p", class_="description card-text").text.strip()
                    print(description)
                except AttributeError as e:
                    description = 'No description'
                    logging.error(f"Error in finding description: {e}")

                try:
                    reviews = element.find("p", class_="float-end review-count").text.strip()
                    print(reviews)
                except AttributeError as e:
                    reviews = 'No reviews'
                    logging.error(f"Error in finding reviews: {e}")

                try:
                    prices = element.find("h4", class_="float-end price card-title pull-right").text.strip()
                    print(prices)
                except AttributeError as e:
                    prices = 'No prices'
                    logging.error(f"Error in finding prices: {e}")

                product_Detail.append({
                    #"Product": searchString,
                    "Name": name,
                    "Description": description,
                    "Reviews": reviews,
                    "Prices": prices
                })

                fw.write(f"{name},{description},{reviews},{prices}\n")

            fw.close()
            logging.info("Logged to CSV: {}".format(product_Detail))
            return render_template('result.html', ProductDetail=product_Detail)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return 'Something went wrong. Please check the logs.'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
