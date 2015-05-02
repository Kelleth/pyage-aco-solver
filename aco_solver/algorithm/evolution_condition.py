from aco_solver.algorithm.ant import ClassicAnt, EgocentricAnt, AltercentricAnt, GoodConflictAnt, BadConflictAnt

class AntTypePosition(object):
	def __init__(self, smarter_ant_type, dumber_ant_type):
		self.smarter_ant_type = smarter_ant_type
		self.dumber_ant_type = dumber_ant_type

class EvolutionDict(dict):
	def __init__(self, *arg, **kwargs):
		super(EvolutionDict, self).__init__(*arg, **kwargs)
		self[BadConflictAnt] = AntTypePosition(EgocentricAnt, BadConflictAnt)
		self[EgocentricAnt] = AntTypePosition(AltercentricAnt, BadConflictAnt)
		self[AltercentricAnt] = AntTypePosition(ClassicAnt, EgocentricAnt)
		self[ClassicAnt] = AntTypePosition(GoodConflictAnt, AltercentricAnt)
		self[GoodConflictAnt] = AntTypePosition(GoodConflictAnt, ClassicAnt)
