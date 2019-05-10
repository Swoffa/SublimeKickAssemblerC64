import sublime
import sys
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch, create_autospec
from module_references import kickassbuild

class TestKickAssCommand(TestCase):

    @patch('platform.system', return_value='Windows')
    def test_commandText_returncommantext(self, platform_mock):
        settings_mock = create_autospec(kickassbuild.SublimeSettings)
        target = kickassbuild.KickAssCommand('TestCommandText', False, False, 'build')
        actual = target.CommandText
        self.assertEqual('TestCommandText', actual)

    #TODO: updateEnvVars
    #TODO: constructor

if __name__ == '__main__':
    unittest.main()