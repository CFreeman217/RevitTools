''' import clr
import sys
import collections
import Autodesk
import Autodesk.Revit.DB as DB

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

class arch_viewport:
    def __init__(self):
        return

class arch_sheet:
    def __init__(self):
        return

def get_sheet_by_name(param_name):
    # Accesses the ID associated with the built-in paramater "System Classification" 
    # See RevitApiDocs: BuiltInParameter Enumeration
    param_id = DB.ElementId(DB.BuiltInParameter.VIEWPORT_SHEET_NAME)
    # The filter needs the ID of the parameter we are searching for:
    # See RevitApiDocs: FilterableValueProvider Class
    param_prov = DB.ParameterValueProvider(param_id)
    # The filter also takes a rule evaluation
    # See RevitApiDocs: FilterStringRuleEvaluator Look at the inheritance Heirarchy
    # to get an idea of what options this has.
    filter_rule = DB.FilterStringContains()
    # This line directly translates from the C# example provided in the documentation
    # to the python equivalent. See RevitApiDocs: ElementParameterFilter Class
    case_sensitive = False
    param_filter = DB.FilterStringRule(param_prov, \
                                            filter_rule, \
                                            param_name, \
                                            case_sensitive)
    # Assigns our filter to the element parameter filter so it fits into the 
    # 'WherePasses' method
    element_filter = DB.ElementParameterFilter(param_filter)
    # Collect a list of items eligible to get picked by the filter.
    # I found OST_PipeCurves from a combination of looking over the built in categories and
    collected_elements = DB.FilteredElementCollector(doc) \
            .OfCategory(DB.BuiltInCategory.OST_Sheets) \
            .WherePasses(element_filter) \
            .ToElements()

    return collected_elements

def get_section_by_name(param_name):
    # Accesses the ID associated with the built-in paramater "System Classification" 
    # See RevitApiDocs: BuiltInParameter Enumeration
    param_id = DB.ElementId(DB.BuiltInParameter.VIEWPORT_SHEET_NAME)
    # The filter needs the ID of the parameter we are searching for:
    # See RevitApiDocs: FilterableValueProvider Class
    param_prov = DB.ParameterValueProvider(param_id)
    # The filter also takes a rule evaluation
    # See RevitApiDocs: FilterStringRuleEvaluator Look at the inheritance Heirarchy
    # to get an idea of what options this has.
    filter_rule = DB.FilterStringContains()
    # This line directly translates from the C# example provided in the documentation
    # to the python equivalent. See RevitApiDocs: ElementParameterFilter Class
    case_sensitive = False
    param_filter = DB.FilterStringRule(param_prov, \
                                            filter_rule, \
                                            param_name, \
                                            case_sensitive)
    # Assigns our filter to the element parameter filter so it fits into the 
    # 'WherePasses' method
    element_filter = DB.ElementParameterFilter(param_filter)
    # Collect a list of items eligible to get picked by the filter.
    # I found OST_PipeCurves from a combination of looking over the built in categories and
    collected_elements = DB.FilteredElementCollector(doc) \
            .OfCategory(DB.BuiltInCategory.OST_Viewports) \
            .WherePasses(element_filter) \
            .ToElements()

    return collected_elements


aud_sheets = get_sheet_by_name("aud.")
for sheet in aud_sheets:
    # print(sheet.Name)
    
    parts = sheet.Name.split(".")
    name_part = parts[1:]
    result = [s.strip() for s in name_part]
    result1 = result[0].split()
    arch_sheet.aud = result1[0]
    arch_sheet.name = (" ".join(result1[1:]))
    print("AUD." + arch_sheet.aud + " " + arch_sheet.name)
 '''
import clr
import sys

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
import Autodesk
import Autodesk.Revit.Creation as CR
import Autodesk.Revit.DB as DB

clr.AddReference("System")
from System.Collections.Generic import *

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

uiapp = __revit__.Application
uidoc = __revit__.ActiveUIDocument
# app = uiapp.Application
doc = uidoc.Document
sel = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]
ebbox = None
for item in sel:
    ebbox = doc.GetElement(item).BoundingBox(None)
if len(sel) > 1:
    sel = sel[1]

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
t = DB.Transaction(doc,"transaction")
t.Start()
doc.Create.NewViewSection(bbox)
t.Commit()