from manim import *
import numpy as np
import math
import random


class GrahamScan(MovingCameraScene):

    def orientation(self, p1: tuple[float,float], p2: tuple[float,float], p3: tuple[float,float]):
        x1, y1, x2, y2, x3, y3 = *p1, *p2, *p3
        diff = (y3-y2)*(x2-x1) - (y2-y1)*(x3-x2)
        return 1 if diff > 0 else (-1 if diff < 0 else 0)

    def dist(self, p1: tuple[float,float], p2: tuple[float,float]):
        x1, y1, x2, y2 = *p1, *p2
        return math.sqrt((y2-y1)**2 + (x2-x1)**2)
    
    def polar_angle(self, p1: tuple[float,float], p2: tuple[float,float]):
        if p1[1] == p2[1]:
            return -math.pi
        dy = p1[1] - p2[1]
        dx = p1[0] - p2[0]
        return math.atan2(dy, dx)
    
    def find_best_direction(self, reference_point: VMobject, other_points: list[VMobject], n=36):
        angles = np.linspace(0, 2*np.pi, n)
        potential_directions = [np.array([np.cos(a), np.sin(a), 0]) for a in angles]
        center = reference_point.get_center()
        other_centers = [p.get_center() for p in other_points]
        return max(
            potential_directions, 
            key=lambda d: sum([np.linalg.norm(oc - (center + d)) for oc in other_centers])
        )
        
    def graham(self, points: list[tuple[float,float]]):
        min_x, max_x = min([p[0] for p in points]), max([p[0] for p in points])
        min_y, max_y = min([p[1] for p in points]), max([p[1] for p in points])

        # drawing the number plane
        number_plane = NumberPlane(
            x_range=(-100, 100),
            y_range=(-100, 100),
            background_line_style={"stroke_color": WHITE, "stroke_opacity": 0.4}
        )
        self.play(FadeIn(number_plane), run_time=0.5)
        
        points_mobs = VDict({
            p: Dot((*p, 0), radius=0.1, color=WHITE, fill_opacity=1.0, z_index=float('inf')) for p in points
        })
        scene_aspect_ratio = config.frame_width / config.frame_height
        # draw points and center the camera on the appropriate area
        self.play(
            self.camera.frame.animate.set(
                width=max((max_x-min_x+1)*1.2, (max_y-min_y+1)*1.2*scene_aspect_ratio)
            ).move_to(
                ((min_x+max_x)/2, (min_y+max_y)/2, 0)
        ), FadeIn(points_mobs))

        # finding lowest point p0
        p0_idx = min(range(len(points)), key=lambda i: (points[i][1], points[i][0]))
        p0 = points[p0_idx]
        p0_label = MathTex("p_0", font_size=32).next_to(points_mobs[p0], DOWN, buff=0.2)
        horizontal_line = Line((min_x-1, p0[1], 0), (max_x+1, p0[1], 0))
        dashed_lines = [DashedLine((*p0, 0), (*p, 0), color="#00EFD1", dash_length=0.15, stroke_width=1.0, z_index=float('-inf')) for p in points if p0 != p]
        self.play(
            Create(horizontal_line),
            points_mobs[p0].animate.set_color("#00EFD1"),
            Write(p0_label),
            run_time=0.5
        )
        self.play(*[Create(l) for l in dashed_lines], run_time=0.5)

        points.sort(key=lambda p: (self.polar_angle(p0, p), self.dist(p0, p)))
        angle = Sector(1.5, angle=self.polar_angle(points[1], p0), fill_opacity=0.6, stroke_color=PURPLE, stroke_width=1.5, color=BLACK)
        angle.shift(points_mobs[p0].get_center() - angle.get_arc_center())
        self.play(FadeIn(angle))

        ccw_icon = Arc(radius=0.5, angle=2/3*TAU, start_angle=1/4*PI, stroke_width=4).add_tip().scale(0.3)
        cw_icon = ccw_icon.copy().flip()
        coll_icon = Arrow(start=ORIGIN, end=RIGHT*3, stroke_width=4).scale(0.3)
        ccw_label = Text("counter clockwise", fill_opacity=0.8, font_size=20)
        cw_label = Text("clockwise", fill_opacity=0.8, font_size=20)
        coll_label = Text("collinear", fill_opacity=0.8, font_size=20)

        hull_lines = []
        hull = [p0]
        for i in range(1, len(points)):
            new_angle = Sector(1.5, angle=self.polar_angle(points[i], p0), fill_opacity=0.6, stroke_color=PURPLE, stroke_width=1.5, color=BLACK)
            new_angle.shift(points_mobs[p0].get_center() - new_angle.get_arc_center())
            line = Line(points_mobs[hull[-1]].get_center(), points_mobs[points[i]].get_center(), color=BLUE if len(hull) >= 2 else ORANGE)
            animations = [
                ReplacementTransform(angle, new_angle),
                Create(line)
            ]
            if len(hull) >= 2:
                best_direction = self.find_best_direction(points_mobs[hull[-1]], [points_mobs[hull[-2]], points_mobs[points[i]]])
                icon, label = {
                    1: (ccw_icon, ccw_label),
                    0: (coll_icon, coll_label),
                    -1: (cw_icon, cw_label)
                }[self.orientation(hull[-2], hull[-1], points[i])]
                icon.next_to(points_mobs[hull[-1]], best_direction)
                label.next_to(icon, best_direction)
                animations.extend([Create(icon), FadeIn(label)])
            self.play(animations, run_time=0.5)
            angle = new_angle
            while len(hull) >= 2 and \
            self.orientation(hull[-2], hull[-1], points[i]) != 1:
                self.wait(0.5)
                hull.pop()
                self.play(
                    Uncreate(hull_lines[-1]),
                    line.animate.put_start_and_end_on(points_mobs[hull[-1]].get_center(), points_mobs[points[i]].get_center()),
                    FadeOut(icon),
                    FadeOut(label),
                    run_time=0.5
                )
                hull_lines.pop()
                if len(hull) >= 2:
                    best_direction = self.find_best_direction(points_mobs[hull[-1]], [points_mobs[hull[-2]], points_mobs[points[i]]])
                    icon, label = {
                        1: (ccw_icon, ccw_label),
                        0: (coll_icon, coll_label),
                        -1: (cw_icon, cw_label)
                    }[self.orientation(hull[-2], hull[-1], points[i])]
                    icon.next_to(points_mobs[hull[-1]], best_direction)
                    label.next_to(icon, best_direction)
                    self.play(Create(icon), FadeIn(label), run_time=0.5)
  
            self.wait(0.5)
            if len(hull) >= 2:
                self.play(
                    line.animate.set_color(ORANGE), 
                    FadeOut(icon),
                    FadeOut(label),
                    run_time=0.5
                )
            hull.append(points[i])
            hull_lines.append(line)
            self.wait(0.5)
            
        line = Line(points_mobs[hull[-1]].get_center(), points_mobs[p0].get_center(), color=ORANGE)
        hull_lines.append(line)
        self.play(Create(line), run_time=0.5)
        convex_hull_text = Text("Convex Hull", font_size=48, color=ORANGE, weight=BOLD).next_to(points_mobs[p0], DOWN, buff=0.2)
        self.play(Write(convex_hull_text), run_time=0.5)
        self.wait(1)
        
    def construct(self):
        points = [
            (5.29, 3.48), (9.75, -1.54), (11.02, -0.28), (10.39, -0.28), (11.02, 0.98), 
            (8.48, -0.911), (9.75, 1), (9.72, 1.6), (9.12, 2.91), (7.85, 2.29), (7.21, 1.62), 
            (6.57, 0.36), (4.65, 2.29), (5.29, 0.36), (3.38, 2.91), (4.03, 1), (2.75, 1), (5.29, -1.573), 
            (3.38, -0.911), (5.94, -2.18), (2.11, -0.911), (4.66, -2.2), (3.38, -2.18), (7.21, -2.782)
        ]
        self.graham(points)
