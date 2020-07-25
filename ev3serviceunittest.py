import unittest
from unittest.mock import Mock, patch
#from ev3dev2.motor import Motor
import ev3service

class Ev3ServiceUnitTest(unittest.TestCase):

	@patch('ev3service.Motor', autospec=True)
	def test_MotorCommands(self, motorMock):
		ev3s = ev3service.Ev3Service()
		returnValueList = ['forward', 'backward', 'stop', 'reset']
		motorMock.return_value.commands = returnValueList

		commands = ev3s.MotorCommands('b')
		self.assertEquals(commands, returnValueList)

	def test_MotorCommands_WithWrongPort(self):
		ev3s = ev3service.Ev3Service()
		self.assertRaises(KeyError, ev3s.MotorCommands, 'y')


if __name__ == '__main__':
    unittest.main()