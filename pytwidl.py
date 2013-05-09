#!/usr/bin/env python

"""
Copyright Yoan Agostini <yoanDOTagostiniATgmailDOTcom>

PyTwiDL is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyTwiDL is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyTwiDL.  If not, see <http://www.gnu.org/licenses/>.

*******************************************************************************
Little and dirty script to download Twitch.tv videos.

More informations here:
http://support.twitch.tv/discussion/1839/how-to-download-a-video-from-twitch-tv
*******************************************************************************
"""

import urllib2
import argparse
from xml.dom.minidom import parse
import os

def main():

	#Arg parsing
	parser = argparse.ArgumentParser(description='Download Twitch.tv videos.')
	parser.add_argument('-c', '--clip-id', required=True, help='The ClipID of the video: http://twitch.tv/username/b/CLIPIDHERE')
	parser.add_argument('-o', '--output-file', default=os.getcwd() + os.sep + 'pytwidl.flv')
	args = parser.parse_args()

	#Getting the video's URI
	uri = 'http://api.justin.tv/api/clip/show/' + args.clip_id + '.xml'
	stream = urllib2.urlopen(uri)
	dom = parse(stream)
	name = dom.getElementsByTagName('video_file_url')
	video_uri = name[0].firstChild.nodeValue
	
	#Downloading the video with progress status
	with open(args.output_file, 'wb') as f:
		u = urllib2.urlopen(video_uri)
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		print "Downloading: %s Bytes: %s" % (args.output_file, file_size)
		
		file_size_dl = 0
		block_sz = 8192
		while True:
			buffer = u.read(block_sz)
			if not buffer:
				break

			file_size_dl += len(buffer)
			f.write(buffer)
			status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
			status = status + chr(8)*(len(status)+1)
			print status,

if __name__ == '__main__':
	main()