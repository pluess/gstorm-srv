#!/usr/bin/env python3
from MicroWebSrv2  import *
from time          import sleep
from _thread       import allocate_lock
import logging
from ev3service import Ev3Service

# Logging
_FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=_FORMAT)
_rootLogger = logging.getLogger('root')
_rootLogger.setLevel(logging.DEBUG)

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

ev3Service = Ev3Service()

@WebRoute(GET, '/gotostart')
def GoTostart(microWebSrv2, request):
	_logger.info('')
	request.Response.ReturnOk()

@WebRoute(GET, '/motor/commands/<port>')
def MotorCommands(microWebSrv2, request, args):
	try:
		_logger.info(args['port'])
		port = args['port'].lower()
		allowedPorts = ['a', 'b', 'c', 'd']
		if port not in allowedPorts:
			request.Response.ReturnBadRequest()
			return
		commands = ev3Service.MotorCommands(port)
		_logger.info(commands)
		request.Response.ReturnOkJSON(commands)
	except Exception as error:
		_logger.exception(error)


@WebRoute(POST, '/move-linear')
def MoveLinear(microWebSrv2, request):
	jsonObect = request.GetPostedJSONObject()
	global _logger
	_logger.info(jsonObect)
	ev3Service.MoveLinear(
		jsonObect['x'],
		jsonObect['y'],
		jsonObect['z'],
	)
	request.Response.ReturnOk()

if __name__ == '__main__':
	# Instanciates the MicroWebSrv2 class,
	mws2 = MicroWebSrv2()

	# For embedded MicroPython, use a very light configuration,
	mws2.SetEmbeddedConfig()

	# Starts the server as easily as possible in managed mode,
	mws2.BindAddress = ('0.0.0.0', 8080)

	mws2.StartManaged()


	try :
		while mws2.IsRunning :
			sleep(1)
	except KeyboardInterrupt :
		pass
