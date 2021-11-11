from enum import IntEnum

NUM_PICKS = 2
MOVIE_LIST_URL='https://docs.google.com/spreadsheets/d/1xpX7RvAveMJH0gS1Zj-XRYPb70exCl5QNlUTdX_KLqk/export?gid=0&format=csv'

class Movie(IntEnum):
    NOMINATOR = 0
    TITLE = 1
    IMDB_ID = 2


class CSVRow(IntEnum):
    NOMINATOR = 0
    CLASS_TITLE = 1
    CLASS_IMDB_ID = 2
    TRASH_TITLE = 3
    TRASH_IMDB_ID = 4
