#!/usr/bin/env python

import unittest

from flightsearch import common as c
from mock import Mock, patch
class WriteDataTestCase(unittest.TestCase):

    @patch('__builtin__.open')
    def test_write_data(self, m_open):
        mock_fp = Mock()
        mock_fp.__enter__ = lambda x: mock_fp
        mock_fp.__exit__ = lambda w, x, y, z: None
        m_open.return_value = mock_fp
        c.write_to_file('data', 'outfile')
        m_open.assert_called_once_with('outfile', 'w')
        mock_fp.write.assert_called_once_with('data')


if __name__ == '__main__':
    unittest.main()
