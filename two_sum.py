from manim import *
from data_structures.element import Element
from data_structures.pointer import Pointer
from data_structures.oned_array import Array


class Algorithm(Scene):

    def two_sum(self, values: list[float], target: float, anim_speed: float=1.0):

        # animation: array creation and display
        arr = Array(values)
        self.play(Create(arr), run_time=1/anim_speed)

        # animation: current sum and target elements creation and display
        sum_elem = Element(
            '-', 'arr[i] + arr[j] = ', label_direction=LEFT, fit_label_to_width=False, label_style={'color': WHITE}
        )
        target_elem = Element(
            target, 'target', label_direction=RIGHT, fit_label_to_width=False, label_style={'color': WHITE}
        )
        VGroup(sum_elem, target_elem).arrange(buff=2)
        self.play(
            FadeIn(sum_elem), FadeIn(target_elem),
            VGroup(
                VGroup(sum_elem, target_elem), arr
            ).animate.arrange(DOWN, buff=1.5).shift(0.5*UP),
            run_time=1/anim_speed
        )
        self.wait(1/anim_speed)

        # pointers creation
        i, j = 0, len(values)-1
        i_ptr = Pointer(Pointer.triangle, 'i')
        j_ptr = Pointer(Pointer.triangle.copy().set_color(ORANGE), 'j')

        to_restore = None
        while i < j:
            # animation: moving pointers, highlighting elements, writing new value of arr[i]+arr[j]
            self.play(
                i_ptr.point_at(arr.elems[i]), 
                j_ptr.point_at(arr.elems[j]),
                arr.elems[i].highlight(YELLOW, WHITE, BLACK, YELLOW, scale_ratio=1.0, restore=False),
                arr.elems[j].highlight(YELLOW, WHITE, BLACK, YELLOW, scale_ratio=1.0, restore=False),
                sum_elem.replace_value(values[i] + values[j]),
                *([to_restore.highlight(
                    BLACK, WHITE, WHITE, BLUE, 0.0, scale_ratio=1.0, restore=False
                )] if to_restore else []),
                run_time=1/anim_speed
            )
            self.wait(1/anim_speed)
            if values[i] + values[j] == target:
                found_text = Text(
                    f'found with arr[{i}]+arr[{j}]', **target_elem.label_style
                ).set_color(GREEN).next_to(target_elem, DOWN)
                # animation: success, highlighting both sum and target in green, shift up found elements
                # and write that it could be found
                self.play(
                    sum_elem.highlight(GREEN, GREEN, BLACK, GREEN, 1.0, restore=False),
                    target_elem.highlight(GREEN, GREEN, BLACK, GREEN, 1.0, restore=False),
                    arr.elems[i].highlight(
                        GREEN, WHITE, BLACK, GREEN, 1.0, scale_ratio=1.0, shift=UP*0.2, restore=False
                    ),
                    arr.elems[j].highlight(
                        GREEN, WHITE, BLACK, GREEN, 1.0, scale_ratio=1.0, shift=UP*0.2, restore=False
                    ),
                    FadeIn(Text('=', font_size=60).move_to((sum_elem.get_right() + target_elem.get_left())/2)),
                    Write(found_text),
                    i_ptr.animate.shift(UP*0.2),
                    j_ptr.animate.shift(UP*0.2),
                    run_time=1.5/anim_speed
                )
                self.wait(5/anim_speed)
                return
            elif values[i] + values[j] < target:
                i += 1
                to_restore = arr.elems[i-1]
                # animation: comparing sum and target and displaying comparison result
                self.play(
                    sum_elem.compare(target_elem),
                    FadeIn(
                        Text('<', font_size=60).move_to((sum_elem.get_right() + target_elem.get_left())/2),
                        rate_func=there_and_back_with_pause
                    ),
                    run_time=0.75/anim_speed
                )
            else:
                j -= 1
                to_restore = arr.elems[j+1]
                # animation: comparing sum and target and displaying comparison result
                self.play(
                    sum_elem.compare(target_elem),
                    FadeIn(
                        Text('>', font_size=60).move_to((sum_elem.get_right() + target_elem.get_left())/2),
                        rate_func=there_and_back_with_pause
                    ),
                    run_time=0.75/anim_speed
                )
        cant_be_found_text = Text(
            'cannot be found', **target_elem.label_style
        ).set_color(RED).next_to(target_elem, DOWN)
        self.wait(1/anim_speed)
        # animation: failture, highlighting target in red and write that it cannot be found
        self.play(
            i_ptr.point_at(arr.elems[i]), 
            j_ptr.point_at(arr.elems[j]),
            sum_elem.replace_value('-'),
            Write(cant_be_found_text),
            target_elem.highlight(RED, RED, BLACK, RED, 1.0, scale_ratio=1.0, restore=False),
            arr.elems[i].highlight(
                BLACK, WHITE, WHITE, BLUE, 0.0, scale_ratio=1.0, restore=False
            ),
            arr.elems[j].highlight(
                BLACK, WHITE, WHITE, BLUE, 0.0, scale_ratio=1.0, restore=False
            ),
            *([to_restore.highlight(
                BLACK, WHITE, WHITE, BLUE, 0.0, scale_ratio=1.0, restore=False
            )] if to_restore else []),
            run_time=1.5/anim_speed
        )
        self.wait(5/anim_speed)

    def construct(self):
        values = [1, 4, 5, 5, 8, 12, 15, 16, 25, 36, 37, 40, 42, 43, 66, 71]
        target = 58

        anim_speed = 1.0
        self.two_sum(values, target, anim_speed)


def two_sum(values: list[float], target: float) -> tuple[int,int]:
    assert isinstance(values, list) and len(values) > 0 \
        and all([isinstance(v, (int, float)) for v in values]), \
        'values must be a non-empty list of numbers'
    assert isinstance(target, (int, float)), 'target must be a number'
    assert values == list(sorted(values)), 'values must be sorted'

    i, j = 0, len(values)-1
    while i < j:
        if values[i] + values[j] == target:
            return (i, j)
        elif values[i] + values[j] < target:
            i += 1
        else:
            j -= 1
    return (-1, -1)


if __name__ == '__main__':
    values = [1, 4, 5, 5, 8, 12, 15, 16, 25, 36, 37, 40, 42, 43, 66, 71]
    target = 58
    print(two_sum(values, target))
