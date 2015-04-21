import json
import pprint

#-----------------------------------------------------------------------
# json_to_svg
#-----------------------------------------------------------------------
def json_to_svg( json_obj ):

  assert type( json_obj ) == list and len( json_obj ) == 1

  svg_tmpl = '''\
<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  {body}
</svg>
'''

  shapes   = _recurse_into_json( json_obj[0] )
  svg_text = svg_tmpl.format( body = '\n  '.join(shapes) )
  return svg_text

#-----------------------------------------------------------------------
# _recurse_into_json
#-----------------------------------------------------------------------
def _recurse_into_json( json_obj, x_y_offset=(0,0) ):

  shapes = []

  def add_offset( x_y ):
    return tuple(a+b for a,b in zip( x_y, x_y_offset ))

  #---------------------------------------------------------------------
  # create rectangles
  #---------------------------------------------------------------------
  def rect( x, y, w, h, fill='rgb(255,255,255)' ):
    return ('<rect x="{x}" y="{y}" height="{h}" width="{w}"'
            ' stroke="rgb(0,0,0)" fill="{fill}"/>').format(**locals())

  for box in json_obj.get('children', []):
    x_y_h_w     = [box[i] for i in ['x','y','width','height']]
    x_y_h_w[:2] = add_offset( x_y_h_w )
    shapes.append( rect( *x_y_h_w ) )

  #---------------------------------------------------------------------
  # create labels
  #---------------------------------------------------------------------
  def text( x, y, text, font_size=11 ):
    return ('<text x="{x}" y="{y}" font-size="{font_size}"'
            ' fill="rgb(0,0,0)">{text}</text>').format(**locals())

  for label in json_obj.get('labels', []):
    label_x_y = add_offset( [label[i] for i in ['x','y']] )
    shapes.append( text( *label_x_y, text=label['text'] ) )

  #---------------------------------------------------------------------
  # create wiring
  #---------------------------------------------------------------------
  def edge( x1, y1, x2, y2, bends=None ):

    if bends: bend_xys = ' '.join( 'L {} {}'.format(x,y) for x,y in bends )
    else:     bend_xys = ''

    return ('<path d="M {x1} {y1} {bend_xys} L {x2} {y2}"'
            ' stroke="rgb(0,0,0)" fill="none"/>').format(**locals())

  for line in json_obj.get('edges', []):
    xy1 = add_offset( [line['sourcePoint'][i] for i in ['x','y']] )
    xy2 = add_offset( [line['targetPoint'][i] for i in ['x','y']] )
    xys = [add_offset([i['x'], i['y']]) for i in line['bendPoints']]
    shapes.append( edge( *(xy1+xy2), bends=xys ) )

    for label in line.get('labels', []):
      label_x_y = [label[i] for i in ['x','y']]
      shapes.append( text( *label_x_y, text=label['text'] ) )

  #---------------------------------------------------------------------
  # create ports
  #---------------------------------------------------------------------
  def circle( x, y, radius, fill='rgb(255,255,255)' ):
    return ('<circle cx="{x}" cy="{y}" r="{radius}"'
            ' stroke="rgb(0,0,0)" fill="{fill}"/>').format(**locals())

  for port in json_obj.get('ports', []):
    x_y_h_w  = [port[i] for i in ['x','y','width','height']]
    radius   = x_y_h_w[-1] / 2.0
    x_y      = [i+radius for i in add_offset( x_y_h_w )]
    shapes.append( circle( *x_y, radius=radius ) )

  #---------------------------------------------------------------------
  # recursively visit children
  #---------------------------------------------------------------------
  for box in json_obj.get('children', []):
    child_x_y_offset = add_offset( [box[i] for i in ['x','y']] )
    shapes += _recurse_into_json( box, child_x_y_offset )

  return shapes

