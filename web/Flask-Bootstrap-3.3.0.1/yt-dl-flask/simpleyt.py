import re
import subprocess
import os

class SimpleYoutube(object):

	def __init__(self, objs):	
		# objects are tuples: ('file_name', 'video_url')
		self._url_objs = objs		
		self._default_folder = 'D:\Willi Hitz\Torben Youtube DL'
		self._url_regex = re.compile(
		r'^(?:http|ftp)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
		r'localhost|' #localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)


	def dl_videos(self):
		# prepend the base/default path to the specified file name(s)
		"""
		self._url_objs = [('\\'.join([self._default_folder, obj[0]]), obj[1]) for obj in self._url_objs]
		self._url_objs = filter(lambda obj: self.__dl_video(obj), self._url_objs)
		"""
		# prepend the base/default path to the specified file name(s) without the (current) file extension (FLV and mp3)
		self._url_objs = [('\\'.join([self._default_folder, obj[0]]), obj[1]) for obj in self._url_objs]
		# reduce the iterables to those who have a valid url
		self._url_objs = filter(lambda obj: self.__is_valid_url(obj[1]), self._url_objs)
		self.__dl_videos()

		# convert the 'valid' FLV files to mp3
		self.__convert_videos()

		# delete the unused FLV files
		self.__del_unused_files()


	def __dl_videos(self):
		for obj in self._url_objs[:]:
			p = subprocess.Popen(['youtube-dl', '-o', obj[0] + '.flv', obj[1]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			ret = p.wait()
			if ret != 0:
				self._url_objs.remove(obj)


	def __convert_videos(self):
		for obj in self._url_objs:
			print obj
			try:
				os.stat(obj[0] + '.mp3')
			except WindowsError:
				p = subprocess.Popen(['ffmpeg', '-i', obj[0] + '.flv', '-f', 'mp3', obj[0] + '.mp3'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				# TODO: needs error handling (or status indication) for client classes
				ret = p.wait()


	def __del_unused_files(self):
		for obj in self._url_objs:
			if os.stat(obj[0] + '.flv') is not None:
				os.remove(obj[0] + '.flv')


	def __is_valid_url(self, url):
		return self._url_regex.match(url) is not None

	@property
	def url_objs(self):
	    return self._url_objs

	@url_objs.setter
	def url_objs(self, value):
   		self._urls = value	

	@url_objs.deleter
	def url_objs(self):
		del self._url_objs


if __name__ == '__main__':
	test_objs = [('Wutanfall', 'https://www.youtube.com/watch?v=aTkmIukBZQc'), ('Flasche Bier', 'https://www.youtube.com/watch?v=0H4WGCL--TA'), ('Foobar', 'Baz_Url')]
	yt = SimpleYoutube(test_objs)
	yt.dl_videos()