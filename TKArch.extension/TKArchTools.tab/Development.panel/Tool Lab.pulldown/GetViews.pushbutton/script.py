import clr # Adds .NET library functionality
import sys # System functions to interact with the interpreeter
import collections # Useful tools for generating and accessing groups of elements
import Autodesk 
import Autodesk.Revit.DB as DB # Allows access to the DB namespace. Lots of tools.
    # See revitapidocs.com

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# I don't think these are nessecary since this script has its own UI window setup
#   but the program works right now and I don't want to risk it.
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

# Allows access to element geometry
clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

# Gets nessecary resources for generating the user input window triggered on tool
#   click.
clr.AddReference("PresentationFramework")
from scriptutils.userinput import WPFWindow
from System.Windows import Window, Application
from System.Windows.Controls import TextBox

# Generate references for the active window and application.
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

viewport_dict = {}
viewports = DB.FilteredElementCollector(doc)\
            .OfCategory(DB.BuiltInCategory.OST_Viewports)\
            .ToElements()

for view in viewports:
    params = view.Parameters
    print(DB.BuiltInParameter.SHEET_NUMBER.toString())
    # for parameter in params:
    #     if parameter.Definition.Name == 'Sheet Number':
    #         if parameter.HasValue

def get_railtype_in_view(param_name):
    # Accesses the ID associated with the built-in paramater 
    # See RevitApiDocs: BuiltInParameter Enumeration
    param_id = DB.ElementId(DB.BuiltInParameter.SHEET_NUMBER)
    # The filter needs the ID of the parameter we are searching for:
    # See RevitApiDocs: FilterableValueProvider Class
    param_prov = DB.ParameterValueProvider(param_id)
    # The filter also takes a rule evaluation
    # See RevitApiDocs: FilterStringRuleEvaluator Look at the inheritance Heirarchy
    # to get an idea of what options this has.
    filter_rule = DB.FilterStringContains()
    # This curve directly translates from the C# example provided in the documentation
    # to the python equivalent. See RevitApiDocs: ElementParameterFilter Class
    case_sensitive = False
    # param_filter = DB.FilterStringRule(param_prov, \
    #                                         filter_rule, \
    #                                         param_name, \
    #                                         case_sensitive)
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
            .OfCategory(DB.BuiltInCategory.OST_RailingHandRail) \
            .WherePasses(element_filter) \
            .ToElements()

    return collected_elements
collector = DB.FilteredElementCollector(doc)\
            .OfCategory(DB.BuiltInCategory.OST_RailingTopRail) \
            .WhereElementIsNotElementType() \
            .ToElements()
