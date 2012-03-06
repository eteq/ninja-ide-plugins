import re

from ninja_ide.core.plugin import Plugin

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QAction

_statrtindentrex = re.compile('(\s*)\S')
_whitespacerex = re.compile('\s*')


class LineContinuer(Plugin):

    def initialize(self):
        self.menuapp_s = self.locator.get_service('menuApp')
        self.action = QAction("Indent selection", self)
        self.connect(self.action, SIGNAL("triggered()"), self.replace_text)
        self.menuapp_s.add_action(self.action)

        self.ncols = 72

    @property
    def editor(self):
        return self.locator.get_service('editor').get_editor()

    def replace_text(self):
        cur = self.editor.textCursor()

        cst = cur.selectionStart()
        cend = cur.selectionEnd()
        if cend - cst > 0:
            cur.setPosition(cst, QTextCursor.MoveAnchor)
            cur.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
            cst = cur.position()

            cur.setPosition(cend, QTextCursor.MoveAnchor)
            cur.movePosition(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
            cend = cur.position()

            cur.setPosition(cst, QTextCursor.KeepAnchor)

            oldtext = str(cur.selection().toPlainText())

            #determine indentation string
            indentstr = _statrtindentrex.match(oldtext).group(1)
            lind = len(indentstr)
            spl = _whitespacerex.split(oldtext.replace('\n', ' '))

            strlist = [indentstr]
            lcnt = lind
            for s in spl:
                ls = len(s)

                if lcnt + ls > self.ncols:
                    strlist.append('\n' + indentstr)
                    strlist.append(s)
                    lcnt = lind + ls
                elif lcnt + ls == self.ncols:
                    strlist.append(s)
                    strlist.append('\n' + indentstr)
                    lcnt = lind
                elif s != '':
                    strlist.append(s)
                    strlist.append(' ')
                    lcnt += ls + 1
            if strlist[-1] != s:
                del strlist[-1]
            cur.insertText(''.join(strlist))
