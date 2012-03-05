from ninja_ide.core.plugin import Plugin

from PyQt4.QtGui import QAction
from PyQt4.QtCore import SIGNAL


class LineContinuer(Plugin):

    def initialize(self):
        self.menuapp_s = self.locator.get_service('menuApp')
        self.action = QAction("Indent selection", self)
        self.connect(self.action, SIGNAL("triggered()"), self.action_click)
        self.menuapp_s.add_action(self.action)

        self.ncols = 72

    def action_click(self):
        print 'msg'
