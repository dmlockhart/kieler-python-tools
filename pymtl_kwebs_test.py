#=======================================================================
# pymtl_kwebs_test.py
#=======================================================================

import os
import pytest
import pprint
import requests

from pymtl       import *
from pymtl_kwebs import *

#-----------------------------------------------------------------------
# py.test fixture
#-----------------------------------------------------------------------
@pytest.fixture
def out_filename( request ):
  nodeid   = request.node.nodeid
  filename = nodeid.split(':')[-1] + '.svg'
  return filename

#-----------------------------------------------------------------------
# test_pymtl_to_json
#-----------------------------------------------------------------------
@pytest.mark.parametrize('show_clk_reset', [True, False])
def test_pymtl_to_json( show_clk_reset ):

  # instantiate and elaborate

  x = MyTestTop( 8 )
  x.elaborate()

  # translate to json

  graph_json = pymtl_to_json( x )

#-----------------------------------------------------------------------
# test_pymtl_to_svg
#-----------------------------------------------------------------------
def test_pymtl_to_svg( out_filename, ModelType, show_clk_reset ):

  # instantiate and elaborate

  x = ModelType( 8 )
  x.elaborate()

  # translate to svg

  try:
    graph_svg = pymtl_to_svg( x, show_clk_reset )
  except requests.ConnectionError as e:
    if 'Connection refused' in str( e.message ):
      pytest.skip('Cannot connect to server.')
    raise e

  # write out the svg file

  if os.path.exists( out_filename ):
    os.remove( out_filename )

  with open( out_filename, 'w' ) as fp:
    fp.write( graph_svg )

  assert os.path.exists( out_filename )

#=======================================================================
# test models
#=======================================================================
class MyTestTop( Model ):
  def __init__( s, nbits ):
    s.in_ = InPort ( nbits )
    s.out = OutPort( nbits )

    s.mod = MyTest ( nbits )
    s.connect_pairs(
      s.in_, s.mod.in_,
      s.out, s.mod.out,
    )

class MyTest( Model ):
  def __init__( s, nbits ):
    s.in_ = InPort ( nbits )
    s.out = OutPort( nbits )
    @s.combinational
    def logic():
      s.out.value = s.in_

class MyTestWire( Model ):
  def __init__( s, nbits ):
    s.in_  = InPort ( nbits )
    s.out  = OutPort( nbits )
    s.out2 = OutPort( nbits )

    s.mod = MyTest ( nbits )
    s.connect_pairs(
      s.in_, s.mod.in_,
      s.out, s.mod.out,
    )

    s.wire = Wire( nbits )
    s.connect_pairs(
      s.in_,  s.wire,
      s.wire, s.out,
    )

pytest.mark.parametrize('ModelType,show_clk_reset', [
  (MyTestTop,  True),
  (MyTestTop,  False),
  (MyTestWire, False),
])( test_pymtl_to_svg )
