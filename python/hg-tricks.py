# check status
/       # check for outstanding changes
        output = self._call(['st']).strip()
        lines = [line for line in output.splitlines()
                 if not line.startswith('?')]
        if lines:
            print "Outstanding changes:"
            print output
            raise AssertionError
