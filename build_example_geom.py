import sys

if __name__ != "__coreformcubit__":
    if "win" in sys.platform:
        path_to_cubit = r"C:\Program Files\Coreform Cubit 2024.3\bin"
    elif "lin" in sys.platform:
        path_to_cubit = r"/opt/Coreform-Cubit-2024.3/bin"
    import cubit
    cubit.init([])

def knuckle():
    cubit.cmd( "reset" )
    cubit.cmd( "import acis './geom/knuckle.sat' nofreesurfaces heal attributes_on  separate_bodies" )
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

def quarter_cylinder():
    cubit.cmd( "reset" )
    cubit.cmd( "create Cylinder height 1 radius 1" )
    cubit.cmd( "create Cylinder height 1 radius 0.75" )
    cubit.cmd( "subtract vol 2 from vol 1" )
    cubit.cmd( "section volume all with xplane offset 0 normal" )
    cubit.cmd( "section volume all with yplane offset 0 normal" )
    cubit.cmd( "compress ids" )
    cubit.cmd( "vol all interval 1" )
    cubit.cmd( "mesh vol 1" )