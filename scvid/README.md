# scvid package repositoory

## About

This application is capable of creating videos from screen shots taken automatically in given period of time. Also, it can add custom audio to the produced video files.

## Installation

To install this package you should clone this repository with git clone https://github.com/dubovyk/scvid and then run ./install.sh as a root.

## Usage

To create a video you should run the program as following:

scvid -d DURATION -t RECORD_TIME [-r  RATE or -i INTERVAL] [-a AUDIO FILE] OUTPUT_FILE

where DURATION is lenghth of the output video given in format hh:mm:ss, RECORD_TIME is a time which during which screenshots will be taken in format hh:mm:ss, RATE is amount of frames per second in output video, INTERVAL - time between screenshots in format hh:mm:ss. AUDIO_FILE - name of the file for audio track in the video (shoudl be in .mp3 format), OUTPUT_FILE - name of the output file (should be .mp4 format).

## Author

Application was created by Serhii Dubovyk in 2016. If you have any questions about using it or want to contact me for some other purpose, feel free to write to my e-mail: sergeydubovick@gmail.com

## License

scvid is published under Apache 2.0 License.