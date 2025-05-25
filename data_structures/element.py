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
            content_style: dict={},
            content_direction: Vector3D=ORIGIN,
            label_style: dict={},
            label_direction: Vector3D=DOWN,
            label_buff: float=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER,
            fit_label_to_width: bool=True
    ):
        super().__init__()
        self.value = value
        self.box = box_style.copy()
        self.content_style = {'font_size': 32}
        self.content_style.update(content_style)
        self.content = Text(str(value), **self.content_style).move_to(self.box.get_center() + content_direction)
        self.content.scale_to_fit_width(min(self.content.width, self.box.width*0.8))
        self.label_style = {'font': 'Consolas', 'font_size': 24, 'color': BLUE}
        self.label_style.update(label_style)
        self.label = Text(str(label), **self.label_style)
        self.show_label = label is not None
        if fit_label_to_width:
            self.label.scale_to_fit_width(min(self.label.width, self.box.width))
        self.label.next_to(self.box, label_direction, label_buff)
        self.add(self.box, self.content, [self.label] if self.show_label else [])

    def replace_value(self, new_value: any):
        self.value = new_value
        self.content.text = str(new_value)
        return Transform(self.content, Text(
            str(new_value), **self.content_style).move_to(self.content)
        )

    def highlight(
            self,
            color: ParsableManimColor=YELLOW,
            stroke_color: ParsableManimColor=YELLOW,
            font_color: ParsableManimColor=BLACK,
            label_color: ParsableManimColor=YELLOW,
            fill_opacity: float=0.8,
            scale_ratio: float=1.2,
            restore: bool=True
    ):
        self.save_state()
        anim_group = AnimationGroup(
            self.box.animate.set_z_index(float('inf')).set_color(
                color
            ).set_stroke(color=stroke_color).set_opacity(fill_opacity).scale(scale_ratio),
            self.content.animate.set_z_index(float('inf')).set_color(
                font_color
            ).scale(scale_ratio),
            [self.label.animate.set_z_index(float('inf')).set_color(
                label_color
            ).scale(scale_ratio)] if self.show_label else []
        )
        return Succession(
            anim_group, *[Wait(0.2), Restore(self)] if restore else []
        )


class TestElement(Scene):
    def construct(self):
        elem = Element(45).shift(UP)
        self.play(Create(elem))
        self.wait()
        self.play(elem.replace_value(99))
        self.wait()
        self.play(elem.highlight(restore=False), run_time=0.5)
        self.wait()       
