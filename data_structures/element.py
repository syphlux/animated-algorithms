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
            fit_label_to_width: bool=True
    ):
        super().__init__()
        self.value = value
        self.box = box_style.copy()
        self.content_style = content_style
        self.content = Text(str(value), **content_style).move_to(self.box.get_center() + content_direction)
        self.content.scale_to_fit_width(min(self.content.width, self.box.width*0.8))
        self.label = Text(str(label), **label_style)
        if fit_label_to_width:
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
            stroke_color: ParsableManimColor=YELLOW,
            font_color: ParsableManimColor=BLACK,
            label_color: ParsableManimColor=YELLOW,
            fill_opacity: float=0.8,
            scale_ratio: float=1.2,
            restore: bool=True,
            run_time: float=0.5
    ):
        self.save_state()
        scene.play(
            self.box.animate.set_z_index(float('inf')).set_color(color).set_stroke(color=stroke_color).set_opacity(fill_opacity).scale(scale_ratio),
            self.content.animate.set_z_index(float('inf')).set_color(font_color).scale(scale_ratio),
            self.label.animate.set_z_index(float('inf')).set_color(label_color).scale(scale_ratio),
            run_time=run_time/3 if restore else run_time
        )
        if restore:
            scene.wait(run_time/3)
            scene.play(Restore(self), run_time=run_time/3)

    @staticmethod
    def highlight_elements(
        scene: Scene,
        elems: list["Element"],
        color: ParsableManimColor=YELLOW,
        stroke_color: ParsableManimColor=YELLOW,
        font_color: ParsableManimColor=BLACK,
        label_color: ParsableManimColor=YELLOW,
        fill_opacity: float=0.8,
        scale_ratio: float=1.2,
        restore: bool=True,
        run_time: float=0.5
    ):
        [elem.save_state() for elem in elems]
        scene.play([anim for elem in elems for anim in 
            [
                elem.box.animate.set_z_index(float('inf')).set_color(color).set_stroke(color=stroke_color).set_opacity(fill_opacity).scale(scale_ratio),
                elem.content.animate.set_z_index(float('inf')).set_color(font_color).scale(scale_ratio),
                elem.label.animate.set_z_index(float('inf')).set_color(label_color).scale(scale_ratio),
            ]
        ], run_time=run_time/3 if restore else run_time)
        if restore:
            scene.wait(run_time/3)
            scene.play([Restore(elem) for elem in elems], run_time=run_time/3)


class TestElement(Scene):
    def construct(self):
        elem = Element(45, 'max')
        self.play(Create(elem))
        elem2 = elem.copy().shift(RIGHT)
        Element.highlight_elements(self, [elem, elem2], restore=False)
        self.wait()

        
