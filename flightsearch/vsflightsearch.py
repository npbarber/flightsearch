#!/use/bin/env python

from flightsearch import common as fs_common


base_url = 'https://www.virgin-atlantic.com'


def login(b, username, password):
    form = b.get_form('flyClubLogin')
    form.set_value(username, 'login_uname')
    form.set_value(password, 'login_pwd')
    b._browser.form = form
    b.submit()
    if 'check and try again' in b.get_html():
        return False
    return True


def load_booking_page(b):
    link = b.find_link('/bookflightsandmore/bookflights/index.jsp')
    b.follow_link(link)


def flight_search(b, dep_date, ret_date):
    form = b.get_form('flightSearch_bookflightsandmore_bookflights_index_jsp')
    form.set_value(['LAX'], 'departure')
    form.set_value(['LONLHR'], 'arrival')
    form.set_value(dep_date, 'departureDate')
    form.set_value(ret_date, 'returnDate')
    form.set_value(['6'], 'classType')
    form.set_value(['6'], 'classTypeReturn')
    form.set_value(['1'], 'adult')
    form.set_value(['0'], 'child')
    form.set_value(['0'], 'infant')
    form.set_value(['redeemMiles'], 'search_type')
    b._browser.form = form
    b.submit()

    # Keep refreshing until the 'Refresh this page' link is no more.
    # We know the search has finished at that point and we have some
    # results to work with
    while b.find_link('Refresh this page'):
        b.follow_link(b.find_link('Refresh this page'))


def write_html_to_disk(b, outfile):
    html = b.get_html()
    fs_common.write_to_file(html, outfile)


def dates_available(b, dep_date, ret_date):
    html = b.get_html()

    # Sometimes, you are taken to the page where you can select flights.
    # If that happened here, we know the selected dates are available.
    if 'Choose Your Flights' in html:
        return True

    # Othertimes, even though our specific dates are available, we are
    # still presented with the calendar where we can change dates.  If
    # that happened here, look at the calendars to see if we have radio
    # buttons available for out selected outbound and inbound dates.
    outday = dep_date.split('/')[0]
    retday = ret_date.split('/')[0]
    if 'date1_%s  ' % outday in html and 'date2_%s  ' % retday in html:
        return True
    return False
