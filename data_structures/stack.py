from manim import *
import numpy.typing as npt
from typing_extensions import TypeAlias
from element import Element


Vector3D: TypeAlias = npt.NDArray[np.float64]

class StackElement(VGroup):
    def __init__(
            self, 
            height: float=1.3, 
            width: float=2.0, 
            ellipse_height: float=0.3,
            stroke_color: ParsableManimColor=WHITE,
            fill_color: ParsableManimColor=DARKER_GREY,
            fill_opacity: float=0.95
        ):
        self.body_height = height - ellipse_height
        self.ellipse_height = ellipse_height
        arc = Arc(radius=width/2, angle=-PI).set_fill(
            color=fill_color, opacity=fill_opacity
        ).stretch_to_fit_height(ellipse_height/2)
        left_edge = Line(
            arc.get_left() + ellipse_height/5*UP, arc.get_left() + (ellipse_height/5+self.body_height)*UP,
            color=stroke_color
        )
        right_edge = left_edge.copy().shift(width*RIGHT)
        rectangle = Rectangle(height=self.body_height, width=width).next_to(left_edge, buff=0.0)
        ellipse = Ellipse(width=width, height=ellipse_height).set_fill(fill_color, fill_opacity).set_stroke(stroke_color).move_to(left_edge.get_end() + width/2 * RIGHT)
        rectangle = Difference(Difference(rectangle, ellipse), arc).set_fill(fill_color, fill_opacity).set_stroke(None, width=0.0, opacity=0.0)
        super().__init__(arc, left_edge, right_edge, rectangle, ellipse)
        self.center()


class Stack(VGroup):

    def __init__(
            self,
            values: list[any]=None,
            stack_label: str=None,
            stack_label_direction: Vector3D=DOWN,
            stack_label_buff: float=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER,
            stack_label_style: dict={'font_size': 28},
            stack_center: Vector3D=ORIGIN,
            inter_elem_buff: float=0.0,
            max_height: float=config.frame_height*0.9,
            box_style: VMobject=StackElement(),
            content_style: dict={'font_size': 32},
            content_direction: Vector3D=ORIGIN
    ):
        assert isinstance(values, list) and len(values) > 0, \
            "values must be a non-empty list"
        
        super().__init__()
        self.values: list = values
        self.n = len(values)
        if isinstance(box_style, StackElement):
            inter_elem_buff += box_style.ellipse_height*DOWN
            content_direction = content_direction.copy() + box_style.ellipse_height/2*DOWN
        self.elems = [
            Element(
                v,
                None,
                box_style, 
                content_style,
                content_direction
            ) for i, v in enumerate(values)
        ]
        print(inter_elem_buff, content_direction)
        VGroup(self.elems).arrange(UP, buff=inter_elem_buff).move_to(stack_center)
        self.label = Text(
            str(stack_label), **stack_label_style
        ).next_to(self.elems[0], stack_label_direction, stack_label_buff)
        self.stack_center = stack_center
        self.stack_label_direction, self.stack_label_buff = stack_label_direction, stack_label_buff
        self.inter_elem_buff = inter_elem_buff
        self.add_indices = False
        self.max_height = max_height
        self.box_style = box_style
        self.content_style, self.content_direction = content_style, content_direction
        self.add([self.label] if stack_label else [], self.elems)
        old_height = self.height
        self.scale_to_fit_height(min(self.height, max_height))
        self._update_styles_after_scaling(self.height/old_height)

    def _update_styles_after_scaling(self, ratio: float):
        self.box_style.scale(ratio)
        self.content_style['font_size'] = self.content_style.get('font_size', 32)*ratio
        self.inter_elem_buff *= ratio


class TestStack(Scene):
    def construct(self):
        stack = Stack([45, 0, 'ff', -9, 85, 0], 'stack', box_style=StackElement(1.0, 1.5), content_style={'font_size': 20})
        self.add(stack)