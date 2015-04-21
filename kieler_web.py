import json
import re
import requests

UNI_KIEL = 'http://layout.rtsys.informatik.uni-kiel.de:9444/layout'

#-----------------------------------------------------------------------
# request_layout
#-----------------------------------------------------------------------
def request_layout( kieler_json_obj, kieler_server_url=UNI_KIEL ):

  # we need to convert nested json into string format
  r = requests.post( kieler_server_url, data = kieler_json_obj )
  assert r.ok
  print r.headers
  return r.text

#-----------------------------------------------------------------------
# fixup_svg
#-----------------------------------------------------------------------
def fixup_svg( svg_data ):
  return re.sub(' w="[0-9]+" ',' ', svg_data, count=1)

#-----------------------------------------------------------------------
# request_svg
#-----------------------------------------------------------------------
#def request_svg( kieler_json_obj, kieler_server_url=UNI_KIEL ):
#
#  if kieler_server_url == UNI_KIEL:
#    'oFormat' : 'org.w3.svg',
#    svg_data = request_layout( kieler_json_obj, kieler_server_url )
#    svg_data = fixup_svg( svg_data )
#
#  else:
#    #'oFormat' : 'org.json',
#    json_data = request_layout( kieler_json_obj, kieler_server_url )
#    svg_data  = json_to_svg( json_data )




