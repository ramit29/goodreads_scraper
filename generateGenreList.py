import requests
import pandas as pd
import requests
from bs4 import BeautifulSoup
import argparse



def generate_booklist(genre):
    print(genre)
    url = "https://www.goodreads.com/shelf/show/{}".format(genre)
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")
    #print(soup.prettify())
    total_items_info = soup.find("div", class_="mediumText").get_text().strip()
    print(total_items_info)
    total_items = 100
    items_per_page = 50  # Adjust this based on the actual number of items per page
    total_pages = (total_items + items_per_page - 1) // items_per_page
    max_pages_to_scrape = 3

    title = []
    url_list = []
    authors = []
    avg_ratings = []
    rating = []
    year = []
    number = []
    href = []


    for page in range(1, min(max_pages_to_scrape, total_pages) + 1):
        # Construct the URL for the current page
        url = '{}?page={}'.format(url,page)
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        book_elements = soup.find_all("div", "elementList")

        # Iterate through each book element on the current page
        for book_element in book_elements:
            # Use try-except blocks to handle potential errors if elements are missing
            try:
                # Extract book details
                book_title = book_element.find("a", "bookTitle").text
                book_href = book_element.find("a", "bookTitle").get("href")
                book_url = "https://www.goodreads.com" + book_href
                num_title = book_href.split('/')[-1]
                book_number = book_href.split('/')[-1].split('-')[0]
                author = book_element.find("a", "authorName").text
                rating_text = book_element.find("span", "greyText smallText").text.split()
                avg_rating = rating_text[2]
                ratings = rating_text[4]
                published_year = rating_text[-1] if len(rating_text) == 9 else ""

                # Append the extracted data to their respective lists
                title.append(book_title)
                url_list.append(book_url)
                authors.append(author)
                avg_ratings.append(avg_rating)
                rating.append(ratings)
                number.append(book_number)
                href.append(num_title)
            except AttributeError:
                # Handle the case where an element is not found
                print(f"Skipping a book on page {page} due to missing data.")

    good_reads = pd.DataFrame({
        "Title": title,
        "URL": url_list,
        "ID" : href,
        "Number" : number,
        "Authors": authors,
        "Avg Ratings": avg_ratings,
        "Rating": rating
    })

    return good_reads


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--genre', type=str)
    parser.add_argument('--output_dir', type=str)

    args = parser.parse_args()

    genre = args.genre
    output = args.output_dir
    booklist = generate_booklist(genre)
    print(booklist)
    booklist.to_csv('{}/{}.csv'.format(output,genre))

if __name__ == '__main__':
    main()
