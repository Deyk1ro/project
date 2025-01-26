import requests
from bs4 import BeautifulSoup
import json
from time import sleep

headers = {
        "accept": "* / *",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.97 Safari/537.36"
    }
film_list = []

def get_url(count):
    
    while True:
        url = f"https://rezka.ag/page/{count}/?filter=last"

        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            break

        soup = BeautifulSoup(response.text, "html.parser")


        contents = soup.find_all("div", class_="b-content__inline_item")

        for film_count in contents:
            films_url = film_count.find("a").get("href")
            
            sleep(0.1)
            
            try:
                print("-"*100)
                
                print(f"Url: {films_url}")

                response = requests.get(films_url, headers=headers)

                soup = BeautifulSoup(response.text, "html.parser")


                contents = soup.find("div", class_="b-content__main")
                
                img_url = contents.find("img").get("src")
                print(f"Image: {img_url}")

                name = contents.find("h1").text.strip()
                print(f"Name: {name}")

                release_date = soup.find_all("tr")
                
                for date in release_date:
                    try:
                        label = date.find("td", class_="l")
                        date_text = None
                        if label and "Дата выхода" in label.text:

                            date_cell = label.find_next_sibling("td")

                            if date_cell:
                                date_text = date_cell.text.strip().split("\n")[0].strip()


                                print(f"Release date: {date_text}")
        
                    except Exception as e:
                        print(f"Error processing line: {e}")
                

                gradings_imdb = contents.find("span", class_="b-post__info_rates imdb")
                grade_imdb = None
                if gradings_imdb:
                    grade_imdb = gradings_imdb.find("span").text.strip()if gradings_imdb.find("span") else "Grade not found"

                gradings_kp = contents.find("span", class_="b-post__info_rates kp")
                grade_kp = None
                if gradings_kp:
                    grade_kp = gradings_kp.find("span").text.strip()if gradings_kp.find("span") else "Grade not found"
                
                print(f"Grades IMDB: {grade_imdb} | Grades KP: {grade_kp}")

                genres = soup.find_all("span", itemprop="genre")

                genre_list = [genre.text.strip() for genre in genres]
                print(f"Genres: {genre_list}")

                timing = soup.find("td", itemprop="duration").text.strip()
                print (f"Timing: {timing}")

                discriptions = contents.find("div", class_="b-post__description_text").text.strip()
                print(f"Discriptions: {discriptions}") 
                
                film_list.append({
                    "Name": name,
                    "Release date": date_text,
                    "Grade IMDB": grade_imdb, "Grade KP": grade_kp, 
                    "Genres": genre_list,
                    "Timing": timing,
                    "Discriptions": discriptions,
                    "Film_url": films_url,
                    "Image": img_url 
                })

            except Exception as ex:
                print(f"Processing error films: {ex}")
        count += 1

def main():
    get_url(0)
if __name__ == "__main__":
    main()

output_file = "hdrezka_films.json"
try:
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(film_list, file, ensure_ascii=False, indent=4)
    print(f"The data is saved to a file: {output_file}")
except Exception as ef:
    print(f"Error writing file: {ef}")