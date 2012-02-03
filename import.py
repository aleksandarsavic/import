# import os for file system functions
import os
# import json
import json
# shutil for file renaming
import shutil
# import flickrapi
# `easy_install flickrapi` or `pip install flickrapi`
from openphoto import OpenPhoto

from os.path import join, getsize


# main program
def main():

  print "Enter your OpenPhoto host: ",
  host = raw_input()
  print "Enter your consumer key: ",
  consumerKey = raw_input()
  print "Enter your consumer secret: ",
  consumerSecret = raw_input()
  print "Enter your token: ",
  token = raw_input()
  print "Enter your token secret: ",
  tokenSecret = raw_input()

  client = OpenPhoto(host, consumerKey, consumerSecret, token, tokenSecret)

  for root, dirs, files in os.walk('fetched/'):
    total = len(files)
    current = 1
    processed = 0
    errored = 0
    print "Found a total of %d files to process" % total
    for i in files:
      print "Processing %d of %d %s ..." % (current, total, i),
      current = current + 1
      infile = "fetched/%s" % i
      f = open(infile, 'r')
      json_str = f.read()
      f.close()
      params = json.loads(json_str)
      resp = client.post('/photo/upload.json', params)
      result = json.loads(resp)
      if result['code'] == 201:
        print "OK"
        processed = processed + 1
        shutil.move(infile, "processed/%s" % i)
      else:
        print "FAILED"
        errored = errored + 1
        shutil.move(infile, "errored/%s" % i)

    if total > 0:
      print "Results. Processed: %d. Errored: %d." % (processed, errored)
  
# create a directory only if it doesn't already exist
def createDirectorySafe( name ):
  if not os.path.exists(name):
    os.makedirs(name)

# check if a processed and errored directories exist else create them
createDirectorySafe('processed')
createDirectorySafe('errored')
main()