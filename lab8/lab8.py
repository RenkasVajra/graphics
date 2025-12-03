import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time


# Глобальные переменные для управления сценой
WIDTH = 600
HEIGHT = 600
MAX_DEPTH = 5  # Максимальная глубина рекурсии для отражений/преломлений


# Класс для источника света
class Light:
    def __init__(self, position, intensity=1.0, color=(1.0, 1.0, 1.0)):
        self.position = np.array(position, dtype=np.float64)
        self.intensity = intensity
        self.color = np.array(color, dtype=np.float64)


# Базовый класс для объектов сцены
class SceneObject:
    def __init__(self, color, ambient=0.1, diffuse=0.7, specular=0.3, shininess=50,
                 reflective=0.0, transparent=0.0, refractive_index=1.0):
        self.color = np.array(color, dtype=np.float64)
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflective = reflective  # Коэффициент отражения (0-1)
        self.transparent = transparent  # Коэффициент прозрачности (0-1)
        self.refractive_index = refractive_index  # Коэффициент преломления
    
    def intersect(self, ray_origin, ray_direction):
        """Возвращает расстояние до пересечения или None"""
        raise NotImplementedError
    
    def get_normal(self, point):
        """Возвращает нормаль в точке пересечения"""
        raise NotImplementedError


# Класс для сферы
class Sphere(SceneObject):
    def __init__(self, center, radius, **kwargs):
        super().__init__(**kwargs)
        self.center = np.array(center, dtype=np.float64)
        self.radius = radius
    
    def intersect(self, ray_origin, ray_direction):
        oc = ray_origin - self.center
        a = np.dot(ray_direction, ray_direction)
        b = 2.0 * np.dot(oc, ray_direction)
        c = np.dot(oc, oc) - self.radius ** 2
        discriminant = b ** 2 - 4 * a * c
        
        if discriminant < 0:
            return None
        
        sqrt_disc = np.sqrt(discriminant)
        t1 = (-b - sqrt_disc) / (2.0 * a)
        t2 = (-b + sqrt_disc) / (2.0 * a)
        
        # Возвращаем ближайшее положительное пересечение
        if t1 > 0.001:
            return t1
        elif t2 > 0.001:
            return t2
        return None
    
    def get_normal(self, point):
        normal = point - self.center
        return normal / np.linalg.norm(normal)


# Класс для плоскости
class Plane(SceneObject):
    def __init__(self, point, normal, **kwargs):
        super().__init__(**kwargs)
        self.point = np.array(point, dtype=np.float64)
        self.normal = np.array(normal, dtype=np.float64)
        self.normal = self.normal / np.linalg.norm(self.normal)
    
    def intersect(self, ray_origin, ray_direction):
        denom = np.dot(self.normal, ray_direction)
        if abs(denom) < 0.001:  # Луч параллелен плоскости
            return None
        
        t = np.dot(self.point - ray_origin, self.normal) / denom
        if t > 0.001:
            return t
        return None
    
    def get_normal(self, point):
        return self.normal


# Функция для вычисления отраженного луча
def reflect(incident, normal):
    """Вычисляет отраженный вектор"""
    return incident - 2 * np.dot(incident, normal) * normal


# Функция для вычисления преломленного луча (закон Снеллиуса)
def refract(incident, normal, n1, n2):
    """Вычисляет преломленный вектор"""
    cos_i = -np.dot(incident, normal)
    if cos_i < 0:
        cos_i = -cos_i
        normal = -normal
        n1, n2 = n2, n1
    
    n = n1 / n2
    sin2_t = n * n * (1 - cos_i * cos_i)
    
    if sin2_t > 1:  # Полное внутреннее отражение
        return None
    
    cos_t = np.sqrt(1 - sin2_t)
    return n * incident + (n * cos_i - cos_t) * normal


# Функция для трассировки лучей с рекурсией
def trace_ray(ray_origin, ray_direction, objects, lights, depth=0, n1=1.0):
    """Рекурсивная трассировка луча"""
    if depth > MAX_DEPTH:
        return np.array([0.0, 0.0, 0.0], dtype=np.float64)
    
    # Находим ближайшее пересечение
    closest_object = None
    closest_t = np.inf
    
    for obj in objects:
        t = obj.intersect(ray_origin, ray_direction)
        if t and t < closest_t:
            closest_t = t
            closest_object = obj
    
    if closest_object is None:
        # Фон (градиент неба)
        t = 0.5 * (ray_direction[1] + 1.0)
        return (1.0 - t) * np.array([1.0, 1.0, 1.0]) + t * np.array([0.5, 0.7, 1.0])
    
    # Точка пересечения
    intersection_point = ray_origin + closest_t * ray_direction
    normal = closest_object.get_normal(intersection_point)
    
    # Начальный цвет
    color = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    
    # Фоновое освещение
    color += closest_object.ambient * closest_object.color
    
    # Обработка источников света
    for light in lights:
        light_direction = light.position - intersection_point
        light_distance = np.linalg.norm(light_direction)
        light_direction = light_direction / light_distance
        
        # Проверка на тени
        shadow_ray_origin = intersection_point + 0.001 * normal
        in_shadow = False
        for obj in objects:
            if obj is closest_object:
                continue
            shadow_t = obj.intersect(shadow_ray_origin, light_direction)
            if shadow_t and shadow_t < light_distance:
                in_shadow = True
                break
        
        if not in_shadow:
            # Диффузное освещение
            diffuse_factor = max(np.dot(normal, light_direction), 0.0)
            color += (closest_object.diffuse * diffuse_factor * 
                     closest_object.color * light.color * light.intensity)
            
            # Зеркальное освещение (модель Фонга)
            view_direction = -ray_direction
            reflect_direction = reflect(-light_direction, normal)
            specular_factor = max(np.dot(view_direction, reflect_direction), 0.0) ** closest_object.shininess
            color += (closest_object.specular * specular_factor * 
                     light.color * light.intensity)
    
    # Рекурсивные отражения
    if closest_object.reflective > 0.0 and depth < MAX_DEPTH:
        reflected_direction = reflect(ray_direction, normal)
        reflected_color = trace_ray(
            intersection_point + 0.001 * normal,
            reflected_direction,
            objects,
            lights,
            depth + 1,
            n1
        )
        color = (1 - closest_object.reflective) * color + closest_object.reflective * reflected_color
    
    # Рекурсивные преломления
    if closest_object.transparent > 0.0 and depth < MAX_DEPTH:
        n2 = closest_object.refractive_index
        refracted_direction = refract(ray_direction, normal, n1, n2)
        
        if refracted_direction is not None:
            refracted_color = trace_ray(
                intersection_point - 0.001 * normal,
                refracted_direction,
                objects,
                lights,
                depth + 1,
                n2
            )
            # Френелевское отражение (упрощенная версия)
            fresnel = 0.1  # Упрощенный коэффициент Френеля
            color = (1 - closest_object.transparent) * color + \
                   closest_object.transparent * (
                       (1 - fresnel) * refracted_color + fresnel * color
                   )
    
    return np.clip(color, 0.0, 1.0)


# Глобальные переменные для объектов сцены
objects = []
lights = []


# Функция рендеринга сцены
def render_scene(width, height):
    """Рендерит сцену в массив пикселей"""
    image = np.zeros((height, width, 3), dtype=np.float32)
    
    # Параметры камеры
    camera_pos = np.array([0.0, 0.0, 5.0], dtype=np.float64)
    aspect_ratio = width / height
    fov = 0.785  # ~45 градусов
    
    for y in range(height):
        for x in range(width):
            # Преобразование координат пикселя в направление луча
            ndc_x = (2.0 * x / width - 1.0) * aspect_ratio * np.tan(fov / 2.0)
            ndc_y = (1.0 - 2.0 * y / height) * np.tan(fov / 2.0)
            
            ray_direction = np.array([ndc_x, ndc_y, -1.0], dtype=np.float64)
            ray_direction = ray_direction / np.linalg.norm(ray_direction)
            
            # Трассировка луча
            color = trace_ray(camera_pos, ray_direction, objects, lights)
            image[y, x] = color
    
    return image


# Класс приложения с GUI
class RayTracingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Трассировка лучей - Управление параметрами")
        
        # Создаем объекты сцены по умолчанию
        self.init_scene()
        
        # Создаем интерфейс
        self.create_ui()
        
        # Запускаем рендеринг
        self.render_image()
    
    def init_scene(self):
        """Инициализация сцены с объектами"""
        global objects, lights
        
        objects = [
            # Красная отражающая сфера
            Sphere(
                center=[-1.5, 0.0, -3.0],
                radius=0.8,
                color=[1.0, 0.2, 0.2],
                ambient=0.1,
                diffuse=0.6,
                specular=0.8,
                shininess=50,
                reflective=0.5,
                transparent=0.0,
                refractive_index=1.0
            ),
            # Зеленая прозрачная сфера
            Sphere(
                center=[1.5, 0.0, -3.0],
                radius=0.8,
                color=[0.2, 1.0, 0.2],
                ambient=0.1,
                diffuse=0.4,
                specular=0.9,
                shininess=100,
                reflective=0.2,
                transparent=0.8,
                refractive_index=1.5
            ),
            # Синяя сфера
            Sphere(
                center=[0.0, -1.5, -4.0],
                radius=0.6,
                color=[0.2, 0.2, 1.0],
                ambient=0.1,
                diffuse=0.7,
                specular=0.5,
                shininess=30,
                reflective=0.3,
                transparent=0.0,
                refractive_index=1.0
            ),
            # Пол (плоскость)
            Plane(
                point=[0.0, -2.0, 0.0],
                normal=[0.0, 1.0, 0.0],
                color=[0.8, 0.8, 0.8],
                ambient=0.2,
                diffuse=0.6,
                specular=0.1,
                shininess=10,
                reflective=0.1,
                transparent=0.0,
                refractive_index=1.0
            ),
        ]
        
        lights = [
            Light([5.0, 5.0, 5.0], intensity=1.0, color=[1.0, 1.0, 1.0]),
            Light([-5.0, 3.0, -5.0], intensity=0.5, color=[1.0, 1.0, 1.0]),
        ]
    
    def create_ui(self):
        """Создание интерфейса управления"""
        # Фрейм для изображения
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()
        
        # Фрейм для управления
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)
        
        # Заголовок
        title = tk.Label(self.control_frame, text="Управление параметрами", 
                        font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Выбор объекта
        tk.Label(self.control_frame, text="Выбрать объект:").pack(anchor=tk.W)
        self.object_var = tk.StringVar(value="Объект 1 (Красная сфера)")
        object_combo = ttk.Combobox(self.control_frame, textvariable=self.object_var,
                                   values=["Объект 1 (Красная сфера)", 
                                          "Объект 2 (Зеленая сфера)",
                                          "Объект 3 (Синяя сфера)",
                                          "Объект 4 (Пол)"],
                                   state="readonly", width=25)
        object_combo.pack(pady=5)
        object_combo.bind("<<ComboboxSelected>>", self.on_object_change)
        
        # Коэффициент отражения
        self.reflective_var = tk.DoubleVar(value=0.5)
        self.create_slider("Отражение:", self.reflective_var, 0.0, 1.0, 
                          self.update_object)
        
        # Коэффициент прозрачности
        self.transparent_var = tk.DoubleVar(value=0.0)
        self.create_slider("Прозрачность:", self.transparent_var, 0.0, 1.0,
                          self.update_object)
        
        # Коэффициент преломления
        self.refractive_var = tk.DoubleVar(value=1.0)
        self.create_slider("Преломление:", self.refractive_var, 1.0, 2.5,
                          self.update_object)
        
        # Диффузное освещение
        self.diffuse_var = tk.DoubleVar(value=0.6)
        self.create_slider("Диффузное:", self.diffuse_var, 0.0, 1.0,
                          self.update_object)
        
        # Зеркальное освещение
        self.specular_var = tk.DoubleVar(value=0.8)
        self.create_slider("Зеркальное:", self.specular_var, 0.0, 1.0,
                          self.update_object)
        
        # Блеск
        self.shininess_var = tk.DoubleVar(value=50.0)
        self.create_slider("Блеск:", self.shininess_var, 1.0, 200.0,
                          self.update_object)
        
        # Кнопка перерисовки
        render_btn = tk.Button(self.control_frame, text="Перерисовать сцену",
                              command=self.render_image, bg="#4CAF50", fg="white",
                              font=("Arial", 12, "bold"), padx=10, pady=5)
        render_btn.pack(pady=20)
        
        # Информация
        info = tk.Label(self.control_frame, 
                       text="Измените параметры и нажмите\n'Перерисовать сцену'",
                       font=("Arial", 9), fg="gray")
        info.pack(pady=10)
        
        self.current_object_index = 0
    
    def create_slider(self, label_text, variable, from_, to, command):
        """Создает слайдер с меткой"""
        frame = tk.Frame(self.control_frame)
        frame.pack(pady=5, fill=tk.X)
        
        label = tk.Label(frame, text=label_text, width=12, anchor=tk.W)
        label.pack(side=tk.LEFT)
        
        slider = tk.Scale(frame, variable=variable, from_=from_, to=to,
                         resolution=0.01, orient=tk.HORIZONTAL, length=150,
                         command=lambda x: None)  # Обновление только при перерисовке
        slider.pack(side=tk.LEFT)
        
        value_label = tk.Label(frame, textvariable=variable, width=6)
        value_label.pack(side=tk.LEFT)
    
    def on_object_change(self, event=None):
        """Обновление слайдеров при смене объекта"""
        index = self.object_var.get()
        if "Объект 1" in index:
            self.current_object_index = 0
        elif "Объект 2" in index:
            self.current_object_index = 1
        elif "Объект 3" in index:
            self.current_object_index = 2
        elif "Объект 4" in index:
            self.current_object_index = 3
        
        obj = objects[self.current_object_index]
        self.reflective_var.set(obj.reflective)
        self.transparent_var.set(obj.transparent)
        self.refractive_var.set(obj.refractive_index)
        self.diffuse_var.set(obj.diffuse)
        self.specular_var.set(obj.specular)
        self.shininess_var.set(obj.shininess)
    
    def update_object(self, event=None):
        """Обновление параметров объекта (вызывается при перерисовке)"""
        obj = objects[self.current_object_index]
        obj.reflective = self.reflective_var.get()
        obj.transparent = self.transparent_var.get()
        obj.refractive_index = self.refractive_var.get()
        obj.diffuse = self.diffuse_var.get()
        obj.specular = self.specular_var.get()
        obj.shininess = self.shininess_var.get()
    
    def render_image(self):
        """Рендеринг изображения в отдельном потоке"""
        self.image_label.config(text="Рендеринг... Пожалуйста, подождите...")
        self.root.update()
        
        def render_thread():
            start_time = time.time()
            image_array = render_scene(WIDTH, HEIGHT)
            elapsed = time.time() - start_time
            
            # Конвертация в PIL Image
            image_array_uint8 = (image_array * 255).astype(np.uint8)
            pil_image = Image.fromarray(image_array_uint8)
            pil_image = pil_image.resize((WIDTH, HEIGHT), Image.NEAREST)
            
            # Обновление GUI в главном потоке
            self.root.after(0, lambda: self.update_image(pil_image, elapsed))
        
        thread = threading.Thread(target=render_thread)
        thread.daemon = True
        thread.start()
    
    def update_image(self, pil_image, elapsed_time):
        """Обновление изображения в GUI"""
        photo = ImageTk.PhotoImage(pil_image)
        self.image_label.config(image=photo, text="")
        self.image_label.image = photo  # Сохраняем ссылку
        
        # Обновляем параметры объекта
        self.update_object()
        
        # Показываем время рендеринга
        info_text = f"Время рендеринга: {elapsed_time:.2f} сек"
        if hasattr(self, 'time_label'):
            self.time_label.config(text=info_text)
        else:
            self.time_label = tk.Label(self.control_frame, text=info_text,
                                      font=("Arial", 9), fg="blue")
            self.time_label.pack(pady=5)


# Главная функция
def main():
    root = tk.Tk()
    app = RayTracingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
