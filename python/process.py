import os
import shlex
import subprocess
import sys

def ps():
    retval = []
    process = subprocess.Popen(['ps', 'axwww'], stdout=subprocess.PIPE)
    stdout, _ = process.communicate()
    header = None
    for line in stdout.splitlines():
        line = line.strip()
        if header is None:
            # first line is the header
            header = line.split()
            continue
        split = line.split(None, len(header)-1)
        process_dict = dict(zip(header, split))
        retval.append(process_dict)
    return retval

def running_processes(name):
    """
    returns a list of 
    {'PID': PID of process (int)
     'command': command line of process (list)}
     with the executable named `name`
    """
    retval = []
    for process in ps():
        command = process['COMMAND']
        command = shlex.split(command)
        prog = command[0]
        basename = os.path.basename(prog)
        if basename == name:
            retval.append((int(process['PID']), command))
    return retval

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        processes = running_processes(arg)
        for pid, command in processes:
            print '%s %s : %s' % (pid, arg, command)
