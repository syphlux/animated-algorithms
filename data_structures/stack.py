from manim import *
import numpy.typing as npt
from typing_extensions import TypeAlias
from element import Element


Vector3D: TypeAlias = npt.NDArray[np.float64]

class StackElement(VGroup):
    def __init__(
            self, 
            height: float=1.3, # total height (ellipse height + body height)
            width: float=2.0, 
            ellipse_height: float=0.3,
            stroke_color: ParsableManimColor=WHITE,
            fill_color: ParsableManimColor=DARKER_GREY,
            fill_opacity: float=0.95
        ):
        self.body_height = height - ellipse_height
        self.ellipse_height = ellipse_height
        bottom_arc = Arc(radius=width/2, angle=-PI).set_fill(
            color=fill_color, opacity=fill_opacity
        ).set_stroke(stroke_color).stretch_to_fit_height(ellipse_height/2)
        left_edge = Line(
            bottom_arc.get_left() + ellipse_height/5*UP, 
            bottom_arc.get_left() + (ellipse_height/5+self.body_height)*UP,
            color=stroke_color
        )
        right_edge = left_edge.copy().shift(width*RIGHT)
        top_ellipse = Ellipse(width=width, height=ellipse_height).set_fill(
            fill_color, fill_opacity
        ).set_stroke(stroke_color).move_to(left_edge.get_end() + width/2 * RIGHT)
        rectangle = Rectangle(height=self.body_height, width=width).next_to(left_edge, buff=0.0)
        rectangle = Difference(
            Difference(rectangle, top_ellipse), bottom_arc
        ).set_fill(fill_color, fill_opacity).set_stroke(None, width=0.0, opacity=0.0)
        super().__init__(bottom_arc, left_edge, right_edge, rectangle, top_ellipse)
        self.center()


class Stack(VGroup):

    def __init__(
            self,
            values: list[any]=None,
            stack_label: str=None,
            stack_label_direction: Vector3D=DOWN,
            stack_label_buff: float=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER,
            stack_label_style: dict={'font_size': 28},
            stack_bottom: Vector3D=config.frame_height/2*0.9*DOWN,
            inter_elem_buff: float=0.0,
            max_height: float=config.frame_height*0.9,
            box_style: VMobject=StackElement(),
            content_style: dict={'font_size': 32},
            content_direction: Vector3D=ORIGIN
    ):
        assert isinstance(values, list), "values must be a list"
        
        super().__init__()
        self.values: list = values
        self.n = len(values)
        if isinstance(box_style, StackElement):
            inter_elem_buff += box_style.ellipse_height*DOWN
            content_direction = content_direction.copy() + box_style.ellipse_height/2*DOWN
            self.base = Arc(
                radius=box_style.width/2, angle=-PI, stroke_width=10.0
            ).stretch_to_fit_height(box_style.ellipse_height/2)
        else:
            self.base = VMobject(stroke_width=10.0).start_new_path(ORIGIN)
            for point in [
                box_style.height/2*DOWN, box_style.height/2*DOWN + box_style.width*RIGHT, box_style.width*RIGHT
            ]:
                self.base.add_line_to(point)
        self.elems = [
            Element(
                v,
                None,
                box_style, 
                content_style,
                content_direction
            ) for i, v in enumerate(values)
        ]
        VGroup(self.elems).arrange(UP, buff=inter_elem_buff)
        self.base.next_to(VGroup(self.elems), DOWN, buff=-self.base.height)
        self.label = Text(
            str(stack_label), **stack_label_style
        ).next_to(self.base, stack_label_direction, stack_label_buff)
        self.base.add_to_back
        self.stack_bottom = stack_bottom
        self.stack_label_direction, self.stack_label_buff = stack_label_direction, stack_label_buff
        self.inter_elem_buff = inter_elem_buff
        self.add_indices = False
        self.max_height = max_height
        self.box_style = box_style
        self.content_style, self.content_direction = content_style, content_direction
        self.add(self.elems, [self.label] if stack_label else [], self.base).next_to(stack_bottom, UP, buff=0.0)
        old_height = self.height
        self.scale_to_fit_height(min(self.height, max_height))
        self._update_styles_after_scaling(self.height/old_height)

    def _update_styles_after_scaling(self, ratio: float):
        self.box_style.scale(ratio)
        self.content_style['font_size'] = self.content_style.get('font_size', 32)*ratio
        self.inter_elem_buff *= ratio

    def push(self, value: any, src_pos: Vector3D=None) -> Succession:
        self.values.append(value)
        self.n += 1
        new_elem = Element(
            value, 
            None, 
            self.box_style, 
            self.content_style,
            self.content_direction
        ).next_to(
            self.elems[-1] if self.n > 1 else self.base, 
            UP,
            self.inter_elem_buff if self.n > 1 else -self.base.height
        )
        src_pos = src_pos if src_pos is not None else self.get_corner(UR) + UR
        self.elems.append(new_elem)
        self.add(new_elem)
        self.base.set_z_index(new_elem.z_index+1)
        return FadeIn(new_elem, target_position=src_pos)
    
    def pop(self, dest_pos: Vector3D=None) -> Succession:
        if self.n == 0:
            return Wait(0.5)
        self.values.pop()
        self.n -= 1
        old_elem = self.elems.pop()
        self.remove(old_elem)
        dest_pos = dest_pos if dest_pos is not None else old_elem.get_center() + UR
        return FadeOut(old_elem, target_position=dest_pos)
    

class TestStack(Scene):
    def construct(self):
        stack = Stack([], 'stack', box_style=Square(1), content_style={'font_size': 20})
        self.add(stack)
        self.wait()
        self.play(stack.push(45))
        self.play(stack.push(45))
        self.play(stack.push(45))
        self.play(stack.push(45))
        self.play(stack.push(45))
        