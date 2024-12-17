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
    @patch('frontend.st_front_objects.open')
    @patch('frontend.st_front_objects.b64encode')
    def setUp(self, b64enc_mock, mock_open):
        mocked_file = MagicMock()
        mocked_file.read.return_value = "Read audio file data"
        mock_b64 = MagicMock()
        mock_b64.decode.return_value = "Decoded b64"  # Expeted init value
        b64enc_mock.return_value = mock_b64
        mock_open.return_value = mocked_file

        self.alarm = st_front_objects.Alarm()

    def test_init_values(self):
        default_path_elements = "resources", "ring_1.wav"
        expected_path = path.join(*default_path_elements)
        expected_audio_base64 = "Decoded b64"  # from setUP

        self.assertEqual(self.alarm.soundfile, expected_path)
        self.assertEqual(self.alarm.audio_base64, expected_audio_base64)

    @patch('frontend.st_front_objects.open')
    @patch('frontend.st_front_objects.b64encode')
    def test_encode_audio(self, b64enc_mock, mock_open):
        mocked_file = MagicMock()
        mock_file_read_value = "Read audio file data"
        mocked_file.read.return_value = mock_file_read_value
        mock_b64 = MagicMock()
        decoded_value = "Decoded b64"
        mock_b64.decode.return_value = decoded_value  # Expeted init value
        b64enc_mock.return_value = mock_b64
        mock_open.return_value.__enter__.return_value = mocked_file

        returned_value = self.alarm.encode_audio()

        mock_open.assert_called_with(self.alarm.soundfile, "rb")
        mocked_file.read.assert_called_once()
        b64enc_mock.assert_called_with(mock_file_read_value)
        mock_b64.decode.assert_called_once()
        self.assertEqual(returned_value, decoded_value)

    @patch('frontend.st_front_objects.st.session_state')
    def test_trigger_audio(self, mock_session_state):
        # Case 1 play_sound is True, muted is False, rest_consumed is True -> true
        # This is the only true case!
        mock_session_state.alert = {"play_sound": True, "muted": False}
        mock_session_state.rest_consumed = True
        expected_value = "true"
        returned_value = self.alarm.trigger_audio()
        self.assertEqual(returned_value, expected_value)

        # Case 2: play_sound is True, muted is True, rest_consumed is False -> false
        mock_session_state.alert = {"play_sound": True, "muted": True}
        mock_session_state.rest_consumed = False
        expected_value = "false"
        returned_value = self.alarm.trigger_audio()
        self.assertEqual(returned_value, expected_value)

        # Case 3: play_sound is False, muted is True, rest_consumed is True -> false
        mock_session_state.alert = {"play_sound": False, "muted": True}
        mock_session_state.rest_consumed = True
        expected_value = "false"
        returned_value = self.alarm.trigger_audio()
        self.assertEqual(returned_value, expected_value)

        # Case 4: play_sound is False, muted is False, rest_consumed is True -> false
        mock_session_state.alert = {"play_sound": False, "muted": False}
        mock_session_state.rest_consumed = True
        expected_value = "false"
        returned_value = self.alarm.trigger_audio()
        self.assertEqual(returned_value, expected_value)

        # Case 5: play_sound is True, muted is False, rest_consumed is False -> false
        mock_session_state.alert = {"play_sound": True, "muted": False}
        mock_session_state.rest_consumed = False
        expected_value = "false"
        returned_value = self.alarm.trigger_audio()
        self.assertEqual(returned_value, expected_value)

        # Case 6: play_sound is False, muted is True, rest_consumed is False -> false
        mock_session_state.alert = {"play_sound": False, "muted": True}
        mock_session_state.rest_consumed = False
        expected_value = "false"
        returned_value = self.alarm.trigger_audio()
        self.assertEqual(returned_value, expected_value)
##
        # Case 7: play_sound is True, muted is True, rest_consumed is True -> false
        mock_session_state.alert = {"play_sound": True, "muted": True}
        mock_session_state.rest_consumed = True
        expected_value = "false"
        returned_value = self.alarm.trigger_audio()
        self.assertEqual(returned_value, expected_value)

        # Case 8: play_sound is False, muted is False, rest_consumed is False -> false
        mock_session_state.alert = {"play_sound": False, "muted": False}
        mock_session_state.rest_consumed = False
        expected_value = "false"
        returned_value = self.alarm.trigger_audio()
        self.assertEqual(returned_value, expected_value)

    @patch('frontend.st_front_objects.st.components.v1.html')
    @patch('frontend.st_front_objects.st.session_state')
    # @patch.object(st_front_objects.Alarm, 'trigger_audio')
    def test_load_player_html(self, mock_session_state, st_html_mock):
        # Case 1: default refresh; trigger is true -> alarm will play
        mock_session_state.alert = {"play_sound": True, "muted": False}
        mock_session_state.rest_consumed = True
        alarm = st_front_objects.Alarm()
        expected_string = \
            f"""
            <script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js">
            </script>
            <script>
            const sound = new Howl({{
                src: ['data:audio/wav;base64,{self.alarm.audio_base64}']
            }});
    
            // Monitor Streamlit for playback trigger
            const checkPlayback = () => {{
                const playAudio = true;
                if (playAudio) {{
                    sound.play();
                }}
            }};
    
            // Poll the server for updates every "refresh_frequency" ms
            setInterval(checkPlayback, 1000);
            </script>
            """
        alarm.load_player_html()
        st_html_mock.assert_called_with(expected_string, height=1)

        # Case 2: default refresh; trigger is false -> alarm will NOT play
        mock_session_state.alert = {"play_sound": True, "muted": False}
        mock_session_state.rest_consumed = False
        alarm = st_front_objects.Alarm()
        expected_string = \
            f"""
            <script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js">
            </script>
            <script>
            const sound = new Howl({{
                src: ['data:audio/wav;base64,{self.alarm.audio_base64}']
            }});
    
            // Monitor Streamlit for playback trigger
            const checkPlayback = () => {{
                const playAudio = false;
                if (playAudio) {{
                    sound.play();
                }}
            }};
    
            // Poll the server for updates every "refresh_frequency" ms
            setInterval(checkPlayback, 1000);
            </script>
            """
        alarm.load_player_html()
        st_html_mock.assert_called_with(expected_string, height=1)

        # Case 3: set refresh value; trigger is true -> alarm will play
        mock_session_state.alert = {"play_sound": True, "muted": False}
        mock_session_state.rest_consumed = True
        alarm = st_front_objects.Alarm()
        expected_string = \
            f"""
            <script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js">
            </script>
            <script>
            const sound = new Howl({{
                src: ['data:audio/wav;base64,{self.alarm.audio_base64}']
            }});
    
            // Monitor Streamlit for playback trigger
            const checkPlayback = () => {{
                const playAudio = true;
                if (playAudio) {{
                    sound.play();
                }}
            }};
    
            // Poll the server for updates every "refresh_frequency" ms
            setInterval(checkPlayback, 500);
            </script>
            """
        alarm.load_player_html(refresh_frequency=500)
        st_html_mock.assert_called_with(expected_string, height=1)


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
