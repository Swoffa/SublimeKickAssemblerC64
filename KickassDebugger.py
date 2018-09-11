"""
Sublime Text plugin for KickAssembler development to manager debuging with vice.
"""
import json
import logging
import os

import sublime
import sublime_plugin


def setup_logging(level):
    """Set up logger level"""
    level_map = {'debug': logging.DEBUG,
                 'info': logging.INFO,
                 'warning': logging.WARNING,
                 'error': logging.ERROR,
                 'critical': logging.CRITICAL}
    logging.basicConfig(format='%(levelname)s: %(message)s')
    log = logging.getLogger()
    # set level on previously created root logger, otherwise calling
    # basicConfig again with new level will have no effect.
    log.setLevel(level_map.get(level, logging.INFO))


class KickassDebugger:
    """
    Name space/utility class for reading settings/definitions
    """
    breakpoints_file = ''

    def __init__(self):
        self.log_level = 'info'
        self.settings = None
        self._register_settings()

    def _register_settings(self):
        """
        Set the settings object and register callback for settings/plugin
        changes.
        """
        self.settings = sublime.load_settings("KickassDebugger.sublime-settings")
        self.settings.add_on_change('reload', self.load)

    def load(self):
        """Load settings and refresh cache table (help_map)"""
        self.log_level = self.settings.get('log_level')
        setup_logging(self.log_level)

        plug_path = sublime.packages_path()
        default_breakpoints_file = os.path.join(plug_path, 'breakpoints.txt')

        KickassDebugger.breakpoints_file = self.settings.get('breakpoints_file', default_breakpoints_file)

class KickassDebuggerCommand(sublime_plugin.ViewEventListener):
    """
    Event listener class for specific view
    """

    def on_hover(self, point, hover_zone):
        """
        Mouse over text object. Check, if there is appropriate data to be
        displayed about the object.
        """

        return


def plugin_loaded():
    """Plugin entry point"""
    debugger = KickassDebugger()
    debugger.load()
    logging.info('KickassDebugger loaded.')
