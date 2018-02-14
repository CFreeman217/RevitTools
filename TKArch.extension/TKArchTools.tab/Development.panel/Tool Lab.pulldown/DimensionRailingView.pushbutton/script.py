import collections
import clr
import sys
import math

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
import Autodesk
import Autodesk.Revit.DB as DB
import Autodesk.Revit.Creation as CR


clr.AddReference("System")
from System.Collections.Generic import *

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

clr.AddReference("PresentationFramework")
from scriptutils.userinput import WPFWindow
from System.Windows import Window, Application
from System.Windows.Controls import TextBox

app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
view = doc.ActiveView



def getRailCurve(element_dict):
    refArray = DB.ReferenceArray()
    # refArray.Append(railCurve.Reference)
    for key in element_dict:
        print("Rail Detected\nELEMENT ID No. : " + str(key) \
                + "\nElement String Representation : " + str(element_dict[key]))
        # refArray.Append(element_dict[key].GetPath().Reference())
        railCurve = element_dict[key].GetPath()
        for curve in railCurve:
            # refArray.Append(curve.Reference)
            print(curve.Reference)
    #     print(str(element_dict[key].HostRailingId))
    #     HostRail = element_dict[key].HostRailingId
    #     HostParams = doc.GetElement(HostRail).Parameters
    #     for param in HostParams:
    #         print("Host Rail PARAMETER NAME :  " + param.Definition.Name)
    #         if param.HasValue:
    #             try:
    #                 print("Value :  " + param.AsString())
    #             except:
    #                 print("Value :  " + param.ToString())
    # for path in reversed(railCurve):
    #     refArray.Append(path.Reference)
    # refArray.Append(railCurve.ReferenceArray)
        refArray.Append(DB.Reference(element_dict[key]))
    return railCurve, refArray

def getBound(valueList):
    max_value = max(valueList)
    min_value = min(valueList)
    return max_value, min_value

def createBBox(geometry_curve, referenceArray):
    tx = DB.Transaction(doc, "test")   
    tx.Start()   
    railCurve = []
    x_val = []
    y_val = []
    z_val = []
    iter = 0
    refArray1 = DB.ReferenceArray()
    refArray2 = DB.ReferenceArray()
    # refArray2.Append(DB.Reference(geometry_curve))
    # refArray1.Append(geometry_curve.Reference)
    for curve in geometry_curve:
        print(str(curve.Length) + " Ft.")
        # print(curve.ToString())
        refArray1.Append(curve.Reference)
        # refArray2.Append(DB.Reference(curve))
        # c_line = DB.Line.CreateBound(curve.GetEndPoint(0), curve.GetEndPoint(1))
        # print("CLINE REF") 
        # print(c_line.Reference)
        # railCurve.append(c_line)

        # print(curve.GetEndPoint(0))
        x_val.append(curve.GetEndPoint(0).X)
        # print("X-coordinate added : " + str(curve.GetEndPoint(0).X))
        x_val.append(curve.GetEndPoint(1).X)
        # print("X-coordinate added : " + str(curve.GetEndPoint(1).X))
        y_val.append(curve.GetEndPoint(0).Y)
        # print("Y-coordinate added : " + str(curve.GetEndPoint(0).Y))
        y_val.append(curve.GetEndPoint(1).Y)
        # print("Y-coordinate added : " + str(curve.GetEndPoint(1).Y))
        z_val.append(curve.GetEndPoint(0).Z)
        # print("Z-coordinate added : " + str(curve.GetEndPoint(0).Z))
        z_val.append(curve.GetEndPoint(1).Z)
        # print("Z-coordinate added : " + str(curve.GetEndPoint(1).Z))
        # newLine = None

        try:
            newLine = doc.Create.NewDetailCurve(view, curve)
            refArray2.Append(newLine.GeometryCurve.Reference)
            # doc.Create.NewDimension(view, newLine, referenceArray)
            # refArray.Append(curve)
            print("Detail Line Drawn")
            # doc.Create.NewDimension(view, curve, newRefArr)
        except:
            print("Rail Segment not visible in plane")
            next
        # refArray.Append(curve.Reference)
        # try:
        #     doc.Create.NewDimension(view, curve, referenceArray)
        #     print("New Dimension Created")
        # except:
        #     print("RefArrayItem Ignored")



        
       
    x_max = max(x_val)
    # print("X Max :" + str(x_max))
    # x_max_index = x_value.index(x_max)
    x_min = min(x_val)
    # print("X Min :" + str(x_min))
    y_max = max(y_val)
    # print("Y Max :" + str(y_max))
    y_min = min(y_val)
    # print("Y Min :" + str(y_min))
    z_max = max(z_val)
    # print("Z Max :" + str(z_max))
    z_min = min(z_val)
    print(str(refArray2.Size))
    iter = 0
    # for curve in geometry_curve:
    try:
        doc.Create.NewDimension(view, geometry_curve[2], refArray2)
    except:
        print("unable to generage dimension")

    # plane = doc.Create.NewReferencePlane(DB.XYZ(x_min, y_min, 0), DB.XYZ(x_max, y_max, 0), DB.XYZ(0,0,z_max), view) 
    # for curve in geometry_curve:
    #     detCurv = doc.Create.NewDetailCurve(view, curve)
    # skplane = doc.FamilyCreate.NewSketchPlane(plane)

    # Create Line Vertices:
    # lnStart = DB.XYZ(0,0,0)
    # lnEnd = DB.XYZ(10,10,0)

    # curve = app.Create.NewLine(lnStart, lnEnd, True)
    # crv = doc.FamilyCreate.NewModelCurve(curve, skplane)

    # print("Z Min :" + str(z_min))
    # w = (x_max - x_min)
    # d = (y_max - y_min)
    # h = (z_max - z_min)
    # if d < 10:
    #     d = 10
    # if w < 10:
    #     w = 10

    # maxPt = (w,h,0)
    # minPt = (-w, -h, -d)
    # bbox = doc.GetElement(geometry_curve).BoundingBoxXYZ()
    # bbox.Enabled = True
    # bbox.Max = maxPt
    # bbox.Min = minPt

    # trans = Transform.Identity

    # midPt = .5 * (bbox.Max + bbox.Min)
    # trans.Origin = midPt
    # print(str(midPt))
    # dim = DB.Dimension(doc.ActiveView,)
    tx.Commit()



def cat_by_view(category,viewId):
    elements = {}
    collected_elements = DB.FilteredElementCollector(doc, viewId)\
                            .OfCategory(category)\
                            .WhereElementIsNotElementType()\
                            .ToElements()
    for element in collected_elements:
        elements[element.Id] = element
    return elements

# def CreateDimension(instance, refNames, direction):
#     references = DB.ReferenceArray()

#     for x in refNames:
#         references.Append(doc.GetElement(instance).GetReferenceByName(x))
    
#     origin = instance.Location.Point
#     transform = instance.GetTotalTransform()
#     transform.Origin = DB.XYZ.Zero
    
#     dimensionDirection = transform.OfPoint(direction)
#     dimensionLine = DB.Line.CreateUnbound(origin, dimensionDirection)
#     doc.Create.NewDiension(doc.ActiveView, dimensionLine, references)


activeViewTopRail = cat_by_view(DB.BuiltInCategory.OST_RailingTopRail, doc.ActiveView.Id)

'''
tx = DB.Transaction(doc, "Create Dimension")
tx.Start()
for item in activeViewTopRail:
    print(activeViewTopRail[item].GetPath()[1])
    CreateDimension(item,["xLeft", "xRight"], DB.XYZ.BasisX)

    # dimen = CR.NewDimension()
    iter += 1
tx.Commit()
'''
r_curve, re_array = getRailCurve(activeViewTopRail)
createBBox(r_curve, re_array)


print("Done")
# t = DB.Transaction(doc, "DrawRailDetail")
# t.Start()

# for key in activeViewTopRail:
#     print("Top Rail Detected" + str(key))
#     print(str(key) + " is the element ID number for :" + str(activeViewTopRail[key]))
#     railCurve = activeViewTopRail[key].GetPath()
#     for curve in railCurve:
#         print(str(curve.GetEndPoint(0)))
#         print(str(curve.GetEndPoint(1)))
#         print(str(curve.GetEndPoint(0).Y))

#         try:
#             doc.Create.NewDetailCurve(doc.ActiveView, curve)
#             doc.ConvertModelToDetailCurves(doc.ActiveView, curve)
#             doc.Create.NewDimension(doc.ActiveView, curve, activeViewTopRail[key])
#             print("Line Generated!")
#         except:
#             print("Line Ignored")
#             next
# print("Done!")
    # convertModelToDetail = doc.ConvertModelToDetailCurves(doc.ActiveView, element.GetPath)
    # drawCurve = doc.Create.NewDetailCurve(doc.ActiveView, element)
# t.Commit()
# app = DocumentManager.Instance.CurrentUIApplication.Application

# uiapp = DocumentManager.Instance.CurrentUIApplication

# def get_railtype_in_view(param_name):
#     # Accesses the ID associated with the built-in paramater "System Classification" 
#     # See RevitApiDocs: BuiltInParameter Enumeration
#     param_id = DB.ElementId(DB.BuiltInParameter.RAILING_SYSTEM_HANDRAILS_TYPES_PARAM)
#     # The filter needs the ID of the parameter we are searching for:
#     # See RevitApiDocs: FilterableValueProvider Class
#     param_prov = DB.ParameterValueProvider(param_id)
#     # The filter also takes a rule evaluation
#     # See RevitApiDocs: FilterStringRuleEvaluator Look at the inheritance Heirarchy
#     # to get an idea of what options this has.
#     filter_rule = DB.FilterStringContains()
#     # This curve directly translates from the C# example provided in the documentation
#     # to the python equivalent. See RevitApiDocs: ElementParameterFilter Class
#     case_sensitive = False
#     param_filter = DB.FilterStringRule(param_prov, \
#                                             filter_rule, \
#                                             param_name, \
#                                             case_sensitive)
#     # Assigns our filter to the element parameter filter so it fits into the 
#     # 'WherePasses' method
#     element_filter = DB.ElementParameterFilter(param_filter)
#     # Collect a list of items eligible to get picked by the filter.
#     # I found OST_PipeCurves from a combination of looking over the built in categories and
#     collected_elements = DB.FilteredElementCollector(doc) \
#             .OfCategory(DB.BuiltInCategory.OST_RailingHandRail) \
#             .WherePasses(element_filter) \
#             .ToElements()

#     return collected_elements
# collector = DB.FilteredElementCollector(doc)\
#             .OfCategory(DB.BuiltInCategory.OST_RailingTopRail) \
#             .WhereElementIsNotElementType() \
#             .ToElements()

# seen_rails = get_railtype_in_view("R1 STAIRS")
# for rail in collector:
#     print(rail.Id)

# railList = []

# for rail in collector:
#     if rail.Name.Equals("R1 STAIRS"):
#         railList.append(rail)

# collection = List[DB.ElementId]([rail.Id for rail in railList])

# selection = uidoc.Selection

# selection.SetElementIds(collection)