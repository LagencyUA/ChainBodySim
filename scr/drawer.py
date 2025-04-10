import pygame as pg
from anchor_point import AnchorPoint

class Drawer:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1280,720))
        self.clock = pg.time.Clock()
        self.points = [AnchorPoint((0,0), 0, True)]

    def build_body(self, widths: list):
        whole_w = sum(widths)
        start_pos_x = self.screen.get_width() / 2 - whole_w / 2
        start_pos_y = self.screen.get_height() / 2
        self.points[0].x = start_pos_x
        self.points[0].y = start_pos_y
        for width in widths:
            start_pos_x += width
            self.points.append(AnchorPoint((start_pos_x, start_pos_y), width))


    def draw(self):
        for point in self.points:
            if point.lead:
                pg.draw.circle(self.screen, "blue", point.coords(), 5)
            else:
                pg.draw.circle(self.screen, "grey", point.coords(), point.len, 2)
                pg.draw.circle(self.screen, "white", point.coords(), 5)
        

    def update(self):
        self.screen.fill("black")
        pressed_key = pg.key.get_pressed()
        if pressed_key[pg.K_SPACE]:
            for point in self.points:
                if point.lead:
                    point.move(pg.mouse.get_pos())
                else:
                    prew_point = self.points[self.points.index(point) - 1]
                    prew_prew_point = None
                    if self.points.index(point) > 1:
                        prew_prew_point = self.points[self.points.index(point) - 2]
                    point.chain_move(prew_point.coords(), prew_prew_point.coords() if prew_prew_point else None)
                    for separation_p in self.points:
                        if point != separation_p:
                            point.separate(separation_p)

        self.draw()


    def run(self):
        while True:

            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            
            self.clock.tick()
            pg.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')
            self.update()
            pg.display.flip()