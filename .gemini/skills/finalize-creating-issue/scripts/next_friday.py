import datetime

def next_friday():
    today = datetime.date.today()
    days_ahead = 4 - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    friday = today + datetime.timedelta(days_ahead)
    print(friday.strftime("%Y-%m-%dT05:00:00.000Z"))

if __name__ == "__main__":
    next_friday()