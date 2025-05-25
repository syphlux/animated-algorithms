from manim import *
import random
import numpy.typing as npt
from typing_extensions import TypeAlias
from .element import Element
        
Vector3D: TypeAlias = npt.NDArray[np.float64]


class Array(VGroup):
    def __init__(
            self,
            values: list[any],
            array_label: str=None,
            array_label_direction: Vector3D=UL,
            array_label_buff: float=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER,
            array_label_style: dict={'font_size': 28},
            array_center: Vector3D=ORIGIN,
            inter_elem_buff: float=0.0,
            add_indices: bool=True,
            max_width: float=config.frame_width*0.9,
            box_style: VMobject=Square(side_length=1),
            content_style: dict={'font_size': 32},
            content_direction: Vector3D=ORIGIN,
            label_style: dict={'font': 'Consolas', 'font_size': 24, 'color': BLUE},
            label_direction: Vector3D=DOWN,
            label_buff: float=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER,
    ):
        assert isinstance(values, list) and len(values) > 0, \
            "values must be a non-empty list"
        
        super().__init__()
        self.values: list = values
        self.n = len(values)
        self.elems = [
            Element(
                v, 
                i if add_indices else None, 
                box_style, 
                content_style,
                content_direction,
                label_style,
                label_direction,
                label_buff
            ) for i, v in enumerate(values)
        ]
        VGroup(self.elems).arrange(RIGHT, buff=inter_elem_buff).move_to(array_center)
        self.label = Text(
            str(array_label), **array_label_style
        ).next_to(self.elems[0], array_label_direction, array_label_buff)
        self.array_center = array_center
        self.array_label_direction, self.array_label_buff = array_label_direction, array_label_buff
        self.inter_elem_buff = inter_elem_buff
        self.add_indices = add_indices
        self.max_width = max_width
        self.box_style = box_style
        self.content_style, self.content_direction = content_style, content_direction
        self.label_style, self.label_direction, self.label_buff = label_style, label_direction, label_buff
        self.add(([self.label] if array_label else []) + self.elems)
        old_width = self.width
        self.scale_to_fit_width(min(self.width, max_width))
        self._update_styles_after_scaling(self.width/old_width)

    def _update_styles_after_scaling(self, ratio: float):
        self.box_style.scale(ratio)
        self.content_style['font_size'] = self.content_style.get('font_size', 32)*ratio
        self.label_style['font_size'] = self.label_style.get('font_size', 24)*ratio
        self.label_buff *= ratio
        self.inter_elem_buff *= ratio
    
    def append(self, scene: Scene, value: any, run_time: float=0.5):
        self.values.append(value)
        self.n += 1
        new_elem = Element(
            value, 
            self.n-1 if self.add_indices else None, 
            self.box_style, 
            self.content_style,
            self.content_direction,
            self.label_style,
            self.label_direction,
            self.label_buff
        ).next_to(self, RIGHT, buff=self.inter_elem_buff+1.0)
        scene.play(Create(new_elem), run_time=run_time/3)
        scene.play(new_elem.animate.next_to(
            self.elems[-1] if self.n > 1 else self.label, 
            RIGHT if self.n > 1 else -self.array_label_direction, 
            buff=self.inter_elem_buff if self.n > 1 else self.array_label_buff
        ), run_time=run_time/3)
        self.elems.append(new_elem)
        self.add(new_elem)
        old_width = self.width
        scene.play(
            self.animate.move_to(self.array_center).scale_to_fit_width(min(self.width, self.max_width)),
            run_time=run_time/3
        )
        self._update_styles_after_scaling(self.width/old_width)
        
    def insert(self, scene: Scene, idx: int, value: any, run_time: float=0.5):
        if idx > self.n or idx < -self.n:
            return
        elif -self.n <= idx < 0:
            idx += self.n
        if idx == self.n:
            self.append(scene, value)
        else:
            self.values.insert(idx, value)
            self.n += 1
            new_elem = Element(
                value, 
                idx if self.add_indices else None, 
                self.box_style, 
                self.content_style,
                self.content_direction,
                self.label_style,
                self.label_direction,
                self.label_buff
            ).next_to(self.elems[idx], UP, buff=1.0)
            scene.play(Create(new_elem), run_time=run_time/3)
            scene.play(
                new_elem.animate.move_to(self.elems[idx]),
                *[elem.animate.shift(
                    RIGHT*(elem.width + self.inter_elem_buff)
                ) for elem in self.elems[idx:]],
                *[Transform(elem.label, Text(
                    str(int(elem.label.text)+1), **self.label_style).move_to(elem.label).shift(
                        RIGHT*(elem.width + self.inter_elem_buff)
                    )
                ) for elem in self.elems[idx:]] if self.add_indices else [],
                run_time=run_time/3
            )
            if self.add_indices:
                for elem in self.elems[idx:]:
                    elem.label.text = str(int(elem.label.text)+1)
            self.elems.insert(idx, new_elem)
            self.add(new_elem)
            old_width = self.width
            scene.play(
                self.animate.move_to(self.array_center).scale_to_fit_width(min(self.width, self.max_width)),
                run_time=run_time/3
            )
            self._update_styles_after_scaling(self.width/old_width)
                
    def pop(self, scene: Scene, idx: int=-1, run_time: float=0.5):
        if idx >= self.n or idx < -self.n:
            return
        elif -self.n <= idx < 0:
            idx += self.n
        self.values.pop(idx)
        self.n -= 1
        old_elem = self.elems[idx]
        scene.play(old_elem.animate.shift(UP*2), run_time=run_time/3)
        scene.play(
            Uncreate(old_elem),
            *[elem.animate.shift(LEFT*(elem.width + self.inter_elem_buff)) for elem in self.elems[idx+1:]],
            *[Transform(elem.label, Text(
                str(int(elem.label.text)-1), **self.label_style).move_to(elem.label).shift(
                    LEFT*(elem.width + self.inter_elem_buff)
                ) 
            ) for elem in self.elems[idx+1:]] if self.add_indices else [],
            run_time=run_time/3
        )
        if self.add_indices:
            for elem in self.elems[idx+1:]:
                elem.label.text = str(int(elem.label.text)-1)
        self.elems.remove(old_elem)
        self.remove(old_elem)
        scene.play(self.animate.move_to(self.array_center), run_time=run_time/3)
        
    def switch(self, scene: Scene, i: int, j: int, run_time: float=0.5):
        if 0 <= i < self.n and 0 <= j < self.n and i != j:
            self.values[i], self.values[j] = self.values[j], self.values[i]
            scene.play(
                self.elems[i].content.animate.shift(UP*2),
                self.elems[j].content.animate.shift(UP*2),
                run_time=run_time/3
            )
            scene.play(
                self.elems[i].content.animate.move_to(self.elems[j].content),
                self.elems[j].content.animate.move_to(self.elems[i].content),
                run_time=run_time/3
            )
            scene.play(
                self.elems[i].content.animate.shift(DOWN*2),
                self.elems[j].content.animate.shift(DOWN*2),
                run_time=run_time/3
            )
            self.elems[i].remove(self.elems[i].content)
            self.elems[i].add(self.elems[j].content)
            self.elems[j].remove(self.elems[j].content)
            self.elems[j].add(self.elems[i].content)
            self.elems[i].content, self.elems[j].content = self.elems[j].content, self.elems[i].content

    def _reorder(self, scene: Scene, indices: list[int], run_time: float=0.5):
        self.values = [self.values[idx] for idx in indices]
        scene.play(
            *[self.elems[idx].animate.move_to(self.elems[i]) for i, idx in enumerate(indices)],
            run_time=2*run_time/3
        )
        scene.play(
            *[Transform(self.elems[idx].label, Text(str(i), **self.label_style).move_to(self.elems[idx].label)) 
            for i, idx in enumerate(indices)] if self.add_indices else [],
            run_time=run_time/3
        )
        if self.add_indices:
            for i, idx in enumerate(indices):
                self.elems[idx].label.text = str(i)
        self.elems = [self.elems[idx] for idx in indices]

    def sort(self, scene: Scene, func=None, reverse: bool=False, run_time: float=0.5):
        if func:
            indices = sorted(list(range(len(self.values))), key=lambda i: func(self.values[i]), reverse=reverse)
        else:
            indices = sorted(list(range(len(self.values))), key=lambda i: self.values[i], reverse=reverse)
        self._reorder(scene, indices, run_time)

    def shuffle(self, scene: Scene, run_time: float=0.5):
        indices = sorted(list(range(len(self.values))), key=lambda _: random.random())
        self._reorder(scene, indices, run_time)


class TestManim(Scene):
    def construct(self):
        a = Array([20, 35, 1, 8, 100, 2, 5, 4, 80], 'array', inter_elem_buff=0.4)
        self.wait()
        a.append(self, 555)
        self.wait()
        a.append(self, 11)
        self.wait()
        a.insert(self, 5, 1000000)
        self.wait()
        a.insert(self, 0, 3)
        self.wait()
        a.pop(self)
        self.wait()
        a.sort(self)
        self.wait()
        a.shuffle(self)
        self.wait()
        a.insert(self, 0, 99)
        self.wait()
        a.pop(self)
        self.wait()
        a.pop(self, 0)
        self.wait()
        a.sort(self)
        self.wait()
        a.sort(self, reverse=True)
        self.wait()
        a.append(self, 44)
        self.wait()
        