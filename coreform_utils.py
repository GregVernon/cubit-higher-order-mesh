import sys

def import_cubit():
    if "win" in sys.platform:
        path_to_cubit = r"C:\Program Files\Coreform Cubit 2024.3\bin"
    elif "lin" in sys.platform:
        path_to_cubit = r"/opt/Coreform-Cubit-2024.3/bin"
    sys.path.append( path_to_cubit )
    import cubit
    cubit.init([])
    return cubit

def set_performance_mode():
    cubit.cmd( "info off" )
    cubit.cmd( "echo off" )
    cubit.cmd( "warning off" )
    cubit.cmd( "journal off" )
    cubit.cmd( "undo off" )
    cubit.cmd( "graphics off" )
    cubit.cmd( "set default autosize off" )

def set_interactive_mode():
    cubit.cmd( "info on" )
    cubit.cmd( "echo on" )
    cubit.cmd( "warning on" )
    cubit.cmd( "journal on" )
    cubit.cmd( "undo on" )
    cubit.cmd( "graphics on" )
    cubit.cmd( "set default autosize on" )

if __name__ != "__coreformcubit__":
    cubit = import_cubit()