"""
Sublime Text plugin for KickAssembler development for displaying information
about certain addresses (VIC/SID registers for example)
"""
import json
import logging
import os

import sublime
import sublime_plugin


TOOLTIP = """<style>%(css)s</style>
<b><u>%(title)s</u></b><br>
<b>%(name)s</b><br>
%(desc)s"""

NUMBER_TOOLTIP = """<style>{css}</style>
<b>${value:02X}</b><br>
<b>%{value:08b}</b><br>
<b>{value}</b><br>"""


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


class KickAssTooltip:
    """
    Name space/utility class for reading settings/definitions
    """
    help_map = {}
    css_file = ''
    scopes = []

    def __init__(self):
        self.log_level = 'info'
        self.settings = None
        self.help_directories = []

        self._register_settings()

    def _register_settings(self):
        """
        Set the settings object and register callback for settings/plugin
        changes.
        """
        self.settings = sublime.load_settings("KickassTooltips.sublime-settings")
        self.settings.add_on_change('reload', self.load)

    def load(self):
        """Load settings and refresh cache table (help_map)"""
        self.log_level = self.settings.get('log_level')
        setup_logging(self.log_level)

        plug_path = sublime.packages_path()
        default_css = os.path.join(plug_path, 'Kick Assembler (C64)/css/default.css')

        KickAssTooltip.css_file = self.settings.get('css_file', default_css)

        KickAssTooltip.scopes = self.settings.get('scopes', [])

        self.help_directories = self.settings.get('help_directories', [])
        self._load_definition()

    def _load_definition(self):
        """
        Read definition from json files and place them in class variable
        help_map
        """
        for dirname in self.help_directories:
            if not os.path.isabs(dirname):
                dirname = os.path.join(sublime.packages_path(), dirname)

            for fname in os.listdir(dirname):
                logging.debug('Loading %s', fname)
                try:
                    with open(os.path.join(dirname, fname),
                              encoding='utf8') as fileobject:
                        try:
                            data = json.load(fileobject)
                        except ValueError as exc:
                            logging.error('Error in JSON file: %s, %s',
                                          fname, exc.message)
                            continue
                    KickAssTooltip.help_map.update(data)
                except EnvironmentError:
                    logging.error('Cannot access file: %s', fname)

        logging.debug('Help map:\n%s', KickAssTooltip.help_map)


class KickassTooltipsCommand(sublime_plugin.ViewEventListener):
    """
    Event listener class for specific view
    """

    def on_hover(self, point, hover_zone):
        """
        Mouse over text object. Check, if there is appropriate data to be
        displayed about the object.
        """

        if hover_zone != sublime.HOVER_TEXT:
            return

        selection = self.view.scope_name(self.view.sel()[0].begin())

        if KickAssTooltip.scopes[0] not in selection:
            return

        text = self.view.substr(self.view.word(point))

        logging.debug('Text under mouse pointer: %s', text)

        if text.lower() in KickAssTooltip.help_map:
            help_message = KickAssTooltip.help_map[text.lower()]
            logging.debug('Help message: %s', help_message)
            html_message = TOOLTIP % {'css': KickAssTooltip.css_file,
                                      'title': text,
                                      'name': help_message['name'],
                                      'desc': help_message['descr']}
            self.show_tooltip(html_message, point)
            return

        val = None
        if "constant.numeric.hex" in selection:
            val = int(text, 16)

        if "constant.numeric.bin" in selection:
            val = int(text, 2)

        if "constant.numeric.decimal" in selection:
            val = int(text)

        if val is not None:
            self.show_numeric_tooltip(val, point)

    def show_numeric_tooltip(self, val, point):
        html_message = NUMBER_TOOLTIP.format(css=KickAssTooltip.css_file,
                                             value=val)
        self.show_tooltip(html_message, point)

    def show_tooltip(self, html_message, point):
        logging.debug('HTML tooltip:\n%s', html_message)
        self.view.show_popup(''.join(html_message),
                            flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                            location=point,
                            max_width=600,
                            on_navigate=self.on_navigate)

    def on_navigate(self):
        """Hide popup on click/escape"""
        self.view.hide_popup()
        logging.debug('on_navigate')


def plugin_loaded():
    """Plugin entry point"""
    tooltip = KickAssTooltip()
    tooltip.load()
    logging.info('KickAssTooltips loaded.')
