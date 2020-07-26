import logging
import math
from ev3dev2.motor import Motor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2 import DeviceNotFound

class Ev3Service:

	_logger = logging.getLogger(__name__)
	_logger.setLevel(logging.DEBUG)

	oneMmX = 360/100
	oneMmY = 360/100
	oneMmZ = 360/100
	speedMax = 50

	x1 = 0.0
	y1 = 0.0
	z1 = 0.0

	def MoveLinear(self, x2, y2, z2):
		self._logger.info("x2=%f, y2=%f, z2=%f", x2, y2, z2)
		mX = Motor(OUTPUT_A)
		mY = Motor(OUTPUT_B)
		mZ = Motor(OUTPUT_C)

		(speedX, speedY) = self.Speed(self.x1, self.y1, x2, y2)

		dx = x2 - self.x1
		dy = y2 - self.y1
		dz = z2 - self.z1

		mZ.on_for_degrees(self.speedMax, self.oneMmZ*dz, block=True)
		mX.on_for_degrees(speedX, self.oneMmX*dx, block=False)
		mY.on_for_degrees(speedY, self.oneMmY*dy, block=False)
		mX.wait_until_not_moving()
		mY.wait_until_not_moving()
		mZ.wait_until_not_moving()

		self.x1 = x2
		self.y1 = y2
		self.z1 = z2

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

	def MotorReset(self, port):
		self._logger.info(port)
		ports = {
			'a': OUTPUT_A,
			'b': OUTPUT_B,
            'c': OUTPUT_C,
			'd': OUTPUT_D
		}
		try:
			motor = Motor(ports[port])
			motor.reset()
		except DeviceNotFound as err:
			self._logger.warn(err.message)
			pass

	"""
	To get a straigt line, the speed for the x and the y-motor must respect
	the ration between the x and y-travel. This ration id given by
		cos(alpah) for x
		sin(alpha) for y
		alpha is given by the x and y-travel with help of the atan function.
	Since we are only interested in the speed, only absolute values are returned.
	"""
	def Speed(self, x1, y1, x2, y2):
		dx = x2 - x1
		dy = y2 - y1
		alpha = math.atan2(dy, dx)
		sx = math.fabs(self.speedMax * math.cos(alpha))
		sy = math.fabs(self.speedMax * math.sin(alpha))
		return (sx, sy)
