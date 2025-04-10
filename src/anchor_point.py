import numpy as np

class AnchorPoint:
    def __init__(self, coords: tuple, len: float, lead: bool = False):
        self.x, self.y = coords
        self.len = len
        self.lead = lead
        self.v = 0.01
        self.speed = 0
        self.max_speed = 1
        self.ang_lim = 0.5
                
    def coords(self) -> tuple:
        return self.x, self.y

    def move(self, targ_coords: tuple):
        t_x, t_y = targ_coords
        move_vec = np.array([t_x - self.x, t_y - self.y], dtype=float)
        move_dist = np.linalg.norm(move_vec)
        if move_dist < 1:
            self.speed = 0
            return
        
        if move_dist > 0:
            move_vec /= move_dist

        required_speed = np.sqrt(2 * self.v * move_dist)

        if self.speed <= self.max_speed and self.speed <= required_speed:
            self.speed += self.v

        if self.speed > required_speed:
            self.speed -= self.v

        self.x += move_vec[0] * self.speed
        self.y += move_vec[1] * self.speed

    def chain_move(self, p_point_coord: tuple, pp_point_coord: tuple = None):
        p_x, p_y = p_point_coord
        move_vec = np.array([self.x - p_x, self.y - p_y], dtype=float)
        move_dist = np.linalg.norm(move_vec)
        

        if move_dist > 0:
            move_vec /= move_dist
        

        if pp_point_coord:
            pp_x, pp_y = pp_point_coord
            p_move_vec = np.array([p_x - pp_x, p_y - pp_y], dtype=float)
            p_move_dist = np.linalg.norm(p_move_vec)

            if p_move_dist > 0:
                p_move_vec /= p_move_dist

            dot_prod = np.dot(move_vec, p_move_vec)
            angle = np.arccos(np.clip(dot_prod, -1.0, 1.0))

            if angle > self.ang_lim:
                cross_prod = np.cross(np.append(move_vec, 0), np.append(p_move_vec, 0))
                rot_sign = -1 if cross_prod[2] > 0 else 1
                rot_mtrx = np.array([
                    [np.cos(self.ang_lim * rot_sign), -np.sin(self.ang_lim * rot_sign)],
                    [np.sin(self.ang_lim * rot_sign), np.cos(self.ang_lim * rot_sign)]
                ], dtype=float)

                move_vec = np.dot(rot_mtrx, p_move_vec)
        

        self.x = p_x + move_vec[0] * self.len
        self.y = p_y + move_vec[1] * self.len


    def separate(self, other):
        vec = np.array([self.x - other.x, self.y - other.y], dtype=float)
        dist = np.linalg.norm(vec)
        min_dist = self.len # Мінімальна допустима відстань

        # Якщо точки перекриваються
        if dist < min_dist and dist > 0:
            vec /= dist  # Нормалізація вектора
            overlap = (min_dist - dist) / 2  # Наскільки вони перекриваються

            # Розсовуємо точки у протилежні сторони
            self.x += vec[0] * overlap
            self.y += vec[1] * overlap
            other.x -= vec[0] * overlap
            other.y -= vec[1] * overlap
