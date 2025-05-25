from manim import *
from data_structures.element import Element
from data_structures.pointer import Pointer
from data_structures.oned_array import Array


class Algorithm(Scene):
    def linear_search(self, values: list[any], target: any, anim_speed: float=1.0):
        arr = Array(values, 'arr')
        ptr = Pointer(Pointer.triangle, 'i')
        target_elem = Element(target, 'target', label_direction=UP)
        VGroup(arr, target_elem).arrange(UP, buff=1.5).shift(0.5*UP)
        target_elem.shift(LEFT*3)
        self.play(Create(arr), Create(target_elem))

        for i in range(len(values)):
            ptr.point_at(self, arr.elems[i])
            if values[i] == target:
                found_text = Text(f'Found at index {i}', weight=BOLD, color=GREEN, font_size=50).next_to(target_elem.box, buff=0.5)
                Element.highlight_elements(
                    self,
                    [target_elem, arr.elems[i]],
                    color=GREEN,
                    stroke_color=GREEN,
                    label_color=GREEN,
                    fill_opacity=1.0,
                    restore=False,
                    run_time=0.5/anim_speed
                )
                self.play(Write(found_text), run_time=1/anim_speed)
                self.wait(4/anim_speed)
                return
            Element.highlight_elements(
                self, 
                [target_elem, arr.elems[i]],
                color=RED,
                stroke_color=WHITE,
                label_color=RED,
                scale_ratio=1.0,
                run_time=0.5/anim_speed
            )
            self.wait(0.2/anim_speed)
        not_found_text = Text('Not found', weight=BOLD, color=RED, font_size=50).next_to(target_elem.box, buff=0.5)
        target_elem.highlight(self, color=RED, stroke_color=RED, label_color=RED, restore=False, run_time=0.5/anim_speed)
        self.play(Write(not_found_text), run_time=1/anim_speed)
        self.wait(4/anim_speed)

    def construct(self):
        values = [4, 1, 8, 6, 3, 0, 4, 9, -5, 3, 7, 10, 7, 5]
        target = 7

        anim_speed = 1.0
        self.linear_search(values, target, anim_speed)


def linear_search(values: list[any], target: any):
    for i in range(len(values)):
        if values[i] == target:
            return i
    return -1


if __name__ == '__main__':
    values = [4, 1, 8, 6, 3, 0, 4, 9, -5, 3, 7, 10, 7, 5]
    target = 7
    print(linear_search(values, target))
