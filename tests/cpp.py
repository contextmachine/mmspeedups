
import os

inc_paths = [os.path.join(os.path.sep, 'usr', 'include'),
             os.path.join(os.path.sep, 'usr', 'local', 'include'), os.path.join(os.path.sep, 'usr', 'local', 'lib')]


import cppyy

# bring in some symbols to resolve the class
cppyy.include('/Users/andrewastakhov/dev/rhino3dm/src/lib/opennurbs/opennurbs.h')
r=cppyy.load_library("librhino3dm_native")
i=cppyy.load_reflection_info("librhino3dm_native.dylib")
#print(r,i)
print(cppyy.gbl.ON_3dPoint.Set.func_defaults)
print(dir(cppyy.gbl.ON_Geometry))
ptt=cppyy.gbl.ON_3dPoint
pt=cppyy.gbl.ON_3dPoint(x=0.0,y=0.0,z=0.0)
print(ptt, type(pt.x))