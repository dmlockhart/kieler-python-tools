import json
import json_to_svg
import pytest
import re
import requests

UNI_KIEL = 'http://layout.rtsys.informatik.uni-kiel.de:9444/layout'

#-----------------------------------------------------------------------
# request_layout
#-----------------------------------------------------------------------
def request_layout( kieler_json_req, kieler_server_url=UNI_KIEL ):
  '''Send a layout request to the specified kieler layout server.

     Expects input request object to be a dictionary containing the
     following fields: config, iFormat, oFormat, graph.
  '''

  # encode json elements (config and graph) as json strings
  for key, value in kieler_json_req.items():
    if not isinstance( value, (str,int) ):
      kieler_json_req[key] = json.dumps( value )

  # post the request
  r = requests.post( kieler_server_url, data = kieler_json_req )

  print r.headers
  if not r.ok:
    print r.text
  assert r.ok
  return r.text

#-----------------------------------------------------------------------
# fixup_kwebs_svg
#-----------------------------------------------------------------------
def fixup_kwebs_svg( svg_data ):
  '''Fixup the broken SVG returned by University of Kiel test server.

   Test server returns illegal SVG with multiple "w" attributes defined,
   this utility function fixes that up.
  '''
  return re.sub(' w="[0-9]+" ',' ', svg_data, count=1)

#-----------------------------------------------------------------------
# json_graph_to_svg
#-----------------------------------------------------------------------
def json_graph_to_svg( object_graph, kieler_server_url=UNI_KIEL ):
  '''Take an object graph and request an svg image with diagram layout.

   Object graph is a hierarchical datastructure of dicts and lists
   (the Python object equivalent of JSON).
  '''

  json_req = {
    'config'  : {
                'spacing'     : 100,
                'algorithm'   : 'de.cau.cs.kieler.klay.layered',
                'edgeRouting' : 'ORTHOGONAL'
                },
    'iFormat' : 'org.json',
    'oFormat' : None,
    'graph'   : object_graph,
  }

  if kieler_server_url == UNI_KIEL:
    json_req['oFormat'] = 'org.w3.svg'
    svg_data = request_layout( json_req, kieler_server_url )
    svg_data = fixup_kwebs_svg( svg_data )

  else:
    json_req['oFormat'] = 'org.json'
    json_data = request_layout( json_req, kieler_server_url )
    json_obj  = json.loads( json_data )
    svg_data  = json_to_svg.json_to_svg( json_obj )

  return svg_data
