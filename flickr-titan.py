# http://stuvel.eu/media/flickrapi-docs/documentation/
# http://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree/
# http://www.doughellmann.com/PyMOTW/xml/etree/ElementTree/parse.html

import flickrapi
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


## Run batch search-and-replace on photo titles and descriptions, by set number

api_key = 'API_KEY'
api_secret = 'API_SECRET'

flickr = flickrapi.FlickrAPI(api_key, api_secret)											# make flickr object 

(token, frob) = flickr.get_token_part_one(perms='write')									# authorize user
if not token: raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))

photoset = flickr.photosets_getPhotos(api_key='API_KEY', photoset_id='PHOTOSET_ID')	# grab a photoset by id

set_tree = ET.ElementTree(photoset)																# load XML response into elementtree object

photo_ids = []																							# make photo_ids list

for node in set_tree.iter('photo'):																# grab all photo ids in set
	photo_ids.append(node.get('id'))

for single_id in photo_ids:																		# iterate over id list
	
	p = flickr.photos_getInfo(photo_id=single_id, api_key='TWEAK_ME')		# get each photo
	
	p_tree = ET.ElementTree(p) 																	# load into elementtree object

	print single_id																					# for user feedback
	
	for node in p_tree.iter('title'):															# get title
		title = node.text
	
	for node in p_tree.iter('description'):													# get description
		description = node.text	
	
	set_title       = title	
	set_description = description.replace('TARGET_STRING', 'NEW_STRING')				# insert target and replacement values
																											# could modify title and other values as well
	
	flickr.photos_setMeta(api_key='API_KEY', photo_id=single_id, title=set_title, description=set_description)