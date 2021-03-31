import gizeh

from muvi_maker import main_logger
from .star import Star
from .base_picture import BasePicture


logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('star_with_bounce')
class StarWithBounce(Star):

    def __init__(self, sound_dict, param_info, screen_size):

        super().__init__(sound_dict, param_info, screen_size)

        self.multiplicity = int(param_info.get('multiplicity', 3))
        self.radius_factor = float(param_info.get('radius_factor', 1))
        self.radius_add = float(param_info.get('radius_add', 2))
        self.max_stroke_width = float(param_info.get('max_stroke_width', 8))
        self.min_stroke_width = float(param_info.get('min_stroke_width', 1))
        self.stroke_width_decline_order = float(param_info.get('stroke_width_decline_order', 2))

    def stroke_width(self, j):
        b = (self.min_stroke_width - self.max_stroke_width) / \
            (1 - (self.multiplicity + 1) ** self.stroke_width_decline_order)
        a = self.max_stroke_width - b
        return a * j ** self.stroke_width_decline_order + b

    def draw(self, ind):
        super(StarWithBounce, self).draw(ind)

        for i in range(self.multiplicity):
            j = i + 1
            if ind > j:
                outer_star1 = gizeh.star(
                    radius=self.radius[ind - j] * (self.radius_add + j) * self.radius_factor,
                    nbranches=10,
                    xy=self.center,
                    fill=None,
                    stroke=self.color[ind - j],
                    stroke_width=self.stroke_width(j),
                )
                outer_star1.draw(self.surface)