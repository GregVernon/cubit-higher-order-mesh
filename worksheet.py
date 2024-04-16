import time
import compute_mesh
import build_example_geom
import coreform_utils

if __name__ != "__coreformcubit__":
    cubit = coreform_utils.import_cubit()

### KNUCKLE ###
build_example_geom.knuckle()
E = cubit.get_entities( "hex" )
for eid in E:
  P = compute_mesh.getHighOrderNodeCoords( eid, (4, 4, 4) )
  coreform_utils.set_performance_mode()
  for i in range( 0, P.shape[0] ):
    cubit.cmd( f"create vertex x {P[i,0]} y {P[i,1]} z {P[i,2]}" )
cubit.cmd( "save cub5 'knuckle_mesh.cub5' overwrite" )

t0 = time.time()
E = cubit.get_entities( "hex" )
num_nodes = 0
for eid in E:
  P = compute_mesh.getHighOrderNodeCoords( eid, (4, 4, 4) )
  num_nodes += P.shape[0]
t1 = time.time()
print( f"Computed {num_nodes} nodes on {len(E)} elements took {t1-t0} seconds" )


### Quarter Cylinder ###
build_example_geom.quarter_cylinder()
E = cubit.get_entities( "hex" )
for eid in E:
  P = compute_mesh.getHighOrderNodeCoords( eid, (4, 4, 4) )
  coreform_utils.set_performance_mode()
  for i in range( 0, P.shape[0] ):
    cubit.cmd( f"create vertex x {P[i,0]} y {P[i,1]} z {P[i,2]}" )
cubit.cmd( "save cub5 'quarter_cylinder.cub5' overwrite" )

t0 = time.time()
E = cubit.get_entities( "hex" )
num_nodes = 0
for eid in E:
  P = compute_mesh.getHighOrderNodeCoords( eid, (4, 4, 4) )
  num_nodes += P.shape[0]
t1 = time.time()
print( f"Computed {num_nodes} nodes on {len(E)} elements took {t1-t0} seconds" )