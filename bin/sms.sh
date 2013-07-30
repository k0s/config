#!/bin/bash
# Send text through adb by Madura A.
# http://0xdeafc0de.wordpress.com/2012/01/28/send-sms-using-android-adb/
# https://market.android.com/details?id=org.jraf.android.nolock
# Please use the above app(or similar) to keep it from locking while
# using this script

adb shell /system/bin/sh /system/bin/am start -a android.intent.action.SENDTO -d sms:$1 –es sms_body "$2" –ez exit_on_sent true
sleep 1
adb shell /system/bin/sh /system/bin/input keyevent 22
sleep 1
adb shell /system/bin/sh /system/bin/input keyevent 66