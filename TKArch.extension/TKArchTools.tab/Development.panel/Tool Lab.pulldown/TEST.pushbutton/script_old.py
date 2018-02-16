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

def get_railing_system():
    # # See RevitApiDocs: BuiltInParameter Enumeration
    # param_id = DB.ElementId(DB.BuiltInParameter.RAILING_SYSTEM_HANDRAILS_TYPES_PARAM)
    # # The filter needs the ID of the parameter we are searching for:
    # # See RevitApiDocs: FilterableValueProvider Class
    # param_prov = DB.ParameterValueProvider(param_id)
    # # The filter also takes a rule evaluation
    # # See RevitApiDocs: FilterStringRuleEvaluator Look at the inheritance Heirarchy
    # # to get an idea of what options this has.
    # filter_rule = DB.FilterStringContains()
    # # This line directly translates from the C# example provided in the documentation
    # # to the python equivalent. See RevitApiDocs: ElementParameterFilter Class
    # case_sensitive = False
    # param_filter = DB.FilterStringRule(param_prov, \
    #                                         filter_rule, \
    #                                         param_name, \
    #                                         case_sensitive)
    # # Assigns our filter to the element parameter filter so it fits into the 
    # # '.WherePasses(element_filter)' method 
    # element_filter = DB.ElementParameterFilter(param_filter)

    # Collect a list of items eligible to get picked by the filter.
    # I found OST_PipeCurves from a combination of looking over the built in categories and
    options for the collected elements
                .WhereElementIsNotElementType().
                .OfClass(typeof(FamilyInstance))
    collected_elements = []
    proj_stairs_railings = []
    proj_hand_railings = []
    proj_top_railings = []
    # print("\n" + "-" * 25 + "Stairs Railings: " + "-" * 25)
    stairs_railings = DB.FilteredElementCollector(doc) \
            .OfCategory(DB.BuiltInCategory.OST_StairsRailing) \
            .WhereElementIsNotElementType() \
            .ToElements()
    for rail in stairs_railings:
        collected_elements.append(rail)
        proj_stairs_railings.append(rail)
        # print(rail.Id)

    # print("\n" + "-" * 25 + "Hand Railings: " + "-" * 25)
    hand_railings = DB.FilteredElementCollector(doc) \
            .OfCategory(DB.BuiltInCategory.OST_RailingHandRail) \
            .WhereElementIsNotElementType() \
            .ToElements()
    for rail in hand_railings:
        collected_elements.append(rail)
        proj_hand_railings.append(rail)

        # print(rail.Id)

    # print("\n" + "-" * 25 + "Top Railings: " + "-" * 25)
    top_railings = DB.FilteredElementCollector(doc) \
            .OfCategory(DB.BuiltInCategory.OST_RailingTopRail) \
            .WhereElementIsNotElementType() \
            .ToElements()
    for rail in top_railings:
        collected_elements.append(rail)
        proj_top_railings.append(rail)
        # print(rail.Id)

    # for element in collected_elements:
    #     print(str(element))
    return collected_elements, proj_stairs_railings, proj_hand_railings, proj_top_railings

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

def get_elevation_by_name(param_name):
 
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

# aud_sheets = get_sheet_by_name("aud.")

# for sheet in aud_sheets:
#     # print(sheet.Name)
    
#     parts = sheet.Name.split(".")
#     name_part = parts[1:]
#     result = [s.strip() for s in name_part]
#     result1 = result[0].split()
#     arch_sheet.aud = result1[0]
#     arch_sheet.name = (" ".join(result1[1:]))
#     # Prints the sheet name, pthonically
#     print("AUD." + arch_sheet.aud + " " + arch_sheet.name)

elevations = get_elevation_by_name("RAIL")
rail_elev_list = []
for elev in elevations:
    # params = elev.Parameters
    # for param in params:
    #     if param.Definition.Name == "Title on Sheet":
    #         print(param.AsString())
    rail_elev_list.append(elev.Id)
    # stairs_railings = DB.FilteredElementCollector(doc) \
    #         .OfCategory(DB.BuiltInCategory.OST_StairsRailing) \
    #         .WhereElementIsNotElementType() \
    #         .ToElements()
    # for railing in stairs_railings:
    #     print(railing.Id)
for line in rail_elev_list:
    print(line)