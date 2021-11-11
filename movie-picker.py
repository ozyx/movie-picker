import random
import csv
import requests
import os
from datetime import datetime
from config import *

random.seed(os.urandom(1024))

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
        message_array.append(
            f'{emoji_list.pop()}: {movie[Movie.TITLE]} - https://www.imdb.com/title/{movie[Movie.IMDB_ID]}')

    message_array.extend([
        f'',
        f'**__TRASH:__**'
    ])

    for movie in selected_trash:
        message_array.append(
            f'{emoji_list.pop()}: {movie[Movie.TITLE]} - https://www.imdb.com/title/{movie[Movie.IMDB_ID]}')

    return '\n'.join(message_array)


class_list = []
trash_list = []
movie_votes = []

with requests.Session() as s:
    download = s.get(MOVIE_LIST_URL)
    decoded_content = download.content.decode('utf-8')

    csv_reader = csv.reader(decoded_content.splitlines(), delimiter=',')
    csv_file = list(csv_reader)

    line_count = 0
    for row_item in csv_file:
        if line_count > 2:
            if row_item[CSVRow.CLASS_TITLE] != '' and row_item[CSVRow.CLASS_IMDB_ID] != '':
                class_list.append(
                    (row_item[CSVRow.NOMINATOR], row_item[CSVRow.CLASS_TITLE], row_item[CSVRow.CLASS_IMDB_ID]))
            if row_item[CSVRow.TRASH_TITLE] != '' and row_item[CSVRow.TRASH_IMDB_ID] != '':
                trash_list.append(
                    (row_item[CSVRow.NOMINATOR], row_item[CSVRow.TRASH_TITLE], row_item[CSVRow.TRASH_IMDB_ID]))
        line_count += 1

selected_class = []
selected_trash = []
participants = []

for i in range(NUM_PICKS):
    class_roll = random.randint(0, len(class_list) - 1)
    trash_roll = random.randint(0, len(trash_list) - 1)

    random.shuffle(class_list)
    while class_list[class_roll][Movie.NOMINATOR] in participants:
        random.shuffle(class_list)
    selected_class.append(class_list[class_roll])
    participants.append(class_list[class_roll][Movie.NOMINATOR])

    random.shuffle(trash_list)
    while trash_list[trash_roll][Movie.NOMINATOR] in participants:
        random.shuffle(trash_list)
    selected_trash.append(trash_list[trash_roll])
    participants.append(trash_list[trash_roll][Movie.NOMINATOR])

    class_list.pop(class_roll)
    trash_list.pop(trash_roll)

print(make_movie_message(selected_class, selected_trash))
