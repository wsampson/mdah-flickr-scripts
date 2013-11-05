# -*- coding: utf-8 -*-

import argparse
import flickrapi
try:
    import xml.etree.cElementTree as ET
    print("running cElementTree as ET")
except ImportError:
    import xml.etree.ElementTree as ET
import csv
try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")
          

parser = argparse.ArgumentParser(description='export metadata for Flickr user by set (or all photos if no set specified)')

parser.add_argument('-u','--user', help='target Flickr user ID')
parser.add_argument('-p','--photoset', default='all', help='target photoset ID (default is all photosets for specified user)')
args = parser.parse_args()

api_key = 'API_KEY'
api_secret = 'API_SECRET'

flickr = flickrapi.FlickrAPI(api_key, api_secret)						 

# authorize user
(token, frob) = flickr.get_token_part_one(perms='write')															
if not token: 
   raw_input('Press ENTER after you authorized this program')
flickr.get_token_part_two((token, frob))

photosets_dict = dict()																																			

f = open('flickr-data.csv', 'w')
writer = csv.writer(f)

def get_photoset_metadata(photoset):
	 
    photoset_info_tree = ET.ElementTree(flickr.photosets_getInfo(api_key=api_key, photoset_id=photoset))	    
    photoset_tree = ET.ElementTree(flickr.photosets_getPhotos(api_key=api_key, photoset_id=photoset))	

    ET.dump(photoset_info_tree)
    ET.dump(photoset_tree)

    photo_ids = []	
    data = []
    data_row = []
    
    for title in photoset_info_tree.iter('title'):
      set_title = unicode(title.text, "utf-8")  
       
    # grab all photo ids in set
    for node in photoset_tree.iter('photo'):
      
      # get each photo
      photo = flickr.photos_getInfo(photo_id=node.get('id'), api_key=api_key)
      photo_tree = ET.ElementTree(photo)

      ET.dump(photo_tree)

      data_row.append(set_title.encode('utf8'))
   	 
      for title in photo_tree.iter('title'):
         data_row.append(title.text.encode('utf8'))
	   
      try:
         geodata = flickr.photos_geo_getLocation(photo_id=node.get('id'), api_key=api_key)
         geodata_tree = ET.ElementTree(geodata)
      	
         for geonode in geodata_tree.iter('location'):            
            data_row.append(geonode.get('latitude').encode('utf8'))
            data_row.append(geonode.get('longitude').encode('utf8'))
            data_row.append(geonode.get('accuracy').encode('utf8'))
         for geonode in geodata_tree.iter('country'):
            data_row.append(geonode.text.encode('utf8'))         
         for geonode in geodata_tree.iter('region'):
            data_row.append(geonode.text.encode('utf8'))
         for geonode in geodata_tree.iter('county'):
            data_row.append(geonode.text.encode('utf8'))
         for geonode in geodata_tree.iter('locality'):
            data_row.append(geonode.text.encode('utf8'))
         for geonode in geodata_tree.iter('neighbourhood'):
            data_row.append(geonode.text.encode('utf8'))
      except Exception as e:
         e = True
        
      writer.writerow(data_row)
      print data_row     
    
      data_row = []
     
if args.photoset == 'all':
   photosets_tree = ET.ElementTree(flickr.photosets_getList(api_key=api_key, user_id=args.user))	

   # grab all photosets		
   for node in photosets_tree.iter('photoset'):
      photosets_dict[node.get('id')] = node[0].text

   # iterate over photosets dictionary
   for key in photosets_dict.iterkeys():
      print '-- Exporting metadata from ' + key + '--'
      get_photoset_metadata(key)

else:
   get_photoset_metadata(args.photoset)
