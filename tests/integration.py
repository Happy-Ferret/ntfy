from os import devnull
from unittest import TestCase, main
from sys import version_info, modules

from mock import patch, mock_open, MagicMock

from ntfy.cli import main as ntfy_main


py = version_info.major

class TestIntegration(TestCase):
    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.cli.json.load')
    @patch('ntfy.backends.pushover.requests.post')
    def test_pushover(self, mock_jsonload, mock_post):
        mock_jsonload.return_value = {
            'backends': ['pushover'],
            'pushover': {'user_key': MagicMock()},
        }
        ntfy_main(['send', 'foobar'])

    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.cli.json.load')
    @patch('ntfy.backends.pushbullet.requests.post')
    def test_pushbullet(self, mock_jsonload, mock_post):
        mock_jsonload.return_value = {
            'backends': ['pushbullet'],
            'pushbullet': {'access_token': MagicMock()},
        }
        ntfy_main(['send', 'foobar'])

    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.cli.json.load')
    def test_linux(self, mock_jsonload):
        old_dbus = modules.get('dbus')
        modules['dbus'] = MagicMock()
        try:
            mock_jsonload.return_value = {
                'backends': ['linux'],
            }
            ntfy_main(['send', 'foobar'])
        finally:
            if old_dbus is not None:
                modules['dbus'] = old_dbus

    @patch(('__builtin__' if py == 2 else 'builtins') +'.open', mock_open())
    @patch('ntfy.cli.json.load')
    def test_darwin(self, mock_jsonload):
        old_foundation = modules.get('Foundation')
        old_objc = modules.get('objc')
        old_appkit = modules.get('AppKit')
        modules['Foundation'] = MagicMock()
        modules['objc'] = MagicMock()
        modules['AppKit'] = MagicMock()
        try:
            mock_jsonload.return_value = {
                'backends': ['darwin'],
            }
            ntfy_main(['send', 'foobar'])
        finally:
            if old_foundation is not None:
                modules['Foundation'] = old_foundation
            if old_objc is not None:
                modules['objc'] = old_objc
            if old_appkit is not None:
                modules['AppKit'] = old_appkit


if __name__ == '__main__':
    main()