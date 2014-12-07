import re
import subprocess
import os
import pyperclip

def main():
	default_folder = 'D:\Willi Hitz\Torben Youtube DL'
	url_regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

	video_url = pyperclip.paste()

	while url_regex.match(video_url) is None:
		raw_input('Keine gueltige URL im Clipboard. Bitte eine URL kopieren und anschliessend hier mit "ENTER" bestaetigen.')
		video_url = pyperclip.paste()

	file_name = raw_input('Dateinamen eingeben (keine Umlaute): ')
	file_names = ['\\'.join([default_folder, file_name]) + '.flv', '\\'.join([default_folder, file_name]) + '.mp3']

	ret_val = dl_video(video_url, file_names[0])
	if ret_val != 0:
		def_error_msg(file_names)

	ret_val = convert_to_mp3(file_names[0], file_names[1])
	if ret_val != 0:
		def_error_msg(file_names)

	del_files([file_names[0]])

	# le non-crossplatform faec
	os.system('cls')
	raw_input('Die Datei %s befindet sich nun im Ordner %s.' % (file_names[1], default_folder))
	

def dl_video(video_url, file_name):
	print '=' * 30
	p = subprocess.Popen(['youtube-dl', '-o', file_name, video_url], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	for line in p.stdout.readlines():
		print line
	print '=' * 30
	return p.wait()


def convert_to_mp3(input_file, output_file):
	p = subprocess.Popen(['ffmpeg', '-i', input_file, '-f', 'mp3', output_file], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return p.wait()


def del_files(file_names):
	for file_name in file_names:
		if os.stat(file_name) is not None:
			os.remove(file_name)


def def_error_msg():
	del_files(file_names)
	raw_input('Fehler waehrend des Downloads. Programm wird beendet..')
	exit(1)


if __name__ == '__main__':
	main()
