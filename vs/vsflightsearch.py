#!/use/bin/env python

import argparse
import sys

from dtk import mail

from twill import get_browser
from twill import commands as tc


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
    while b.find_link('Refresh this page'):
        b.follow_link(b.find_link('Refresh this page'))


def dates_available(b, dep_date, ret_date):
    html = b.get_html()

    if 'Choose Your Flights' in html:
        return True

    outday = dep_date.split('/')[0]
    retday = ret_date.split('/')[0]
    if 'date1_%s  ' % outday in html and 'date2_%s  ' % retday in html:
        return True
    return False


def send_alert(sender, recipients, depdate, retdate):
    print 'Dates available! %s -> %s' % (depdate, retdate)
    recipients = [
        'neil.barber@disneyanimation.com',
        'npbarber@gmail.com',
        '6268412568@messaging.sprintpcs.com'
    ]
    emailer = mail.Email(sender, recipients,
                         'FLIGHTS AVAILABLE %s to %s' % (depdate, retdate),
                         'Check out the free flights at Virgin')
    emailer.send()


def parse_args():
    parser = argparse.ArgumentParser(description='find my free flights')
    parser.add_argument('-u', '--username', help='flying club username',
                        required=True)
    parser.add_argument('-p', '--password', help='flying club password',
                        required=True)
    parser.add_argument('-d', '--depdate', help='departure d/m/yy',
                        required=True)
    parser.add_argument('-r', '--retdate', help='return d/m/yy',
                        required=True)
    parser.add_argument('-s', '--sender', help='who an alert is sent from',
                        required=True)
    parser.add_argument('--recipient', help='who gets alerts',
                        action='append', required=True)
    return parser.parse_args()


def bail(msg):
    print msg
    sys.exit(1)

def main():
    args = parse_args()
    tc.config('acknowledge_equiv_refresh', False)
    b = get_browser()
    b.go('%s' % base_url)
    if not login(b, args.username, args.password):
        bail('Login Error')

    load_booking_page(b)

    flight_search(b, args.depdate, args.retdate)
    if not dates_available(b, args.depdate, args.retdate):
        return

    send_alert(args.sender, args.recipient, args.depdate, args.retdate)

if __name__ == '__main__':
    main()
