import clr # Adds .NET library functionality
import sys # System functions to interact with the interpreeter
import string
import collections # Useful tools for generating and accessing groups of elements
import Autodesk 
import Autodesk.Revit.DB as DB # Allows access to the DB namespace. Lots of tools.
    # See revitapidocs.com

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


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

viewports = DB.FilteredElementCollector(doc, doc.ActiveView.Id)\
            .OfCategory(DB.BuiltInCategory.OST_Viewports)\
            .ToElements()

# titleblocks = DB.FilteredElementCollector(doc)\
#                 .OfCategory()

def set_detail_number(view, label):
    t = DB.Transaction(doc,'set_detail')
    t.Start()
    detail_number = view.get_Parameter(DB.BuiltInParameter.VIEWPORT_DETAIL_NUMBER)
    detail_number.Set('{}'.format(label))
    t.Commit()

for view in viewports:
    try:
        label_location = view.GetLabelOutline()
        print('\nViewPort with Element ID :{}\n'.format(view.Id))
        # print('Associated ViewId : {}'.format(view.ViewId))
        # print('Associated SheetId : {}'.format(view.SheetId))
        max_x = label_location.MaximumPoint.X * 12
        min_x = label_location.MinimumPoint.X * 12
        max_y = label_location.MaximumPoint.Y * 12
        min_y = label_location.MinimumPoint.Y * 12
        left_right = lambda x : int((x+.8)/2)
        x_label = left_right(min_x)
        up_down = dict(enumerate(string.ascii_uppercase,0))
        y_label = up_down[int((min_y - 1)/2)]
        new_detail_label = '{}{}'.format(y_label,x_label)
        print('Label Lower Left Coordinates (inches) : ({} , {})'.format(min_x, min_y))
        print('New Detail Number : {}'.format(new_detail_label))
        set_detail_number(view, new_detail_label)
    except:
        print('\n~~Detail view detected that does not have a label. Ignoring this case.~~\n')
