import unittest
from unittest.mock import Mock
import main
from MicroWebSrv2  import HttpRequest
from ev3service import Ev3Service

class MainUnitTest(unittest.TestCase):

	def test_MoveLinear(self):        
		main.ev3Service = Mock(spec=Ev3Service)

		httpRequest = Mock(spec=HttpRequest)
		httpRequest.GetPostedJSONObject = Mock(return_value={'x': 1.1, 'y': 2.2, 'z': 3.3})

		main.MoveLinear(None, httpRequest)
		main.ev3Service.MoveLinear.assert_called_once_with(1.1, 2.2, 3.3)
		httpRequest.Response.ReturnOk.assert_called_once()

	def test_MotorCommands(self):
		main.ev3Service = Mock(spec=Ev3Service)
		returnValueList = ['forward', 'backward', 'stop', 'reset']
		main.ev3Service.MotorCommands = Mock(return_value=returnValueList)
		httpRequest = Mock(spec=HttpRequest)
		args = {'port': 'A'}

		main.MotorCommands(None, httpRequest, args)
		main.ev3Service.MotorCommands.assert_called_once_with('a')
		httpRequest.Response.ReturnOkJSON.assert_called_once_with(returnValueList)

	def test_MotorCommands_WithWrongPort(self):
		main.ev3Service = Mock(spec=Ev3Service)
		returnValueList = ['forward', 'backward', 'stop', 'reset']
		httpRequest = Mock(spec=HttpRequest)
		args = {'port': 'z'}

		main.MotorCommands(None, httpRequest, args)
		httpRequest.Response.ReturnBadRequest.assert_called_once()
		main.ev3Service.MotorCommands.assert_not_called()


if __name__ == '__main__':
    unittest.main()