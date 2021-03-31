import abc

import gizeh
import numpy as np
import matplotlib.cm as cm

from muvi_maker import main_logger
from .base_picture import BasePicture

logger = main_logger.getChild(__name__)


class BaseForm(BasePicture, abc.ABC):

    def __init__(self, sound_dict, param_info, screen_size):
        super(BaseForm, self).__init__(sound_dict, param_info, screen_size)

        self.surface = None

        # --------------------- Position ----------------------- #
        self.center = param_info.get('center', [screen_size[0] / 2, screen_size[1] / 2])

        # ---------------------- Radius ------------------------ #
        radius_sound_name = param_info['radius']
        max_radius = float(param_info.get('max_radius', min(self.screen_size) / 2))
        radius_smooth = int(param_info.get('radius_smooth', 1))

        radius_sound = self.sound_dict[radius_sound_name]
        radius_power = radius_sound.get_power()
        radius = radius_power / max(radius_power) * max_radius

        if radius_smooth > 1:
            rl = list()
            for i in range(len(radius)):
                h, b = np.histogram(radius[i:i + radius_smooth])
                rl.append(b[np.argmax(h)])
            radius = np.array(rl)

        self.radius = radius

        # ---------------------- Colour ------------------------ #
        colour_sound_name = param_info['colour']
        colour_cmap = param_info.get('cmap', 'plasma')
        colour_smooth = int(param_info.get('colour_smooth', 1))

        colour_sound = self.sound_dict[colour_sound_name]
        colour_chroma = colour_sound.get_chroma()
        cmap = cm.get_cmap(colour_cmap)

        max_inds = [np.argmax(c) / len(c) for c in colour_chroma]

        if colour_smooth > 1:
            cl = list()
            for i in range(len(max_inds)):
                h, b = np.histogram(max_inds[i:i + colour_smooth])
                cl.append(b[np.argmax(h)])
            color = [cmap(cli) for cli in cl]

        else:
            color = [cmap(imi) for imi in max_inds]

        self.color = color

    def create_surface(self):
        self.surface = gizeh.Surface(int(self.screen_size[0] * 2), int(self.screen_size[1] * 2))

    def make_frame_per_frame(self, ind):
        self.create_surface()
        self.draw(ind)
        return self.surface.get_npimage(transparent=True)

    @abc.abstractmethod
    def draw(self, ind):
        pass