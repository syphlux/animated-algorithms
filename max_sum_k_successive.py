from manim import *
from data_structures.element import Element
from data_structures.pointer import Pointer
from data_structures.oned_array import Array


class Algorithm(Scene):
    def max_sum_k_successive(self, values: list[any], k: int, anim_speed: float=1.0):

        assert isinstance(values, list) and len(values) > 0, "values list can't be empty"
        assert 1 <= k <= len(values), "k must be between 1 and len(values)"

        # animation: array creation and display
        arr = Array(values)
        self.play(Create(arr))

        # animation: current sum, max sum, and max sum start index elements creation and display
        curr_sum, max_sum, max_sum_idx = sum(values[:k]), float('-inf'), -1
        curr_sum_elem = Element(
            '-', 'window\n sum', label_direction=UP, fit_label_to_width=False, label_style={'color': WHITE}
        )
        max_sum_elem = Element(
            float('-inf'), 'max\nsum', label_direction=UP, fit_label_to_width=False, label_style={'color': WHITE}
        )
        VGroup(curr_sum_elem, max_sum_elem).arrange(buff=3)
        max_sum_idx_elem = Element(
            '-', 
            '  max sum\nstart index', 
            label_direction=UP, 
            fit_label_to_width=False, 
            content_style=arr.label_style, 
            label_style={'color': WHITE}
        ).next_to(max_sum_elem, buff=0.5)
        self.play(
            FadeIn(curr_sum_elem), FadeIn(max_sum_elem), FadeIn(max_sum_idx_elem),
            VGroup(
                VGroup(curr_sum_elem, max_sum_elem, max_sum_idx_elem), arr
            ).animate.arrange(DOWN, buff=2.0).shift(0.5*UP)
        )
        self.wait(1/anim_speed)

        # animation: window and pointer creation and display
        window = RoundedRectangle(
            corner_radius=0.3, 
            height=arr.elems[0].box.height+0.3, 
            width=k*arr.elems[0].box.width+0.3, 
            fill_opacity=0.3, 
            color=YELLOW
        ).move_to(arr.elems[0].box.get_left() + RIGHT*k/2*arr.elems[0].box.width)
        window_brace = Brace(window, UP, buff=0.1, fill_opacity=0.5)
        window_size_label = Text(f'k = {k}', font_size=30, fill_opacity=0.5).next_to(window_brace, UP)
        ptr = Pointer(Pointer.triangle, 'i')
        self.play(FadeIn(window), FadeIn(window_brace), Write(window_size_label), ptr.point_at(arr.elems[0]))
        self.wait(1/anim_speed)

        old_elem_label_1 = Text(
            '-arr[i-1]', weight=BOLD, font='Consolas', font_size=18, color=RED
        ).next_to(arr.elems[0], DOWN, buff=0.15)
        old_elem_label_2 = Text(
            '(old element)', font='Arial', font_size=16, color=RED
        ).next_to(old_elem_label_1, DOWN, buff=0.15)
        new_elem_label_1 = Text(
            '+arr[i+k-1]', weight=BOLD, font='Consolas', font_size=18, color=GREEN
        ).next_to(arr.elems[k], DOWN, buff=0.15)
        new_elem_label_2 = Text(
            '(new element)', font='Arial', font_size=16, color=GREEN
        ).next_to(new_elem_label_1, DOWN, buff=0.15)
        
        # iterating over windows
        for i in range(len(values)-k+1):
            if i == 0: # initial window
                # animation: adding all first k elements
                self.play(
                    *[FadeOut(elem.content.copy(), target_position=curr_sum_elem) for elem in arr.elems[:k]],
                    curr_sum_elem.replace_value(sum(values[:k]))
                )
                self.wait(1/anim_speed)
            else: # later iterations
                # animation: shift window, pointer, and old and new elements labels
                anims = [
                    VGroup(window, window_brace, window_size_label).animate.shift(arr.elems[0].width*RIGHT),
                    ptr.point_at(arr.elems[i]),
                    arr.elems[i-1].highlight(RED, WHITE, BLACK, RED, 0.5, 1.0, restore=False),
                    arr.elems[i+k-1].highlight(GREEN, WHITE, BLACK, GREEN, 0.5, 1.0, restore=False),
                ]
                if i == 1:
                    anims.append(FadeIn(VGroup(
                        old_elem_label_1, old_elem_label_2, new_elem_label_1, new_elem_label_2
                    )))
                else:
                    anims.extend([
                        VGroup(
                            old_elem_label_1, old_elem_label_2, new_elem_label_1, new_elem_label_2
                        ).animate.shift(arr.elems[0].width*RIGHT),
                        Restore(arr.elems[i-2]),
                        Restore(arr.elems[i+k-2])
                    ])
                self.play(anims)
                self.wait(1/anim_speed)

                # animation: subtract old element and add new element
                curr_sum += values[i+k-1] - values[i-1]
                old_elem_value_copy = arr.elems[i-1].content.copy().set_color(WHITE).move_to(curr_sum_elem.content)
                new_elem_value_copy = arr.elems[i+k-1].content.copy().set_color(WHITE)
                self.add(old_elem_value_copy, new_elem_value_copy)
                self.play(
                    old_elem_value_copy.animate.set_color(RED).move_to(arr.elems[i-1].content),
                    new_elem_value_copy.animate.set_color(GREEN).move_to(curr_sum_elem.content),
                    curr_sum_elem.replace_value(curr_sum), 
                    run_time=1
                )
                self.remove(old_elem_value_copy, new_elem_value_copy)
                self.wait(1/anim_speed)
            
            # animation: compare current sum and max sum to see if replacement is needed
            self.play(curr_sum_elem.compare(max_sum_elem), run_time=1.0)
            self.wait(0.5/anim_speed)
            if curr_sum > max_sum:
                # animation: replace max sum and its index by new max sum and new index
                max_sum, max_sum_idx = curr_sum, i
                curr_sum_elem_copy, curr_idx_elem_copy = curr_sum_elem.content.copy(), arr.elems[i].label.copy()
                self.add(curr_sum_elem_copy, curr_idx_elem_copy)
                self.play(
                    max_sum_elem.replace_value(curr_sum_elem.value),
                    curr_sum_elem_copy.animate.move_to(max_sum_elem.content),
                    max_sum_idx_elem.replace_value(i),
                    curr_idx_elem_copy.animate.move_to(max_sum_idx_elem.content),
                    run_time=1.0
                )
                self.remove(curr_sum_elem_copy, curr_idx_elem_copy)
        self.wait(2/anim_speed)

        # animation: showcase max sum
        shift_to_max_idx = arr.elems[0].width*LEFT*(i-max_sum_idx)
        max_sum_idx_elem_copy = max_sum_idx_elem.content.copy().set_color(GREEN)
        self.add(max_sum_idx_elem_copy) 
        self.play([
            VGroup(window, window_brace, window_size_label).animate.shift(shift_to_max_idx).set_color(GREEN),
            FadeOut(VGroup(
                old_elem_label_1, old_elem_label_2, new_elem_label_1, new_elem_label_2
            )),
            ptr.shape.animate.next_to(arr.elems[max_sum_idx], DOWN).set_color(GREEN),
            FadeOut(ptr.label),
            max_sum_idx_elem.content.animate.set_color(GREEN),
            max_sum_idx_elem_copy.animate.move_to(arr.elems[max_sum_idx].label),
            max_sum_elem.highlight(GREEN, GREEN, BLACK, GREEN, fill_opacity=1.0, restore=False),
            Restore(arr.elems[-1]),
            Restore(arr.elems[-k-1])
        ], run_time=2/anim_speed)
        self.wait(5/anim_speed)

    def construct(self):
        values = [5, 2, 8, 0, 5, 100, 2, 5, 3, 80, 2, 44, 2]
        k = 4

        anim_speed = 1.0
        self.max_sum_k_successive(values, k, anim_speed)


def max_sum_k_successive(values: list[float], k: int) -> tuple[int,float]:

    assert isinstance(values, list) and len(values) > 0, "values list can't be empty"
    assert 1 <= k <= len(values), "k must be between 1 and len(values)"

    curr_sum, max_sum, max_sum_idx = sum(values[:k]), sum(values[:k]), 0
    for i in range(1, len(values)-k+1):
        curr_sum += values[i+k-1] - values[i-1]
        if curr_sum > max_sum:
            max_sum, max_sum_idx = curr_sum, i
    return max_sum_idx, max_sum


if __name__ == '__main__':
    values = [5, 2, 8, 0, 5, 100, 2, 8, 3, 80, 2, 44, 2]
    k = 4
    print(max_sum_k_successive(values, k))
