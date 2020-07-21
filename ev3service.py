import logging

class Ev3Service:

	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	def MoveLinear(self, x, y, z):
		self.logger.info("x=%f, y=%f, z=%f", x, y, z)
