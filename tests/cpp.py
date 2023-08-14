import os


import numpy as np
# append local headers & libraries
inc_paths = [os.path.join(os.path.sep, 'usr', 'include'),
             os.path.join(os.path.sep, 'usr', 'local', 'include'), os.path.join(os.path.sep, 'usr', 'local', 'lib')]
import cppyy

# bring in some symbols to resolve the class
cppyy.include('/Users/andrewastakhov/dev/rhino3dm/src/lib/opennurbs/opennurbs.h')
# librhino3dm_native.so/librhino3dm_native.dylib you have to build beforehand
cppyy.load_library("librhino3dm_native")
cppyy.load_reflection_info("librhino3dm_native.dylib")

# A simple check that everything went correctly:
print(cppyy.gbl.ON_Geometry, dir(cppyy.gbl.ON_Geometry))
ptt = cppyy.gbl.ON_3dPoint
pt = cppyy.gbl.ON_3dPoint(x=0.0, y=0.0, z=0.0)
print(ptt, type(pt.x))


def make_array(points):
    arr = cppyy.gbl.ON_3dPointArray()
    for pt in points:
        arr.Append(cppyy.gbl.ON_3dPoint(*pt))
    return arr


class OnBezier:
    def __new__(cls, points):
        self = super().__new__(cls)
        self.points = points
        self._proxy = cppyy.gbl.ON_BezierCurve(make_array(points))
        return self

    def evaluate(self, t):
        if isinstance(t, (float, int)):
            res = self._proxy.PointAt(t)
            return res.x, res.y, res.z
        else:
            return [self.evaluate(tt) for tt in t]

    def cpts(self):
        cpts = []
        for i in range(self._proxy.CVCount()):
            res = self._proxy.ControlPoint(i)
            cpts.append((res.x, res.y, res.z, res.w))
        return cpts

    def tessellate(self):
        return self.evaluate(np.linspace(0, 1, 100).tolist())

    def domain(self):
        dmn = self._proxy.Domain()
        return dmn.Min(), dmn.Max()

    def length(self):
        return self._proxy.Length()


class OnNurbsCurve(OnBezier):
    def __new__(cls, points):
        self = super().__new__(cls, points)
        self._proxy = cppyy.gbl.ON_NurbsCurve(self._proxy)

        return self

    def bbox(self):
        return self._proxy.BoundingBox()


class OnNurbsSurface:
    def __new__(cls, curves):
        self = super().__new__(cls)
        self._proxy = cppyy.gbl.ON_NurbsSurface()
        arr = cppyy.gbl.ON_ClassArray[type(curves[0]._proxy)]
        self.bezier = cppyy.gbl.ON_BezierSurface()

        val = cppyy.gbl.ON_ClassArray[cppyy.gbl.ON_BezierCurve]()
        for crv in curves:
            val.Append(crv._proxy)
        self.bezier.Loft(val)
        self.bezier.GetNurbForm(self._proxy)

        return self

    def evaluate(self, u, v):
        if isinstance(u, (float, int)) and isinstance(v, (float, int)):
            res = self._proxy.PointAt(u, v)
            return res.x, res.y, res.z
        else:
            l = []
            for i in u:
                for j in v:
                    l.append(self.evaluate(i, j))
            return l

# language=CXX
WriteExampleModel = cppyy.cppdef(
    """
static bool Internal_WriteExampleModel(
  const ONX_Model& model,
  const wchar_t* filename,
  ON_TextLog& error_log
)
{
  int version = 0;

  // writes model to archive
  return model.Write( filename, version, &error_log );
}""")

model = cppyy.gbl.ONX_Model()
model.AddDefaultLayer("default", cppyy.gbl.ON_Color.RandomColor())


def write_as_model(obj, attrs=cppyy.gbl.ON_3dmObjectAttributes()):
    return model.AddModelGeometryComponent(obj, attrs)


def write_model(name) -> bool:
    return cppyy.gbl.Internal_WriteExampleModel(model, name, cppyy.gbl.ON_TextLog())




left_curve=OnBezier([[-59.6, 100.6, 32.5],
[-43.8, 116.6, 17.9],
[-4.2, 100.6, 17.9] ,
[24.9, 100.6, -32.5]])
right_curve=OnBezier([[-59.6, 47, -0.4],
[-39.5, 47, -14.3]         ,
[-4.2, 47, 17.9]           ,
[24.9, 47, 9.7]             ])

surface=OnNurbsSurface([left_curve, right_curve])

surface._proxy.Duplicate()

offset_tolerance=0.001

write_as_model(surface._proxy)
write_as_model(cppyy.gbl.ON_NurbsCurve(right_curve._proxy))
write_as_model(cppyy.gbl.ON_NurbsCurve(left_curve._proxy))
write_model("test.3dm")