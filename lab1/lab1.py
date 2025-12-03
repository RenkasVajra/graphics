import math
from tkinter import Tk, Canvas, Frame, Button
from typing import List, Tuple


class Pen:
    def __init__(self, thickness: int, color: str):
        self.thickness = thickness
        self.color = color


class Line:
    def __init__(self, start_point: Tuple[int, int], end_point: Tuple[int, int],
                 pen: Pen, line_type='solid', cap_style='round'):

        self.start_point = start_point
        self.end_point = end_point
        self.pen = pen
        self.line_type = line_type
        self.cap_style = cap_style

    def draw(self, canvas: Canvas):
        if self.line_type == 'solid':
            canvas.create_line(
                *self.start_point,
                *self.end_point,
                fill=self.pen.color,
                width=self.pen.thickness,
                capstyle=self.cap_style
            )
        elif self.line_type == 'dash':
            canvas.create_line(
                *self.start_point,
                *self.end_point,
                fill=self.pen.color,
                dash=(4, 4),
                width=self.pen.thickness,
                capstyle=self.cap_style
            )

    def erase(self, canvas: Canvas, background_color: str):
        # Эффект стирания путём перерисовки той же линии цветом фона
        temp_pen = Pen(thickness=self.pen.thickness, color=background_color)
        eraser_line = Line(start_point=self.start_point, end_point=self.end_point, pen=temp_pen)
        eraser_line.draw(canvas)


class Ellipse:
    def __init__(self, center: Tuple[int, int], radius_x: float, radius_y: float,
                 outline_color: str, fill_color: str):

        self.center = center
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.outline_color = outline_color
        self.fill_color = fill_color

    def draw(self, canvas: Canvas):
        left_top_corner = (self.center[0]-self.radius_x, self.center[1]-self.radius_y)
        right_bottom_corner = (self.center[0]+self.radius_x, self.center[1]+self.radius_y)
        canvas.create_oval(left_top_corner + right_bottom_corner,
                           outline=self.outline_color, fill=self.fill_color)

    def label(self, canvas: Canvas, label_text: str, font_size: int = 12):
        canvas.create_text(self.center, text=label_text, fill='black', font=f'Times {font_size}')

    def erase(self, canvas: Canvas, background_color: str):
        erased_ellipse = Ellipse(
            center=self.center,
            radius_x=self.radius_x,
            radius_y=self.radius_y,
            outline_color=background_color,
            fill_color=background_color
        )
        erased_ellipse.draw(canvas)


class Polygon:
    def __init__(self, vertices: List[Tuple[int, int]], outline_color: str, fill_color: str):

        self.vertices = vertices # Список вершин многоугольника
        self.outline_color = outline_color
        self.fill_color = fill_color

    @staticmethod
    def create_regular_polygon(center: Tuple[int, int], num_sides: int, side_length: float):
        """Создание регулярного многоугольника"""
        angle_step = 2*math.pi / num_sides
        points = []
        for i in range(num_sides):
            x = center[0] + side_length * math.cos(i * angle_step)
            y = center[1] + side_length * math.sin(i * angle_step)
            points.append((x, y))
        return points

    def draw(self, canvas: Canvas):
        canvas.create_polygon(self.vertices, outline=self.outline_color, fill=self.fill_color)

    def erase(self, canvas: Canvas, background_color: str):
        erased_polygon = Polygon(vertices=self.vertices, outline_color=background_color, fill_color=background_color)
        erased_polygon.draw(canvas)


# Основная форма приложения
root = Tk()
canvas_width = 800
canvas_height = 600
canvas_bg_color = '#FFFFFF'

canvas_frame = Frame(root)
canvas_frame.pack(side='top', pady=10)

canvas = Canvas(canvas_frame, bg=canvas_bg_color, height=canvas_height, width=canvas_width)
canvas.pack(fill='both', expand=True)

pen = Pen(thickness=2, color='#FF0000')


line = Line(start_point=(50, 50), end_point=(200, 200), pen=pen, line_type='dash')
ellipse = Ellipse(center=(400, 300), radius_x=100, radius_y=50, outline_color='#0000FF', fill_color='#FFFF00')
polygon_vertices = [(300, 400), (350, 450), (400, 400)]
polygon = Polygon(vertices=polygon_vertices, outline_color='#00FF00', fill_color='#808080')


def draw_all():
    """Функция отображения фигур"""
    line.draw(canvas)
    ellipse.draw(canvas)
    polygon.draw(canvas)


def clear_canvas():
    """Функция очистки листа"""
    canvas.delete("all")


draw_button = Button(root, text="Draw All Shapes", command=draw_all)
clear_button = Button(root, text="Clear Canvas", command=clear_canvas)

draw_button.pack(padx=10, pady=5)
clear_button.pack(padx=10, pady=5)

root.mainloop()
