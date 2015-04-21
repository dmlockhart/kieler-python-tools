from json_to_svg import json_to_svg

def test_simple():

  json_object = \
  [{u'children': [{u'height': 100,
                 u'id': u'n1',
                 u'labels': [{u'height': 0, u'text': u'n1', u'width': 0,
                              u'x': 0, u'y': 0}],
                 u'padding': {u'bottom': 0, u'left': 0, u'right': 0, u'top': 0},
                 u'width': 100,
                 u'x': 12,
                 u'y': 117.33333587646484},
                {u'children': [{u'height': 20,
                                u'id': u'n3',
                                u'labels': [{u'height': 0, u'text': u'n3',
                                             u'width': 0, u'x': 0, u'y': 0}],
                                u'padding': {u'bottom': 0, u'left': 0,
                                             u'right': 0, u'top': 0},
                                u'width': 20,
                                u'x': 12,
                                u'y': 12},
                               {u'height': 20,
                                u'id': u'n4',
                                u'labels': [{u'height': 0, u'text': u'n4',
                                             u'width': 0, u'x': 0, u'y': 0}],
                                u'padding': {u'bottom': 0, u'left': 0,
                                             u'right': 0, u'top': 0},
                                u'width': 20,
                                u'x': 132,
                                u'y': 12}],
                 u'edges': [{u'bendPoints': [],
                             u'id': u'e4',
                             u'source': u'n3',
                             u'sourcePoint': {u'x': 32, u'y': 22},
                             u'target': u'n4',
                             u'targetPoint': {u'x': 132, u'y': 22}}],
                 u'height': 44,
                 u'id': u'n2',
                 u'labels': [{u'height': 0,
                              u'text': u'n2',
                              u'width': 0,
                              u'x': 0,
                              u'y': 0}],
                 u'padding': {u'bottom': 0,
                              u'left': 0,
                              u'right': 0,
                              u'top': 0},
                 u'ports': [{u'height': 10,
                             u'id': u'n2_p1',
                             u'padding': {u'bottom': 0, u'left': 0,
                                          u'right': 0, u'top': 0},
                             u'width': 10,
                             u'x': -10,
                             u'y': 17}],
                 u'width': 164,
                 u'x': 322,
                 u'y': 162},
                {u'height': 50,
                 u'id': u'n5',
                 u'labels': [{u'height': 0, u'text': u'n5', u'width': 0,
                              u'x': 0, u'y': 0}],
                 u'padding': {u'bottom': 0, u'left': 0, u'right': 0, u'top': 0},
                 u'width': 100,
                 u'x': 322,
                 u'y': 12}],
  u'edges': [{u'bendPoints': [],
              u'id': u'e1',
              u'labels': [{u'height': 0, u'text': u'e1', u'width': 0,
                           u'x': 212, u'y': 185}],
              u'source': u'n1',
              u'sourcePoint': {u'x': 112, u'y': 184},
              u'target': u'n2',
              u'targetPoint': {u'x': 312, u'y': 184},
              u'targetPort': u'n2_p1'},
             {u'bendPoints': [{u'x': 162, u'y': 150.6666717529297},
                              {u'x': 162, u'y': 37}],
              u'id': u'e2',
              u'labels': [{u'height': 0, u'text': u'e2', u'width': 0,
                           u'x': 212, u'y': 36}],
              u'source': u'n1',
              u'sourcePoint': {u'x': 112, u'y': 150.6666717529297},
              u'target': u'n5',
              u'targetPoint': {u'x': 322, u'y': 37}}],
  u'height': 229.3333282470703,
  u'id': u'root',
  u'padding': {u'bottom': 0, u'left': 0, u'right': 0, u'top': 0},
  u'width': 498,
  u'x': 0,
  u'y': 0}]

  svg_text = json_to_svg( json_object )

  rects = paths = texts = 0

  for line in svg_text.split('\n'):
    if '<rect' in line: rects += 1
    if '<path' in line: paths += 1
    if '<text' in line: texts += 1

  assert rects == 5
  assert paths == 3
  assert texts == 7



