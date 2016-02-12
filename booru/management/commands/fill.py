# Standalone script which should populate database with pictures in DIR directory.
# Subdirectories are counted as pools (unimplemented yet).
# Tags and other is taken from Danbooru using IQDB.
# TODO: other sources.
# Uploaded_by is first created superuser (normally we should have one of them, so this is not a problem).
# Usage: python manage.py fill 'path/to/picture/folder'

import os
import urllib2

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from booru.models import Picture


class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('dir', nargs='+', type=str)

	def handle(self, *args, **options):
		DIR = options['dir'][0]
		MIN_SIMILARITY = 80
		os.chdir(DIR)
		count = 0
		for f in os.listdir('./'):
			while True:
				try:
					image_file = open(f, 'rb')
					r = requests.post("http://iqdb.org/", files={'file': image_file}, data={"submit": True})
					image_file.close()
					soup = BeautifulSoup(r.text, 'html.parser')

					lst = soup.find_all('td', attrs={'class': 'image'})

					# Searching for suitable picture
					url = ''
					for i in lst:
						# Searching picture with maximum similarity. If similarity lesser than MIN_SIMILARITY, skip.
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
						if i is not None and i.a is not None and i.a['href'] is not None and i.a['href'].find(
								"danboo") >= 0:
							url = i.a['href']
							break
					if url == '':
						print "Picture wasn't found"
						image_file = open(f, 'rb')
						pic = Picture.objects.create_picture(
								src='',
								rating='s',
								score=0,
								tag_string='not_founded',
								image_data=image_file.read(),
								file_extension=f.split('.')[-1]
						)
						image_file.close()
						break
					else:
						count += 1
						print count
					if url.startswith(r'//'):
						url = 'http:' + url
					elif not url.startswith('http'):
						url = 'http://' + url
					xml_url = url + '.xml'
					print url

					soup = BeautifulSoup(requests.get(xml_url).text, 'xml')
					post = soup.post
					tag_string = post.find('tag-string').text
					large_file_url = post.find('large-file-url').text
					picture_url = "http://danbooru.donmai.us" + large_file_url
					# Adding new database entry.
					pic = Picture.objects.create_picture(
							src=url,
							rating=post.rating.text,
							score=post.score.text,
							tag_string=tag_string,
							image_data=urllib2.urlopen(picture_url).read(),
							file_extension=picture_url.split('.')[-1]
					)
					break
				except requests.exceptions.ConnectionError:
					print "Connection error... retry..."

		print "All pictures processed"
