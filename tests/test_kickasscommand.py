import sublime
import sys
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch, create_autospec

version = sublime.version()

if version < '3000':
    # st2
    kickassbuild = sys.modules["kickass_build"]
else:
    # st3
    kickassbuild = sys.modules["SublimeKickAssemblerC64.kickass_build"]


class TestKickAssCommand(TestCase):

    @patch('platform.system', return_value='Windows')
    def test_commandText_returncommantext(self, platform_mock):
        settings_mock = create_autospec(kickassbuild.SublimeSettings)
        target = kickassbuild.KickAssCommand('TestCommandText', False, False, 'build')
        actual = target.CommandText
        self.assertEqual('TestCommandText', actual)

if __name__ == '__main__':
    unittest.main()