import requests
from bs4 import BeautifulSoup
import json
from time import sleep

headers = {
        "accept": "* / *",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.97 Safari/537.36"
    }

books = []

def get_url(count):

    while True:
        url = f"https://books.toscrape.com/catalogue/page-{count}.html"
    
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            break
       
        soup = BeautifulSoup(response.text, "html.parser")

        data = soup.find_all("article", class_="product_pod")

        for gen_books_url in data:
            book_url = f"https://books.toscrape.com/catalogue/{gen_books_url.find("a").get("href")}"
            sleep(0.1)
            try:
                print("-"* 80)

                print(f"URL: {book_url}")

                response = requests.get(book_url, headers=headers)
                soup = BeautifulSoup(response.text, "html.parser")

                data = soup.find("div", class_="container-fluid page")
                
                img_url = f"https://books.toscrape.com/catalogue{data.find("img").get("src")}"
                print(f"Image: {img_url}")
                
                name = data.find("h1").text
                print(f"name: {name}")
                
                price = data.find("p", class_="price_color").text.strip()
                pricing = price.replace("Â", "")
                print(f"Pricing: {pricing}")
                
                stocks = data.find("p", class_="instock availability").text.strip()
                print(f"stocks: {stocks}")

                descriptions_header = data.find("div", id="product_description")
                book_descript = descriptions_header.find_next("p").text.strip()
                descr_replace = book_descript.replace("â", "")
                print(f"Descriptions: {descr_replace}")

                books.append({
                        "Name": name,
                        "Link": book_url,
                        "Image": img_url,
                        "Price": pricing,
                        "Stock": stocks,
                        "Description": descr_replace
                    })
            except Exception as ex:
                print(f"Помилка в обробці книги: {ex}")
        count += 1 

def main():
    get_url(1)
if __name__ == "__main__":
    main()

output_file = "books.json"

try:
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(books, file, ensure_ascii=False, indent=4)  
    print(f"Дані збережено в файл {output_file}") 
except Exception as e:
    print(f"Помилка запису файлу: {e}") 