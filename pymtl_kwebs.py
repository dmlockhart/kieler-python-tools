#=======================================================================
# pymtl_kwebs.py
#=======================================================================

from kieler_web import json_graph_to_svg

#-----------------------------------------------------------------------
# pymtl_to_svg
#-----------------------------------------------------------------------
def pymtl_to_svg( pymtl_model, show_clk_reset=True ):

  graph_json = pymtl_to_json( pymtl_model, show_clk_reset )
  graph_svg  = json_graph_to_svg( graph_json )

  return graph_svg

#-----------------------------------------------------------------------
# pymtl_to_json
#-----------------------------------------------------------------------
def pymtl_to_json( pymtl_model, show_clk_reset=True ):

  children = [ _recurse_pymtl_hierarchy( pymtl_model, show_clk_reset ) ]

  graph_json = {'id'      : 'root',
                'children': children,
                'padding' : {'left': 20, 'top': 20, 'right': 20, 'bottom': 20},
               }

  return graph_json

#-----------------------------------------------------------------------
# _recurse_pymtl_hierarchy
#-----------------------------------------------------------------------
def _recurse_pymtl_hierarchy( pymtl_model, show_clk_reset=True ):

  #---------------------------------------------------------------------
  # visit children
  #---------------------------------------------------------------------

  children = []
  for submodel in pymtl_model.get_submodules():
    children.append( _recurse_pymtl_hierarchy(submodel,show_clk_reset) )

  #---------------------------------------------------------------------
  # visit ports
  #---------------------------------------------------------------------

  ports = []
  for port in pymtl_model.get_ports():
    # hide clk and reset ports if requested, edges will automatically
    # be hidden by layout tool
    if not show_clk_reset and port.name in ['clk','reset']:
      continue
    port_dict = {
      'id'     : id(port),
      'labels' : [{'text':port.name}],
      'width'  : 10,
      'height' : 10,
    }
    ports.append( port_dict )

  #---------------------------------------------------------------------
  # visit connections
  #---------------------------------------------------------------------

  edges = []
  for edge in pymtl_model.get_connections():
    src, dest = edge.src_node, edge.dest_node
    if 'Wire' in src.__class__.__name__ or 'Wire' in dest.__class__.__name__:
      continue
    if src.parent == None or dest.parent == None:
      continue
    edge_dict = {
      'id'         : id(edge),
      'source'     : id(src.parent),
      'target'     : id(dest.parent),
      'sourcePort' : id(src),
      'targetPort' : id(dest),
    }
    edges.append( edge_dict )

  #---------------------------------------------------------------------
  # create the subgraph
  #---------------------------------------------------------------------

  subgraph = {
    'id'       : id(pymtl_model),
    'labels'   : [{'text':pymtl_model.name},
                  #{'text':pymtl_model.class_name},
                 ],
    'ports'    : ports,
    'edges'    : edges,
    'children' : children,

    # Set width/height to 0 if children, allow auto sizing
    'width'    : 0 if children else 100,
    'height'   : 0 if children else 100,
  }

  return subgraph

