from manim import *
from data_structures.stack import Stack
from data_structures.pointer import Pointer


class Algorithm(Scene):

    def valid_parentheses(self, s: str, anim_speed: float=1.0):
        opening_par = {'(', '{', '['}
        closing_par = {')', '}', ']'}
        close_open_map = {')': '(', '}': '{', ']': '['}

        assert set(s).issubset(opening_par.union(closing_par)), \
        "string s must be made of parentheses only (){}[]"

        s_text = Text(f'"{s}"', font='Consolas', font_size=40)
        s_text.scale_to_fit_width(
            min(s_text.width, config.frame_width*0.7)
        ).shift(config.frame_width*0.1*RIGHT)
        fh, fw = config.frame_height, config.frame_width
        stack = Stack([], 'stack', stack_bottom=fh/2*0.9*DOWN + fw*0.4*LEFT)
        ptr = Pointer(Pointer.triangle)
        map_text = Text("( )    { }    [ ]", font_size=48).next_to(s_text, UP, buff=1.5).shift(3*RIGHT)
        valid_pairs_text = Text("valid open/close pairs:", font_size=28).next_to(map_text, UP)
        self.play(
            *[Create(obj) for obj in [s_text, stack, ptr, valid_pairs_text, map_text]], 
            run_time=1/anim_speed
        )
        success = True
        for i in range(1, len(s_text)-1):
            self.play(ptr.point_at(s_text[i]), run_time=0.5/anim_speed)
            par = s[i-1]
            if par in opening_par:
                self.play(
                    stack.push(par, src_pos=s_text[i]), s_text[i].animate.set_color(GREEN),
                    run_time=0.5/anim_speed
                )
            elif len(stack.elems) == 0:
                x_character = Text('X', color=RED, font='Consolas', font_size=70).next_to(stack, UP)
                failure_reason = Text(
                    'Closing parentheses with empty stack', color=RED, font_size=36
                ).next_to(s_text, DOWN, buff=1.0)
                failure_text = Text(
                    'Invalid parentheses sequence!', color=RED, font_size=50
                ).next_to(failure_reason, DOWN)
                self.play(
                    FadeIn(x_character),
                    s_text[i].animate.set_color(RED),
                    Write(failure_reason),
                    Write(failure_text),
                    run_time=2.0/anim_speed
                )
                success = False
                break
            elif close_open_map[par] != stack.elems[-1].value:
                failure_reason = Text(
                    f"'{par}' doesn't match latest opening parentheses '{stack.elems[-1].value}'", color=RED, font_size=32
                ).next_to(s_text, DOWN, buff=1.0)
                failure_text = Text(
                    'Invalid parentheses sequence!', color=RED, font_size=50
                ).next_to(failure_reason, DOWN)
                self.play(
                    stack.elems[-1].highlight(RED, RED, BLACK, restore=False),
                    s_text[i].animate.set_color(RED),
                    Write(failure_reason),
                    Write(failure_text),
                    run_time=2.0/anim_speed
                )
                success = False
                break
            else:
                self.play(
                    stack.elems[-1].highlight(GREEN, GREEN, BLACK, restore=False),
                    s_text[i].animate.set_color(GREEN),
                    run_time=0.5/anim_speed
                )
                self.play(stack.pop(), run_time=1/anim_speed)
        if success:
            if len(stack.elems) > 0:
                failure_reason = Text(
                    f"There are remaining unclosed parentheses", color=RED, font_size=32
                ).next_to(s_text, DOWN, buff=1.0)
                failure_text = Text(
                    'Invalid parentheses sequence!', color=RED, font_size=50
                ).next_to(failure_reason, DOWN)
                self.play(
                    *[elem.highlight(
                        RED, RED, BLACK, scale_ratio=1.0, restore=False
                    ) for elem in stack.elems],
                    FadeOut(ptr),
                    Write(failure_reason),
                    Write(failure_text),
                    run_time=2.0/anim_speed
                )
            else:
                success_text = Text(
                    'Valid parentheses sequence!', color=GREEN, font_size=60
                ).next_to(s_text, DOWN, buff=1.0)
                self.play(
                    FadeOut(ptr),
                    Write(success_text),
                    run_time=2.0/anim_speed
                )
        self.wait(4/anim_speed)

    def construct(self):
        s = '(({[({})]}()[([])])){()()}'

        anim_speed = 2.0
        self.valid_parentheses(s, anim_speed)


def valid_parentheses(s: str):
    stack = []
    opening_par = {'(', '{', '['}
    closing_par = {')', '}', ']'}
    close_open_map = {')': '(', '}': '{', ']': '['}

    assert set(s).issubset(opening_par.union(closing_par)), \
        "string s must be made of parentheses only (){}[]"
    
    for par in s:
        if par in opening_par:
            stack.append(par)
        elif len(stack) == 0 or close_open_map[par] != stack[-1]:
            return False
        else:
            stack.pop()
    
    return len(stack) == 0


if __name__ == '__main__':
    s = '(){}[({(())})](())((})'
    print(valid_parentheses(s))
