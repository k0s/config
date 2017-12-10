#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
mount inserted usb disk

[   33.854905] usb-storage 1-1.2:1.0: USB Mass Storage device detected
[   33.854946] scsi6 : usb-storage 1-1.2:1.0
[   33.855002] usbcore: registered new interface driver usb-storage
[   34.855894] scsi 6:0:0:0: Direct-Access     PNY      USB 2.0 FD       8.07 PQ: 0 ANSI: 4
[   34.856108] sd 6:0:0:0: Attached scsi generic sg2 type 0
[   34.857281] sd 6:0:0:0: [sdb] 249999360 512-byte logical blocks: (127 GB/119 GiB)
[   34.858452] sd 6:0:0:0: [sdb] Write Protect is off
[   34.858455] sd 6:0:0:0: [sdb] Mode Sense: 23 00 00 00
[   34.859678] sd 6:0:0:0: [sdb] Write cache: disabled, read cache: enabled, doesn't support DPO or FUA
[   40.782414]  sdb: sdb1
[   40.787010] sd 6:0:0:0: [sdb] Attached SCSI removable disk

"""

import argparse
import os
import subprocess
import sys


def main(args=sys.argv[1:]):

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-m', '--mount', dest='mount_point',
                        default='/mnt/media',
                        help="mount point")
    options = parser.parse_args(args)

    dmesg = subprocess.check_output(['dmesg']).splitlines()
    for string in  ('usbcore: registered new interface driver usb-storage',
                    'USB Mass Storage device detecte'):
        for index in reversed(range(len(dmesg))):
            line = dmesg[index]
            if string in line:
                break
        else:
            continue
        break
    else:
        sys.exit(1)

    for line in dmesg[index:]:
        line = line.split(']', 1)[-1].strip()
        if ':' in line:
            try:
                disk, partition = line.split(':')
            except ValueError:
                continue
            disk = disk.strip()
            partition = partition.strip()
            if partition.startswith(disk):
                print ("partition: {}".format(partition))
                break
    else:
        parser.error("No partition found")

    device = os.path.join('/dev', partition)
    assert os.path.exists(device)
    print ("Device: {}".format(device))

    command = ['sudo', 'mount', device, options.mount_point]
    print (' '.join(command))

if __name__ == '__main__':
    main()
