#!/usr/bin/env python3
from MicroWebSrv2  import *
from time          import sleep
from _thread       import allocate_lock
import logging
from ev3service import Ev3Service

# Logging
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
rootLogger = logging.getLogger('root')
rootLogger.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ev3Service = Ev3Service()

@WebRoute(GET, '/gotostart')
def GoTostart(microWebSrv2, request):
	logger.info('')
	request.Response.ReturnOk()

@WebRoute(POST, '/move-linear')
def MoveLinear(microWebSrv2, request):
	jsonObect = request.GetPostedJSONObject()
	global logger
	logger.info(jsonObect)
	ev3Service.MoveLinear(
		jsonObect['x'],
		jsonObect['y'],
		jsonObect['z'],
	)
	request.Response.ReturnOk()


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
