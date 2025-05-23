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
            values,
            name='',
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
        
    def insert(self, value, index=0):
        pass
        
    def append(self, value, scene: Scene|None=None):
        self.values.append(value)
        self.n += 1
        elem = ArrayElement(value, self.n-1).next_to(self.elems, RIGHT, buff=1.0)
        if scene:
            scene.play(Create(elem), run_time=0.25)
            scene.play(elem.animate.next_to(self.elems, RIGHT, buff=0.0), run_time=0.25)
        self.elems.add(elem)
        if scene:
            scene.play(self.animate.move_to(self.array_center), run_time=0.25)

    def pop(self, scene: Scene|None=None):
        if self.n > 0:
            self.values.pop()
            self.n -= 1
            elem = self.elems[-1]
            self.elems.remove(elem)
            if scene:
                scene.play(Uncreate(elem), run_time=0.25)
                scene.play(self.animate.move_to(self.array_center), run_time=0.25)

    def switch(self, i: int, j: int, scene: Scene|None=None):
        if 0 <= i < self.n and 0 <= j < self.n and i != j:
            self.values[i], self.values[j] = self.values[j], self.values[i]
            if scene:
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

    def _reorder(self, indices: list[int], scene: Scene|None=None):
        self.values = [self.values[idx] for idx in indices]
        if scene:
            scene.play(
                *[self.elems[idx].text.animate.move_to(self.elems[i].text) for i, idx in enumerate(indices)]
                +[self.elems[idx].box.animate.move_to(self.elems[i].box) for i, idx in enumerate(indices)],
                run_time=1
            )
            scene.remove(self.elems)
        self.elems = VGroup([ArrayElement(v, i) for i, v in enumerate(self.values)]).arrange(RIGHT, buff=0.0).move_to(self.array_center)
        if scene:
            scene.add(self.elems)
        
    def sort(self, reverse: bool=False, scene: Scene|None=None):
        indices = sorted(list(range(len(self.values))), key=lambda i: self.values[i], reverse=reverse)
        self._reorder(indices, scene)

    def shuffle(self, scene: Scene|None=None):
        indices = sorted(list(range(len(self.values))), key=lambda i: random.random())
        self._reorder(indices, scene)



class TestManim(Scene):
    def construct(self):
        a = Array([20, 35, 1, 8, 100, 2, 5]).display(self)
        a.shuffle(self)
        self.wait(2)
        a.shuffle(self)
        self.wait(2)
        a.sort(scene=self)
        self.wait(2)
        a.sort(reverse=True, scene=self)
        self.wait(2)
        a.shuffle(self)
        self.wait(1)
        a._reorder([0, 5, 6, 2, 3, 1, 4], self)
        self.wait(1)
        a._reorder([0, 5, 6, 2, 3, 1, 4], self)
        




        