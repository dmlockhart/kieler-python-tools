import os
import json
import pytest
import requests

import json_to_svg as j2s
import kieler_web  as kw

#-----------------------------------------------------------------------
# test_request_layout
#-----------------------------------------------------------------------
@pytest.mark.parametrize('oFormat', ['org.w3.svg', 'org.json'])
def test_request_layout( oFormat ):

  test_data = {
    'config'  : {
                'spacing'     : 100,
                'algorithm'   : 'de.cau.cs.kieler.klay.layered',
                'edgeRouting' : 'ORTHOGONAL'
                },
    'iFormat' : 'org.json',
    'oFormat' : oFormat,
    'graph'   : {
                'id': "root",
                'children': [
                  {'id': "n1", 'labels': [{'text':"n1"}], 'width':100, 'height':100},
                  {'id': "n2", 'labels': [{'text':"n2"}], 'width':100, 'height': 50,
                   'ports': [{ 'id': "n2_p1", 'width': 10, 'height': 10 }],
                   'children': [
                     {'id': "n3", 'labels': [{'text':"n3" }], 'width':20, 'height':20 },
                     {'id': "n4", 'labels': [{'text':"n4" }], 'width':20, 'height':20 }
                   ],
                   'edges': [{'id': "e4", 'source': "n3", 'target': "n4"}]
                  },
                  {'id': "n5", 'labels': [ {'text':"n5"} ], 'width':100, 'height':50}
                ],
                'edges': [
                  {'id':"e1", 'labels': [{'text':"e1"} ],
                   'source':"n1", 'target': "n2", 'targetPort': "n2_p1"},
                  {'id':"e2", 'labels': [{'text':"e2"} ],
                   'source':"n1", 'target': "n5" }
                ]
                },
  }

  # request the layout
  output = kw.request_layout( test_data )

  # request the layout
  if   'svg'  in oFormat:
    svg_text = kw.fixup_kwebs_svg( output )
  elif 'json' in oFormat:
    json_text = json.loads( output )
    svg_text  = j2s.json_to_svg( json_text )
  else:
    assert "Unsupported request type!" == True

  # save the output to a file

  filen  = oFormat+'.svg'
  if os.path.exists( filen ):
    os.remove( filen )

  with open( filen, 'w' ) as fp:
    fp.write( svg_text )

  assert os.path.exists( filen )

#-----------------------------------------------------------------------
# test_json_graph_to_svg
#-----------------------------------------------------------------------
@pytest.mark.parametrize('server', [
  'http://layout.rtsys.informatik.uni-kiel.de:9444/layout',
  'http://localhost:9444/live',
])
def test_json_graph_to_svg( server ):
  graph = { 'id': "root",
          'children': [
            {'id': "n1", 'labels': [{'text':"n1"}], 'width':100, 'height':100},
            {'id': "n2", 'labels': [{'text':"n2"}], 'width':100, 'height': 50,
             'ports': [{ 'id': "n2_p1", 'width': 10, 'height': 10 }],
             'children': [
               {'id': "n3", 'labels': [{'text':"n3" }], 'width':20, 'height':20 },
               {'id': "n4", 'labels': [{'text':"n4" }], 'width':20, 'height':20 }
             ],
             'edges': [{'id': "e4", 'source': "n3", 'target': "n4"}]
            },
            {'id': "n5", 'labels': [ {'text':"n5"} ], 'width':100, 'height':50}
          ],
          'edges': [
            {'id':"e1", 'labels': [{'text':"e1"} ],
             'source':"n1", 'target': "n2", 'targetPort': "n2_p1"},
            {'id':"e2", 'labels': [{'text':"e2"} ],
             'source':"n1", 'target': "n5" }
          ]
          }

  try:
    svg_text = kw.json_graph_to_svg( graph, server )
  except requests.ConnectionError as e:
    if 'Connection refused' in str( e.message ):
      pytest.skip('Cannot connect to server.')
    raise e

  filen  = 'kwebs.svg' if 'kiel' in server else 'localhost.svg'
  if os.path.exists( filen ):
    os.remove( filen )

  with open( filen, 'w' ) as fp:
    fp.write( svg_text )

  assert os.path.exists( filen )
