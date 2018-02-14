import clr
import sys

clr.AddReferences("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
import Autodesk
import Autodesk.Revit.Creation as CR
import Autodesk.Revit.DB as DB

clr.AddReference("Sytem")
from System.Collections.Generic import *

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

uiapp = __revit__.Application
uidoc = __revit__.ActiveUIDocument
app = uiapp.Application
doc = uidoc.Document
sel = uidoc.Selection
e = sel.Elements

ebbox = e.BoundingBox(None)
w = (ebbox.Max.X - ebbox.Min.X)
d = (ebbox.Max.Y - ebbox.Min.Y)
h = (ebbox.Max.Z - ebbox.Min.Z)

if d < 10:
    d = 10
if w < 10:
    w = 10

# Orient to front

maxPt = XYZ(w,h,0)
minPt = XYZ(-w, -h, -d)

bbox = BoundingBoxXYZ()
bbox.Enabled = True
bbox.Max = maxPt
bbox.Min = minPt

# Set Transform

trans = Transform.Identity

# Find midpoint

midPt = XYZ((.5 * (ebbx.Max + ebbox.Min)))

# Set Origin

trans.Origin = midPt

# Determines View Direction

trans.BasisX = XYZ.BasisX
trans.BasisY = XYZ.BasisZ
trans.BasisZ = -XYZ.BasisY

bbox.Transform = trans

doc.Create.NewViewSection(bbox)