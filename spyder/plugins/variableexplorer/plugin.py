# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
Variable Explorer Plugin.
"""

# Local imports
from spyder.api.plugins import Plugins, SpyderDockablePlugin
from spyder.api.shellconnect.mixins import ShellConnectMixin
from spyder.api.translations import get_translation
from spyder.plugins.variableexplorer.confpage import (
    VariableExplorerConfigPage)
from spyder.plugins.variableexplorer.widgets.main_widget import (
    VariableExplorerWidget)

# Localization
_ = get_translation('spyder')


class VariableExplorer(SpyderDockablePlugin, ShellConnectMixin):
    """
    Variable explorer plugin.
    """
    NAME = 'variable_explorer'
    REQUIRES = [Plugins.IPythonConsole, Plugins.Preferences]
    TABIFY = None
    WIDGET_CLASS = VariableExplorerWidget
    CONF_SECTION = NAME
    CONF_FILE = False
    CONF_WIDGET_CLASS = VariableExplorerConfigPage
    DISABLE_ACTIONS_WHEN_HIDDEN = False

    # ---- SpyderDockablePlugin API
    # ------------------------------------------------------------------------
    def get_name(self):
        return _('Variable explorer')

    def get_description(self):
        return _('Display, explore load and save variables in the current '
                 'namespace.')

    def get_icon(self):
        return self.create_icon('dictedit')

    def register(self):
        # Plugins
        ipyconsole = self.get_plugin(Plugins.IPythonConsole)
        preferences = self.get_plugin(Plugins.Preferences)

        # Preferences
        preferences.register_plugin_preferences(self)

        # Register IPython console.
        self.register_ipythonconsole(ipyconsole)

        self.get_widget().sig_free_memory_requested.connect(
            self.sig_free_memory_requested)

    def unregister(self):
        # Plugins
        ipyconsole = self.get_plugin(Plugins.IPythonConsole)

        # Unregister IPython console.
        self.unregister_ipythonconsole(ipyconsole)

    # ---- Public API
    # ------------------------------------------------------------------------
    def current_widget(self):
        """
        Return the current widget displayed at the moment.

        Returns
        -------
        spyder.plugins.plots.widgets.namespacebrowser.NamespaceBrowser
        """
        return self.get_widget().current_widget()

    def add_shellwidget(self, shellwidget, external):
        """
        Add a new shellwidget to be registered.

        This function registers a new NamespaceBrowser for browsing variables
        in the shellwidget.

        Parameters
        ----------
        shellwidget: spyder.plugins.ipyconsole.widgets.shell.ShellWidget
            The shell widget.
        external: bool
            True if the kernel is external
        """
        self.get_widget().add_shellwidget(shellwidget)

        if external:
            shellwidget.set_namespace_view_settings()
            shellwidget.refresh_namespacebrowser()
