from manim import *
import numpy.typing as npt
from typing_extensions import TypeAlias


Vector3D: TypeAlias = npt.NDArray[np.float64]

class Element(VGroup):
    def __init__(
            self, 
            value: any, 
            label: any=None, 
            box_style: VMobject=Square(side_length=1),
            content_style: dict={'font_size': 32},
            content_direction: Vector3D=ORIGIN,
            label_style: dict={'font': 'Consolas', 'font_size': 24, 'color': BLUE},
            label_direction: Vector3D=DOWN,
            label_buff: float=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER,
    ):
        super().__init__()
        self.value = value
        self.box = box_style.copy()
        self.content = Text(str(value), **content_style).move_to(self.box.get_center() + content_direction)
        self.content.scale_to_fit_width(min(self.content.width, self.box.width*0.8))
        self.label = Text(str(label), **label_style)
        self.label.scale_to_fit_width(min(self.label.width, self.box.width))
        self.label.next_to(self.box, label_direction, label_buff)
        self.add([self.box, self.content] + ([self.label] if label is not None else []))


class TestElement(Scene):
    def construct(self):
        top = Ellipse(height=0.3)
        bot = Arc(radius=1, angle=-PI).shift(DOWN*0.5).stretch_to_fit_height(0.15)

        left_edge = Line(top.get_left(), bot.get_corner(UL))
        right_edge = Line(top.get_right(), bot.get_corner(UR))
        puce = VGroup(top, bot, left_edge, right_edge).set_stroke(color=WHITE).set_color(BLACK).set_opacity(1.0)
        self.add(puce)
        elem = Element(45, label_direction=UP, box_style=puce, content_direction=DOWN*0.15).shift(UP*2)
        elem2 = elem.copy().next_to(elem, UP, buff=-0.3)
        self.add(elem, elem2)

        
