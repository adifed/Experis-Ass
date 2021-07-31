from bs4 import BeautifulSoup
import requests

import re


def find_movie_name(bs):
    titleName = bs.find("h1", {'class': re.compile('TitleHeader*')})
    if titleName is None:  # in case of null
        name = ""
    else:
        name = titleName.contents[0].replace(u'\xa0', u'')
    return name


def find_genre(bs):
    info = ""
    genre = bs.find_all('li', class_="ipc-metadata-list__item")
    for li in genre:
        lable = li.find('span', class_="ipc-metadata-list-item__label")
        if lable != None:
            content = li.find('div')

            if lable.get_text() == "Genres":
                info = info + content.get_text(',')
            #  print(f"{lable.get_text()} : {content.get_text(',')}")
    return info


def find_directors(bs):
    names = ""
    directors = bs.find("div", {'class': re.compile('ipc-metadata-list*')})
    for director in directors.contents[0]:
        names = director.getText(",") + names
        # print(director.getText() + " ")
    return names


def find_actors(bs):
    names = ""
    all_cast = bs.find_all('section', {"data-testid": "title-cast"})
    if len(all_cast) == 0:
        return names
    cast = all_cast[0]

    all_items = cast.find_all('div', {"data-testid": "title-cast-item"})
    for item in all_items:
        data = item.get_text("#$#")
        names = names + "," + data.split("#$#")[0]

    names = names[1:]

    return names


def find_info(bs):
    rating = bs.find("div", {'class': re.compile('TitleBlock*')}).find_all('li')
    str = ""
    for r in rating:
        if r != None:
            str = str + "|" + r.getText()

    index = str[1:].find('|')
    str = str[index + 2:]
    if str.isdigit():
        str = ""
    return str


if __name__ == '__main__':

    f = open("output.txt", "a+", encoding="utf8")
    index = 0
    user_input = input("Enter something:\n> ")  # The user enters a title
    search_terms = user_input.split()
    url = "http://www.imdb.com/find?q=" + '+'.join(search_terms) + '&s=tt' + '&ttype=ft'  # tt for titles
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a.attrs.get('href') for a in soup.select('td.result_text a')]  # links is array of  all the movies(tv..)

    for link in links:  # Loop for each movie
        search_terms = link.split()
        url2 = "http://www.imdb.com/" + '+'.join(search_terms)  # The url of specific movie
        response2 = requests.get(url2)
        soup2 = BeautifulSoup(response2.text, 'html.parser')

        movie_name = find_movie_name(soup2)
        directors_names = find_directors(soup2)
        genre_info = find_genre(soup2)
        info = find_info(soup2)
        actors = find_actors(soup2)

        if movie_name.lower().find(user_input.lower()) != -1:
            s = movie_name + "|" + genre_info + "|" + info + "|" + directors_names + "|" + actors + "\n"
            f.write(s)
            print(s)

    f.close()
