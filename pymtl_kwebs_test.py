#=======================================================================
# pymtl_kwebs_test.py
#=======================================================================

import os
import pytest
import pprint

from pymtl       import *
from pymtl_kwebs import *

#-----------------------------------------------------------------------
# test_pymtl_to_json
#-----------------------------------------------------------------------
@pytest.mark.parametrize('show_clk_reset', [True, False])
def test_pymtl_to_json( show_clk_reset ):

  # instantiate and elaborate

  x = MyTest2( 8 )
  x.elaborate()

  # translate to json

  graph_json = pymtl_to_json( x )

#-----------------------------------------------------------------------
# test_pymtl_to_svg
#-----------------------------------------------------------------------
@pytest.mark.parametrize('show_clk_reset', [True, False])
def test_pymtl_to_svg( show_clk_reset ):

  # instantiate and elaborate

  x = MyTest2( 8 )
  x.elaborate()

  # translate to svg

  try:
    graph_svg = pymtl_to_svg( x, show_clk_reset )
  except requests.ConnectionError as e:
    if 'Connection refused' in str( e.message ):
      pytest.skip('Cannot connect to server.')
    raise e

  # write out the svg file

  filen  = 'pymtl-clk.svg' if show_clk_reset else 'pymtl-no-clk.svg'
  if os.path.exists( filen ):
    os.remove( filen )

  with open( filen, 'w' ) as fp:
    fp.write( graph_svg )

  assert os.path.exists( filen )

#=======================================================================
# test models
#=======================================================================

class MyTest( Model ):
  def __init__( s, nbits ):
    s.in_ = InPort ( nbits )
    s.out = OutPort( nbits )
    @s.combinational
    def logic():
      s.out.value = s.in_

class MyTest2( Model ):
  def __init__( s, nbits ):
    s.in_ = InPort ( nbits )
    s.out = OutPort( nbits )

    s.mod = MyTest ( nbits )
    s.connect_pairs(
      s.in_, s.mod.in_,
      s.out, s.mod.out,
    )
