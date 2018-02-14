import clr
import sys
import re
import collections
import Autodesk
import Autodesk.Revit.DB as DB

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

import System
from System.Collections.Generic import *

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]

elevationRegex = re.compile(r'''(
    (\w+\.)             # Aud. Label
    (\s)?               # Space
    (\d+)               # Aud. Number
    (\s)                # Space
    (\w+\s\w+)          # "RAIL ELEVATION"
    (\s.\s)?            # " - "
    (\d+)               # View Number
                            )''', re.VERBOSE | re.IGNORECASE)

'''
1. Find all elevation views.
2. look through the elevation view names for "rail" in the title.
3. in these views, find the rails
4. determine the auditorium location for each of these rails.
'''

elevation_dict = {}
elevations = DB.FilteredElementCollector(doc)\
            .OfCategory(DB.BuiltInCategory.OST_Viewports)\
            .ToElements()
for elevation in elevations:
    params = elevation.Parameters
    for param in params:
        if param.Definition.Name == "View Name":
            elevation_dict[elevation.Id.IntegerValue] = param.AsString()
 
            splitMatch = elevationRegex.findall(param.AsString())
            if splitMatch != None:     
                for match in splitMatch:
                    aud_num = match[3]
                    elev_name = match[5]
                    view_num = match[7]
                    print("Element Number: " + str(elevation.Id.IntegerValue) + " : "+ "AUD." + " " + aud_num + " " + elev_name + " - " + view_num)
                    handRails = []
                    handRail_collector = DB.FilteredElementCollector(doc, elevation.ViewId).\
                                                        OfCategory(DB.BuiltInCategory.OST_RailingHandRail).\
                                                        WhereElementIsNotElementType().\
                                                        ToElements()
                    for item in handRail_collector:
                        if item.Id not in handRails:
                            handRails.append(item.Id)
                            print("Hand Rail Detected: " + str(item.Id))
                    topRails = []
                    topRail_collector = DB.FilteredElementCollector(doc, elevation.ViewId).\
                                                        OfCategory(DB.BuiltInCategory.OST_RailingTopRail).\
                                                        WhereElementIsNotElementType().\
                                                        ToElements()
                    for item in topRail_collector:
                        if item.Id not in topRails:
                            topRails.append(item.Id)
                            print("Top Rail Detected: " + str(item.Id))
                    stairRails = []
                    stairRail_collector = DB.FilteredElementCollector(doc, elevation.ViewId).\
                                                        OfCategory(DB.BuiltInCategory.OST_StairsRailing).\
                                                        WhereElementIsNotElementType().\
                                                        ToElements()
                    for item in stairRail_collector:
                        if item.Id not in stairRails:
                            stairRails.append(item.Id)
                            print("Stair Rail Detected: " + str(item.Id))
                    regRails = []
                    regRail_collector = DB.FilteredElementCollector(doc, elevation.ViewId).\
                                                        OfCategory(DB.BuiltInCategory.OST_Railings).\
                                                        WhereElementIsNotElementType().\
                                                        ToElements()
                    for item in regRail_collector:
                        if item.Id not in regRails:
                            regRails.append(item.Id)
                            print("Regular Rail Detected: " + str(item.Id))
                    regHandRails = []
                    regHandRail_collector = DB.FilteredElementCollector(doc, elevation.ViewId).\
                                                        OfCategory(DB.BuiltInCategory.OST_RailingHandRail).\
                                                        WhereElementIsNotElementType().\
                                                        ToElements()
                    for item in regHandRail_collector:
                        if item.Id not in regHandRails:
                            regRails.append(item.Id)
                            print("Regular Rail Detected: " + str(item.Id))
                    sysRails = []
                    sysRail_collector = DB.FilteredElementCollector(doc, elevation.ViewId).\
                                                        OfCategory(DB.BuiltInCategory.OST_RailingSystemRail).\
                                                        WhereElementIsNotElementType().\
                                                        ToElements()
                    for item in sysRail_collector:
                        if item.Id not in sysRails:
                            sysRails.append(item.Id)
                            print("System Rail Detected: " + str(item.Id))
                    sysTopRails = []
                    sysTopRail_collector = DB.FilteredElementCollector(doc, elevation.ViewId).\
                                                        OfCategory(DB.BuiltInCategory.OST_RailingSystemTopRail).\
                                                        WhereElementIsNotElementType().\
                                                        ToElements()
                    for item in sysTopRail_collector:
                        if item.Id not in sysTopRails:
                            sysTopRails.append(item.Id)
                            print("System Top Rail Detected: " + str(item.Id))
                    sysHandRails = []
                    sysHandRail_collector = DB.FilteredElementCollector(doc, elevation.ViewId).\
                                                        OfCategory(DB.BuiltInCategory.OST_RailingSystemHandRail).\
                                                        WhereElementIsNotElementType().\
                                                        ToElements()
                    for item in sysHandRail_collector:
                        if item.Id not in sysHandRails:
                            sysHandRails.append(item.Id)
                            print("System Hand Rail Detected: " + str(item.Id))
                    sysSegRails = []
                    sysSegRail_collector = DB.FilteredElementCollector(doc, elevation.ViewId).\
                                                        OfCategory(DB.BuiltInCategory.OST_RailingSystemSegment).\
                                                        WhereElementIsNotElementType().\
                                                        ToElements()
                    for item in sysSegRail_collector:
                        if item.Id not in sysSegRails:
                            sysSegRails.append(item.Id)
                            print("System Segment Rail Detected: " + str(item.Id))
                    sysRailsSys = []
                    sysRailSys_collector = DB.FilteredElementCollector(doc, elevation.ViewId).\
                                                        OfCategory(DB.BuiltInCategory.OST_RailingSystem).\
                                                        WhereElementIsNotElementType().\
                                                        ToElements()
                    for item in sysRailSys_collector:
                        if item.Id not in sysRailSys:
                            sysRailsSys.append(item.Id)
                            print("System Rail System Detected: " + str(item.Id))

print("Done!")