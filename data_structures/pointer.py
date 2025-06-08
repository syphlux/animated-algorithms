from manim import *
import numpy.typing as npt
from typing_extensions import TypeAlias


Vector3D: TypeAlias = npt.NDArray[np.float64]

class Pointer(VGroup):

    circle = Circle(radius=0.2, color=ORANGE, fill_opacity=1.0)
    triangle = Triangle(color=PURPLE, fill_opacity=1.0).stretch_to_fit_height(0.75).scale(0.25)

    def __init__(
            self, 
            pointer_style: VMobject=circle, 
            label: any=None,
            label_buff: float=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER,
            label_style: dict={'font': 'Consolas', 'font_size': 24}
        ):
        super().__init__()
        self.shape = pointer_style.copy()
        self.label_buff = label_buff
        self.label = Text(label if label is not None else '', **label_style).next_to(self.shape, buff=label_buff)
        self.angle = 0
        self.add([self.shape] + ([self.label] if label is not None else []))
        
    def _find_best_direction(self, pointed_at: Mobject, to_avoid: list[Vector3D|Mobject], num_dirs: int=36):
        angles = np.linspace(0, TAU, num_dirs)
        potential_directions = [np.array([np.cos(a), np.sin(a), 0]) for a in angles]
        centers_to_avoid = [p if isinstance(p, Vector3D) else p.get_center() for p in to_avoid]
        # returns the direction with the greatest total sum of distances from points to avoid
        return max(
            potential_directions, 
            key=lambda d: sum([np.linalg.norm(c - (pointed_at.get_center() + d)) for c in centers_to_avoid])
        )

    def point_at(
            self,
            pointed_at: Mobject, 
            direction: Vector3D|str=DOWN, 
            buff: float=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER, 
            to_avoid: list[Vector3D|Mobject]=None
        ):
        if isinstance(direction, str) and direction == 'auto':
            direction = self._find_best_direction(pointed_at, to_avoid) if to_avoid != [] else DOWN
        rotation_degrees = 90 + np.degrees(np.arctan2(direction[1], direction[0]))
        target_shape = self.shape.copy().next_to(pointed_at, direction, buff).rotate((rotation_degrees-self.angle)*DEGREES)
        anims = [
            self.shape.animate.next_to(pointed_at, direction, buff).rotate((rotation_degrees-self.angle)*DEGREES),
            self.label.animate.next_to(target_shape, direction, self.label_buff)
        ]
        self.angle = rotation_degrees
        return AnimationGroup(anims)


class TestPointer(Scene):
    def construct(self):
        d = Square(z_index=float('inf')).shift(UL)
        p = Pointer(Pointer.triangle, label='curr')
        self.play(Create(d))
        self.wait()
        self.play(p.point_at(self, d, UP, buff=0.0))
        self.wait(0.5)
        self.play(p.point_at(self, d, UP, buff=0.0))
        self.wait(0.5)
                