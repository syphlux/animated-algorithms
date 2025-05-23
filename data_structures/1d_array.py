from manim import *
import random


class ArrayElement(VGroup):
    def __init__(self, value, index=0):
        super().__init__()
        self.value = value
        self.box = Rectangle(height=1, width=1)
        self.text = Text(str(value), font_size=32)
        self.index = Text(str(index), font='Consolas', font_size=24)
        self._bring_text_and_index()
        self.add(self.box, self.text, self.index)

    def _bring_text_and_index(self):
        self.text.move_to(self.box)
        self.index.next_to(self.box, DOWN)
        

class Array(VGroup):
    def __init__(
            self,
            values: list[any],
            name: str='',
            array_center=ORIGIN
    ):
        super().__init__()
        self.values: list = values
        self.n = len(values)
        self.name = name
        self.array_center = array_center
        self.elems = VGroup([ArrayElement(v, i) for i, v in enumerate(values)]).arrange(RIGHT, buff=0.0).move_to(array_center)
        self.add(self.elems)

    def display(self, scene: Scene):
        scene.play(Create(self))
        return self
    
    def append(self, scene: Scene, value: any):
        self.values.append(value)
        self.n += 1
        elem = ArrayElement(value, self.n-1).next_to(self.elems, RIGHT, buff=1.0)
        scene.play(Create(elem), run_time=0.25)
        scene.play(elem.animate.next_to(self.elems, RIGHT, buff=0.0), run_time=0.25)
        self.elems.add(elem)
        scene.play(self.animate.move_to(self.array_center), run_time=0.25)
        
    def insert(self, scene: Scene, idx: int, value: any):
        if idx > self.n or idx < -self.n:
            return
        elif -self.n <= idx < 0:
            idx += self.n
        if idx == self.n:
            self.append(scene, value)
        else:
            self.values.insert(idx, value)
            self.n += 1
            new_elem = ArrayElement(value, idx).next_to(self.elems[idx], UP, buff=1.0)
            scene.play(Create(new_elem), run_time=0.25)
            scene.play(
                new_elem.animate.move_to(self.elems[idx]),
                *[elem.animate.shift(RIGHT * elem.width) for elem in self.elems[idx:]],
                *[Transform(elem.index, Text(str(int(elem.index.text)+1), font='Consolas', font_size=24).move_to(elem.index).shift(RIGHT*elem.width)) for elem in self.elems[idx:]]
            )
            for elem in self.elems[idx:]:
                elem.index.text = str(int(elem.index.text)+1)
            self.elems.insert(idx, new_elem)
            scene.play(self.animate.move_to(self.array_center), run_time=0.25)
                
    def pop(self, scene: Scene):
        if self.n > 0:
            self.values.pop()
            self.n -= 1
            elem = self.elems[-1]
            self.elems.remove(elem)
            scene.play(Uncreate(elem), run_time=0.25)
            scene.play(self.animate.move_to(self.array_center), run_time=0.25)

    def switch(self, scene: Scene, i: int, j: int):
        if 0 <= i < self.n and 0 <= j < self.n and i != j:
            self.values[i], self.values[j] = self.values[j], self.values[i]
            scene.play(
                self.elems[i].text.animate.shift(UP*2),
                self.elems[j].text.animate.shift(UP*2),
                run_time=0.25
            )
            scene.play(
                self.elems[i].text.animate.move_to(self.elems[j].text),
                self.elems[j].text.animate.move_to(self.elems[i].text),
                run_time=0.25
            )
            scene.play(
                self.elems[i].text.animate.shift(DOWN*2),
                self.elems[j].text.animate.shift(DOWN*2),
                run_time=0.25
            )
            self.elems[i].text, self.elems[j].text = self.elems[j].text, self.elems[i].text

    def _reorder(self, scene: Scene, indices: list[int]):
        self.values = [self.values[idx] for idx in indices]
        scene.play(
            *[self.elems[idx].text.animate.move_to(self.elems[i].text) for i, idx in enumerate(indices)],
            *[self.elems[idx].box.animate.move_to(self.elems[i].box) for i, idx in enumerate(indices)]
        )
        scene.clear()
        self.elems = VGroup([ArrayElement(v, i) for i, v in enumerate(self.values)]).arrange(RIGHT, buff=0.0).move_to(self.array_center)
        scene.add(self.elems)
        
    def sort(self, scene: Scene, reverse: bool=False):
        indices = sorted(list(range(len(self.values))), key=lambda i: self.values[i], reverse=reverse)
        self._reorder(scene, indices)

    def shuffle(self, scene: Scene):
        indices = sorted(list(range(len(self.values))), key=lambda i: random.random())
        self._reorder(scene, indices)


class TestManim(Scene):
    def construct(self):
        a = Array([20, 35, 1, 8, 100, 2, 5]).display(self)
        self.wait(1)
        a.insert(self, 2, 400)
        self.wait(1)
        a.insert(self, 0, 99)
        self.wait(1)
        a.insert(self, 9, 555)
        self.wait(1)
        a.insert(self, 9, 666)
        self.wait(1)
        a.insert(self, 0, 333)
        self.wait(1)
        a.insert(self, 3, -9)
        self.wait(1)
        a.append(self, 88)
        self.wait(1)
        a.shuffle(self)
        self.wait(1)
        a.sort(self)
        self.wait(1)
        a.switch(self, 1, 4)
        self.wait(1)
        a.sort(self)
        self.wait(1)
        




        