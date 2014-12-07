import re
import subprocess
import os
import pyperclip
import youtube_dl
import ConfigParser

def main():
	# populating important attributes from the properties file ('props.ini')
	"""
		default_folder = read_config()
		if default_folder == '' or default_folder is None:
			default_folder = 'D:\Willi Hitz\Torben Youtube DL'	

		print default_folder
		print 'D:\Willi Hitz\Torben Youtube DL'
	"""
	
	default_folder = 'D:\Willi Hitz\Torben Youtube DL'	


	""" 
	Generel regexp for URLs
	url_regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	"""

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

			while url_regex_yt.match(video_url) is None:
				raw_input('Keine gueltige (Youtube-)URL im Clipboard. Bitte eine URL kopieren und anschliessend hier mit "ENTER" bestaetigen:  ')
				video_url = pyperclip.paste()

			title = extract_title(video_url)
			# le non-crossplatform faec
			os.system('cls')
			user_confirm = raw_input(title.encode('ascii', 'ignore') + ' -- Herunterladen (j/n)?  ')

		#file_name = raw_input('Dateinamen eingeben (keine Umlaute): ')
		file_name = title.encode('ascii', 'ignore')

		file_exists = True
		try:
			file_exists = os.stat('\\'.join([default_folder, file_name]) + '.mp3') is not None
		except WindowsError:
			file_exists = False

		# only download and convert the video if the file doesn't already exist
		# (needed because ffmpeg will hang forever if the file already exists)
		if not file_exists:
			# sanity checks and possible replacements
			file_name = file_name.replace('"', '')
			file_name = file_name.replace('/', ' ')

			file
			file_names = ['\\'.join([default_folder, file_name]) + '.flv', '\\'.join([default_folder, file_name]) + '.mp3']

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


def read_config():
	cfg_parser = ConfigParser.ConfigParser()
	try:
		cfg_parser.read('props.ini')
	except e:
		return None
	return cfg_parser.get('GeneralSettings', 'OutputFolder')


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
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(video_url, process=False)
		return info['title']
def del_files(file_names):
	for file_name in file_names:
		try:
			os.remove(file_name)
		except:
			pass


def def_error_msg(file_names):
	del_files(file_names)
	raw_input('Fehler waehrend des Downloads. Programm wird beendet..')
	exit(1)


if __name__ == '__main__':
	main()
