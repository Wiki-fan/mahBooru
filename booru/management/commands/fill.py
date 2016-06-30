# Standalone script which should populate database with pictures in DIR directory.
# Subdirectories are counted as pools (unimplemented yet).
# Tags and other is taken from Danbooru using IQDB.
# TODO: other sources.
# Uploaded_by is first created superuser (normally we should have one of them, so this is not a problem).
# Usage: python manage.py fill 'path/to/picture/folder'

import os
import urllib.request, urllib.error, urllib.parse

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from booru.models import Picture

def save_as_not_founded(image_file_name):
	image_file = open(image_file_name, 'rb')
	pic = Picture.objects.create_picture(
		src='',
		rating='s',
		score=0,
		tag_string='not_founded',
		image_data=image_file.read(),
		file_extension=image_file_name.split('.')[-1]
	)
	image_file.close()

def get_from_url(url, count,):
	if url == '':
		print("Picture wasn't found")
		save_as_not_founded(f)
		return
	else:
		count += 1
	if url.startswith(r'//'):
		url = 'http:' + url
	elif not url.startswith('http'):
		url = 'http://' + url

	if url.startswith("http://danbooru.donmai.us/"):
		xml_url = url + '.xml'
		print('Founded at "%s"'%xml_url)
		soup = BeautifulSoup(requests.get(xml_url).text, 'xml')
		post = soup.post
		if post.find('is-banned').text == 'true':
			print('Post was banned')
			return False
		tag_string = post.find('tag-string').text
		large_file_url = post.find('large-file-url').text
		picture_url = "http://danbooru.donmai.us" + large_file_url
		# Adding new database entry.
		pic = Picture.objects.create_picture(
			src=url,
			rating=post.rating.text,
			score=post.score.text,
			tag_string=tag_string,
			image_data=urllib.request.urlopen(picture_url).read(),
			file_extension=picture_url.split('.')[-1],
			artist=post.find('tag-string-artist').text,
			character=post.find('tag-string-character').text,
			copyright=post.find('tag-string-copyright').text
		)
		return True
	elif url.startswith("http://-yande.re/") or url.startswith("-http://konachan.com/"):
		xml_url = url.split('post')[0] + 'post.xml?id='+url.split('/')[-1]
		print(xml_url)
		soup = BeautifulSoup(requests.get(xml_url).text, 'xml')
		post = soup.post
		tag_string = post['tags']
		large_file_url = post['file-url']

		if url.startswith("http://yande.re/"):
			picture_url = "http://yande.re/" + large_file_url
		elif url.startswith("http://konachan.net/"):
			picture_url = "http://konachan.net/" + large_file_url

		# Adding new database entry.
		pic = Picture.objects.create_picture(
			src=url,
			rating=post['rating'],
			score=post['score'],
			tag_string=tag_string,
			image_data=urllib.request.urlopen(picture_url).read(),
			file_extension=picture_url.split('.')[-1]
		)
		return True
	else:
		return False

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('dir', nargs='+', type=str)

	def handle(self, *args, **options):
		#proxies={'socks':'socks://127.0.0.1:9050/'}

		DIR = options['dir'][0]
		MIN_SIMILARITY = 80
		os.chdir(DIR)
		count = 0
		for f in os.listdir('./'):
			print('Looking at file "%s"' % f)
			if f.lower().endswith('.gif'):
				print('Gif founded')
				save_as_not_founded(f)
			elif f.lower().endswith('.webm'):
				print('Webm founded. Skipping.')
			elif f.lower().endswith('.jpg') or f.lower().endswith('.jpeg') or f.lower().endswith('.png'):
				while True:
					try:
						image_file = open(f, 'rb')
						r = requests.post("http://iqdb.org/", files={'file': image_file}, data={"submit": True})#, proxies=proxies)
						image_file.close()
						soup = BeautifulSoup(r.text, 'html.parser')

						lst = soup.find_all('td', attrs={'class': 'image'})

						# Searching for suitable picture
						url = ''
						for i in lst:
							# Searching picture with maximum similarity. If similarity lesser than MIN_SIMILARITY, skip.
							if i is None or i.parent is None or i.parent.next_sibling is None or i.parent.next_sibling.next_sibling is None:
								continue
							similarity_string = i.parent.next_sibling.next_sibling.next_sibling
							similarity = -1
							if similarity_string is not None:
								similarity = int(similarity_string.text.split('%')[0])
							# Skipping pictures with no similarity (quick fix, actually).
							if similarity == -1:
								continue
							# Pictures are sorted by similarity, so it's not necessary to check further.
							if similarity <= MIN_SIMILARITY:
								break
							# If suitable picture is founded, break
							if i is not None and i.a is not None and i.a['href'] is not None:
								url = i.a['href']
								if get_from_url(url, count):
									break
						break

					except requests.exceptions.ConnectionError:
						print("Connection error... retry...")
				continue
			else:
				print('Unknown format')

		print("All pictures processed")
