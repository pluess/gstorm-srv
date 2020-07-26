import unittest
from unittest.mock import Mock, patch
import ev3service

class Ev3ServiceUnitTest(unittest.TestCase):

	def setUp(self):
		self.ev3s = ev3service.Ev3Service()
		self.ev3s.speedMax = 20

	@patch('ev3service.Motor', autospec=True)
	def test_MotorCommands(self, motorMock):
		returnValueList = ['forward', 'backward', 'stop', 'reset']
		motorMock.return_value.commands = returnValueList

		commands = self.ev3s.MotorCommands('b')
		self.assertEqual(commands, returnValueList)

	def test_MotorCommands_WithWrongPort(self):
		self.assertRaises(KeyError, self.ev3s.MotorCommands, 'y')

	@patch('ev3service.Motor', autospec=True)
	def test_MotorReset(self, motorMock):
		self.ev3s.MotorReset('b')
		motorMock.return_value.reset.assert_called_once()

	@patch('ev3service.Motor', autospec=True)
	def test_MoveLinear(self, motorMock):
		self.ev3s.MoveLinear(10.0, 10.0, 0.0)
		assert motorMock.return_value.on_for_degrees.call_count == 3
		assert motorMock.return_value.wait_until_not_moving.call_count == 3
		self.assertEqual(self.ev3s.x1, 10.0)
		self.assertEqual(self.ev3s.y1, 10.0)
		self.assertEqual(self.ev3s.z1, 0.0)

	def test_Speed(self):
		testData = (
			{'desc': '45 degrees', 'x1': 0.0, 'y1': 0.0, 'x2': 10.0, 'y2': 10.0, 'sx': 14.14, 'sy': 14.14},
			{'desc': 'horizontal', 'x1': 0.0, 'y1': 0.0, 'x2': 10.0, 'y2': 0.0, 'sx': 20, 'sy': 0.0},
			{'desc': 'vertical', 'x1': 0.0, 'y1': 0.0, 'x2': 0.0, 'y2': 10.0, 'sx': 0.0, 'sy': 20},
			{'desc': '225 degrees (negative coodrinates)', 'x1': 0.0, 'y1': 0.0, 'x2': -10.0, 'y2': -10.0, 'sx': 14.14, 'sy': 14.14}
		)

		for testRow in testData:
			with self.subTest(testRow['desc']):
				(sx, sy) = self.ev3s.Speed(testRow['x1'], testRow['y1'], testRow['x2'], testRow['y2'])
				self._assertEqualWithDelta('x', sx, testRow['sx'], 0.01)
				self._assertEqualWithDelta('y', sy, testRow['sy'], 0.01)

	"""
	Tests floats for almost equal values.
	"""
	def _assertEqualWithDelta(self, desc, actual, expected, delta):
		emin = expected - delta
		emax = expected + delta
		assert emin <= actual and actual<=emax, "%s is %f which is not between %f and %f" % (desc, actual, emin, emax)

if __name__ == '__main__':
    unittest.main()