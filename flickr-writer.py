# http://stuvel.eu/media/flickrapi-docs/documentation/
# http://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree/
# http://www.doughellmann.com/PyMOTW/xml/etree/ElementTree/parse.html

## Write complete title and descriptions to photos by set.

import flickrapi
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

api_key = 'API_KEY'
api_secret = 'API_SECRET'

collection_title = 'COLLECTION_NAME'
collection_call  = 'CALL_NUMBER'

# make flickr object
flickr = flickrapi.FlickrAPI(api_key, api_secret)						 

# authorize user
(token, frob) = flickr.get_token_part_one(perms='write')															
if not token: raw_input('Press ENTER after you authorized this program')
flickr.get_token_part_two((token, frob))

# grab a photoset by id
photoset = flickr.photosets_getPhotos(api_key='API_KEY', photoset_id='SET_ID')

# load XML response into elementtree object
set_tree = ET.ElementTree(photoset)																										

# make photo_ids list		
photo_ids = []																																			

# grab all photo ids in set		
for node in set_tree.iter('photo'):																								
	photo_ids.append(node.get('id'))

# iterate over id list	
for single_id in photo_ids:																												

 # get each photo
	photo = flickr.photos_getInfo(photo_id=single_id, api_key='API_KEY')				

 # load into elementtree object		
	photo_tree = ET.ElementTree(photo) 																							
	
	# get description texts. May need adjustment depending on photo batch. Some photos will not have embedded metadata in the tiffs, or may have that metadata in a different layout.				
	for node in photo_tree.iter('description'):
		
		# find the descriptive text
		sysid_start   = node.text.find('Sysid')
		description   = node.text[5:sysid_start]
		description   = description.strip()

		# find the 'Scanned...' text		
		scanned_start = node.text.find('Scanned')
		scanned_end   = node.text.find('MDAH.')	
		scan_text     = node.text[scanned_start:scanned_end + 5]	
	
		print scan_text
		
 # get the item's system id					
	for node in photo_tree.iter('title'):						
		sysid_end = node.text.find('-')
		sysid = node.text[0:sysid_end]
					
		new_description = '<b>Collection: </b>'  + collection_title + '\n' + '<b>Call number: </b>' + collection_call  + '\n' + '<b>System ID: </b>' + sysid + '.' + '\n' + '<a href="http://zed.mdah.state.ms.us/cgi-bin/koha/opac-detail.pl?biblionumber=' + sysid + '" rel="nofollow">Link to the catalog</a>\n\n' + description + '\n\n' + 'Please see our <a href="http://www.flickr.com/people/mississippi-dept-of-archives-and-history/">profile page</a> for information on ordering.' + '\n\n' + scan_text + '\n\n' + 'Credit:  Courtesy of the Mississippi Department of Archives and History'
	
		
		### CLOSELY view the output of following line to make sure the two previous for loops have correctly grabbed and applied the title, sysid, etc.		
			
		print '\n\n'		
		print description + ' :' + new_description
		print 'mdah:sysid=' + sysid
		print '\n\n'
		
		### Uncomment *ONLY* when ready to commit changes
				
		# flickr.photos_setMeta(api_key='API_KEY', photo_id=single_id, title=description, description=new_description)
		# flickr.photos_setTags(api_key='API_KEY', photo_id=single_id, tags='mdah:sysid=' + sysid)