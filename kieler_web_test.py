import json
import kieler_web as kw

def test_request_layout():

  test_data = {
    'config'  : json.dumps({
                'spacing'     : 100,
                'algorithm'   : 'de.cau.cs.kieler.klay.layered',
                'edgeRouting' : 'ORTHOGONAL'
                }),
    'iFormat' : 'org.json',
    'oFormat' : 'org.w3.svg',
    #'oFormat' : 'org.json',
    'graph'   : json.dumps({
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
                }),
  }

  output = kw.request_layout( test_data )
  output = kw.fixup_svg( output )
  with open('test_svg.svg', 'w') as fp:
    fp.write( output )

