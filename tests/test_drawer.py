import unittest
from unittest.mock import patch, MagicMock
import pygame as pg
from src.drawer import Drawer

class TestDrawer(unittest.TestCase):

    @patch('pygame.display.set_mode')
    @patch('pygame.display.flip')
    def test_drawer_init(self, mock_flip, mock_set_mode):
        drawer = Drawer()
        self.assertEqual(len(drawer.points), 1)
        self.assertEqual(drawer.points[0].x, 0)
        self.assertEqual(drawer.points[0].y, 0)

    @patch('pygame.display.set_mode')
    @patch('pygame.display.flip')
    def test_build_body(self, mock_flip, mock_set_mode):
        drawer = Drawer()
        drawer.build_body([30, 40, 50])
        self.assertEqual(len(drawer.points), 4)  # Включаючи початкову точку

    @patch('pygame.display.set_mode')
    @patch('pygame.display.flip')
    @patch('pygame.draw.circle')
    def test_draw_lead_point(self, mock_circle, mock_flip, mock_set_mode):
        drawer = Drawer()
        drawer.draw()
        self.assertTrue(mock_circle.called)

    @patch('pygame.display.set_mode')
    @patch('pygame.display.flip')
    @patch('pygame.draw.circle')
    def test_draw_non_lead_points(self, mock_circle, mock_flip, mock_set_mode):
        drawer = Drawer()
        drawer.points = []  # Очистимо початкову
        drawer.points.append(MagicMock(lead=False, coords=MagicMock(return_value=(10, 10)), len=20))
        drawer.draw()
        self.assertEqual(mock_circle.call_count, 2)

    @patch('pygame.key.get_pressed')
    @patch('pygame.mouse.get_pos', return_value=(100, 100))
    @patch('pygame.display.set_mode')
    @patch('pygame.draw.circle')
    def test_update_logic(self, mock_circle, mock_set_mode, mock_mouse, mock_get_pressed):
        mock_screen = MagicMock()
        mock_set_mode.return_value = mock_screen

        mock_keys = [0] * 512
        mock_keys[pg.K_SPACE] = 1
        mock_get_pressed.return_value = mock_keys

        drawer = Drawer()
        lead_point = MagicMock(lead=True)
        non_lead = MagicMock(lead=False)
        drawer.points = [lead_point, non_lead]

        drawer.update()

        mock_screen.fill.assert_called_once_with("black")
        lead_point.move.assert_called_once_with((100, 100))
        non_lead.chain_move.assert_called()
        non_lead.separate.assert_called()

    @patch('pygame.time.Clock')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.display.flip')
    @patch('pygame.event.get')
    @patch.object(Drawer, 'update')
    def test_run_once(self, mock_update, mock_event, mock_flip, mock_caption, mock_set_mode, mock_clock_class):
        mock_screen = MagicMock()
        mock_set_mode.return_value = mock_screen

        mock_clock = MagicMock()
        mock_clock.get_fps.return_value = 60.0
        mock_clock_class.return_value = mock_clock

        # Щоб вийти з циклу вручну, передамо дві події:
        # 1. звичайну, яка дозволить пройти один цикл
        # 2. pg.QUIT, щоб після цього Drawer.run() завершився
        mock_event.side_effect = [
            [MagicMock(type=pg.NOEVENT)],
            [MagicMock(type=pg.QUIT)]
        ]

        drawer = Drawer()

        with self.assertRaises(SystemExit):
            drawer.run()

        # Перевірки
        mock_clock.tick.assert_called_once()
        mock_update.assert_called_once()
        mock_caption.assert_called_once_with('FPS: 60.00')
        mock_flip.assert_called_once()


if __name__ == '__main__':
    unittest.main()
