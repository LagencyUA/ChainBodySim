import unittest
from src.anchor_point import AnchorPoint

class TestAnchorPoint(unittest.TestCase):

    def test_init(self):
        # Тест ініціалізації
        p1 = AnchorPoint((0, 0), 10)
        self.assertEqual(p1.x, 0)
        self.assertEqual(p1.y, 0)
        self.assertEqual(p1.len, 10)
        self.assertFalse(p1.lead)
        self.assertEqual(p1.v, 0.01)
        self.assertEqual(p1.speed, 0)
        self.assertEqual(p1.max_speed, 1)
        self.assertEqual(p1.ang_lim, 0.5)

    def test_coords(self):
        # Тест для координат
        p1 = AnchorPoint((3, 4), 10)
        self.assertEqual(p1.coords(), (3, 4))

    def test_move(self):
        # Тест руху точки
        p1 = AnchorPoint((0, 0), 10)
        p1.move((10, 10))  # Рухаємо точку
        self.assertGreater(p1.x, 0)
        self.assertGreater(p1.y, 0)

    def test_chain_move(self):
        # Тест для руху точки по ланцюгу
        p1 = AnchorPoint((0, 0), 10)
        p2 = AnchorPoint((20, 0), 10)
        p1.chain_move(p2.coords())
        self.assertNotEqual(p1.coords(), (0, 0))  

    def test_separate(self):
        # Тест для перевірки методики розділення точок
        p1 = AnchorPoint((0, 0), 10)
        p2 = AnchorPoint((5, 0), 10)
        p1.separate(p2)
        self.assertGreaterEqual(((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5, 10)

    def test_separate_overlap(self):
        # Тест для перекриття точок
        p1 = AnchorPoint((0, 0), 10)
        p2 = AnchorPoint((5, 0), 10)
        p1.separate(p2)
        dist = ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5
        self.assertGreaterEqual(dist, p1.len)
    
    def test_move_no_dist(self):
        # Тест для випадку, коли точка не має рухатись
        p1 = AnchorPoint((0, 0), 10)
        p1.move((0, 0))  # Точка не повинна рухатись
        self.assertEqual(p1.x, 0)
        self.assertEqual(p1.y, 0)
    
    def test_move_min_dist(self):
        # Тест для маленької відстані
        p1 = AnchorPoint((0, 0), 10)
        p1.move((1, 0))  # Відстань маленька, точка повинна рухатись
        self.assertGreater(p1.x, 0)
    
    def test_chain_move_with_angle(self):
        # Тест для руху з перевіркою кута
        p1 = AnchorPoint((0, 0), 10)
        p2 = AnchorPoint((20, 0), 10)
        p3 = AnchorPoint((40, 0), 10)
        p1.chain_move(p2.coords(), p3.coords())
        self.assertNotEqual(p1.coords(), (0, 0))  
        
if __name__ == '__main__':
    unittest.main()