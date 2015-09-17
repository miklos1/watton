import glob
import re
import collections
import numpy as np


def read_file(nodes, s_id):
    oname = 'measure_%04d.o%d' % (nodes, s_id)
    ename = 'measure_%04d.e%d' % (nodes, s_id)

    names = []
    times = []
    nrounds_list = []
    with open(oname, 'r') as ofile, open(ename, 'r') as efile:
        for line in ofile:
            if line.startswith('name:'):
                # Select second word, chop off newline
                names.append(line.split(' ')[1][:-1])

            if "cell_closure" in line:
                # cell_closure seconds {name}: {mean} +- {stddev}
                words = line.split(' ')
                mean = float(words[3])
                stddev = float(words[5])
                times.append((mean, stddev))

        for line in efile:
            if "cell closure" in line:
                # [0] pyop2:INFO Communication rounds for cell closure: {nrounds}
                words = line.split(' ')
                nrounds = int(words[7])
                nrounds_list.append(nrounds)
    assert len(names) == len(times) == len(nrounds_list)

    result = {}
    for i in xrange(len(names)):
        result[names[i]] = {
            'mean': times[i][0],
            'stddev': times[i][1],
            'rounds': nrounds_list[i],
        }

    return result


results = collections.defaultdict(list)

prog = re.compile('measure_(\d+)\.o(\d+)')
for filename in glob.iglob('measure_*.o*'):
    match = prog.match(filename)
    nodes = int(match.group(1))
    s_id = int(match.group(2))
    results[nodes].append(read_file(nodes, s_id))

print '(standard deviation / mean value) for time values across MPI ranks: max.',
print max(result["stddev"] / result["mean"]
          for jobs in results.values()
          for job in jobs
          for result in job.values())

print 'Is the number of communication rounds different between experiments?'
for nodecount in sorted(results):
    jobs_per_nodecount = results[nodecount]

    nrounds = collections.defaultdict(set)
    for job in jobs_per_nodecount:
        for name, result in job.iteritems():
            nrounds[name].add(result["rounds"])
    print "{0}: {1}".format(nodecount, all(len(v) <= 1 for v in nrounds.values()))

print '**** Number of communication rounds in tabular form'

comm_rounds = collections.defaultdict(dict)
for nodecount, jobs_per_nodecount in results.iteritems():
    for job in jobs_per_nodecount:
        for name, result in job.iteritems():
            comm_rounds[name][nodecount] = result["rounds"]
for name, dictionary in comm_rounds.iteritems():
    print '**', name
    table = np.array(sorted(dictionary.iteritems()))
    table[:, 0] *= 24  # switch from nodes to cores
    m, b = np.polyfit(np.log(table[:, 0]), np.log(table[:, 1]), 1)

    for entry in table:
        print "%d,%d" % tuple(entry)
    print 'log-log linear fitting slope:', m


print '**** Execution times in tabular form'

name_times = collections.defaultdict(dict)
for nodecount in sorted(results):
    jobs_per_nodecount = results[nodecount]

    ntimes = collections.defaultdict(list)
    for job in jobs_per_nodecount:
        for name, result in job.iteritems():
            ntimes[name].append(result["mean"])
    for name, times in ntimes.iteritems():
        name_times[name][nodecount] = np.average(times)
for name, dictionary in name_times.iteritems():
    print '**', name
    table = np.array(sorted(dictionary.iteritems()))
    table[:, 0] *= 24  # switch from nodes to cores

    for entry in table:
        print "%d,%g" % tuple(entry)
