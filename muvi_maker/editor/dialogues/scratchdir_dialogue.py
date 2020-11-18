from muvi_maker import main_logger, mv_scratch_key, set_scratch_dir
from muvi_maker.editor.dialogues.base_dialogue import BaseDialogue
import tkinter as tk
import os


logger = main_logger.getChild(__name__)


class ScratchDirDialogue(BaseDialogue):
    """Only to be called when the scratch directory doesn't exist or wasn't given!"""

    def __init__(self, parent):
        logger.debug(f'Calling ScratchDirDialogue')

        mv_scratch = os.environ.get(mv_scratch_key, 'None')
        msg = ''
        if not os.path.isdir(mv_scratch):
            if isinstance(mv_scratch, type(None)):
                msg = 'No working directory given!'
            if isinstance(mv_scratch, str):
                msg = f'{mv_scratch} is not a directory!'
        else:
            logger.warning(f'Called ScratchDirDialogue but {mv_scratch} is a directory!')

        BaseDialogue.__init__(self,
                              parent,
                              title='select working directory',
                              def_msg=msg,
                              button_text='OK',
                              insert="Enter working directory")

    def button_action(self):
        scr = self.entry.get()
        if os.path.isdir(scr):
            self.set_scratch_and_exit()
        else:
            self.msg.set(f'\"{scr}\" is not a directory!')

    def set_scratch_and_exit(self):
        """Sets the scratch directory to input"""
        set_scratch_dir(self.entry.get())
        self.destroy()