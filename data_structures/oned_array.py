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
        self.add([self.label] if array_label else [], self.elems)
        old_width = self.width
        self.scale_to_fit_width(min(self.width, max_width))
        self._update_styles_after_scaling(self.width/old_width)

    def _update_styles_after_scaling(self, ratio: float):
        self.box_style.scale(ratio)
        self.content_style['font_size'] = self.content_style.get('font_size', 32)*ratio
        self.label_style['font_size'] = self.label_style.get('font_size', 24)*ratio
        self.label_buff *= ratio
        self.inter_elem_buff *= ratio
    
    def append(self, value: any):
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
        ).next_to(self, RIGHT, buff=self.inter_elem_buff+RIGHT)
        self.elems.append(new_elem)
        self.add(new_elem)
        return Succession([
            Create(new_elem),
            new_elem.animate.next_to(
                self.elems[-2] if self.n > 1 else self.label, 
                RIGHT if self.n > 1 else -self.array_label_direction, 
                self.inter_elem_buff if self.n > 1 else self.array_label_buff
            )
        ])
        
    def insert(self, idx: int, value: any):
        if idx > self.n or idx < -self.n:
            return
        elif -self.n <= idx < 0:
            idx += self.n
        if idx == self.n:
            return self.append(value)
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
            anims = [
                Create(new_elem),
                AnimationGroup([
                    new_elem.animate.move_to(self.elems[idx]),
                    *[elem.animate.shift(
                        RIGHT*(elem.width + self.inter_elem_buff)
                    ) for elem in self.elems[idx:]],
                    *([Transform(elem.label, Text(
                        str(int(elem.label.text)+1), **self.label_style).move_to(elem.label).shift(
                            RIGHT*(elem.width + self.inter_elem_buff)
                        )
                    ) for elem in self.elems[idx:]] if self.add_indices else [])
                ])
            ]
            if self.add_indices:
                for elem in self.elems[idx:]:
                    elem.label.text = str(int(elem.label.text)+1)
            self.elems.insert(idx, new_elem)
            self.add(new_elem)
            return Succession(anims)
                
    def pop(self, idx: int=-1):
        if idx >= self.n or idx < -self.n:
            return
        elif -self.n <= idx < 0:
            idx += self.n
        self.values.pop(idx)
        self.n -= 1
        old_elem = self.elems[idx]
        anims = [
            old_elem.animate.shift(UP*2),
            AnimationGroup([
                Uncreate(old_elem),
                *[elem.animate.shift(LEFT*(elem.width + self.inter_elem_buff)) for elem in self.elems[idx+1:]],
                *([Transform(elem.label, Text(
                    str(int(elem.label.text)-1), **self.label_style).move_to(elem.label).shift(
                        LEFT*(elem.width + self.inter_elem_buff)
                    ) 
                ) for elem in self.elems[idx+1:]] if self.add_indices else []),
            ])
        ]
        if self.add_indices:
            for elem in self.elems[idx+1:]:
                elem.label.text = str(int(elem.label.text)-1)
        self.elems.remove(old_elem)
        self.remove(old_elem)
        return Succession(anims)
        
    def switch(self, i: int, j: int):
        if 0 <= i < self.n and 0 <= j < self.n and i != j:
            self.values[i], self.values[j] = self.values[j], self.values[i]
            anims = [
                AnimationGroup(
                    self.elems[i].content.animate.shift(UP*2),
                    self.elems[j].content.animate.shift(UP*2)
                ),
                AnimationGroup(
                    self.elems[i].content.animate.move_to(self.elems[j].content.get_center() + UP*2),
                    self.elems[j].content.animate.move_to(self.elems[i].content.get_center() + UP*2)
                ),
                AnimationGroup(
                    self.elems[i].content.animate.move_to(self.elems[j].content),
                    self.elems[j].content.animate.move_to(self.elems[i].content)
                ),
            ]
            self.elems[i].remove(self.elems[i].content)
            self.elems[i].add(self.elems[j].content)
            self.elems[j].remove(self.elems[j].content)
            self.elems[j].add(self.elems[i].content)
            self.elems[i].content, self.elems[j].content = self.elems[j].content, self.elems[i].content
            return Succession(anims)

    def _reorder(self, indices: list[int]):
        self.values = [self.values[idx] for idx in indices]
        anims = [
            AnimationGroup([
                self.elems[idx].animate.move_to(self.elems[i]) for i, idx in enumerate(indices)
            ])
        ]
        if self.add_indices:
            anims.append(
                AnimationGroup([
                    Transform(self.elems[idx].label, Text(str(i), **self.label_style).move_to(self.elems[i].label)) 
                    for i, idx in enumerate(indices)
                ])
            )
            for i, idx in enumerate(indices):
                self.elems[idx].label.text = str(i)
        self.elems = [self.elems[idx] for idx in indices]
        return Succession(anims)

    def sort(self, func=None, reverse: bool=False):
        if func:
            indices = sorted(list(range(len(self.values))), key=lambda i: func(self.values[i]), reverse=reverse)
        else:
            indices = sorted(list(range(len(self.values))), key=lambda i: self.values[i], reverse=reverse)
        return self._reorder(indices)

    def shuffle(self):
        indices = sorted(list(range(len(self.values))), key=lambda _: random.random())
        return self._reorder(indices)


class TestManim(Scene):
    def construct(self):
        a = Array([20, 35, 1, 8, 10, 12, 50], 'array', inter_elem_buff=0.4)
        self.play(Create(a))
        self.wait()
        self.play(a.append(88))
        self.wait()
        self.play(a.append(99))
        self.wait()
        self.play(a.insert(2, -4))
        self.wait()
        self.play(a.switch(0, 4))
        self.wait()
        self.play(a.shuffle())
        self.wait()
        self.play(a.insert(0, 1))
        self.wait()
        self.play(a.sort())
        self.wait()
