import random
import csv
import requests
from tabulate import tabulate


class_list = []
trash_list = []
movie_votes = []

movie_list_url = "https://docs.google.com/spreadsheets/d/1xpX7RvAveMJH0gS1Zj-XRYPb70exCl5QNlUTdX_KLqk/export?gid=0&format=csv"

with requests.Session() as s:
    download = s.get(movie_list_url)

    decoded_content = download.content.decode('utf-8')
    csv_reader = csv.reader(decoded_content.splitlines(), delimiter=',')
    csv_file = list(csv_reader)
    line_count = 0
    for row in csv_file:
        if line_count == 0:
            date = row[0]
        elif line_count == 2:
            columns = row
        else:
            if row[1] != '' and row[2] != '':
                class_list.append((row[0], row[1], row[2]))
            if row[3] != '' and row[4] != '':
                trash_list.append((row[0], row[3], row[4]))
        line_count += 1

selected_class = []
selected_trash = []

for i in range(2):
    class_roll = random.randint(0, len(class_list) - 1)
    trash_roll = random.randint(0, len(trash_list) - 1)

    selected_class.append(class_list[class_roll])
    selected_trash.append(trash_list[trash_roll])

    class_list.pop(class_roll)
    trash_list.pop(trash_roll)

print("Congratulations! Here are your choices: ")
table = []
for movie in selected_class:
    table.append(["Class", movie[1], movie[2]])
for movie in selected_trash:
    table.append(["Trash", movie[1], movie[2]])

print(tabulate(table, headers=["Category", "Movie Title", "IMDB"]))