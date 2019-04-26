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


class TestKickAssCommandFactory(TestCase):

    @patch('platform.system', return_value='Windows')
    def test_getExt_platformiswindows_returnbat(self, platform_mock):
        settings_mock = create_autospec(kickassbuild.SublimeSettings)
        target = kickassbuild.KickAssCommandFactory(settings_mock)
        actual = target.getExt()
        self.assertEqual('bat', actual)

    @patch('platform.system', return_value='Linux')
    def test_getExt_platformislinux_returnsh(self, platform_mock):
        settings_mock = create_autospec(kickassbuild.SublimeSettings)
        target = kickassbuild.KickAssCommandFactory(settings_mock)
        actual = target.getExt()
        self.assertEqual('sh', actual)

    @patch('platform.system', return_value='Darwin')
    def test_getExt_platformisDarwin_returnsh(self, platform_mock):
        settings_mock = create_autospec(kickassbuild.SublimeSettings)
        target = kickassbuild.KickAssCommandFactory(settings_mock)
        actual = target.getExt()
        self.assertEqual('sh', actual)

if __name__ == '__main__':
    unittest.main()