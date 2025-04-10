import unittest
from unittest.mock import patch, MagicMock
from src.drawer import Drawer

class TestDrawer(unittest.TestCase):

    @patch('pygame.display.set_mode')
    @patch('pygame.display.flip')
    def test_drawer_init(self, mock_flip, mock_set_mode):
        # Тест ініціалізації Drawer
        drawer = Drawer()
        self.assertEqual(len(drawer.points), 1)
        self.assertEqual(drawer.points[0].x, 0)
        self.assertEqual(drawer.points[0].y, 0)

    @patch('pygame.display.set_mode')
    @patch('pygame.display.flip')
    def test_build_body(self, mock_flip, mock_set_mode):
        # Тест для побудови тіла
        drawer = Drawer()
        drawer.build_body([30, 40, 50])
        self.assertEqual(len(drawer.points), 4)  # Включаючи початкову точку

    @patch('pygame.display.set_mode')
    @patch('pygame.display.flip')
    @patch('pygame.draw.circle')
    def test_draw(self, mock_circle, mock_flip, mock_set_mode):
        # Тест для малювання точок
        drawer = Drawer()
        drawer.draw()
        self.assertTrue(mock_circle.called)  # Перевірка, що draw.circle був викликаний

if __name__ == '__main__':
    unittest.main()
