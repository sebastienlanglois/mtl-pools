import dateparser
from datetime import datetime, timedelta, timezone
import pytz


class Config(object):

    # User-defined
    schedule = "Samedi 18:00 - 19:00"
    query = "piscine"
    delay_register_days = 3

    # Constants
    day = dateparser.parse(u"{}".format(schedule.split()[0])).date()
    if dateparser.parse(u"{}".format(schedule.split()[0])).date() <= datetime.today().date():
        day = day + timedelta(days=7)
    day_of_week = str((day.weekday() + 1) % 7)

    datetime_to_register = pytz.timezone('America/Montreal') \
        .localize(datetime.strptime((day - timedelta(days=delay_register_days)).strftime("%Y-%m-%d") + ' ' + schedule.split()[1], '%Y-%m-%d %H:%M')) \
        .astimezone(pytz.utc)

    ready_to_register = True if (datetime_to_register - datetime.now(timezone.utc)) < timedelta(minutes=14) else False

    website_url = "https://loisirs.montreal.ca/IC3/#/U2010"
    table_activities_url = 'https://loisirs.montreal.ca/IC3/#/U5200/search/?searchParam='
    specific_activity_prefix_url = "https://loisirs.montreal.ca/IC3/#/U5200/view"

    params = {"filter": {"isCollapsed": 'false',
                         "value": {"dayOfWeekId": day_of_week,
                                   "canRegisterStatuses": "1"}},
              "search": query,
              "sortable": {"isOrderAsc": 'true',
                           "column": "description"}
              }
