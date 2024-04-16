import sys

if __name__ != "__coreformcubit__":
    if "win" in sys.platform:
        path_to_cubit = r"C:\Program Files\Coreform Cubit 2024.3\bin"
    elif "lin" in sys.platform:
        path_to_cubit = r"/opt/Coreform-Cubit-2024.3/bin"
    import cubit
    cubit.init([])

import numpy

cubitHexNodeCoords = {
                        0: ( -1, -1, +1 ), # ( -X, -Y, +Z )
                        1: ( -1, -1, -1 ), # ( -X, -Y, -Z )
                        2: ( -1, +1, -1 ), # ( -X, +Y, -Z )
                        3: ( -1, +1, +1 ), # ( -X, +Y, +Z )
                        4: ( +1, -1, +1 ), # ( +X, -Y, +Z )
                        5: ( +1, -1, -1 ), # ( +X, -Y, -Z )
                        6: ( +1, +1, -1 ), # ( +X, +Y, -Z )
                        7: ( +1, +1, +1 )  # ( +X, +Y, +Z )
                     }

TPNodesInCubitNodes = {
                        0: 4, # ( -X, -Y, +Z )
                        1: 0, # ( -X, -Y, -Z )
                        2: 2, # ( -X, +Y, -Z )
                        3: 6, # ( -X, +Y, +Z )
                        4: 5, # ( +X, -Y, +Z )
                        5: 1, # ( +X, -Y, -Z )
                        6: 3, # ( +X, +Y, -Z )
                        7: 7  # ( +X, +Y, +Z )
                      }

cubitNodesInTPNodes = {
                        0: 1, # ( -X, -Y, -Z )
                        1: 5, # ( +X, -Y, -Z )
                        2: 2, # ( -X, +Y, -Z )
                        3: 6, # ( +X, +Y, -Z )
                        4: 0, # ( -X, -Y, +Z )
                        5: 4, # ( +X, -Y, +Z )
                        6: 3, # ( -X, +Y, +Z )
                        7: 7  # ( +X, +Y, +Z )
                      }

cubitNodesInTPEdges = {
                        0: ( 1, 5 ),  # ( -/+X,   -Y,   -Z )
                        1: ( 2, 6 ),  # ( -/+X,   +Y,   -Z )
                        2: ( 0, 4 ),  # ( -/+X,   -Y,   +Z )
                        3: ( 3, 7 ),  # ( -/+X,   +Y,   +Z )
                        4: ( 1, 2 ),  # (   -X, -/+Y,   -Z )
                        5: ( 5, 6 ),  # (   +X, -/+Y,   -Z )
                        6: ( 0, 3 ),  # (   -X, -/+Y,   +Z )
                        7: ( 4, 7 ),  # (   +X, -/+Y,   +Z )
                        8: ( 1, 0 ),  # (   -X,   -Y, -/+Z )
                        9: ( 5, 4 ),  # (   +X,   -Y, -/+Z )
                        10: ( 2, 3 ), # (   -X,   +Y, -/+Z )
                        11: ( 6, 7 )  # (   +X,   +Y, -/+Z )
                      }

cubitNodesInTPFaces = {
                        0: ( 0, 1, 2, 3 ), # -X
                        1: ( 4, 5, 6, 7 ), # +X
                        2: ( 0, 1, 4, 5 ), # -Y
                        3: ( 2, 3, 6, 7 ), # +Y
                        4: ( 1, 2, 5, 6 ), # -Z
                        5: ( 0, 3, 4, 7 )  # +Z
                      }

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
        nodes[(i,j,k)] = ( getUniformNode1D( degree[0], i ), getUniformNode1D( degree[1], j ), getUniformNode1D( degree[2], k ) )
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

def getSurfaceFromFaceNodes( n1, n2, n3, n4 ):
  s1 = cubit.parse_cubit_list( "surface", f"in node {n1}" )
  s2 = cubit.parse_cubit_list( "surface", f"in node {n2}" )
  s3 = cubit.parse_cubit_list( "surface", f"in node {n3}" )
  s4 = cubit.parse_cubit_list( "surface", f"in node {n4}" )
  s = list( set(s1).intersection(s2).intersection(s3).intersection(s4) )
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
        local_node_id = getUniformNodeID( degree, i, j, k )
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

E = cubit.get_entities( "hex" )
for eid in E:
  P = getHighOrderNodeCoords( eid, (3, 3, 3) )
  for i in range( 0, P.shape[0] ):
    cubit.cmd( f"create vertex x {P[i,0]} y {P[i,1]} z {P[i,2]}" )
