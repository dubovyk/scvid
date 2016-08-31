#!/usr/bin/python
"""
Copyright 2016 Serhii Dubovyk
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import datetime
import autopy
import argparse
import subprocess
import sys
import re

from time import sleep
from threading import Timer

__version__ = "0.2.0"


class ImageTakerTimer:
    def __init__(self, interval, function):
        self._timer = None
        self._interval = interval
        self._is_running = False
        self._function = function
        self._index = 1

    def _run(self):
        self._is_running = False
        self.start()
        self._function(self._index)
        self._index += 1

    def start(self):
        if not self._is_running:
            self._timer = Timer(self._interval, self._run)
            self._timer.start()
            self._is_running = True

    def stop(self):
        self._timer.cancel()
        self._is_running = False


class ScreenVideoMaker:
    def __init__(self, video_duration, record_time, interval, frame_rate, output_file, audio_file=None):
        self._video_duration = video_duration
        self._record_time = record_time
        self._interval = interval
        self._frame_rate = frame_rate
        self._output_file = output_file
        self._audio_file = audio_file
        self._id = 0

    def _getName(self, id):
        name = 'img/' + '00000'[:5 - len(str(id))] + str(id) + '.png'
        print name
        return name

    def _getImage(self, id):
        img = autopy.bitmap.capture_screen()
        img.save(self._getName(id))

    def capture(self):
        subprocess.call(['rm', '-rf', 'img'])
        subprocess.call(['mkdir', 'img'])
        image_taker = ImageTakerTimer(
            self._interval, self._getImage, )
        image_taker.start()
        sleep(self._record_time)
        image_taker.stop()

        print 'finished taking images'
        print 'starting creating video'
        command = ['ffmpeg', '-framerate', '{}'.format(self._frame_rate), '-r', '{}'.format(self._frame_rate),
                   '-i', 'img/%05d.png']

        if self._audio_file:
            subprocess_args = ("ffprobe", "-show_entries",
                               "format=duration", "-i", self._audio_file)
            popen = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE)
            popen.wait()
            output = popen.stdout.read()
            expr = '[0-9]+.[0-9]+'
            lenght = re.search(expr, output)
            lenght = lenght.group(0)
            repeat_audio = self._video_duration // float(lenght) + 1

            print lenght, repeat_audio
            com = ['sox', '-e', 'ima-adpcm', '{}'.format(self._audio_file),
                   'audio/{}'.format(self._audio_file), 'repeat', '{}'.format(repeat_audio)]
            subprocess.call(com)
            command += ['-i', 'audio/{}'.format(self._audio_file), '-shortest']
        command += ['-c:v', 'libx264', '-strict',
                    '-2', '{}'.format(self._output_file)]
        print ' '.join(command)
        subprocess.call(command)
        print 'finished creating video'


def getSec(s):
    L = s.split(':')
    if len(L) == 1:
        return float(L[0])
    elif len(L) == 2:
        datee = datetime.datetime.strptime(s, "%M:%S")
        return float(datee.minute * 60 + datee.second)
    elif len(L) == 3:
        datee = datetime.datetime.strptime(s, "%H:%M:%S")
        return float(datee.hour * 3600 + datee.minute * 60 + datee.second)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('output_name', metavar='output file',
                        type=str, help='This is a name for the video file')

    parser.add_argument('-d', '--duration', dest='duration', metavar='duration',
                        help='Specify duration of the video in format 00m00s')

    parser.add_argument('-t', '--time', dest='record_time', metavar='time to record',
                        help='Specify how long should the program take screenshots')

    parser.add_argument('-r', '--rate', dest='rate', metavar='rate', type=int,
                        help='Set amount of frames per second in output video')

    parser.add_argument('-i', dest='interval', metavar='interval',
                        type=int, help='Set the interval (in seconds) between screenshots.')

    parser.add_argument('-a', dest='audio', metavar='audio file',
                        help='Path to the target audio file')

    parser.add_argument('--img', action='store_true', dest='img_only',
                        help='Use this option if you want just to capture screenshorts with interval given in "-i" without creating video')

    parser.add_argument('-delay', dest='delay', metavar='delay before capture',
                        help='Set the amount of time between running this app and capturing first screenshot')
    args = parser.parse_args()

    try:
        if args.rate:
            args.rate = float(args.rate)
        if args.duration:
            args.duration = float(getSec(args.duration))
        if args.record_time:
            args.record_time = float(getSec(args.record_time))
        if args.interval:
            args.interval = float(getSec(args.interval))
        if args.delay:
            args.delay = float(getSec(args.delay))
    except Exception:
        print 'Wrong type of argument'
        sys.exit()

    if not args.record_time:
        print 'Please specify "-t" lenght of the record.'
        sys.exit()

    if not (args.duration or args.rate or args.interval):
        print 'Duration of the output video, interval between screenshots and video rate is not set.'
        print 'Please specify "-d" lenght of the output video file.'
        sys.exit()

    if not args.audio:
        print 'Using no audio file'

    if args.img_only:
        print 'No video will be created'

    if args.interval and args.rate:
        print 'Please specify only interval or rate, but not both'
        ans = raw_input(
            'Do you want to use given interval? If no, rate will be used[Y/n]')
        if ans in ['Y', 'Yes', 'y', 'yes', '', None]:
            args.rate = None
        else:
            args.interval = None

    if not (args.interval or args.rate):
        print 'Interval and rate not specified. Using default rate of 30 fps'
        args.rate = 30.0

    if not args.interval:
        args.interval = args.record_time / (args.duration * args.rate)

    print 'Output file name: {},\nVideo duration: {},\nRecord time: {},\nInterval: {},\nRate: {},\nDelay before start: {}'.format(args.output_name, args.duration, args.record_time, args.interval, args.rate, args.delay)

    confirm = raw_input('Start recording screenshots and making video?[Y/n]')
    if confirm not in ['Y', 'Yes', 'y', 'yes', '', None]:
        print 'Cancelled'
        sys.exit()

    if args.delay:
        sleep(args.delay)

    if args.audio:
        runner = ScreenVideoMaker(args.duration, args.record_time,
                                  args.interval, args.rate, args.output_name, args.audio)
    else:
        runner = ScreenVideoMaker(
            args.duration, args.record_time, args.interval, args.rate, args.output_name)
    runner.capture()
