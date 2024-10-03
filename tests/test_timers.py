from unittest import TestCase, main as unittest_main
from unittest.mock import patch, Mock, MagicMock
from datetime import timedelta

import rationalbreaks.timers
from rationalbreaks.timers import RatioNalTimer


class TestRationalTimer(TestCase):
    """Setup for downstream tests
    In tests representing time calculation with integer operations, as both use underlying __sub__ and __add__
    operators, but integer tests are easier to follow and construct."""
    def setUp(self):
        self.timer = RatioNalTimer()

    def test_init(self):
        # Case 1: default ratio
        expected_ratio = 3
        expected_status = "Not started"
        expected_timestamps = []
        self.assertEqual(self.timer._ratio, expected_ratio)
        self.assertEqual(self.timer._status, expected_status)
        self.assertEqual(self.timer._cycle_timestamps, expected_timestamps)
        self.assertEqual(self.timer._current_cycle_time, timedelta(0))
        self.assertEqual(self.timer._saved_work, timedelta(0))
        self.assertEqual(self.timer._saved_rest, timedelta(0))

        # Case 2: testing with non-default ratio
        self._test_timer = RatioNalTimer(5)
        expected_ratio = 5
        expected_status = "Not started"
        expected_timestamps = []
        self.assertEqual(self._test_timer._ratio, expected_ratio)
        self.assertEqual(self._test_timer._status, expected_status)
        self.assertEqual(self._test_timer._cycle_timestamps, expected_timestamps)
        self.assertEqual(self._test_timer._current_cycle_time, timedelta(0))
        self.assertEqual(self._test_timer._saved_work, timedelta(0))
        self.assertEqual(self._test_timer._saved_rest, timedelta(0))

        # Case 3: non-integer ratio
        self._test_timer = RatioNalTimer(1.5)
        expected_ratio = 1.5
        expected_status = "Not started"
        expected_timestamps = []
        self.assertEqual(self._test_timer._ratio, expected_ratio)
        self.assertEqual(self._test_timer._status, expected_status)
        self.assertEqual(self._test_timer._cycle_timestamps, expected_timestamps)
        self.assertEqual(self._test_timer._current_cycle_time, timedelta(0))
        self.assertEqual(self._test_timer._saved_work, timedelta(0))
        self.assertEqual(self._test_timer._saved_rest, timedelta(0))

        # Case 4: invalid ratio
        passed_invalid_value = "abc"
        with self.assertRaises(ValueError):
            self._test_timer = RatioNalTimer(passed_invalid_value)

    @patch('rationalbreaks.timers.datetime')
    def test_start(self, mock_now):
        # Case 1: Using first time
        expected_status = "Working"
        time_value_for_mock = "mocked_datetime"
        mock_now.now.return_value = time_value_for_mock

        self.timer.start()

        self.assertEqual(self.timer._status, expected_status)
        self.assertEqual(self.timer._cycle_timestamps, [time_value_for_mock])

        # Case 2: Using again
        self.timer._status = "Resting"
        time_value_for_mock2 = "mocked_datetime 2"
        mock_now.now.return_value = time_value_for_mock2

        self.timer.start()

        self.assertEqual(self.timer._cycle_timestamps, [time_value_for_mock, time_value_for_mock2])
        self.assertEqual(self.timer._status, expected_status)

    @patch('rationalbreaks.timers.RatioNalTimer._save_cycle_work')
    @patch('rationalbreaks.timers.RatioNalTimer._save_cycle_rest')
    @patch('rationalbreaks.timers.datetime')
    def test_reset(self, datetime_mock, save_rest_mock, save_work_mock):
        # setting up preconditions
        self.timer._status = "Working"

        # mock and expected values
        expected_status = "Resting"
        time_value_for_mock = "mocked_datetime"
        datetime_mock.now.return_value = "mocked_datetime"
        expected_time_values = self.timer._cycle_timestamps + [time_value_for_mock]

        self.timer.rest()

        # assertions
        self.assertEqual(self.timer._cycle_timestamps, expected_time_values)
        self.assertEqual(self.timer._status, expected_status)
        save_work_mock.assert_called_once()
        save_rest_mock.assert_called_once()

    @patch('rationalbreaks.timers.RatioNalTimer._save_cycle_rest')
    @patch('rationalbreaks.timers.RatioNalTimer.start')
    def test_continue_work(self, mock_start, mock_save_rest):
        self.timer.continue_work()
        mock_start.assert_called_once()
        mock_save_rest.assert_called_once()

    @patch('rationalbreaks.timers.datetime')
    def test_calculate_cycle_time(self, datetime_mock):
        # representing time calculation with integer operations
        value_for_timestamp = 3
        value_for_mock = 5
        datetime_mock.now.return_value = value_for_mock
        self.timer._cycle_timestamps.append(value_for_timestamp)

        output = self.timer._calculate_cycle_time()

        self.assertEqual(output, value_for_mock - value_for_timestamp)
        datetime_mock.now.assert_called_once()

    def _test_status(self):
        self.assertEqual(self.timer.status(), self.timer._status)

    @patch('rationalbreaks.timers.RatioNalTimer._calclate_cycle_time')
    def _test_work_time(self, cycle_time_mock):
        # representing time calculation with integer operations
        # Case 1: Working
        self.timer._status = "Working"
        self.timer._saved_work = 0
        value_for_mock = 5
        expected = self.timer._saved_work + value_for_mock

        output = self.timer.work_time()

        self.assertEqual(output, expected)
        cycle_time_mock.assert_called_once()

        # Case 2: Resting
        self.timer._status = "Resting"
        expected = self.timer._saved_work

        output = self.timer.work_time()

        self.assertEqual(output, expected)
        cycle_time_mock.assert_called_once()

    @patch('rationalbreaks.timers.RatioNalTimer._calculate_cycle_time')
    def test_save_cycle_work(self, cycle_time_mock):
        # representing time calculation with integer operations
        self.timer._saved_work = 3
        value_for_mock = 5
        cycle_time_mock.return_value = value_for_mock
        expected = value_for_mock + self.timer._saved_work

        self.timer._save_cycle_work()

        self.assertEqual(self.timer._saved_work, expected)

    @patch('rationalbreaks.timers.RatioNalTimer._calculate_remaining_rest')
    @patch('rationalbreaks.timers.RatioNalTimer._calculate_cycle_time')
    def test_rest_time(self, mock_cycle_time, mock_remaining_rest):
        # representing time calculation with integer operations
        # Case 1: Working
        self.timer._status = "Working"
        self.timer._saved_rest = 3
        value_for_time_mock = 5
        mock_cycle_time.return_value = value_for_time_mock
        expected = self.timer._saved_rest + value_for_time_mock / self.timer._ratio

        output = self.timer.rest_time()

        self.assertEqual(output, expected)
        mock_cycle_time.assert_called_once()
        mock_remaining_rest.assert_not_called()

        # Case 2: Resting
        self.timer._status = "Resting"
        self.timer._saved_rest = 3
        value_for_time_mock = 5
        mock_remaining_rest.return_value = value_for_time_mock
        expected = value_for_time_mock

        output = self.timer.rest_time()

        self.assertEqual(output, expected)
        mock_cycle_time.assert_called_once()
        mock_remaining_rest.assert_called_once()

    @patch('rationalbreaks.timers.RatioNalTimer._calculate_cycle_time')
    @patch('rationalbreaks.timers.timedelta')
    def test_calculate_remaining_rest(self, mock_timedelta, mock_cycle_time):
        # representing time calculation with integer operations
        # Case 1: More saved rest available than what got consumed in the cycle
        self.timer._saved_rest = 9
        value_for_mock = 5
        value_for_timedelta_mock = 0
        mock_cycle_time.return_value = value_for_mock
        mock_timedelta.return_value = value_for_timedelta_mock
        expected = self.timer._saved_rest - value_for_mock

        output = self.timer._calculate_remaining_rest()

        self.assertEqual(output, expected)
        mock_cycle_time.assert_called_once()
        mock_timedelta.assert_called_once()

        # Case 1: Less saved rest available than what got consumed in the cycle
        self.timer._saved_rest = 3
        value_for_mock = 5
        value_for_timedelta_mock = 0
        mock_cycle_time.return_value = value_for_mock
        mock_timedelta.return_value = value_for_timedelta_mock
        expected = value_for_timedelta_mock

        output = self.timer._calculate_remaining_rest()

        self.assertEqual(output, expected)
        self.assertEqual(mock_cycle_time.call_count, 2)
        self.assertEqual(mock_timedelta.call_count, 3)

    @patch('rationalbreaks.timers.RatioNalTimer.rest_time')
    def test__save_cycle_rest(self, mock_rest_time):
        value_for_mock = "mock_time"
        mock_rest_time.return_value = value_for_mock
        self.timer._save_cycle_rest()
        expected = value_for_mock

        self.assertEqual(self.timer._saved_rest, expected)
        mock_rest_time.assert_called_once()

    @patch('rationalbreaks.timers.RatioNalTimer.work_time')
    @patch('rationalbreaks.timers.RatioNalTimer.rest_time')
    def test_work_and_rest_time(self, mock_rest_time, mock_work_time):
        value_for_mock_work = "time1"
        value_for_mock_rest = "time2"
        mock_rest_time.return_value = value_for_mock_rest
        mock_work_time.return_value = value_for_mock_work
        expected = value_for_mock_work, value_for_mock_rest

        output = self.timer.work_and_rest_time()

        self.assertEqual(output, expected)
        mock_rest_time.assert_called_once()
        mock_work_time.assert_called_once()


if __name__ == '__main__':
    unittest_main()
