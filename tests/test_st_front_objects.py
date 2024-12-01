from unittest import TestCase, main as unittest_main
from unittest.mock import patch, Mock, MagicMock

from os import path

from frontend import st_front_objects
from rationalbreaks.timers import RatioNalTimer


class TestRationalTimerStreamlit(TestCase):
    @patch('frontend.st_front_objects.st.cache_resource', lambda x: x)
    def test_init(self):
        timer = st_front_objects.RatioNalTimerStreamlit()
        self.assertIsInstance(timer, RatioNalTimer)


class TestAlarm(TestCase):
    @patch('frontend.st_front_objects.st.cache_resource', lambda x: x)
    @patch('frontend.st_front_objects.sa.WaveObject.from_wave_file')
    def setUp(self, mock_from_wave_file):
        mocked_player = MagicMock()
        mock_from_wave_file.return_value = mocked_player
        self.alarm = st_front_objects.Alarm()

    def test_init_values(self):
        default_path_elements = "resources", "ring_1.wav"
        expected_path = path.join(*default_path_elements)
        expected_play_object_at_init = None

        self.assertEqual(self.alarm.soundfile, expected_path)
        self.assertEqual(self.alarm.play_object, expected_play_object_at_init)

    @patch('frontend.st_front_objects.sa.WaveObject.from_wave_file')
    def test_create_player(self, mock_from_wave_file):
        mocked_return_val = "mocked_player"
        mock_from_wave_file.return_value = mocked_return_val
        player = self.alarm.create_player()
        self.assertEqual(player, mocked_return_val)

    def test_play(self):
        # Case 1: Not played yet (no play_object)
        self.alarm.play_object = None
        player_mock = MagicMock()
        play_object_mock = MagicMock()
        player_mock.play.return_value = play_object_mock
        self.alarm.player = player_mock

        self.alarm.play()

        self.assertEqual(self.alarm.play_object, play_object_mock)
        player_mock.play.assert_called_once()

        # Case 2: Sound is being played: Play object exists, is_playing is True
        player_mock_2 = MagicMock()
        play_object_mock_2 = MagicMock()
        play_object_mock_2.is_playing.return_value = True
        self.alarm.play_object = play_object_mock_2
        mock_return_value = "Should not have been called"
        player_mock_2.play.return_value = mock_return_value
        self.alarm.player = player_mock_2

        self.alarm.play()

        self.assertEqual(self.alarm.play_object, play_object_mock_2)
        player_mock_2.play.assert_not_called()
        self.assertNotEqual(self.alarm.play_object, mock_return_value)

        # Case 3: Sound is ended and should be replayed: Play object exists, is_playing is False
        player_mock_3 = MagicMock()
        play_object_mock_3 = MagicMock()
        play_object_mock_3.is_playing.return_value = False
        self.alarm.play_object = play_object_mock_3
        mock_return_value = MagicMock()
        player_mock_3.play.return_value = mock_return_value
        self.alarm.player = player_mock_3

        self.alarm.play()

        self.assertEqual(self.alarm.play_object, mock_return_value)
        player_mock_3.play.assert_called_once()

    def test_stop(self):
        mock_play_object = MagicMock()
        self.alarm.play_object = mock_play_object

        self.alarm.stop()

        mock_play_object.stop.assert_called_once()

    def test_toogle(self):
        # Case 1: sound is being played
        mock_play_object = MagicMock()
        mock_play_object.is_playing.return_value = True
        self.alarm.play_object = mock_play_object

        self.alarm.toogle()

        mock_play_object.is_playing.assert_called_once()
        mock_play_object.stop.assert_called_once()
        mock_play_object.play.assert_not_called()

        # Case 2: sound is not being played at the moment
        mock_play_object2 = MagicMock()
        mock_play_object2.is_playing.return_value = False
        mock_player = MagicMock()
        self.alarm.player = mock_player
        self.alarm.play_object = mock_play_object2

        self.alarm.toogle()

        mock_play_object2.is_playing.assert_called_once()
        mock_play_object2.stop.assert_not_called()
        mock_player.play.assert_called_once()


class TestStatusControl(TestCase):

    def setUp(self) -> None:
        self.mock_timer_instance = MagicMock()
        self.control = st_front_objects.StatusControl(self.mock_timer_instance)

    def test_init(self):
        mock_timer_instance = MagicMock()
        test_control = st_front_objects.StatusControl(mock_timer_instance)
        self.assertEqual(test_control.timer, mock_timer_instance)

    @patch('frontend.st_front_objects.st.session_state', new_callable=dict)
    def test_start(self, mock_session_state):
        expected_val_status = "Working"

        self.control.start()

        self.assertEqual(mock_session_state["status"], expected_val_status)
        self.mock_timer_instance.start.assert_called_once()

    @patch('frontend.st_front_objects.st.session_state', new_callable=dict)
    def test_rest(self, mock_session_state):
        expected_val_status = "Resting"
        expected_val_rest_cons = False

        # Case 1: Alert/play_sound is True
        mock_session_state["alert"] = {"play_sound": True, "muted": True}
        expected_val_muted = False
        self.control.rest()
        self.assertEqual(mock_session_state["status"], expected_val_status)
        self.assertEqual(mock_session_state["rest_consumed"], expected_val_rest_cons)
        self.assertEqual(mock_session_state["alert"]["muted"], expected_val_muted)
        self.mock_timer_instance.rest.assert_called_once()

        # Case 2: Alert/play_sound is False
        mock_session_state["alert"] = {"play_sound": False, "muted": False}
        expected_val_muted = False
        self.control.rest()
        self.assertEqual(mock_session_state["status"], expected_val_status)
        self.assertEqual(mock_session_state["rest_consumed"], expected_val_rest_cons)
        self.assertEqual(mock_session_state["alert"]["muted"], expected_val_muted)
        self.assertEqual(self.mock_timer_instance.rest.call_count, 2)

    @patch('frontend.st_front_objects.st.session_state', new_callable=dict)
    def test_continue_work(self, mock_session_state):
        expected_val_status = "Working"
        expected_val_muted = True
        mock_session_state["alert"] = {"muted": True}

        self.control.continue_work()

        self.assertEqual(mock_session_state["status"], expected_val_status)
        self.assertEqual(mock_session_state["alert"]["muted"], expected_val_muted)
        self.mock_timer_instance.continue_work.assert_called_once()

    def test_stop(self):
        pass

    @patch('frontend.st_front_objects.st.session_state', new_callable=dict)
    def test_reset(self, mock_session_state):
        expected_val_status = "Not started"
        expected_val_muted = True
        mock_session_state["alert"] = {"muted": False}

        self.control.reset()
        self.assertEqual(mock_session_state["status"], expected_val_status)
        self.assertEqual(mock_session_state["alert"]["muted"], expected_val_muted)
        self.mock_timer_instance.reset.assert_called_once()

    @patch('frontend.st_front_objects.st.session_state', new_callable=dict)
    @patch('frontend.st_front_objects.st.rerun')
    def test_mute_alarm(self, mock_st_rerun, mock_session_state):
        expected_val_muted = True
        mock_session_state["alert"] = {"muted": False}

        self.control.mute_alarm()
        self.assertEqual(mock_session_state["alert"]["muted"], expected_val_muted)
        mock_st_rerun.assert_called_once()

class TestCheckRestConsumed(TestCase):
    @patch('frontend.st_front_objects.st.session_state', new_callable=dict)
    def test_check_rest_consumed(self, mock_session_state):
        mock_timer = MagicMock()

        # Case 1: All rest consumed, not resting
        mock_timer.all_rest_consumed.return_value = True
        mock_session_state["status"] = "Working"
        mock_session_state["rest_consumed"] = False
        expected_session_state_rest_consumed = False
        expected_return = False

        check = st_front_objects.check_rest_consumed(mock_timer)
        self.assertEqual(mock_session_state["rest_consumed"], expected_session_state_rest_consumed)
        self.assertEqual(check, expected_return)

        # Case 2: Not yet consumed all rest, resting is true
        mock_timer.all_rest_consumed.return_value = False
        mock_session_state["status"] = "Resting"
        expected_session_state_rest_consumed = False
        expected_return = False

        check = st_front_objects.check_rest_consumed(mock_timer)
        self.assertEqual(mock_session_state["rest_consumed"], expected_session_state_rest_consumed)
        self.assertEqual(check, expected_return)

        # Case 3: Not yet consumed all rest, not resting
        mock_timer.all_rest_consumed.return_value = False
        mock_session_state["status"] = "Working"
        expected_session_state_rest_consumed = False
        expected_return = False

        check = st_front_objects.check_rest_consumed(mock_timer)
        self.assertEqual(mock_session_state["rest_consumed"], expected_session_state_rest_consumed)
        self.assertEqual(check, expected_return)

        # Case 4: All rest consumed, resting is true
        mock_timer.all_rest_consumed.return_value = True
        mock_session_state["status"] = "Resting"
        expected_session_state_rest_consumed = True
        expected_return = True

        check = st_front_objects.check_rest_consumed(mock_timer)
        self.assertEqual(mock_session_state["rest_consumed"], expected_session_state_rest_consumed)
        self.assertEqual(check, expected_return)

class TestDisplayTimers(TestCase):
    @patch('frontend.st_front_objects.check_rest_consumed')
    @patch('frontend.st_front_objects.st.empty')
    @patch('frontend.st_front_objects.st.session_state', new_callable=dict)
    def test_display_timers(self, mock_check_rest_cons, mock_st_empty, mock_sessions_state):
        timer_mock = MagicMock()


if __name__ == '__main__':
    unittest_main()
