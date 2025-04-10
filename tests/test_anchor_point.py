import unittest
from src.anchor_point import AnchorPoint

class TestAnchorPoint(unittest.TestCase):
	def test_coords_return(self):
		point = AnchorPoint((10, 20), 5)
		self.assertEqual(point.coords(), (10, 20))

	def test_move_towards_target(self):
		point = AnchorPoint((0, 0), 5)
		target = (10, 0)
		initial_x = point.x
		point.move(target)
		self.assertGreater(point.x, initial_x)
		self.assertEqual(point.y, 0)

	def test_separate_overlap(self):
		p1 = AnchorPoint((0, 0), 10)
		p2 = AnchorPoint((5, 0), 10)
		p1.separate(p2)
		dist = ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5
		self.assertGreaterEqual(dist, p1.len)

if __name__ == "__main__":
	unittest.main()