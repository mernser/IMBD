# 1. Необходимо пробежаться по странице https://www.imdb.com/calendar/
# 2. Собрать список фильмов и для каждого фильма собрать список актеров.
# 3. Построить плот с частотой участия актеров по годам.

import requests
from bs4 import BeautifulSoup
import json
import re
import matplotlib.pyplot as plt

# Cобираем список фильмов

url = 'https://www.imdb.com/calendar/'
r = requests.get(url)
soup = BeautifulSoup(r.text, features="html.parser")

# Делаем ссылки на фильмы
tables = soup.find('div', {'id': 'main'})
links = []
for tag in tables.find_all("a"):
    links.append("https://www.imdb.com/" + tag['href'])

# Список фильмов с датами
movies = []
for tag in tables.find_all("li"):
    movies.append(tag.text.strip())

# Список фильмов по годам
years = []
for i in movies:
    years.append(int(re.findall("\d\d\d\d", i)[-1]))
years = set(years)
movies_years = {}
for i in years:
    movies_years.setdefault(i, [])

for i in movies:
    movies_years[int(re.findall("\d\d\d\d", i)[-1])].append(i)


# Делаем список актеров в привязке к году съемок (займет около 60 секунд)

actors = {}
for i, k in zip(links, movies):
    page = requests.get(i)
    soup = BeautifulSoup(page.text, features="html.parser")

    actors_in_movie = json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))

    for i in actors_in_movie["actor"]:
        if i["name"] not in actors:
            actors.setdefault(i["name"], [])
        actors[i["name"]].append(int(re.findall("\d\d\d\d", k)[-1]))

# for key, value in actors.items():
#     print(key + ':', value, end='\n')

new = list(actors.values())
years = list(movies_years)
freq = []
for i in years:
    counter = 0
    for c in new:
        if i in c:
            counter += c.count(i)
    freq.append(counter)

# Построить плот с частотой участия актеров по годам.

plt.ylabel('число актеров')
plt.xlabel('год')
plt.plot(years, freq)
plt.scatter(years, freq)
plt.show()

# Дополонительные материалы:
# Список актеров для ускоренного дебага
# actors = {"Alexa PenaVega": [2020],
#           "Raven-Symoné": [2020],
#           "Carlos PenaVega": [2020],
#           "Janel Parrish": [2020],
#           "Bella Thorne": [2020],
#           "Jake Manley": [2020],
#           "Marisa Coughlan": [2020],
#           "Amber Riley": [2020],
#           "Russell Crowe": [2020],
#           "Jimmi Simpson": [2020],
#           "Caren Pistorius": [2020],
#           "Gabriel Bateman": [2020],
#           "Orlando Bloom": [2020],
#           "Scott Eastwood": [2020, 2021],
#           "Caleb Landry Jones": [2020, 2020],
#           "Milo Gibson": [2020],
#           "Jake Watkins": [2020],
#           "Katie McKenna": [2020],
#           "Chelsea Greenwood": [2020],
#           "AJ Blackwell": [2020],
#           "John David Washington": [2020],
#           "Robert Pattinson": [2020],
#           "Elizabeth Debicki": [2020, 2020],
#           "Aaron Taylor-Johnson": [2020, 2020],
#           "Yifei Liu": [2020],
#           "Donnie Yen": [2020],
#           "Li Gong": [2020],
#           "Jet Li": [2020],
#           "Alison Brie": [2020, 2020],
#           "Dan Stevens": [2020],
#           "Sheila Vand": [2020],
#           "Jeremy Allen White": [2020],
#           "Imelda Staunton": [2020],
#           "Carla Juri": [2020],
#           "Alec Secareanu": [2020],
#           "Angeliki Papoulia": [2020],
#           "Gemma Arterton": [2020, 2020],
#           "Gugu Mbatha-Raw": [2020],
#           "Penelope Wilton": [2020],
#           "Tom Courtenay": [2020],
#           "Keanu Reeves": [2020, 2020, 2021],
#           "Clancy Brown": [2020],
#           "Awkwafina": [2020, 2021, 2021],
#           "Tom Kenny": [2020],
#           "Stephen Root": [2020],
#           "Joel Courtney": [2020],
#           "Rasneet Kaur": [2020],
#           "Aaron Poole": [2020],
#           "Max Easton": [2020],
#           "Adam Hillier": [2020],
#           "Emma Von Schreiber": [2020],
#           "Remy Bataille": [2020],
#           "Pedro Pascal": [2020],
#           "Gal Gadot": [2020, 2020],
#           "Connie Nielsen": [2020],
#           "Chris Pine": [2020],
#           "Olivia Cooke": [2019],
#           "Riz Ahmed": [2019],
#           "Mathieu Amalric": [2019],
#           "Lauren Ridloff": [2019],
#           "Angelina Jolie": [2020, 2020, 2021],
#           "Sam Rockwell": [2020],
#           "Bryan Cranston": [2020],
#           "Helen Mirren": [2020, 2021],
#           "Harvey Keitel": [2020],
#           "Goran Visnjic": [2020],
#           "Joaquim de Almeida": [2020],
#           "Sônia Braga": [2020],
#           "Janelle Monáe": [2020, 2020],
#           "Eric Lange": [2020],
#           "Jena Malone": [2020],
#           "Jack Huston": [2020],
#           "Alex Winter": [2020],
#           "Samara Weaving": [2020],
#           "Brigette Lundy-Paine": [2020],
#           "Kevin Costner": [2020],
#           "Diane Lane": [2020],
#           "Lesley Manville": [2020],
#           "Kayli Carter": [2020],
#           "Maisie Williams": [2020],
#           "Anya Taylor-Joy": [2020, 2021],
#           "Charlie Heaton": [2020],
#           "Blu Hunt": [2020],
#           "Rachel Brosnahan": [2020],
#           "Benedict Cumberbatch": [2020],
#           "Jessie Buckley": [2020],
#           "Eysteinn Sigurðarson": [2020],
#           "Brad Owens": [2020],
#           "Scotty Sparks": [2020],
#           "Bob Young": [2020],
#           "William Wylie": [2020],
#           "Emily Blunt": [2020],
#           "Millicent Simmonds": [2020],
#           "Cillian Murphy": [2020],
#           "Noah Jupe": [2020],
#           "Milla Jovovich": [2020],
#           "Tony Jaa": [2020],
#           "T.I.": [2020],
#           "Meagan Good": [2020],
#           "Liam Neeson": [2020],
#           "Kate Walsh": [2020],
#           "Jai Courtney": [2020],
#           "Jeffrey Donovan": [2020],
#           "John Lennon": [2020],
#           "Paul McCartney": [2020],
#           "George Harrison": [2020],
#           "Ringo Starr": [2020],
#           "Chris Coy": [2020],
#           "Clayne Crawford": [2020],
#           "Arri Graham": [2020],
#           "Bruce Graham": [2020],
#           "Walter Robert Duckworth": [2020],
#           "Briana Cristal": [2020],
#           "Vera Farmiga": [2020, 2021],
#           "Patrick Wilson": [2020],
#           "Julian Hilliard": [2020],
#           "Charlene Amoia": [2020],
#           "Jessica Jade Andres": [2020],
#           "Benita Robledo": [2020],
#           "Emilia Bogdanova": [2020],
#           "Montgomery Markland": [2020],
#           "Jim Caviezel": [2019, 2021],
#           "Claudia Karvan": [2019],
#           "Hal Ozsan": [2019],
#           "Stelio Savante": [2019],
#           "Ralph Fiennes": [2020, 2020],
#           "Matthew Goode": [2020],
#           "Evan Rachel Wood": [2020],
#           "Gina Rodriguez": [2020],
#           "Debra Winger": [2020],
#           "Diana Maria Riva": [2020],
#           "Isha Talwar": [2020],
#           "Farhan Akhtar": [2020],
#           "Mrunal Thakur": [2020],
#           "Paresh Rawal": [2020],
#           "Yahya Abdul-Mateen II": [2020],
#           "Teyonah Parris": [2020],
#           "Nathan Stewart-Jarrett": [2020],
#           "Colman Domingo": [2020],
#           "Alicia Vikander": [2020, 2021],
#           "Julianne Moore": [2020],
#           "Timothy Hutton": [2020],
#           "Steve Lewington": [2020],
#           "Alastair Natkiel": [2020],
#           "Oliver Mason": [2020],
#           "Tom Plenderleith": [2020],
#           "Jamie Bell": [2020],
#           "Michael B. Jordan": [2020],
#           "Cam Gigandet": [2020],
#           "Jacob Scipio": [2020],
#           "Jackson Rathbone": [2019],
#           "Amanda Arcuri": [2019],
#           "Kerri Medders": [2019],
#           "Elise Luthman": [2019],
#           "Tom Hanks": [2020, 2020],
#           "Skeet Ulrich": [2020],
#           "Samira Wiley": [2020],
#           "Anne Hathaway": [2020],
#           "Octavia Spencer": [2020],
#           "Stanley Tucci": [2020],
#           "Chris Rock": [2020],
#           "Annette Bening": [2020],
#           "Armie Hammer": [2020],
#           "Kenneth Branagh": [2020],
#           "Anthony Michael Hall": [2020],
#           "Jamie Lee Curtis": [2020],
#           "Judy Greer": [2020],
#           "Kyle Richards": [2020],
#           "Timothée Chalamet": [2020, 2020],
#           "Elisabeth Moss": [2020],
#           "Tilda Swinton": [2020],
#           "Saoirse Ronan": [2020],
#           "Eddie Redmayne": [2020],
#           "Alex Sharp": [2020],
#           "Sacha Baron Cohen": [2020],
#           "Jeremy Strong": [2020],
#           "Henry Golding": [2020],
#           "Andrew Koji": [2020],
#           "Úrsula Corberó": [2020],
#           "Steven Allerick": [2020],
#           "Abbi Jacobson": [2020],
#           "Danny McBride": [2020],
#           "Maya Rudolph": [2020],
#           "Michael Rianda": [2020],
#           "Nicholas Hoult": [2020],
#           "Jon Bernthal": [2020, 2021],
#           "Aidan Gillen": [2020],
#           "Max Harwood": [2020],
#           "Lauren Patel": [2020],
#           "Richard E. Grant": [2020],
#           "Sharon Horgan": [2020],
#           "Airlie Dodds": [2019],
#           "Linda Ngo": [2019],
#           "Taylor Ferguson": [2019],
#           "Ebony Vagulans": [2019],
#           "Scarlett Johansson": [2020],
#           "Robert Downey Jr.": [2020],
#           "Florence Pugh": [2020],
#           "Rachel Weisz": [2020],
#           "John Cho": [2020],
#           "Jimmy Wong": [2020],
#           "Natasha Liu Bordizzo": [2020],
#           "Constance Wu": [2020],
#           "Matt Damon": [2020, 2020],
#           "Abigail Breslin": [2020],
#           "Camille Cottin": [2020],
#           "Deanna Dunagan": [2020],
#           "Rachel Blanchard": [2020],
#           "Tracy Letts": [2020],
#           "Lil Rel Howery": [2020],
#           "Finn Wittrock": [2020],
#           "Mickey Rourke": [2019],
#           "Eric Roberts": [2019],
#           "Richard Tyson": [2019],
#           "Louis Mandylor": [2019],
#           "Eiza González": [2020],
#           "Millie Bobby Brown": [2020],
#           "Alexander Skarsgård": [2020],
#           "Rebecca Hall": [2020],
#           "Jamie Foxx": [2020],
#           "Tina Fey": [2020],
#           "Quest Love": [2020],
#           "Daveed Diggs": [2020],
#           "Ana de Armas": [2020],
#           "Daniel Craig": [2020],
#           "Léa Seydoux": [2020],
#           "Dan Levy": [2020],
#           "Kristen Stewart": [2020],
#           "Mackenzie Davis": [2020],
#           "Colin Farrell": [2020],
#           "Tye Sheridan": [2020],
#           "Isaac Hempstead Wright": [2020],
#           "Lily-Rose Depp": [2020],
#           "Bryn Clayton Jones": [2020],
#           "Leona Britt": [2020],
#           "Tommy Lee Driver": [2020],
#           "Erik Franklin": [2020],
#           "Jodie Comer": [2020, 2020],
#           "Taika Waititi": [2020],
#           "Ryan Reynolds": [2020, 2020],
#           "Joe Keery": [2020],
#           "Rebecca Ferguson": [2020, 2021],
#           "Jason Momoa": [2020],
#           "Zendaya": [2020],
#           "Eddie Murphy": [2020],
#           "Arsenio Hall": [2020],
#           "Jermaine Fowler": [2020],
#           "Leslie Jones": [2020],
#           "Ansel Elgort": [2020],
#           "Rachel Zegler": [2020],
#           "Ariana DeBose": [2020],
#           "David Alvarez": [2020],
#           "Jennifer Connelly": [2020],
#           "Tom Cruise": [2020],
#           "Val Kilmer": [2020],
#           "Jon Hamm": [2020],
#           "Michael Peña": [2020],
#           "Rob Delaney": [2020],
#           "Colin Jost": [2020],
#           "Ken Jeong": [2020],
#           "Nicolas Cage": [2020],
#           "Emma Stone": [2020, 2021],
#           "Leslie Mann": [2020],
#           "Lacy Hartselle": [2019],
#           "Kate Kilcoyne": [2019],
#           "Rae Hunt": [2019],
#           "Aaron Mirtes": [2019],
#           "Neil Sandilands": [2020],
#           "Chukwudi Iwuji": [2020],
#           "Helena Zengel": [2020],
#           "Marlene Hauser": [2018],
#           "Luzia Oppermann": [2018],
#           "Karin Pauer": [2018],
#           "Birgit Minichmayr": [2018],
#           "Taylor Russell": [2020],
#           "Logan Miller": [2020],
#           "Isabelle Fuhrman": [2020],
#           "Thomas Cocquerel": [2020],
#           "Ben Affleck": [2020],
#           "Adam Driver": [2020],
#           "Jessica McNamee": [2021],
#           "Hiroyuki Sanada": [2021],
#           "Tadanobu Asano": [2021],
#           "Mehcad Brooks": [2021],
#           "Jason Statham": [2021],
#           "Josh Hartnett": [2021],
#           "Holt McCallany": [2021],
#           "James Corden": [2020],
#           "Lennie James": [2020],
#           "Margot Robbie": [2020],
#           "Jessica Chastain": [2021],
#           "Sebastian Stan": [2021],
#           "Diane Kruger": [2021],
#           "Penélope Cruz": [2021],
#           "Daisy Ridley": [2021],
#           "Tom Holland": [2021],
#           "Mads Mikkelsen": [2021],
#           "Cynthia Erivo": [2021],
#           "Ben Schwartz": [2021],
#           "Terry Crews": [2021],
#           "Joe Anoa'i": [2021],
#           "Will Arnett": [2021],
#           "Natalie Morales": [2021],
#           "Denzel Washington": [2021],
#           "Jared Leto": [2021, 2021],
#           "Rami Malek": [2021],
#           "Camila Cabello": [2021],
#           "Billy Porter": [2021],
#           "Nicholas Galitzine": [2021],
#           "Minnie Driver": [2021],
#           "Kumail Nanjiani": [2021],
#           "Richard Madden": [2021],
#           "Salma Hayek": [2021],
#           "Dylan O'Brien": [2021, 2021],
#           "Jessica Henwick": [2021],
#           "Michael Rooker": [2021],
#           "Ellen Hollman": [2021],
#           "Sharon Stone": [2021],
#           "Andy Garcia": [2021],
#           "Iain Glen": [2021],
#           "Rosabell Laurenti Sellers": [2021],
#           "Finn Wolfhard": [2021],
#           "Carrie Coon": [2021],
#           "Sigourney Weaver": [2021],
#           "Bill Murray": [2021],
#           "Corey Stoll": [2021],
#           "Ray Liotta": [2021],
#           "Cassie Steele": [2021],
#           "Adria Arjona": [2021],
#           "J.K. Simmons": [2021],
#           "Michael Keaton": [2021],
#           "Kristin Scott Thomas": [2021],
#           "Alec Baldwin": [2021],
#           "John Flanagan": [2021],
#           "James McGrath": [2021],
#           "Maia Morgenstern": [2021],
#           "Christo Jivkov": [2021],
#           "Francesco De Vito": [2021],
#           "Charlize Theron": [2021],
#           "Vin Diesel": [2021],
#           "Michelle Rodriguez": [2021],
#           "Thandie Newton": [2021],
#           "Hugh Jackman": [2021],
#           "Angela Sarafyan": [2021],
#           "Thomasin McKenzie": [2021],
#           "Diana Rigg": [2021],
#           "Matt Smith": [2021],
#           "Simu Liu": [2021],
#           "Tony Chiu-Wai Leung": [2021],
#           "Fala Chen": [2021],
#           "Carrie-Anne Moss": [2021],
#           "Jonathan Groff": [2021],
#           "Priyanka Chopra": [2021],
#           "Morgan David Jones": [2021],
#           "Ali Johnson": [2021],
#           "Dan Petronijevic": [2021],
#           "Samuel L. Jackson": [2021],
#           "Mark Strong": [2021],
#           "Emma Thompson": [2021],
#           "Jamie Demetriou": [2021],
#           "Mark Wahlberg": [2021],
#           "Chiwetel Ejiofor": [2021],
#           "Rupert Friend": [2021]}

# делаем список актеров в привязке в фильму (займет около 60 секунд)

# actors = {}
# for i, k in zip(links, movies):
#     page = requests.get(i)
#     soup = BeautifulSoup(page.text, features="html.parser")
#
#     actors_in_movie = json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))
#
#     for i in actors_in_movie["actor"]:
#         if i["name"] not in actors:
#             actors.setdefault(i["name"], [])
#         actors[i["name"]].append(k)
#
# for key, value in actors.items():
#     print(key + ':', value, end='\n')