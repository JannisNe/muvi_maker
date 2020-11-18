import tkinter as tk
from muvi_maker import main_logger
from muvi_maker.editor.dialogues import OpenProjectDialogue, NewFileDialogue

logger = main_logger.getChild(__name__)


class Filemenu(tk.Menu):

    def __init__(self, menubar):
        logger.debug('setting up filemenu')
        tk.Menu.__init__(self, menubar)
        self._setup_commands()

    def _setup_commands(self):
        logger.debug('setting up commands')
        self.add_command(label='New Project', command=self._new_project)
        self.add_command(label='Open Project', command=self._open_project)
        self.add_command(label='Save Project', command=self._save_project)

    def _new_project(self):
        NewFileDialogue(self)

    def _open_project(self):
        OpenProjectDialogue(self)

    def _save_project(self):
        pass

    # def get_project_handler(self):
    #     return self.master.get_project_handler()
    #
    # def set_project_handler(self, project_handler):
    #     self.master.set_project_handler(project_handler)