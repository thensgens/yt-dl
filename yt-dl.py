import re
import subprocess
import os
import sys
import pyperclip
import youtube_dl
import ConfigParser
from config import ConfigProperties

CONST_DEFAULT_OUTPUT_DIR = os.path.expandvars('%HOMEDRIVE%\%HOMEPATH%\Youtube Downloader')

def main():

	#__test_bundled_ffmpeg()

	props = read_config()

	# Regexp for youtube domain only
	url_regex_yt = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
   	r'www.youtube.com'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

	outer_loop = 'initial'

	while outer_loop != 'e':
		user_confirm = 'n'
		while user_confirm == 'n':
			video_url = pyperclip.paste()
			while not is_string_or_buffer(video_url) or url_regex_yt.match(video_url) is None:
				raw_input('Keine gueltige (Youtube-)URL im Clipboard. Bitte eine gueltige Youtube-URL kopieren und anschliessend mit "ENTER" bestaetigen:  ')
				video_url = pyperclip.paste()

			title_result, success = extract_title(video_url)
			if not success:
				raw_input(title_result)
				continue

			# le non-crossplatform faec
			os.system('cls')
			file_name = remove_reserved_chars(title_result).encode('ascii', 'ignore')
			user_confirm = raw_input(file_name + ' -- Herunterladen (j/n)?  ')

		file_exists = True
		try:
			file_exists = os.stat('\\'.join([props.output_dir, file_name]) + '.mp3') is not None
		except WindowsError:
			file_exists = False

		# only download and convert the video if the file doesn't already exist
		# (needed because ffmpeg will hang forever if the file already exists)
		if not file_exists:
			file_names = ['\\'.join([props.output_dir, file_name]) + '.flv', '\\'.join([props.output_dir, file_name]) + '.mp3']

			ret_val = dl_video(video_url, file_names[0])
			if ret_val != 0:
				def_error_msg(file_names)

			convert_to_mp3(file_names[0], file_names[1])
			del_files([file_names[0]])

			# le non-cross platform faec
			os.system('cls')
		else:
			# le non-crossplatform faec
			os.system('cls')
			print 'Datei wurde bereits heruntergeladen.'
		outer_loop = raw_input('Neue URL kopieren und mit "ENTER" bestaetigen oder "e", um das Programm zu beenden:  ')


def __test_bundled_ffmpeg():
	import distutils.spawn
	ffmp = distutils.spawn.find_executable('ffmpeg')
	print type(ffmp)
	print ffmp
	#p = subprocess.Popen(['youtube-dl', '-o', file_name, video_url], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

"""
Checks whether or not the input is either a string/unicode or a buffer, thus a valid input for the caller.
"""
def is_string_or_buffer(input):
	return type(input) == str or type(input) == unicode or type(input) == buffer


"""
Remove reserved chars for file names on the windows platform
"""
def remove_reserved_chars(file_name):
	file_name = file_name.replace('"', '')
	file_name = file_name.replace('/', ' ')
	file_name = file_name.replace('~', ' ')
	file_name = file_name.replace('|', ' ')
	file_name = file_name.replace('<', ' ')
	file_name = file_name.replace('>', ' ')
	file_name = file_name.replace('*', ' ')
	file_name = file_name.replace('?', ' ')
	file_name = file_name.replace(':', ' ')
	file_name = file_name.replace('\\', ' ')
	return file_name


def read_config():
	props_cfg_path = os.path.expandvars('%HOMEDRIVE%\%HOMEPATH%\yt-dl_props.ini')
	cfg_parser = ConfigParser.ConfigParser()
	res = cfg_parser.read(props_cfg_path)
	if not res:
		write_default_config(cfg_parser, props_cfg_path)
	return populateProperties(cfg_parser)


def populateProperties(parser):
	props = ConfigProperties()
	props.output_dir = parser.get('GeneralSettings', 'OutputDir')
	return props


def write_default_config(parser, path):
	parser.add_section('GeneralSettings')
	parser.set('GeneralSettings', 'OutputDir', CONST_DEFAULT_OUTPUT_DIR)
	with open(path, 'w') as cfgfile:
		parser.write(cfgfile)


def dl_video(video_url, file_name):
	print '=' * 30
	p = subprocess.Popen(['youtube-dl', '-o', file_name, video_url], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	for line in p.stdout.readlines():
		print line
	print '=' * 30
	return p.wait()


def convert_to_mp3(input_file, output_file):
	p = subprocess.Popen(['ffmpeg', '-i', input_file, '-f', 'mp3', output_file], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p.communicate()


def extract_title(video_url):
	ydl_opts = {}
	result = None
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(video_url, process=False)
		try:
			result = info['title'], True
		except KeyError:
			result = 'Kein Youtube-Video ausgesucht. Bitte neue URL kopieren.', False
	return result


def del_files(file_names):
	for file_name in file_names:
		try:
			os.remove(file_name)
		except:
			pass


def def_error_msg(file_names):
	del_files(file_names)
	raw_input('Fehler waehrend des Downloads. Programm wird beendet..')
	sys.exit(1)


if __name__ == '__main__':
	main()