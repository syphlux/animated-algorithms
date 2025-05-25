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
        self.content_style = content_style
        self.content = Text(str(value), **content_style).move_to(self.box.get_center() + content_direction)
        self.content.scale_to_fit_width(min(self.content.width, self.box.width*0.8))
        self.label = Text(str(label), **label_style)
        self.label.scale_to_fit_width(min(self.label.width, self.box.width))
        self.label.next_to(self.box, label_direction, label_buff)
        self.add([self.box, self.content] + ([self.label] if label is not None else []))

    def replace_value(self, scene: Scene, new_value: any, run_time: float=0.5):
        self.value = new_value
        self.content.text = str(new_value)
        scene.play(Transform(self.content, Text(
            str(new_value), **self.content_style).move_to(self.content)
        ), run_time=run_time)

    def highlight(
            self,
            scene: Scene,
            color: ParsableManimColor=YELLOW, 
            font_color: ParsableManimColor=BLACK, 
            scale_ratio: float=1.2, 
            run_time: float=0.5
    ):
        self.save_state()
        scene.play(
            self.box.animate.set_stroke(color=color, opacity=1.0).set_color(color).set_opacity(0.8).scale(scale_ratio),
            self.content.animate.set_color(font_color),
            self.label.animate.scale(scale_ratio),
            run_time=run_time/3
        )
        scene.wait(run_time/3)
        scene.play(Restore(self), run_time=run_time/3)


class TestElement(Scene):
    def construct(self):
        elem = Element(45, 'max')
        self.play(Create(elem))
        self.wait(0.5)
        elem.highlight(self)
        self.wait()
        elem.replace_value(self, 98)
        print(elem.content.text)
        self.wait()
        self.play(elem.animate.shift(RIGHT))
        self.wait()

        
