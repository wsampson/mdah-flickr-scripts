mdah-flickr-scripts
============

flickr-batch-replace.py batch searches-and-replaces text in photos' titles and descriptions on Flickr. Photos are
selected by set ID. Edit flickr-batch-replace.py and replace the ALL_CAPS variables with relevant values for your account.

flickr-writer.py handles the embedded metadata in MDAH .tiff files to construct descriptive text for the new set of images on Flickr.
Be sure to check the output of the script before uncommenting the last two lines to commit your changes. 

Run from command line, suggested Python 2.7.x or later. Requires python-flickrapi and ElementTree.
