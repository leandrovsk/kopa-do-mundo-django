from teams.exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError
from datetime import datetime


def data_processing(data):
    current_date = datetime.today()
    first_cup_date = datetime.strptime(data["first_cup"], "%Y-%m-%d")
    max_titles = (current_date.year - first_cup_date.year) / 4

    if data["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")
    if first_cup_date.year < 1930 or (first_cup_date.year - 1930) % 4 != 0:
        raise InvalidYearCupError("there was no world cup this year")
    if max_titles < data["titles"]:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")
