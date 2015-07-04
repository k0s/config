#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
slice a clip with `ffmpeg`:

ffmpeg -ss <00:00:00> -t <sec> -i <input_file> -q 1  <output_file> #

--ss = start time ;

-t = length of video to create from the start time in seconds.
"""

# imports
import argparse
import os
import subprocess
import sys

# module globals
__all__ = ['main', 'Parser']
here = os.path.dirname(os.path.realpath(__file__))
string = (str, unicode)


def ensure_dir(directory):
    """ensure a directory exists"""
    if os.path.exists(directory):
        assert os.path.isdir(directory)
        return directory
    os.makedirs(directory)
    return directory


def convert_seconds_to_hhmmss(time_sec):
    """converts `time_sec` to (hh,mm,ss)"""

    hh = int(time_sec / 3600)
    mm = int((time_sec % 3600) / 60)
    ss = int((time_sec % 3600) % 60)
    return (hh,mm,ss)


def format_seconds_to_hhmmss(time_sec, separator=':'):
    """converts `time_sec` to string 'hh:mm:ss'"""
    return separator.join(['{:0>2d}'.format(i)
                           for i in convert_seconds_to_hhmmss(time_sec)])


def duration(clip, ffprobe='ffprobe'):
    """get the duration in seconds using `ffprobe` from ffmpeg"""

    command = [ffprobe, clip]
    assert os.path.exists(clip), "Missing clip, duration not available"

    # probe the file
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        # (for some reason, ffprobe sends output to stderr)
    except subprocess.CalledProcessError as e:
        print (e.output)
        raise

    duration = None
    for line in output.splitlines():
        # Parse the output of `ffprobe`
        # look for a line like:
        #   Duration: 00:00:59.73, start: 0.000000, bitrate: 7783 kb/s

        line = line.strip()
        if line.startswith("Duration:"):
            if duration:
                raise AssertionError("Duplicate duration - already found: {}".format(duration))
            line = line.split(',')[0]
            duration = line.split(':', 1)[1].strip()

    if duration:
        hh, mm, ss = [float(i) for i in duration.split(':')]
        duration = 3600*hh + 60*mm + ss

        return duration


class FFSliceParser(argparse.ArgumentParser):
    """fflice CLI option parser"""

    default_slice_time = 300.

    def __init__(self):
        argparse.ArgumentParser.__init__(self, description=__doc__)
        self.add_argument('clips', metavar='clip', nargs='+', help="clips to slice")
        self.add_argument('-d', '--directory', dest='directory',
                          default=os.getcwd(),
                          help="output directory [DEFAULT: %(default)s]")
        self.add_argument('--durations', '--print-durations', dest='print_durations',
                          action='store_true', default=False,
                          help="print durations and exit")
        self.add_argument('-n', dest='number', type=int,
                          help="number of slices")
        self.add_argument('-t', '--time', dest='slice_time',
                          type=float,
                          help="time of each slice [DEFAULT: {}]".format(self.default_slice_time))
        self.add_argument('--dry-run', dest='dry_run',
                          action='store_true', default=False,
                          help="print out what will be done")
        self.add_argument('--hhmmss', dest='hhmmss',
                          action='store_true', default=False,
                          help="display times in 'hh:mm:ss' format; thedefault is in seconds")

        self.add_argument('-v', '--verbose', dest='verbose',
                          action='store_true', default=False,
                          help="be verbose")
        self.options = None

    def parse_args(self, *args, **kw):
        options = argparse.ArgumentParser.parse_args(self, *args, **kw)
        self.validate(options)
        self.options = options
        return options

    def validate(self, options):
        """validate options"""

        missing = [clip for clip in options.clips
                   if not os.path.exists(clip)]
        if missing:
            self.error("Not found: {}".format(', '.join(missing)))

        if options.slice_time and options.number:
            self.error("Cannot specify slice time and number of slices")
            # TODO: allow specification of both
        elif options.slice_time is None and options.number is None:
            options.slice_time = self.default_slice_time

        ensure_dir(options.directory)

    def format_seconds(self, seconds):
        """format seconds to string"""
        if self.options.hhmmss:
            return format_seconds_to_hhmmss(seconds)
        return '{:.2}'.format(seconds)

    def slice(self):
      """
      iterates over all the specified clips and slices them as per input params.
      The sliced clips are stored under the provided coommand line destinati
      on directory or current working dir
      """

      for clip_path in self.options.clip_paths:
        print "***** Processing {0}".format(clip_path)

        if not os.path.exists(clip_path):
          print "File not found! skipping {0}".format(clip_path)
          continue

        #making sure the slice time is within bounds of the clip duration
        duration = self.duration(clip_path)
        print "Duration: {0}".format(duration)
        if self.options.slice_length_sec > duration:
          print "Skipping {0}, slice_time {1} is GREATER than file duration {2} ".format(clip_path,self.options.slice_length_sec ,duration)
          continue

        #calculating  the number slices to create
        num_slices = 0
        if self.options.num_slices:
          num_slices = min (self.options.num_slices, int(duration/(self.options.slice_length_sec)))
        else: #number of slice were not specified
          num_slices = int(duration/(self.options.slice_length_sec))
        print "Slicing in {0} parts, {1} seconds each".format(num_slices,self.options.slice_length_sec)

        hh = 0
        mm = 0
        ss = 0
        start_time_secs = 0
        [out_filename,out_file_ext] = clip_path.split("/")[-1].split(".") #assuming the file path to be something like /df/dsf/dsf/dsf.mp4
        ensure_dir(self.options.out_directory)
        #creating slices
        for i in range(num_slices):
          [hh,mm,ss] = self.format_seconds_to_hhmmss(start_time_secs)
          out_file_path = "{0}/{1}_{2}.{3}".format(self.options.out_directory,out_filename,i,out_file_ext)
          command = "ffmpeg  -ss {0}:{1}:{2} -t {3} -i {4} -q {5} -strict -2 {6}".format(hh,mm,ss,self.options.slice_length_sec,
                    clip_path,1, out_file_path)

          try:
            output = subprocess.call(command, shell=True)
          except subprocess.CalledProcessError as e:
            print (e.output)
            raise
          start_time_secs += self.options.slice_length_sec


def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line options
    parser = FFSliceParser()
    options = parser.parse_args(args)

    # compute durations
    durations = {clip: duration(clip) for clip in options.clips}
    if options.print_durations:
        returncode = 0
        total = 0.
        for clip in options.clips:
            _duration = durations[clip]
            if _duration is None:
                print ("Duration not found: '{}'".format(clip))
                returncode = 1
            else:
                print ('{} : {}'.format(clip,
                                        parser.format_seconds(_duration)))
        sys.exit(returncode)

    parser.slice()

if __name__ == '__main__':
    main()

