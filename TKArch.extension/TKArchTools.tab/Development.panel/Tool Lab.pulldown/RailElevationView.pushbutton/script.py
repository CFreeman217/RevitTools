"""
1. User selects railings in a view.
2. Click button to draw dialog box to request the auditorium location if not set already
3. Populate the railing tag names.
4. Generate a section view that contains the highlighted railings.
5. Populate the XYZ coordinates of the start and end points from the view generated
6. Draw a dimension along the view for each edge
    - if extra text is needed for a railing type, populate it in a new parameter
        create a tag that can reference the extra railing text required, and populate the tag on the view
    - generate a parameter to store the location of each rail. Either ask for user input or populate from room location?

"""

"""

"""

import clr # Adds .NET library functionality
import sys # System functions to interact with the interpreeter
import collections # Useful tools for generating and accessing groups of elements
import Autodesk 
import Autodesk.Revit.DB as DB # Allows access to the DB namespace. Lots of tools.
    # See revitapidocs.com
# 
# Import DocumentManager and TransactionManager
# clr.AddReference("RevitServices")
# import RevitServices
# from RevitServices.Persistence import DocumentManager
# from RevitServices.Transactions import TransactionManager

# Allows access to element geometry
# clr.AddReference("ProtoGeometry")
# from Autodesk.DesignScript.Geometry import *

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

# Create a class to hold instances of each pipe section element.
class pipe_section:
    # Script runs when an instance is created
    def __init__(self):
        # We can define instance variables later as we need them
        return

# A class that holds the GUI user input data.
class inputData:
    # By defining these instance variables in the GUIgenerator class,
    # it is much easier to add buttons or functionality by just changing
    # that line in the script.
    def __init__(self):
        return

# The GUI generator.
class GUIgenerator(WPFWindow):
    # Calling the class and feeding it a window. 
    # This command generates the window popup
    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)
        self.DataContext = self

    # This function is called when the button is clicked.
    # Gathers information about the state of the gui.
    def sizeSystem_button(self, sender, e):       
        inputData.sys_length = self.TDL_textBox.Text
        inputData.press_drop_sel = self.presDrop_comboBox.SelectedValue.ToString()
        inputData.inlet_press_sel = self.inPressure_comboBox.SelectedValue.ToString()
        inputData.pressureState = self.HP_radioButton.IsChecked
        inputData.geometry = self.geo_ckbx.IsChecked
        inputData.closeAfter = self.cl_ckbx.IsChecked
        inputData.natGas = self.NG_radioButton.IsChecked
    
    # Trying to fix the error called when the x is clicked in the upper right
    # corner of the window.


# Gathers parameters and returns the dictionary, stolen from example code on 
# the apidocs website. Computationally expensive. Eliminate this.
def collect_params(param_element):
    """
    Collects parameters of the provided element.
    Args:
        param_element: Element that holds the parameters.
    Returns:
        Returns a dictionary, with parameters.
    """

    parameters = param_element.Parameters
    param_dict = collections.defaultdict(list)

    for param in parameters:
        param_dict[param.Definition.Name].append(param.StorageType.ToString().split(".")[-1])
        param_dict[param.Definition.Name].append(param.HasValue)

        param_value = None
        if param.HasValue:
            if param.StorageType.ToString() == "ElementId":
                param_value = param.AsElementId().IntegerValue
            elif param.StorageType.ToString() == "Integer":
                param_value = param.AsInteger()
            elif param.StorageType.ToString() == "Double":
                param_value = param.AsDouble()
            elif param.StorageType.ToString() == "String":
                param_value = param.AsString()
        param_dict[param.Definition.Name].append(str(param_value))

    return param_dict

def get_railing_system():
    # Accesses the ID associated with the built-in paramater "System Classification" 
    # See RevitApiDocs: BuiltInParameter Enumeration
    param_id = DB.ElementId(DB.BuiltInParameter.RAILING_SYSTEM_HANDRAILS_TYPES_PARAM)
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
    '''
    param_filter = DB.FilterStringRule(param_prov, \
                                            filter_rule, \
                                            param_name, \
                                            case_sensitive)
    '''
    # Assigns our filter to the element parameter filter so it fits into the 
    # '.WherePasses(element_filter)' method 
    '''
    element_filter = DB.ElementParameterFilter(param_filter)

    '''
    # Collect a list of items eligible to get picked by the filter.
    # I found OST_PipeCurves from a combination of looking over the built in categories and
    '''
    options for the collected elements
                .WhereElementIsNotElementType().
                .OfClass(typeof(FamilyInstance))
    '''
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


def main():
    # input_params = GUIgenerator('SectionGenerator.xaml').ShowDialog()
    selected_elids = []
    selected_elements = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]
    for element in selected_elements:
        selected_elids.append(element.Id)

    all_rails, stair_rails, hand_rails, top_rails = get_railing_system()

    all_rail_elids = []
    for rail in all_rails:
        all_rail_elids.append(rail.Id)
    filtered_all_rails = set(all_rail_elids).intersection(selected_elids)

    stair_rail_elids = []
    for rail in stair_rails:
        stair_rail_elids.append(rail.Id)
    filtered_stair_rails = set(stair_rail_elids).intersection(selected_elids)

    hand_rail_elids = []
    for rail in hand_rails:
        hand_rail_elids.append(rail.Id)
    filtered_hand_rails = set(hand_rail_elids).intersection(selected_elids)

    top_rail_elids = []
    for rail in top_rails:
        top_rail_elids.append(rail.Id)
    filtered_top_rails = set(top_rail_elids).intersection(selected_elids)

    print("\n" + "-" * 25 + "Intersecting Railings: " + "-" * 25)

    # for int_rail in filtered_top_rails:
    #     print("\n" * 2 + str(int_rail))
    #     rail_parameters = doc.GetElement(int_rail).Parameters
    #     rail_location = doc.GetElement(int_rail).LocationPoint.ToString()
    #     rail_name = doc.GetElement(int_rail).Name
    #     print("Top Rail Type")
    #     print("Rail Name = " + rail_name)
    #     print("Rail Location = " + str(rail_location))

    #     for parameter in rail_parameters:
    #         def print_param(parameter_string):
    #             if parameter.Definition.Name == parameter_string:
    #                 print(parameter_string + " = " + str(parameter.AsString()))

    #         print_param("Mark")
    #         print_param("Comments")
    #         print_param("ELEVATION")
    #         print_param("LOCATION")

    for int_rail in filtered_stair_rails:
        print("\n" * 2 + str(int_rail))
        rail_parameters = doc.GetElement(int_rail).Parameters
        rail_location = doc.GetElement(int_rail).Location
        rail_name = doc.GetElement(int_rail).Name
        print("Stair Rail Type")
        print("Rail Name = " + rail_name)
        print("Rail Curve = " + str(rail_location))
        print([x for x in dir(int_rail)])
        for parameter in rail_parameters:
            def print_param(parameter_string):
                if parameter.Definition.Name == parameter_string:
                    print(parameter_string + " = " + str(parameter.AsString()))

            print_param("Mark")
            print_param("Comments")
            print_param("ELEVATION")
            print_param("LOCATION")

    # for int_rail in filtered_hand_rails:
    #     print("\n" * 2 + str(int_rail))
    #     rail_parameters = doc.GetElement(int_rail).Parameters
    #     # rail_location = doc.GetElement(int_rail).Location.ToString()
    #     rail_name = doc.GetElement(int_rail).Name
    #     print("Hand Rail Type")
    #     print("Rail Name = " + rail_name)
    #     # print("Rail Location = " + str(rail_location))

    #     for parameter in rail_parameters:
    #         def print_param(parameter_string):
    #             if parameter.Definition.Name == parameter_string:
    #                 print(parameter_string + " = " + str(parameter.AsString()))

    #         print_param("Mark")
    #         print_param("Comments")
    #         print_param("ELEVATION")
    #         print_param("LOCATION")

    # for int_rail in filtered_all_rails:
    #     print("\n" * 2 + str(int_rail))
    #     rail_parameters = doc.GetElement(int_rail).Parameters
    #     # rail_location = doc.GetElement(int_rail).LocationCurve.ToString()
    #     rail_name = doc.GetElement(int_rail).Name
    #     print("Rail Name = " + rail_name)
    #     # print("Rail Location = " + str(rail_location))

    #     for parameter in rail_parameters:
    #         def print_param(parameter_string):
    #             if parameter.Definition.Name == parameter_string:
    #                 print(parameter_string + " = " + str(parameter.AsString()))

    #         print_param("Mark")
    #         print_param("Comments")
    #         print_param("ELEVATION")
    #         print_param("LOCATION")

    # if selection.Count > 0:

    # else:
    #     print("Please select an element")

main()