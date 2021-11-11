import random
import csv
import requests
import os
from datetime import datetime
from enum import IntEnum

random.seed(os.urandom(1024))
class Movie(IntEnum):
    NOMINATOR = 0
    TITLE = 1
    IMDB_ID = 2


def make_movie_message(selected_class, selected_trash):
    """
    This function will take the selected class and trash picks and return a formatted
    Discord message.
    """
    emoji_list = [
        ':bonehands',
        ':REX:',
        ':brobocop:',
        ':hark:',
        ':dreamer:',
        ':wishmaster:',
        ':sneakyweng:',
        ':peekaboo:',
        ':dogg:',
        ':pooo:',
        ':leningrad:'
    ]
    random.shuffle(emoji_list)

    todays_date = datetime.now().strftime("%m/%d/%Y")
    message_array = [
        f'@everyone',
        f'**__MOVIE NIGHT {todays_date}:__**',
        f'',
        f'Please vote on the movies we will be watching tonight!',
        f'',
        f'**__CLASS:__**',
    ]

    for movie in selected_class:
        message_array.append(f'{emoji_list.pop()}: {movie[Movie.TITLE]} - https://www.imdb.com/title/{movie[Movie.IMDB_ID]}')

    message_array.extend([
        f'',
        f'**__TRASH:__**'
    ])

    for movie in selected_trash:
        message_array.append(f'{emoji_list.pop()}: {movie[Movie.TITLE]} - https://www.imdb.com/title/{movie[Movie.IMDB_ID]}')

    return '\n'.join(message_array)


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
participants = []

for i in range(2):
    class_roll = random.randint(0, len(class_list) - 1)
    trash_roll = random.randint(0, len(trash_list) - 1)

    random.shuffle(class_list)
    while class_list[class_roll][0] in participants:
        random.shuffle(class_list)
    selected_class.append(class_list[class_roll])
    participants.append(class_list[class_roll][0])

    random.shuffle(trash_list)
    while trash_list[trash_roll][0] in participants:
        random.shuffle(trash_list)
    selected_trash.append(trash_list[trash_roll])
    participants.append(trash_list[trash_roll][0])

    class_list.pop(class_roll)
    trash_list.pop(trash_roll)

print(make_movie_message(selected_class, selected_trash))
