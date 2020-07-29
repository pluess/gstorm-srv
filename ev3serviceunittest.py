import math
import unittest
from unittest.mock import Mock, patch, call
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

	def test_Angle(self):
		testData = (
			{'desc': 'positiv horizontal', 'x': 2.0, 'y': 2.0, 'xCenter': 10.0, 'yCenter': 2.0, 'alpha': 0.0},
			{'desc': 'negative horizontal', 'x': 2.0, 'y': 2.0, 'xCenter': -10.0, 'yCenter': 2.0, 'alpha': math.pi},
			{'desc': 'almost positive vertical', 'x': 3.0, 'y': 3.0, 'xCenter': 3.0, 'yCenter': 6.0001, 'alpha': math.pi/2},
			{'desc': 'positive vertical', 'x': 3.0, 'y': 3.0, 'xCenter': 3.0, 'yCenter': 6.0, 'alpha': math.pi/2},
			{'desc': 'negative vertical', 'x': 3.0, 'y': 3.0, 'xCenter': 3.0, 'yCenter': -6.0, 'alpha': -math.pi/2},
			{'desc': '45 degrees', 'x': 0.0, 'y': 0.0, 'xCenter': 1.0, 'yCenter': 1.0, 'alpha': math.pi/4},
			{'desc': '135 degrees', 'x': 0.0, 'y': 0.0, 'xCenter': -1.0, 'yCenter': 1.0, 'alpha': math.pi * 3/4},
			{'desc': '225 degrees', 'x': 1.0, 'y': 1.0, 'xCenter': -1.0, 'yCenter': -1.0, 'alpha': -math.pi * 3/4},
			{'desc': '315 degrees', 'x': 0.0, 'y': 0.0, 'xCenter': 1.0, 'yCenter': -1.0, 'alpha': -math.pi/4}
		)

		for testRow in testData:
			with self.subTest(testRow['desc']):
				alpha = self.ev3s.Angle(testRow['x'], testRow['y'], testRow['xCenter'], testRow['yCenter'])
				self._assertEqualWithDelta('alpha', alpha, testRow['alpha'], 0.01)


	def test_MoveArc(self):
		self.ev3s.MoveLinear = Mock()
		# semi circel with r=1 arround x=1, y=0
		# start in x=0, y=0, stop in x=2, y=0
		self.ev3s.MoveArc(2.0, 0.0, 0.0, 1.0, 0.0 ,True)
		self.assertEqual(181, self.ev3s.MoveLinear.call_count) # semi circle + last step
		self.assertEqual(2.0, self.ev3s.x1)
		self.assertEqual(0.0, self.ev3s.y1)

		calls = [
			call(1.0, 1.0, 0.0, name='1/4 circle, 12 o clock'),
			call(2.0, 0.0, 0.0, name='1/2 circle, 3 o clock'),
			call(1-math.sqrt(2)/2, math.sqrt(2)/2, 0.0, name='45°'),
			call(1+math.sqrt(2)/2, math.sqrt(2)/2, 0.0, name='135°'),
		]
		self._assertHasCallsWithDelta(self.ev3s.MoveLinear, calls, 0.0001)				

	"""
	Tests floats for almost equal values.
	"""
	def _assertEqualWithDelta(self, desc, actual, expected, delta):
		emin = expected - delta
		emax = expected + delta
		assert emin <= actual and actual<=emax, "%s is %f which is not between %f and %f" % (desc, actual, emin, emax)
		
	def _isEqualWithDelta(self, actual, expected, delta):
		emin = expected - delta
		emax = expected + delta
		return emin <= actual and actual<=emax

	"""
	Wie mock.assert_has_calls wird überprüft, ob die Mehtode mind. einmal mit diesen Werten
	aufgerufen wurde. Dabei werden nur float Werte mit einem Delta überprüft.
	"""
	def _assertHasCallsWithDelta(self, mockMethod, calls, delta):
		for expectedCall in calls:
			foundExpected = False
			expectedArgs = expectedCall.args
			for callArg in mockMethod.call_args_list:
				actualArgs = callArg.args
				if (len(expectedArgs)==len(callArg.args)):
					found = True
					for i in range(len(expectedArgs)):
						expectedFloat = expectedArgs[i]
						actualFloat = actualArgs[i]
						if (found and not (isinstance(expectedFloat, float) and isinstance(actualFloat, float) and self._isEqualWithDelta(actualFloat, expectedFloat, delta))):
						  	found = False
					if (found):
						foundExpected = True
						print("name=%s / found actual=%s / expected=%s" % (expectedCall.kwargs['name'], actualArgs, expectedArgs))
						break
			assert foundExpected, "name=%s / expected=%s not found" % (expectedCall.kwargs['name'], expectedArgs)

if __name__ == '__main__':	
	unittest.main()