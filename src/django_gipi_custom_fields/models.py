
class Orari():
	"""
	Describes oraries during a week. Naturally the data type
	is a list of 4 datetime objects for each day.

	>>> o = Orari()
	>>> o.orari
	{'monday': None, 'tuesday': None, 'wednesday': None, 'thursday': None, 'friday': None, 'saturday': None, 'sunday': None}
	"""
	def __init__(self, monday=None, tuesday=None, wednesday=None, thursday=None, friday=None, saturday=None, sunday=None):
		self.orari = {
			'monday': monday,
			'tuesday': tuesday,
			'wednesday': wednesday,
			'thursday': thursday,
			'friday': friday,
			'saturday': saturday,
			'sunday': sunday,
		}
