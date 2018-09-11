"""
Sublime Text plugin for KickAssembler development to manager debuging with vice.
"""
import json
import logging
import os
import uuid

import sublime
import sublime_plugin

breakpointLists = BreakpointLists()

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

def get_selected_line(view):
    sel = view.sel()[0]
    line = view.line(sel)
    lineNum = view.rowcol(line.a)[0] + 1
    return (line, lineNum)

def should_track(view):
    return view.settings().get("language", None) is not None

def is_valid_scope(view):
    """
    checks selection in given view to determine
    scope and compares against supported scopes
    defined for this language
    """
    if not should_track(view):
        return False
    language = view.settings().get("language", None)
    supported_scopes = language.get("scopes")
    # if no scopes are specified, any point is ok
    if len(supported_scopes) == 0:
        return True
    # NOTE - only gets scope of first selection
    scope = view.scope_name(view.sel()[0].a).split()
    matching = [s for s in supported_scopes if s in scope]
    if len(matching) > 0:
        return True
    return False

def if_valid_scope(fn):
    def wrapper(*args, **kwargs):
        # NOTE: assumes first arg is
        # self for a BreakpointList
        # TODO - make safer
        if is_valid_scope(args[0].view):
            return fn(*args, **kwargs)
        return False
    return wrapper

class MissingRegionException(Exception):
    pass

class Breakpoint(object):
    """
    keeps track of a breakpoint's config, including the
    line associated with the breakpoint
    """
    def __init__(self, view, line):
        # TODO - use beginning of line
        print("breakpoint added for line %s" % line)
        self.enabled = True
        self.id = str(uuid.uuid4())
        self.condition = None
#        viewSettings = view.settings()
#        self.enabledCondition = viewSettings.get("enabled")
#        self.disabledCondition = viewSettings.get("disabled")
#        self.debugger = viewSettings.get("debugger")
        self.draw(view, line)

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def draw(self, view, line=None, hidden=False):
        # if no line was provided, try to use
        # the existing breakpoint region as the
        # line to draw at
        if line is None:
            # TODO - catch MissingRegionException?
            line = self.getIcon(view)
            self.clear(view)

        # enabled, no conditional
        color = "keyword"
        # if disabled
        if self.enabled == False:
            color = "comment"
        # if conditional
        elif self.condition is not None:
            color = "string"
        # hidden beats all
        if hidden:
            color = ""
        view.add_regions(self.id, [line], color, "circle", sublime.HIDDEN | sublime.PERSISTENT)

    def clear(self, view):
        view.erase_regions(self.id)

    def destroy(self, view):
        self.clear(view)

    def isContained(self, view, line):
        bp = None
        try:
            bp = self.getIcon(view)
        except (MissingRegionException):
            print("Couldnt find breakpoint region... must've been undo'd from history")
            return
        return line.contains(bp)

    def getIcon(self, view):
        regions = view.get_regions(self.id)
        if not len(regions):
            raise MissingRegionException()
        return regions[0]


#
class BreakpointList(object):
    def __init__(self, view):
        self.view = view
        self.list = []

    def add(self, line):
        b = Breakpoint(self.view, line)
        self.list.append(b)
        return b

    def remove(self, line):
        b = self.get(line)
        if not b:
            raise MissingBreakpointException("No breakpoint at line %s, region %s" % (get_line_num(line), line))
        b.destroy(self.view)
        self.list.remove(b)

    def get(self, line):
        for b in self.list:
            if b.isContained(self.view, line):
                print("line", line, "contains bp", b.id)
                return b


class BreakpointLists(object):
    def __init__(self):
        self.lists = {}

    def get(self, view):
        l = self.lists.get(view.id(), None)
        if l:
            return l
#        logging.debug("creating bp list for view", view.id())
        l = BreakpointList(view)
        self.lists[view.id()] = l
        return l

class KickassDebuggerAddCommand(sublime_plugin.TextCommand):
#    @if_valid_scope
    def run(self, edit, **args):
        l = breakpointLists.get(self.view)
        line, lineNum = get_selected_line(self.view)
#        logging.debug("add at", lineNum)
        l.add(line)

#   @if_valid_scope
    def is_enabled(self):
        l = breakpointLists.get(self.view)
        line, lineNum = get_selected_line(self.view)
        b = l.get(line)
        return not b

class KickassDebuggerRemoveCommand(sublime_plugin.TextCommand):
#    @if_valid_scope
    def run(self, edit, **args):
        l = breakpointLists.get(self.view)
        line, lineNum = get_selected_line(self.view)
#        logging.debug("remove at", lineNum)
        l.remove(line)

#    @if_valid_scope
    def is_enabled(self):
        l = breakpointLists.get(self.view)
        line, lineNum = get_selected_line(self.view)
        b = l.get(line)
        return bool(b)


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

def plugin_loaded():
    """Plugin entry point"""
    debugger = KickassDebugger()
    debugger.load()
    logging.info('KickassDebugger loaded.')
