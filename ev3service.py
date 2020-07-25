import logging
from ev3dev2.motor import LargeMotor, Motor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2 import DeviceNotFound

class Ev3Service:

	_logger = logging.getLogger(__name__)
	_logger.setLevel(logging.DEBUG)

	def MoveLinear(self, x, y, z):
		self._logger.info("x=%f, y=%f, z=%f", x, y, z)
		mA = LargeMotor(OUTPUT_A)
		mB = LargeMotor(OUTPUT_B)

	def MotorCommands(self, port):
		self._logger.info(port)
		ports = {
			'a': OUTPUT_A,
			'b': OUTPUT_B,
            'c': OUTPUT_C,
			'd': OUTPUT_D
		}
		try:
			motor = Motor(ports[port])
			commands = motor.commands
			self._logger.info(commands)
			return commands
		except DeviceNotFound:
			return list()

