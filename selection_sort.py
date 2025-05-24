from manim import *
from data_structures.oned_array import Array
from data_structures.pointer import Pointer


class Algorithm(Scene):

    def selection_sort(self, values: list[any]):
        arr = Array(values).display(self)
        separator = Line(ORIGIN, UP*5).next_to(arr.elems[0], LEFT, 0.0)
        sorted_label = Text('sorted', font='Arial', font_size=28).next_to(separator, UL)
        unsorted_label = Text('unsorted', font='Arial', font_size=28).next_to(separator, UR)
        self.play(Create(separator), Create(sorted_label), Create(unsorted_label))
        i_ptr = Pointer(Triangle(color=ORANGE, fill_opacity=0.8).scale(0.2), 'i')
        j_ptr = Pointer(Triangle(color=PURPLE, fill_opacity=0.8).scale(0.1), 'j')
        min_ptr = Pointer(Dot(radius=0.1, color=BLUE, fill_opacity=0.8), 'min')
        for i in range(len(values)):
            i_ptr.point_at(self, arr.elems[i], buff=0.25)
            min_idx = i
            min_ptr.point_at(self, arr.elems[min_idx], UP, buff=0.25)
            for j in range(i+1, len(values)):
                j_ptr.point_at(self, arr.elems[j], buff=0.25)
                if values[j] < values[min_idx]:
                    min_idx = j
                    min_ptr.point_at(self, arr.elems[j], UP, buff=0.25)
            arr.switch(self, i, min_idx)
            arr.elems[i].save_state()
            self.play(
                separator.animate.shift(RIGHT*arr.elems[0].box.width),
                unsorted_label.animate.shift(RIGHT*arr.elems[0].box.width),
                sorted_label.animate.shift(RIGHT*arr.elems[0].box.width),
                arr.elems[i].box.animate.set_stroke(opacity=0.2),
                arr.elems[i].text.animate.set_opacity(0.2),
                arr.elems[i].index.animate.set_opacity(0.2),
                FadeOut(j_ptr),
                FadeOut(min_ptr)
            )
        self.play(
            *[Restore(elem) for elem in arr.elems],
            FadeOut(i_ptr)
        )
        self.wait(3)

    def construct(self):
        self.selection_sort([4, 10, -3, 5, 200, 0, 4, 8, 9, 4, 12])


def selection_sort(values: list[any]):
    for i in range(len(values)):
        min_idx = i
        for j in range(i+1, len(values)):
            if values[j] < values[min_idx]:
                min_idx = j
        values[i], values[min_idx] = values[min_idx], values[i]
    return values


if __name__ == '__main__':
    values = [4, 10, -3, 5, 200, 0, 4, 8, 9, 4, 12]
    print(selection_sort(values))
