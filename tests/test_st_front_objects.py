from unittest import TestCase, main as unittest_main
from unittest.mock import patch, Mock, MagicMock

from frontend import st_front_objects
from rationalbreaks.timers import RatioNalTimer


class TestRationalTimerStreamlit(TestCase):
    @patch('frontend.st_front_objects.st.cache_resource', lambda x: x)
    def test_init(self):
        timer = st_front_objects.RatioNalTimerStreamlit()
        self.assertIsInstance(timer, RatioNalTimer)

# class TestAlarm(TestCase):
#     @patch('frontend.st_front_objects.st.cache_resource', lambda x: x)
#     def setUp(self):
#         test_alarm = st_front_objects.Alarm()

    # Case 1: default sound
    # @patch('frontend.st_front_objects.st.cache_resource', lambda x: x)
    # # @patch('frontend.st_front_objects.Alarm.create_player')
    # @patch.object(st_front_objects.Alarm, 'create_player')
    # @patch('frontend.st_front_objects.path')
    # def test_init(self, mock_player, mock_path):
    #     mocked_path_value = "mocked_path"
    #     mocked_player_value = "mocked_player"
    #     mock_path.join.return_value = mocked_path_value
    #     mock_player.return_value = mocked_player_value
    #     default_sound_path_elements = ("resources", "ring_1.wav")
    #
    #     alarm = st_front_objects.Alarm()
    #
    #     self.assertEqual(alarm.soundfile, mocked_path_value)
    #     self.assertEqual(alarm.player, mocked_player_value)
    #     mock_path.join.assert_called_with(*default_sound_path_elements)
    #     mock_player.assert_called_once()

    # def test_init(self):
    #     pass

    # @patch('frontend.st_front_objects.sa.WaveObject.from_wave_file')
    # def test_create_player(self):
    #     pass

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
        expected_val_refresh = True
        mock_session_state["alert"] = {"muted": True}

        self.control.continue_work()

        self.assertEqual(mock_session_state["status"], expected_val_status)
        self.assertEqual(mock_session_state["alert"]["muted"], expected_val_muted)
        self.assertEqual(mock_session_state["refresh"], expected_val_refresh)
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
        expected_val_refresh = True
        mock_session_state["alert"] = {"muted": False}

        self.control.mute_alarm()
        self.assertEqual(mock_session_state["refresh"], expected_val_refresh)
        self.assertEqual(mock_session_state["alert"]["muted"], expected_val_muted)
        mock_st_rerun.assert_called_once()


if __name__ == '__main__':
    unittest_main()
