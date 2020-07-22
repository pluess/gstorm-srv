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
		#httpRequest.Response = Mock() #Mock(spec=HttpRequest.HttpResponse)

		main.MoveLinear(None, httpRequest)
		main.ev3Service.MoveLinear.assert_called_with(1.1, 2.2, 3.3)
		#httpRequest.Response.ReturnOk.called()

if __name__ == '__main__':
    unittest.main()