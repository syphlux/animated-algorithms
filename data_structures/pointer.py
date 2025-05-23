from manim import *


class Pointer(VGroup):
    def __init__(self, shape: VMobject, label: str=''):
        super().__init__()
        self.shape = shape
        self.label = Text(label, font='Consolas', font_size=24)
        self.angle = 0
        self.add(shape)
        if label:
            self.add(self.label)

    def _find_best_direction(self, pointed_at: VMobject, points_to_avoid: list[VMobject], num_dirs: int=36):
        angles = np.linspace(0, 2*np.pi, num_dirs)
        potential_directions = [np.array([np.cos(a), np.sin(a), 0]) for a in angles]
        center = pointed_at.get_center()
        other_centers = [p.get_center() for p in points_to_avoid]
        return max(
            potential_directions, 
            key=lambda d: sum([np.linalg.norm(oc - (center + d)) for oc in other_centers])
        )

    def point_at(self, scene: Scene, pointed_at, direction=DOWN, buff=0.5, points_to_avoid=None, run_time=0.5):
        if isinstance(direction, str) and direction == 'auto':
            if not isinstance(points_to_avoid, list) or points_to_avoid == []:
                direction = DOWN
            else:
                direction = self._find_best_direction(pointed_at, points_to_avoid)
        rotation_degrees = 90+np.degrees(np.arctan2(direction[1], direction[0]))
        scene.play(
            self.shape.animate.next_to(pointed_at, direction, buff).rotate((rotation_degrees-self.angle)*DEGREES),
            self.label.animate.next_to(pointed_at, direction*2, buff+0.25),
            run_time=run_time
        )
        self.angle = rotation_degrees


class TestPointer(Scene):
    def construct(self):
        d = Square(z_index=float('inf')).shift(UL)
        p = Pointer(Triangle(fill_opacity=1.0).scale(0.2), 'curr')
        self.play(Create(d))
        p.point_at(self, d, UP, buff=0.5)
        self.wait(0.5)
        p.point_at(self, d, DOWN, buff=0.5)
        self.wait(0.5)
        p.point_at(self, d, LEFT, buff=0.5)
        self.wait(0.5)
        p.point_at(self, d, UR, buff=0.5)
        self.wait(0.5)
        p.point_at(self, d, DL, buff=0.5)
        self.wait(0.5)
                
        
        