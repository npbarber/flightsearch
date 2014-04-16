#!/usr/bin/python

import unittest
from mock import call, patch, Mock

from flightsearch import vsflightsearch as vfs

class VSFLightSearchTestCase(unittest.TestCase):

    def setUp(self):
        self.browser = Mock()

    def test_login_fail(self):
        self.browser.get_html.return_value = 'xxxx check and try again xxxx'
        form = Mock()
        self.browser.get_form.return_value = form
        self.assertFalse(vfs.login(self.browser, 'user', 'pass'))
        expected = [call('user', 'login_uname'), call('pass', 'login_pwd')]
        self.assertEqual(expected, form.set_value.call_args_list)
        self.browser.submit.asser_called_once_with()
        self.browser.get_form.assert_called_once_with('flyClubLogin')

    def test_login_ok(self):
        self.browser.get_html.return_value = 'xxxx  xxxx'
        form = Mock()
        self.browser.get_form.return_value = form
        self.assertTrue(vfs.login(self.browser, 'user', 'pass'))

    def test_load_booking_page(self):
        self.browser.find_link.return_value = 'link'
        vfs.load_booking_page(self.browser)
        self.browser.find_link.assert_called_once_with('/bookflightsandmore/bookflights/index.jsp')
        self.browser.follow_link.assert_called_once_with('link')

    def test_flight_search(self):
        self.browser.find_link.side_effect = ['link1', 'link2', None]
        form = Mock()
        self.browser.get_form.return_value = form
        vfs.flight_search(self.browser, 'depdate', 'retdate')
        self.browser.get_form.assert_called_once_with('flightSearch_bookflightsandmore_bookflights_index_jsp')
        form.set_value.assert_any_call('depdate', 'departureDate')
        form.set_value.assert_any_call('retdate', 'returnDate')
        form.set_value.assert_any_call(['LAX'], 'departure')
        form.set_value.assert_any_call(['LONLHR'], 'arrival')
        form.set_value.assert_any_call(['6'], 'classType')
        form.set_value.assert_any_call(['6'], 'classTypeReturn')
        form.set_value.assert_any_call(['1'], 'adult')
        form.set_value.assert_any_call(['0'], 'child')
        form.set_value.assert_any_call(['0'], 'infant')
        form.set_value.assert_any_call(['redeemMiles'], 'search_type')
        self.browser.submit.assert_called_once_with()
        self.browser.find_link.assert_any_call('Refresh this page')
        self.browser.follow_link.assert_called_once_with('link2')

    def test_dates_available_select_flight(self):
        self.browser.get_html.return_value = 'xxx Choose Your Flights xxx'
        self.assertTrue(vfs.dates_available(self.browser, '10/12/13', '14/15/16'))

    def test_dates_available_select_from_calendar(self):
        self.browser.get_html.return_value = 'xxx date1_10  yyyyy date2_14  xxx'
        self.assertTrue(vfs.dates_available(self.browser, '10/12/13', '14/15/16'))

    def test_dates_available_nothing_available(self):
        self.browser.get_html.return_value = 'xxx  xxx'
        self.assertFalse(vfs.dates_available(self.browser, '10/12/13', '14/15/16'))

    @patch('flightsearch.vsflightsearch.mail')
    def test_send_alert(self, m_mail):
        emailer = Mock()
        m_mail.Email.return_value = emailer
        vfs.send_alert('s', 'r', 'd', 'r')
        m_mail.Email.assert_called_once_with('s', 'r', 'FLIGHTS AVAILABLE d to r', 'Check out the free flights at Virgin')
        emailer.send.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
