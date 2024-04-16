#!python
import numpy

#def initialize():
cubit.cmd( "reset" )
cubit.cmd( "import acis 'C:/Users/Owner/Documents/CubitTemp/examples/required_files/knuckle.sat' nofreesurfaces heal attributes_on  separate_bodies" )
cubit.cmd( "remove surface 15 extend" )
cubit.cmd( "webcut volume 1 with loop curve 47 48" )
cubit.cmd( "webcut volume 2  with sheet extended from surface 16" )
cubit.cmd( "webcut volume all with plane normal to curve 35  fraction .5 from start" )
cubit.cmd( "webcut volume all with plane normal to curve 77  fraction .5 from start" )
cubit.cmd( "webcut volume all with plane normal to curve 11  fraction .5 from start" )
cubit.cmd( "webcut volume all with plane normal to curve 355  close_to vertex 19" )
cubit.cmd( "webcut volume all with plane normal to curve 106  close_to vertex 32" )  
cubit.cmd( "webcut volume all with plane normal to curve 121  close_to vertex 29" )
cubit.cmd( "composite create surface 252 134 263 103 88 260 153 272 keep angle 15" )
cubit.cmd( "imprint all" )
cubit.cmd( "merge all" )
cubit.cmd( "volume all size 5" )
cubit.cmd( "volume 20 22 21 18  redistribute nodes off" )
cubit.cmd( "volume 20 22 21 18  scheme Sweep Vector -1 0 0 sweep transform least squares" )
cubit.cmd( "volume 20 22 21 18  autosmooth target on  fixed imprints off  smart smooth off" )
cubit.cmd( "volume 2 5 8 11 13 14 15 16  redistribute nodes off" )
cubit.cmd( "volume 2 5 8 11 13 14 15 16  autosmooth target on  fixed imprints off  smart smooth off" )
cubit.cmd( "volume 2  scheme Sweep  source surface 214 169    target surface 166   sweep transform least squares" )
cubit.cmd( "volume 5  scheme Sweep  source surface 182 223    target surface 180   sweep transform least squares" )
cubit.cmd( "volume 8  scheme Sweep  source surface 230 192    target surface 190   sweep transform least squares" )
cubit.cmd( "volume 11  scheme Sweep  source surface 238 205    target surface 202   sweep transform least squares" )
cubit.cmd( "volume 13  scheme Sweep  source surface 173 174    target surface 176   sweep transform least squares" )
cubit.cmd( "volume 14  scheme Sweep  source surface 184 187    target surface 186   sweep transform least squares" )
cubit.cmd( "volume 15  scheme Sweep  source surface 198 197    target surface 200   sweep transform least squares" )
cubit.cmd( "volume 16  scheme Sweep  source surface 209 210    target surface 211   sweep transform least squares" )
cubit.cmd( "volume 1 4 7 10 redistribute nodes off" )
cubit.cmd( "volume 1 4 7 10 autosmooth target on  fixed imprints off  smart smooth off" )
cubit.cmd( "volume 1  scheme Sweep  source surface 76 78    target surface 74   sweep transform least squares" )
cubit.cmd( "volume 4  scheme Sweep  source surface 122 123    target surface 120   sweep transform least squares" )
cubit.cmd( "volume 7  scheme Sweep  source surface 81 82    target surface 84   sweep transform least squares" )
cubit.cmd( "volume 10  scheme Sweep  source surface 127 128    target surface 130   sweep transform least squares" )
cubit.cmd( "volume 1 4 7 10 scheme submap" )
cubit.cmd( "volume 3 6 9 12 scheme map" )
cubit.cmd( "mesh vol all" )

cubitHexNodeCoords = {
                        0: ( -1, -1, +1 ),
                        1: ( -1, -1, -1 ),
                        2: ( -1, +1, -1 ),
                        3: ( -1, +1, +1 ),
                        4: ( +1, -1, +1 ),
                        5: ( +1, -1, -1 ),
                        6: ( +1, +1, -1 ),
                        7: ( +1, +1, +1 ) }

TPNodesInCubitNodes = { 0: 4, 1: 0, 2: 2, 3: 6, 4: 5, 5: 1, 6: 3, 7: 7 }

cubitNodesInTPNodes = { 
                        0: 1,  # -X, -Y, -Z
                        1: 5,  # +X, -Y, -Z
                        2: 2,  # -X, +Y, -Z
                        3: 6,  # +X, +Y, -Z
                        4: 0,  # -X, -Y, +Z
                        5: 4,  # +X, -Y, +Z
                        6: 3,  # -X, +Y, +Z
                        7: 7 } # +X, +Y, +Z

cubitNodesInTPEdges = {
                        0: ( 1, 5 ),    # -/+X,   -Y,   -Z
                        1: ( 2, 6 ),    # -/+X,   +Y,   -Z
                        2: ( 0, 4 ),    # -/+X,   -Y,   +Z
                        3: ( 3, 7 ),    # -/+X,   +Y,   +Z
                        4: ( 1, 2 ),    #   -X, -/+Y,   -Z
                        5: ( 5, 6 ),    #   +X, -/+Y,   -Z
                        6: ( 0, 3 ),    #   -X, -/+Y,   +Z
                        7: ( 4, 7 ),    #   +X, -/+Y,   +Z
                        8: ( 1, 0 ),    #   -X,   -Y, -/+Z
                        9: ( 5, 4 ),    #   +X,   -Y, -/+Z
                        10: ( 2, 3 ),   #   -X,   +Y, -/+Z
                        11: ( 6, 7 ) }  #   +X,   +Y, -/+Z

cubitNodesInTPFaces = { 
                        0: ( 0, 1, 2, 3 ),  # -X
                        1: ( 4, 5, 6, 7 ),  # +X 
                        2: ( 0, 1, 4, 5 ),  # -Y
                        3: ( 2, 3, 6, 7 ),  # +Y
                        4: ( 1, 2, 5, 6 ),  # -Z
                        5: ( 0, 3, 4, 7 ) } # +Z

def evalLagrangeBasis1D( degree, basis_idx, variate ):
  nodes = [ getUniformNode1D( degree, n ) for n in range( 0, degree + 1 ) ]
  basis_val = 1
  for i in range( 0, degree + 1 ):
    if ( i != basis_idx ):
      basis_val *= ( variate - nodes[i] ) / ( nodes[basis_idx] - nodes[i] )
  return basis_val

def evalLagrangeBasis3D( degree, basis_idx, variate ):
  basis_components = [ evalLagrangeBasis1D( degree[i], basis_idx[i], variate[i] ) for i in range( 0, 3 ) ]
  basis_val = basis_components[0] * basis_components[1] * basis_components[2]
  return basis_val

def getUniformNode1D( degree, basis_idx ):
  nodes = numpy.linspace( -1, 1, degree + 1 )
  node = nodes[basis_idx]
  return node

def getUniformNodes3D( degree ):
  nodes = {}
  for k in range( 0, degree[2] + 1 ):
    for j in range( 0, degree[1] + 1 ):
      for i in range( 0, degree[0] + 1 ):
        nodes[(i,j,k)] = ( getUniformNode1D( degree[i], i ), getUniformNode1D( degree[j], j ), getUniformNode1D( degree[k], k ) )
  return nodes

def getUniformNodeID( degree, i, j, k ):
  nodes = getUniformNodeIDs( degree )
  return nodes[(i,j,k)]

def getUniformNodeIDs( degree ):
  nodes = {}
  n = -1
  for k in range( 0, degree[2] + 1 ):
    for j in range( 0, degree[1] + 1 ):
      for i in range( 0, degree[0] + 1 ):
        n += 1
        nodes[( i, j, k )] = n
  return nodes

def getLinearHexNodeCoords( elem_id ):
  node_coords = numpy.zeros( shape=( 8, 3 ) )
  node_ids = cubit.get_connectivity( "hex", elem_id )
  for n in range( 0, 8 ):
    node_coords[n,:] = cubit.get_nodal_coordinates( node_ids[cubitNodesInTPNodes[n]] )
  return node_coords

def evalLinearHexBasisVector( xi ):
  degree = [1,1,1]
  basis = numpy.zeros( 8 )
  n = 0
  for k in range( 0, 2 ):
    for j in range( 0, 2 ):
      for i in range( 0, 2 ):
        basis[n] = evalLagrangeBasis3D( degree, [i,j,k], xi )
        n += 1
  return basis

def linearHexMapping( elem_id, xi ):
  P = getLinearHexNodeCoords( elem_id )
  N = evalLinearHexBasisVector( xi )
  x = numpy.matmul( P.transpose(), N )
  return x

def getVertexFromNode( n ):
  v = cubit.parse_cubit_list( "vertex", f"in node {n}" )
  if len( v ) == 1:
    v = v[0]
  else:
    v = None
  return v

def getCurveFromNode( n ):
  c = cubit.parse_cubit_list( "curve", f"in node {n}" )
  if len( c ) == 1:
    c = c[0]
  else:
    c = None
  return c

def getSurfaceFromNode( n ):
  s = cubit.parse_cubit_list( "surface", f"in node {n}" )
  if len( s ) == 1:
    s = s[0]
  else:
    s = None
  return s

def getCurveFromEdgeNodes( n1, n2 ):
  e1 = cubit.parse_cubit_list( "edge", f"in node {n1}" )
  e2 = cubit.parse_cubit_list( "edge", f"in node {n2}" )
  e = list( set(e1).intersection(e2) )
  c = cubit.parse_cubit_list( "curve", f"in edge {e[0]}" )
  if len( c ) > 0:
    c = c[0]
  else:
    c = None
  return c

def getCurveFromEdgeNodes( n1, n2 ):
  c1 = cubit.parse_cubit_list( "curve", f"in node {n1}" )
  c2 = cubit.parse_cubit_list( "curve", f"in node {n2}" )
  c = list( set(c1).intersection(c2) )
  if len( c ) > 0:
    c = c[0]
  else:
    c = None
  return c

def getSurfaceFromEdgeNodes( n1, n2 ):
  s1 = cubit.parse_cubit_list( "surface", f"in node {n1}" )
  s2 = cubit.parse_cubit_list( "surface", f"in node {n2}" )
  s = list( set(s1).intersection(s2) )
  if len( s ) > 0:
    s = s[0]
  else:
    s = None
  return s

def isTPNodeInNode( degree, i, j, k ):
  if i == 0 and j == 0 and k == 0:
    return ( True, cubitNodesInTPNodes[ 0 ] )
  elif i == degree[0] and j == 0 and k == 0:
    return ( True, cubitNodesInTPNodes[ 1 ] )
  elif i == 0 and j == degree[1] and k == 0:
    return ( True, cubitNodesInTPNodes[ 2 ] )
  elif i == degree[0] and j == degree[1] and k == 0:
    return ( True, cubitNodesInTPNodes[ 3 ] )
  elif i == 0 and j == 0 and k == degree[2]:
    return ( True, cubitNodesInTPNodes[ 4 ] )
  elif i == degree[0] and j == 0 and k == degree[2]:
    return ( True, cubitNodesInTPNodes[ 5 ] )
  elif i == 0 and j == degree[1] and k == degree[2]:
    return ( True, cubitNodesInTPNodes[ 6 ] )
  elif i == degree[0] and j == degree[1] and k == degree[2]:
    return ( True, cubitNodesInTPNodes[ 7 ] )
  else:
    return ( False, None )
  
def isTPNodeInEdge( degree, i, j, k ):
  if (i == 0) and (j == 0):
    return ( True, 8 )
  elif (i == 0) and (k == degree[2]):
    return ( True, 6 )
  elif (i == 0) and (j == degree[1]):
    return ( True, 10 )
  elif (i == 0) and (k == 0):
    return ( True, 4 )
  elif (i == degree[0]) and (j == 0):
    return ( True, 9 )
  elif (i == degree[0]) and (k == degree[2]):
    return ( True, 7 )
  elif (i == degree[0]) and (j == degree[1]):
    return ( True, 11 )
  elif (i == degree[0]) and (k == 0):
    return ( True, 5 )
  elif (j == 0) and (k == 0):
    return ( True, 0 )
  elif (j == 0) and (k == degree[2]):
    return ( True,  2 )
  elif (j == degree[1]) and (k == 0):
    return ( True, 1 )
  elif (j == degree[1]) and (k == degree[2]):
    return ( True, 3 )
  else:
    return ( False, None )

def isTPNodeInFace( degree, i, j, k ):
  if (i == 0):
    return ( True, 0 )
  elif (i == degree[0]):
    return ( True, 1 )
  elif (j == 0):
    return ( True, 2 )
  elif (j == degree[1]):
    return ( True, 3 )
  elif (k == 0):
    return ( True, 4 )
  elif (k == degree[2]):
    return ( True, 5 )
  else: 
    return ( False, None )

def getHighOrderNodeCoords( elem_id, degree ):
  elem_node_ids = cubit.get_connectivity( "hex", elem_id )
  param_coords = getUniformNodes3D( degree )
  deform_coords = numpy.zeros( shape=( len( param_coords ), 3 ), dtype="double" )
  for k in range( 0, degree[2] + 1 ):
    for j in range( 0, degree[1] + 1 ):
      for i in range( 0, degree[0] + 1 ):
        local_node_id = getUniformNodeIDs( (i,j,k) )
        # Check what geometric entity owns the node
        owning_vertex_id = None
        owning_curve_id = None
        owning_surface_id = None
        if isTPNodeInNode( degree, i, j, k )[0]:
          cubit_node_id = elem_node_ids[isTPNodeInNode( degree, i, j, k )[1]]
          owning_vertex_id = getVertexFromNode( cubit_node_id )
          owning_curve_id = getCurveFromNode( cubit_node_id )
          deform_coords[local_node_id,:] = cubit.get_nodal_coordinates( cubit_node_id )
        elif isTPNodeInEdge( degree, i, j, k )[0]:
          tp_edge = isTPNodeInEdge( degree, i, j, k )[1]
          n1 = elem_node_ids[cubitNodesInTPEdges[tp_edge][0]]
          n2 = elem_node_ids[cubitNodesInTPEdges[tp_edge][1]]
          owning_curve = getCurveFromEdgeNodes( n1, n2 )
          owning_surface = getSurfaceFromEdgeNodes( n1, n2 )
          if owning_curve:
            curve = cubit.curve( owning_curve )
            xi = param_coords[(i,j,k)]
            x, y, z = linearHexMapping( elem_id, xi )
            deform_coords[local_node_id,:] = curve.closest_point_trimmed( (x, y, z) )
          elif owning_surface:
            surface = cubit.surface( owning_surface )
            xi = param_coords[(i,j,k)]
            x, y, z = linearHexMapping( elem_id, xi )
            deform_coords[local_node_id,:] = surface.closest_point_trimmed( (x, y, z) )
          else:
            xi = param_coords[(i,j,k)]
            deform_coords[local_node_id,:] = linearHexMapping( elem_id, xi )
        elif isTPNodeInFace( degree, i, j, k )[0]:
          tp_face = isTPNodeInFace( degree, i, j, k )[1]
          n1 = elem_node_ids[cubitNodesInTPFaces[tp_face][0]]
          n2 = elem_node_ids[cubitNodesInTPFaces[tp_face][1]]
          n3 = elem_node_ids[cubitNodesInTPFaces[tp_face][2]]
          n4 = elem_node_ids[cubitNodesInTPFaces[tp_face][3]]
          owning_surface = getSurfaceFromFaceNodes( n1, n2, n3, n4 )
          if owning_surface:
            surface = cubit.surface( owning_surface )
            xi = param_coords[(i,j,k)]
            x, y, z = linearHexMapping( elem_id, xi )
            deform_coords[local_node_id,:] = surface.closest_point_trimmed( (x, y, z) )
          else:
            xi = param_coords[(i,j,k)]
            deform_coords[local_node_id,:] = linearHexMapping( elem_id, xi )
        else:
            xi = param_coords[(i,j,k)]
            deform_coords[local_node_id,:] = linearHexMapping( elem_id, xi )
  return deform_coords

getHighOrderNodeCoords( 1, (2, 2, 2) )
