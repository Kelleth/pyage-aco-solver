#!/usr/bin/env python2.6
import os, commands
  
dir = os.path.dirname(os.path.realpath(__file__))

#inputs[0] : ants
#inputs[1] : iterations
#inputs[2] : city
#inputs[3] : ptype (population type)
#inputs[4] : egocentric
#inputs[5] : altercentric
#inputs[6] : goodConflict
#inputs[7] : badConflict
#inputs[8] : name (population name)

inputs = []
with open('input.txt') as f:
	inputs = f.readline().split()

cmd_module = "module load libs/python-numpy"
cmd_cd_to_app = "cd %s/pyage-aco-solver/" % (dir)
cmd_run = "python -m aco_solver.runner.parallel_runner %s %s %s -p 5 -t %s -q 1 -o outputs/parametrized/ --egocentric %s --altercentric %s --goodConflict %s --badConflict %s --classic 0.0 --paremetrizedName %s" % tuple(inputs)

cmd_generate_stats = "python -m aco_solver.stats.avg_summary_generator %s %s %s outputs/parametrized/ %s" % (inputs[0], inputs[1], inputs[2], inputs[8])
output_file = "%s/pyage-aco-solver/outputs/parametrized/%s_%s_%s_%s_avg_summary.dat" % (dir, inputs[2], inputs[0], inputs[1], inputs[8])

status, output = commands.getstatusoutput(cmd_module + ' && ' + cmd_cd_to_app + ' && ' + cmd_run + '&&' + cmd_generate_stats)

if status == 0:
	result = []
	with open(output_file) as f:
		result = f.readlines()
		result_last_iter_fitness = result[-1].split(';')[1]
		with open('output.txt', 'wb+') as f2:
			f2.write(result_last_iter_fitness)
else:
	with open('output.txt', 'wb+') as f2:
		f2.write(output)