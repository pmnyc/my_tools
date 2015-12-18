# -*- coding: utf-8 -*-
#COPYRIGHT 2013 ESRI
#
#TRADE SECRETS: ESRI PROPRIETARY AND CONFIDENTIAL
#Unpublished material - all rights reserved under the
#Copyright Laws of the United States.
#
#For additional information, contact:
#Environmental Systems Research Institute, Inc.
#Attn: Contracts Dept
#380 New York Street
#Redlands, California, USA 92373
#
#email: contracts@esri.com
import glob
import imp
import os
import sys
import warnings

from arcpy.geoprocessing import gp
from arcpy.geoprocessing import env
from arcpy.geoprocessing._base import gptooldoc as _gptooldoc
from arcpy.toolbox import *
from arcpy.arcobjects import *
import arcpy.da
from arcgisscripting import ExecuteError, ExecuteWarning
from arcgisscripting import RasterToNumPyArray as _RasterToNumPyArray
from arcgisscripting import NumPyArrayToRaster as _NumPyArrayToRaster
import mapping
import arcpy.sa
from sa import Raster
import arcpy.utils as utils
import arcpy.time as time

# Conditional import of mobile tools
try:
    from . import toolbox
    from mobile import mobile
    toolbox.mobile = mobile
    if not hasattr(mobile, '__all__'):
        mobile.__all__ = []
    if not hasattr(toolbox, '__all__'):
        toolbox.__all__ = []
    for toolname in getattr(mobile, '__all__', []):
        toolbox.__all__.append("%s_%s" % (toolname, mobile.__alias__))
        setattr(toolbox, "%s_%s" % (toolname, mobile.__alias__), getattr(mobile, toolname))
    from toolbox import *
    del toolname
except ImportError:
    pass

# Conditional import of production tools
try:
    from . import toolbox
    from production import production
    toolbox.production = production
    if not hasattr(production, '__all__'):
        production.__all__ = []
    if not hasattr(toolbox, '__all__'):
        toolbox.__all__ = []
    for toolname in getattr(production, '__all__', []):
        toolbox.__all__.append("%s_%s" % (toolname, production.__alias__))
        setattr(toolbox, "%s_%s" % (toolname, production.__alias__), getattr(production, toolname))
    from toolbox import *
    del toolname
except ImportError:
    pass

# Conditional import of arcpad tools
try:
    from . import toolbox
    import arcpad
    toolbox.arcpad = arcpad
    if not hasattr(arcpad, '__all__'):
        arcpad.__all__ = []
    if not hasattr(toolbox, '__all__'):
        toolbox.__all__ = []
    for toolname in getattr(arcpad, '__all__', []):
        toolbox.__all__.append("%s_%s" % (toolname, arcpad.__alias__))
        setattr(toolbox, "%s_%s" % (toolname, arcpad.__alias__), getattr(arcpad, toolname))
    from toolbox import *
    del toolname
except ImportError:
    pass

# Conditional import of site-package tools
sitepackpth = [f for f in sys.path if (os.path.basename(f) == 'site-packages')][0]
for arcpy_module in glob.glob(os.path.join(sitepackpth, '*', 'esri','arcpy','*.py')):
    try:
        _arcpy_module = imp.load_source(os.path.split(arcpy_module)[1].strip('.py'), arcpy_module)
        alias = str(_arcpy_module.__alias__)
        setattr(arcpy, alias, _arcpy_module)
        if not hasattr(_arcpy_module, '__all__'):
            _arcpy_module.__all__ = []
        for toolname in getattr(_arcpy_module, '__all__',[]):
            setattr(arcpy, str("%s_%s" % (toolname, alias)), 
                                      getattr(_arcpy_module, toolname))
        del toolname, alias, _arcpy_module
    except ImportError:
        pass
del sitepackpth

def ImportToolbox(input_file, module_name=None):
    """ImportToolbox(input_file, {module_name})

       Imports the specified toolbox into ArcPy, allowing for access to the
       toolbox's associated tools.

         input_file(String):
       The geoprocessing toolbox to be added to the ArcPy site package.

         module_name{String}:
       If the toolbox does not have an alias, the module_name is required.

       When a tool is accessed through the ArcPy site package, the toolbox alias
       where the tool is contained is a required suffix (
       arcpy.<toolname>_<alias> ).  Since ArcPy depends on toolbox aliases to
       access and execute the correct tool, aliases are extremely important when
       importing custom toolboxes.  A good practice is to always define a custom
       toolbox's alias.  However, if the toolbox alias is not defined, a
       temporary alias can be set as the second parameter."""
    from toolbox_code import import_toolbox
    return import_toolbox(input_file, module_name)

# Conditional imports of any Python wrappers registered in additional products
modulename, filename, item, filepath = None, None, None, None

def import_local(filename, local_dict):
    "Loads a module into another module's local context"
    module_name = os.path.basename(os.path.splitext(filename)[0])
    dirname = os.path.abspath(os.path.dirname(filename))
    module_description = imp.find_module(module_name, [dirname])
    module_object = imp.load_module(module_name, *module_description)
    local_dict[module_name] = module_object
    attributes = getattr(module_object, '__all__',
                         (att for att in dir(module_object)
                            if not att.startswith('_')))
    alias = getattr(module_object, '__alias__', None)
    for attribute in attributes:
        attribute_name = (attribute if not alias
                          else "{}_{}".format(attribute, alias))
        if hasattr(module_object, attribute):
            local_dict[attribute_name] = getattr(module_object,
                                                 attribute)

for modulename, filename in sum([[(os.path.splitext(os.path.basename(item))[0],
                                   item)
                                        for item in
                                            glob.glob(os.path.join(filepath, "*.py"))]
                                        for filepath in
                                            arcpy.gp.getSystemToolboxesPaths()],
                                []):
    try:
        import_local(filename, locals())
    except:
        warnings.warn("Failed importing {0}".format(filename))

del modulename, filename, item, filepath

# Geoprocessor methods
def GetInstallInfo(product=None):
    """GetInstallInfo()

       The GetInstallInfo function returns a Python dictionary that contains
       information on the installation type properties."""
    return gp.getInstallInfo()

def ListInstallations():
    """ListInstallations()

       The ListInstallations function returns a Python List of the installation
       types (server, desktop, and engine)."""
    return gp.listInstallations()

def SetProgressor(type, message=None, min_range=None, max_range=None, step_value=None):
    """SetProgressor(type, {message}, {min_range}, {max_range}, {step_value})

       Establishes a progressor object which allows progress information to be
       passed to a progress dialog box. The appearance of the progress dialog
       box can be controlled by choosing either the default progressor or the
       step progressor.

         type(String):
       The progressor type (default or step).

        * default:   The progressor moves back and forth continuously.

        * step:   The progressor shows the percentage complete.

         message{String}:
       The progressor label. The default is no label.

         min_range{Integer}:
       Starting value for progressor. Default is 0.

         max_range{Integer}:
       Ending value for progressor. Default is 100.

         step_value{Integer}:
       The progressor step interval for updating the progress bar."""
    return gp.setProgressor(type, message, min_range, max_range, step_value)

def ResetProgressor():
    """ResetProgressor()

       Resets the progressor back to its initial state."""
    return gp.resetProgressor()

def SetProgressorLabel(label):
    """SetProgressorLabel(label)

       Updates the progressor dialog box label.

         label(String):
       The label to be used on the progressor dialog box."""
    return gp.setProgressorLabel(label)

def SetProgressorPosition(position=None):
    """SetProgressorPosition({position})

       Updates the status bar in the progressor dialog box.

         position{Integer}:
       Sets the position of the status bar in the progressor dialog box."""
    return gp.setProgressorPosition(position)

def ResetEnvironments():
    """ResetEnvironments()

       Resets all environment settings to their default settings."""
    return gp.resetEnvironments()

def ClearEnvironment(environment_name):
    """ClearEnvironment(environment_name)

       Resets a specific environment setting to its default.

         environment_name(String):
       The name of the environment setting that will be reset to its default
       setting."""
    return gp.clearEnvironment(environment_name)

def GetMessage(index):
    """GetMessage(index)

       Returns a geoprocessing tool message by its index position.

         index(Integer):
       The message to retrieve."""
    return gp.getMessage(index)

def GetReturnCode(index):
    """GetReturnCode(index)

       Return the message error code by index.

       If the message for the specified index is a warning or informative
       message the function will return a 0; if the message is an error the
       function will return a value other than 0.

         index(Integer):
       The specified position of the message in the returned list of messages,
       warnings, or errors."""
    return gp.getReturnCode(index)

def GetMessages(severity=None):
    """GetMessages({severity})

       Returns the geoprocessing messages from a tool by specified severity
       level..

         severity{Integer}:
       The severity level of messages to return.

        * 0:   messages returned.

        * 1:   warning messages returned.

        * 2:   error messages returned.

       Not specifying a severity will return all types of messages."""
    if severity is None:
        return gp.getMessages()
    else:
        return gp.getMessages(severity)

def AddMessage(message):
    """AddMessage(message)

       Creates a geoprocessing informative message (Severity=0) that can be
       accessed with any of the GetMessages functions.

         message(String):
       The message to add."""
    return gp.addMessage(message)

def AddIDMessage(message_type, message_ID, add_argument1=None, add_argument2=None):
    """AddIDMessage(message_type, message_ID, {add_argument1}, {add_argument2})

       Allows you to use system messages with a script tool.  A list of messages
       and IDs that can be used are provided under Understanding geoprocessing
       tool errors and warnings .

         message_type(String):
       The message type defines whether the message will be an error, warning,
       or informative. Valid message types are:

        * ERROR:   Adds an error message to the tool messages.

        * INFORMATIVE: Adds an informative message to the tool messages.

        * WARNING:   Adds a warning message to the tool messages.

         message_ID(Integer):
       The message ID allows you to reference existing messages for your
       scripting errors and warnings.

         add_argument1{Object}:
       Depending on which message ID is used, an argument may be necessary to
       complete the message. Common examples include dataset or field names.
       Datatype can be string, integer, or double.

         add_argument2{Object}:
       Depending on which message ID is used, an argument may be necessary to
       complete the message. Common examples include dataset or field names.
       Datatype can be string, integer, or double."""
    return gp.addIDMessage(message_type, message_ID, add_argument1, add_argument2)

def GetIDMessage(message_ID, default_message=None):
    """GetIDMessage(message_ID)

       Get the string of the error or warning ID message.

         message_ID(Integer):
       The geoprocessing message ID."""
    return gp.getIDMessage(message_ID, default_message)

def AddError(message):
    """AddError(message)

       Creates a geoprocessing tool error message (Severity=2) that can be
       accessed by any of the GetMessages functions.

         message(String):
       The message to add."""
    return gp.addError(message)

def AddWarning(message):
    """AddWarning(message)

       Creates a geoprocessing warning message (Severity=1) that can be accessed
       by any of the GetMessages functions.

         message(String):
       The message to add."""
    return gp.addWarning(message)

def AddReturnMessage(index):
    """AddReturnMessage(index)

       Sets the return message of a script tool as an output message by index.

         index(Integer):
       The message index."""
    return gp.addReturnMessage(index)

def SetProduct(product):
    """SetProduct(product)

       The SetProduct function defines the desktop license. SetProduct returns
       information on the license.

       The product level should be set by importing the appropriate product
       module ( arcinfo , arceditor , arcview , arcserver , arcenginegeodb , or
       arcengine ) prior to importing arcpy. The SetProduct function is a legacy
       function and cannot set the product once arcpy has been imported.

       For scripts using the arcgisscripting module, the equivalent SetProduct
       method is still supported.

         product(String):
       Product code for the product being set.

        * arcview:   ArcGIS for Desktop Basic product code

        * arceditor:   ArcGIS for Desktop Standard product code

        * arcinfo:   ArcGIS for Desktop Advanced product code

        * engine:   Engine Runtime product code

        * enginegeodb:   Engine Geodatabase Update product code

        * arcserver:   Server product code"""
    return gp.setProduct(product)

def CheckProduct(product):
    """CheckProduct(product)

       Checks to see if the requested license is available.

         product(String):
       Product code for the product being checked.

        * arcview:   ArcGIS for Desktop Basic product code

        * arceditor:   ArcGIS for Desktop Standard product code

        * arcinfo:   ArcGIS for Desktop Advanced product code

        * engine:   Engine Runtime product code

        * enginegeodb:   Engine Geodatabase Update product code

        * arcserver:   Server product code"""
    return gp.checkProduct(product)

def ProductInfo():
    """ProductInfo()

       Returns the current product license."""
    return gp.productInfo()

def CheckOutExtension(extension_code):
    """CheckOutExtension(extension_code)

       Retrieves the license from the License Manager.

       Once the extension license has been retrieved by the script, tools using
       that extension can be used. Once a script is finished with an extension's
       tools, the CheckInExtension function should be used to return the license
       to the License Manager so other applications can use it. All checked-out
       extension licenses and set product licenses are returned to the License
       Manager when a script completes.

         extension_code(String):
       Keyword for the extension product that is being checked.

        * 3D:   3D Analyst

        * Schematics:   ArcGIS Schematics

        * ArcScan:   ArcScan

        * Business:   Business Analyst

        * DataInteroperability:   Data Interoperability

        * GeoStats:   Geostatistical Analyst

        * JTX:   Workflow Manager

        * Network:   Network Analyst

        * Aeronautical:   Esri Aeronautical Solution

        * Defense:   Esri Defense Solution

        * Foundation:   Esri Production Mapping

        * Datareviewer:   ArcGIS Data Reviewer

        * Nautical:   Esri Nautical Solution

        * Nauticalb: Esri Bathymetry

        * Spatial:   Spatial Analyst

        * StreetMap:   StreetMap

        * Tracking:   Tracking   Licensing and extensions"""
    return gp.checkOutExtension(extension_code)

def CheckInExtension(extension_code):
    """CheckInExtension(extension_code)

       Returns the license to the License Manager so other applications can use
       it.

       Once the extension license has been retrieved by the script, tools using
       that extension can be used. Once a script is finished with an extension's
       tools, the CheckInExtension function should be used to return the license
       to the License Manager so other applications can use it. All checked-out
       extension licenses and set product licenses are returned to the License
       Manager when a script completes.

         extension_code(String):
       Keyword for the extension product that is being checked.

        * 3D:   3D Analyst

        * Schematics:   ArcGIS Schematics

        * ArcScan:   ArcScan

        * Business:   Business Analyst

        * DataInteroperability:   Data Interoperability

        * GeoStats:   Geostatistical Analyst

        * JTX:   Workflow Manager

        * Network:   Network Analyst

        * Aeronautical:   Esri Aeronautical Solution

        * Defense:   Esri Defense Solution

        * Foundation:   Esri Production Mapping

        * Datareviewer:   ArcGIS Data Reviewer

        * Nautical:   Esri Nautical Solution

        * Nauticalb: Esri Bathymetry

        * Spatial:   Spatial Analyst

        * StreetMap:   StreetMap

        * Tracking:   Tracking   Licensing and extensions"""
    return gp.checkInExtension(extension_code)

def CheckExtension(extension_code):
    """CheckExtension(extension_code)

       Checks to see if a license is available to be checked out for a specific
       type of extension.

       Once the extension license has been retrieved by the script, tools using
       that extension can be used. Once a script is finished with an extension's
       tools, the CheckInExtension function should be used to return the license
       to the License Manager so other applications can use it. All checked-out
       extension licenses and set product licenses are returned to the License
       Manager when a script completes.

         extension_code(String):
       Keyword for the extension product that is being checked.

        * 3D:   3D Analyst

        * Schematics:   ArcGIS Schematics

        * ArcScan:   ArcScan

        * Business:   Business Analyst

        * DataInteroperability:   Data Interoperability

        * GeoStats:   Geostatistical Analyst

        * JTX:   Workflow Manager

        * Network:   Network Analyst

        * Aeronautical:   Esri Aeronautical Solution

        * Defense:   Esri Defense Solution

        * Foundation:   Esri Production Mapping

        * Datareviewer:   ArcGIS Data Reviewer

        * Nautical:   Esri Nautical Solution

        * Nauticalb: Esri Bathymetry

        * Spatial:   Spatial Analyst

        * StreetMap:   StreetMap

        * Tracking:   Tracking   Licensing and extensions"""
    return gp.checkExtension(extension_code)

def ListSpatialReferences(wild_card=None, spatial_reference_type=None):
    """ListSpatialReferences({wild_card}, {spatial_reference_type})

       Returns a Python list of available spatial reference names for use as an
       argument to arcpy.SpatialReference .

         wild_card{String}:
       Limit the spatial references listed by a simple wildcard check. The check
       is not case sensitive.

       For example, arcpy.ListSpatialReferences("*Eckert*") would list Eckert I
       , Eckert II , and so forth.

         spatial_reference_type{String}:
       Limit the spatial references listed by type.

        * GCS:   List only Geographic Coordinate Systems.

        * PCS: List only Projected Coordinate Systems.

        * ALL:   List both Projected and Geographic Coordinate Systems. This is
        the default."""
    return gp.listSpatialReferences(wild_card, spatial_reference_type)

def ListTransformations(from_sr, to_sr, extent=None):
    """ListTransformations(from_sr, to_sr, {extent})

       Returns a list of valid transformation methods for converting data from
       one spatial reference to another.  An extent can be used to narrow the
       list of valid transformation methods for a specific geographic area.

         from_sr(SpatialReference):
       The starting geographic coordinate system. Can be specified with a
       SpatialReference object, the name of the spatial reference, or a path to
       a projection file (.prj).

         to_sr(SpatialReference):
       The final geographic coordinate system.  Can be specified with a
       SpatialReference object, the name of the spatial reference, or a path to
       a projection file (.prj).

         extent{Extent}:
       Only transformations that span the entire extent will be returned.  The
       extent needs to be specified in coordinates from the in_sr .  When
       working with data, the extent on a Describe object can be used."""
    return gp.listTransformations(from_sr, to_sr, extent)

def GetParameterAsText(index):
    """GetParameterAsText(index)

       Gets the specified parameter by its index position from the list of
       parameters.

         index(Integer):
       The numeric position of the parameter in the parameter list."""
    return gp.getParameterAsText(index)

def SetParameterAsText(index, text):
    """SetParameterAsText(index, text)

       Sets a specified parameter property by index using a string value. This
       is used when passing values from a script to a script tool. If you need
       to pass an object, such as a spatial reference to a script tool, use
       SetParameter .

         index(Integer):
       The specified parameter's index position in the parameter list.

         text(String):
       The string value that will set the specified parameter's property."""
    return gp.setParameterAsText(index, text)

def GetParameter(index):
    """GetParameter(index)

       From the parameter list, select the desired parameter by its index value.
       The parameter is returned as an object.

         index(Integer):
       Selects the specified parameter, by its index, from the parameter list."""
    return gp.getParameter(index)

def SetParameter(index, value):
    """SetParameter(index, value)

       Sets a specified parameter property by index using an object. This is
       used when passing objects from a script to a script tool. If you need to
       pass a text value to a script tool, use SetParameterAsText .

         index(Integer):
       The specified parameter's index position in the parameter list.

         value(Object):
       The object that will set the specified parameter's property."""
    return gp.setParameter(index, value)

def CopyParameter(from_param, to_param):
    """CopyParameter(to_param, from_param)

       Copies the specified parameter by index to another parameter in the
       script tool. The specified parameters must be of the same data type.

         to_param(Integer):
       The index position of the parameter to be copied.

         from_param(Integer):
       The index position of the parameter that will be copied to."""
    return gp.copyParameter(from_param, to_param)

def ListFiles(wild_card=None):
    """ListFiles({wild_card})

       Returns a list of files in the current workspace based on a query string.
       Specifying search conditions can be used to limit the results.

         wild_card{String}:
       The wild card limits the results returned. If no wild card is specified,
       all values are returned."""
    return gp.listFiles(wild_card)

def ListTools(wild_card=None):
    """ListTools({wild_card})

       Lists the geoprocessing tools, limited by name. A Python list is returned
       from the function.

         wild_card{String}:
       The wild card limits the results returned. If no wild card is specified,
       all values are returned."""
    return gp.listTools(wild_card)

def ListEnvironments(wild_card=None):
    """ListEnvironments({wild_card})

       The ListEnvironments function returns a Python list of geoprocessing
       environment names.

         wild_card{String}:
       The wild card limits the results returned. If no wild card is specified,
       all values are returned.   # A wild_card of "*workspace" will return a
       list including the
       #   workspace and scratchWorkspace environment names
       arcpy.ListEnvironments("*workspace")"""
    return gp.listEnvironments(wild_card)

def ListToolboxes(wild_card=None):
    """ListToolboxes({wild_card})

       Lists the geoprocessing toolboxes, limited by name. A Python List is
       returned from the function.

         wild_card{String}:
       The wild card limits the results returned. If no wild card is specified,
       all values are returned."""
    return gp.listToolboxes(wild_card)

def AddToolbox(input_file, module_name=None):
    """AddToolbox(input_file, {module_name})

       Imports the specified toolbox into ArcPy, allowing for access to the
       toolbox's associated tools.

        Equivalent to the ImportToolbox function.

         input_file(String):
       The geoprocessing toolbox to be added to the ArcPy site package.

         module_name{String}:
       If the toolbox does not have an alias, the module_name is required.

       When a tool is accessed through the ArcPy site package, the toolbox alias
       where the tool is contained is a required suffix (
       arcpy.<toolname>_<alias> ).  Since ArcPy depends on toolbox aliases to
       access and execute the correct tool, aliases are extremely important when
       importing custom toolboxes.  A good practice is to always define a custom
       toolbox's alias.  However, if the toolbox alias is not defined, a
       temporary alias can be set as the second parameter."""
    return ImportToolbox(input_file, module_name)

def RemoveToolbox(toolbox):
    """RemoveToolbox(toolbox)

       Removes the specified toolbox, either by specifying its path or
       referencing its alias. Removes the specified toolbox from the current
       geoprocessing session. Server toolboxes can also be removed using a
       semicolon delimiter.

         toolbox(String):
       The name of the toolbox, including either path or alias, to be removed
       from the current geoprocessing session. The name/path or alias should be
       placed in a double-quoted string.

       Server toolboxes can be removed using a semicolon delimiter.   The name,
       including path, or alias, of the toolbox to be removed from the current
       geoprocessing session. Place the name/path, or alias, string inside
       double quotes. Server toolboxes can also be removed using a semicolon
       delimiter.

         Syntax for Internet ArcGIS for Server    URL
         servername;{username};{password}    Syntax for Local ArcGIS for Server
         machinename;servername .   Syntax for Internet ArcGIS for Server
         URL;servername;{username};{password}    Syntax for Local ArcGIS for
         Server    machinename;servername"""
    return gp.removeToolbox(toolbox)

def GetSystemEnvironment(environment):
    """GetSystemEnvironment(environment)

       Gets the specified system environment variable value, such as "TEMP".

         environment(String):
       The name of the system environment variable."""
    return gp.getSystemEnvironment(environment)

def Command(command_line):
    """Command(command_line)

       Executes a geoprocessing tool as a single string.

         command_line(String):
       The double-quoted string representing a command line command that is to
       be executed."""
    return gp.command(command_line)

def Usage(tool_name):
    """Usage(tool_name)

       Returns the syntax for the specified tool or function.

         tool_name(String):
       The tool name to display the syntax."""
    return gp.usage(tool_name)

def Exists(dataset):
    """Exists(dataset)

       Determines the existence of the specified data object. Tests for the
       existence of feature classes, tables, datasets, shapefiles, workspaces,
       layers, and files in the current workspace. The function returns a
       Boolean indicating if the element exists.

         dataset(String):
       The name, path, or both of a feature class, table, dataset, layer,
       shapefile, workspace, or file to be checked for existence."""
    return gp.exists(dataset)

def RefreshCatalog(dataset):
    """RefreshCatalog(dataset)

       Forces a refresh of the Catalog window or Catalog tree .

         dataset(String):
       Data element to be refreshed."""
    return gp.refreshCatalog(dataset)

def RefreshActiveView():
    """RefreshActiveView()

       Refreshes the active view and table of contents of the current map
       document."""
    return gp.refreshActiveView()

def RefreshTOC():
    """RefreshTOC()

       Refreshes the table of contents."""
    return gp.refreshTOC()

def ListFeatureClasses(wild_card=None, feature_type=None, feature_dataset=None):
    """ListFeatureClasses({wild_card}, {feature_type}, {feature_dataset})

       Lists the feature classes in the workspace, limited by name, feature
       type, and optional feature dataset. A Python List is returned from the
       function.

         wild_card{String}:
       The wild card limits the results returned. If no wild card is specified,
       all values are returned.

         feature_type{String}:
       The feature type to limit the results returned by the wild card argument.
       Valid feature types are:

        * Annotation:   Only annotation feature classes are returned.

        * Arc:   Only arc (or line) feature classes are returned.

        * Dimension:   Only dimension feature classes are returned.

        * Edge: Only edge feature classes are returned.

        * Junction: Only junction feature classes are returned.

        * Label:   Only label feature classes are returned.

        * Line:   Only line (or arc) feature classes are returned.

        * Multipatch: Only multipatch feature classes are returned.

        * Node:   Only node feature classes are returned.

        * Point:   Only point feature classes are returned.

        * Polygon:   Only polygon feature classes are returned.

        * Polyline: Only line (or arc) feature classes are returned.

        * Region:   Only region feature classes are returned.

        * Route:   Only route feature classes are returned.

        * Tic:   Only tic feature classes are returned.

        * All:   All datasets in the workspace. This is the default value.

         feature_dataset{String}:
       Limits the feature classes returned to the feature dataset, if specified.
       If blank, only stand-alone feature classes will be returned in the
       workspace."""
    return gp.listFeatureClasses(wild_card, feature_type, feature_dataset)

def ListDatasets(wild_card=None, feature_type=None):
    """ListDatasets({wild_card}, {feature_type})

       Lists all of the datasets in a workspace. Search conditions can be
       specified for the dataset name and dataset type to limit the Python List
       that is returned.

         wild_card{String}:
       The wild card limits the results returned. If no wild card is specified,
       all values are returned.

         feature_type{String}:
       The feature type to limit the results returned by the wildcard argument.
       Valid dataset types are:

        * Coverage: Only coverages.

        * Feature: Coverage or geodatabase dataset, depending on the workspace.

        * GeometricNetwork: Only geometric network datasets.

        * Mosaic: Only mosaic datasets.

        * Network:   Only network datasets.

        * ParcelFabric: Only parcel fabric datasets.

        * Raster:   Only raster datasets.

        * RasterCatalog: Only raster catalog datasets.

        * Schematic: Only schematic datasets.

        * Terrain: Only terrain datasets.

        * Tin:   Only TIN datasets.

        * Topology: Only topology datasets.

        * All:   All datasets in the workspace. This is the default value."""
    return gp.listDatasets(wild_card, feature_type)

def ListTables(wild_card=None, table_type=None):
    """ListTables({wild_card}, {table_type})

       Lists the tables in the workspace, limited by name and table type. A
       Python List is returned from the function.

         wild_card{String}:
       The wild card limits the results returned. If no wild card is specified,
       all values are returned.

         table_type{String}:
       The table type to limit the results returned by the wild card argument.
       Valid table types are:

        * dBASE:   Only tables of type dBASE are returned.

        * INFO:   Only stand-alone INFO tables are returned.

        * ALL:   All stand-alone tables, including geodatabase tables, are
        returned. This is the default."""
    return gp.listTables(wild_card, table_type)

def ListRasters(wild_card=None, raster_type=None):
    """ListRasters({wild_card}, {raster_type})

       Returns a Python list of the rasters in the workspace, limited by name
       and raster type.

         wild_card{String}:
       The wild card limits the results returned. If no wild card is specified,
       all values are returned.

         raster_type{String}:
       The raster type to limit the results returned by the wild card argument.
       Valid raster types are:

        * BMP:   Bitmap graphic raster dataset format.

        * GIF:   Graphic Interchange Format for raster datasets.

        * IMG:   ERDAS IMAGINE raster data format.

        * JP2:   JPEG 2000 raster dataset format.

        * JPG:   Joint Photographics Experts Group raster dataset format.

        * PNG:   Portable Network Graphics raster dataset format.

        * TIFF:   Tagged Image File Format for raster datasets.

        * GRID:   GRID data format.

        * All:   All supported raster types are returned. This is the default."""
    return gp.listRasters(wild_card, raster_type)

def ListWorkspaces(wild_card=None, workspace_type=None):
    """ListWorkspaces({wild_card}, {workspace_type})

       Lists all of the workspaces within the set workspace. Search conditions
       can be specified for the workspace name and workspace type to limit the
       Python List that is returned.

         wild_card{String}:
       The wild card limits the results returned. If no wild card is specified,
       all values are returned.

         workspace_type{String}:
       The workspace type to limit the results returned by the wild card
       argument. There are six possible workspace types:

        * Access:   Only personal geodatabases will be selected.

        * Coverage:   Only coverage workspaces will be selected.

        * FileGDB:   Only file geodatabases will be selected.

        * Folder:   Only shapefile workspaces will be selected.

        * SDE:   Only ArcSDE databases will be selected.

        * All:   All workspaces will be selected. This is the default."""
    return gp.listWorkspaces(wild_card, workspace_type)

def ListVersions(sde_workspace):
    """ListVersions(sde_workspace)

       Lists the versions the connected user has permission to use. A Python
       List is returned by the function.

         sde_workspace(String):
       An ArcSDE geodatabase workspace."""
    return gp.listVersions(sde_workspace)

def ListUsers(sde_workspace):
    """ListUsers(sde_workspace)

       Returns a list of named tuples containing information for users who are
       connected to an enterprise geodatabase.

         sde_workspace(String):
       An
         enterprise geodatabase (sde connection file).

       The connection properties specified in the enterprise geodatabase must
       have administrative rights that allow the user to disconnect other
       connections."""
    return utils.listofnamedtuples(gp.listUsers(sde_workspace), 'user')

def DisconnectUser(sde_workspace, users=None):
    """DisconnectUser(sde_workspace, {users})

       Allows an administrator to disconnect users who are currently connected
       to an Enterprise geodatabase.

         sde_workspace(String):
       The Enterprise geodatabase containing the users to be disconnected.

       The connection properties specified in the Enterprise Geodatabase must
       have administrative rights that allow the user to disconnect other
       connections.

         users{Integer}:
       Specifies which users will be disconnected from the geodatabase.

        * sde_id: The ID value returned from the ListUsers function or the
        Connections tab in the Geodatabase Administration dialog. This can be
        passed to the function as an individual sde_id or a Python list
        containing multiple sde_ids.

        * ALL: Keyword specifying that all connected users should be
        disconnected.

       DisconnectUser will not disconnect the user who is executing the
       function."""
    return gp.disconnectUser(sde_workspace, users)

@_gptooldoc(None, [[["FeatureLayer", "Table", "TableView", "Dataset", "FeatureDataset"], "", "", ""]])
def ListFields(dataset, wild_card=None, field_type=None):
    """ListFields(dataset, {wild_card}, {field_type})

       Lists the fields in a feature class, shapefile, or table in a specified
       dataset. The returned list can be limited with search criteria for name
       and field type and will contain field objects.

         dataset(String):
       The specified feature class or table whose fields will be returned.

         wild_card{String}:
       The wild card limits the results returned. If no wild card is specified,
       all values are returned.

         field_type{String}:
       The specified field type to be returned. Valid field types are:

        * All:   All field types are returned. This is the default.

        * BLOB: Only field types of BLOB are returned.

        * Date:   Only field types of Date are returned.

        * Double:   Only field types of Double are returned.

        * Geometry:   Only field types of Geometry are returned.

        * GlobalID: Only field types of GlobalID are returned.

        * GUID:   Only field types of GUID are returned.

        * Integer:   Only field types of Integer are returned.

        * OID:   Only field types of OID are returned.

        * Raster:   Only field types of Raster are returned.

        * Single:   Only field types of Single are returned.

        * SmallInteger:   Only field types of SmallInteger are returned.

        * String:   Only field types of String are returned."""
    return gp.listFields(dataset, wild_card, field_type)

@_gptooldoc(None, [[["FeatureLayer", "Table", "TableView", "Dataset", "FeatureDataset"], "", "", ""]])
def ListIndexes(dataset, wild_card=None):
    """ListIndexes(dataset, {wild_card})

       Lists the indexes in a feature class, shapefile, or table in a specified
       dataset. The Python List returned can be limited with search criteria for
       index name and will contain index objects.

         dataset(String):
       The specified feature class or table whose indexes will be returned.

         wild_card{String}:
       The wild card limits the results returned. If no wild card is specified,
       all values are returned."""
    return gp.listIndexes(dataset, wild_card)

@_gptooldoc(None, [[["FeatureLayer", "Table", "TableView", "Dataset", "FeatureDataset"], "", "", ""]])
def SearchCursor(dataset, where_clause=None, spatial_reference=None, fields=None, sort_fields=None):
    """SearchCursor(dataset, {where_clause}, {spatial_reference}, {fields},
       {sort_fields})

       The SearchCursor function establishes a read-only cursor on a feature
       class or table. The SearchCursor can be used to iterate through row
       objects and extract field values. The search can optionally be limited by
       a where clause or by field, and optionally sorted.

         dataset(String):
       The feature class, shapefile, or table containing the rows to be
       searched.

         where_clause{String}:
       An optional expression that limits the rows returned in the cursor. For
       more information on WHERE clauses and SQL statements, see
       About_building_an_SQL_expression .

         spatial_reference{Object}:
       When specified, features will be projected on the fly using the
       spatial_reference provided.

         fields{String}:
       The fields to be included in the cursor. By default, all fields are
       included.

         sort_fields{String}:
       Fields used to sort the rows in the cursor. Ascending and descending
       order for each field is denoted by A and D."""
    return gp.searchCursor(dataset, where_clause, spatial_reference, fields, sort_fields)

@_gptooldoc(None, [[["FeatureLayer", "Table", "TableView", "Dataset", "FeatureDataset"], "", "", ""]])
def UpdateCursor(dataset, where_clause=None, spatial_reference=None, fields=None, sort_fields=None):
    """UpdateCursor(dataset, {where_clause}, {spatial_reference}, {fields},
       {sort_fields})

       The UpdateCursor function creates a cursor that lets you update or delete
       rows on the specified feature class, shapefile, or table. The cursor
       places a lock on the data that will remain until either the script
       completes or the update cursor object is deleted.

         dataset(String):
       The feature class, shapefile, or table containing the rows to be updated
       or deleted.

         where_clause{String}:
       An optional expression that limits the rows returned in the cursor. For
       more information on WHERE clauses and SQL statements, see
       About_building_an_SQL_expression .

         spatial_reference{Object}:
       Coordinates are specified in the spatial_reference provided and converted
       on the fly to the coordinate system  of the dataset.

         fields{String}:
       The fields to be included in the cursor. By default, all fields are
       included.

         sort_fields{String}:
       Fields used to sort the rows in the cursor. Ascending and descending
       order for each field is denoted by A and D."""
    return gp.updateCursor(dataset, where_clause, spatial_reference, fields, sort_fields)

@_gptooldoc(None, [[["FeatureLayer", "Table", "TableView", "Dataset", "FeatureDataset"], "", "", ""]])
def InsertCursor(dataset, spatial_reference=None):
    """InsertCursor(dataset, {spatial_reference})

       Inserts rows into a feature class, shapefile, or table. The InsertCursor
       returns an enumeration object that hands out row objects.

         dataset(String):
       The table, feature class, or shapefile into which rows will be inserted.

         spatial_reference{Object}:
       Coordinates are specified in the spatial_reference provided and converted
       on the fly to the coordinate system  of the dataset."""
    return gp.insertCursor(dataset, spatial_reference)

@_gptooldoc(None, [[["FeatureLayer", "Table", "TableView", "Dataset", "FeatureDataset"], "", "", ""]])
def Describe(value):
    """Describe(value)

       The Describe function returns a Describe object, with multiple
       properties, such as data type, fields, indexes, and many others. Its
       properties are dynamic, meaning that depending on what data type is
       described, different describe properties will be available for use.

       Describe properties are organized into a series of property groups. Any
       particular dataset will acquire the properties of at least one of these
       groups. For instance, if describing a geodatabase feature class, you
       could access properties from the GDB FeatureClass , FeatureClass , Table
       , and Dataset property groups. All data, regardless of the data type,
       will always acquire the generic Describe Object properties.

         value(String):
       The specified data element or geoprocessing object to describe."""
    return gp.describe(value)

def CreateObject(name, options=None):
    """CreateObject(name, {options})

       Creates geoprocessing objects. The extra arguments can be used to specify
       additional requirements for the object creation such as the number of
       columns in the ValueTable object.

         name(String):
       Name of the object to be created (ArcSDESQLExecute, Array, Extent,
       FeatureSet, Field, FieldInfo, FieldMap, FieldMappings, Geometry,
       NetCDFFileProperties, Point, RecordSet, Result, SpatialReference,
       ValueTable).

         options{Object}:
       Optional argument(s) depend on the object being created."""
    return gp.createObject(name, options)

def ValidateFieldName(name, workspace=None):
    """ValidateFieldName(name, {workspace})

       Takes a string (field name) and a workspace path and returns a valid
       field name based on name restrictions in the output geodatabase. All
       invalid characters in the input string will be replaced with an
       underscore ( _ ). The field name restrictions depend on the specific
       database used (Structured Query Language [SQL] or Oracle).

         name(String):
       The field name to be validated. If the optional workspace is not
       specified, the field name is validated against the current workspace.

         workspace{String}:
       An optional specified workspace to validate the field name against. The
       workspace can be a file system or a personal, file, or ArcSDE
       geodatabase.

       If the workspace is not specified, the field name is validated using the
       current workspace environment.  If the workspace environment has not been
       set, the field name is validated based on a folder workspace."""
    return gp.validateFieldName(name, workspace)

def ValidateTableName(name, workspace=None):
    """ValidateTableName(name, {workspace})

       Takes a table name and a workspace path and returns a valid table name
       for the workspace. An underscore "_" will replace any invalid character
       found in the table name and will honor the name restrictions for the
       workspace. The table name restrictions depend on the specific RDBMS used.

         name(String):
       The table name to be validated.

         workspace{String}:
       The optional workspace against which to validate the table name.

       If the workspace is not specified, the table name is validated using the
       current workspace environment.  If the workspace environment has not been
       set, the table name is validated based on a folder workspace."""
    return gp.validateTableName(name, workspace)

def ParseFieldName(name, workspace=None):
    """ParseFieldName(name, {workspace})

       Parses a fully qualified field name into its components (database, owner
       name, table name, and field name) depending on the workspace.
       ParseFieldName returns a string containing the parsed table name,
       containing the database, owner, table, and field names separated by
       commas. The workspace must be a personal, file, or ArcSDE geodatabase.

         name(String):
       The field name to be parsed.

         workspace{String}:
       Specifies the workspace for fully qualifying the field name. The
       workspace must be a personal, file, or ArcSDE geodatabase."""
    return gp.parseFieldName(name, workspace)

def ParseTableName(name, workspace=None):
    """ParseTableName(name, {workspace})

       Parses a table name into its components (database, owner, table)
       depending on the workspace. ParseTableName returns a string containing
       the parsed table name, with the database name, owner name, and table name
       separated by commas. This workspace must be a personal, file, or ArcSDE
       geodatabase.

         name(String):
       Specifies which table will be parsed.

         workspace{String}:
       Specifies the workspace for fully qualifying the table name. The
       workspace must be a personal, file, or ArcSDE geodatabase."""
    return gp.parseTableName(name, workspace)

def CreateScratchName(prefix=None, suffix=None, data_type=None, workspace=None):
    """CreateScratchName({prefix}, {suffix}, {data_type}, {workspace})

       Creates a unique scratch path name for the specified data type. If no
       workspace is given the current workspace is used.

         prefix{String}:
       The prefix that is added to the scratchname. By default, a prefix of xx
       is used.

         suffix{String}:
       The suffix added to the scratchname. This can be an empty double-quoted
       string.

         data_type{String}:
       The data type which will be used to create the scratchname. Valid
       datatypes are:

        * Coverage:   Only valid Coverage names are returned.

        * Dataset:   Only valid Dataset names are returned.

        * FeatureClass:   Only valid FeatureClass names are returned.

        * FeatureDataset:   Only valid FeatureDataset names are returned.

        * Folder:   Only valid Folder names are returned.

        * Geodataset:   Only valid Geodataset names are returned.

        * GeometricNetwork:   Only valid Geometric Network names are returned.

        * ArcInfoTable:   Only valid ArcInfo Table names are returned.

        * NetworkDataset:   Only valid Network Dataset names are returned.

        * RasterBand:   Only valid Raster Band names are returned.

        * RasterCatalog:   Only valid Raster Catalog names are returned.

        * RasterDataset:   Only valid Raster Dataset names are returned.

        * Shapefile:   Only valid Shapefile names are returned.

        * Terrain:   Only valid Terrain names are returned.

        * Workspace:   Only valid Workspace scratchnames are returned.

         workspace{String}:
       The workspace used to determine the scratch name to be created. If not
       specified, the current workspace is used."""
    return gp.createScratchName(prefix, suffix, data_type, workspace)

def CreateUniqueName(base_name, workspace=None):
    """CreateUniqueName(base_name, {workspace})

       Creates a unique name in the specified workspace by appending a number to
       the input name. This number is increased until the name is unique. If no
       workspace is specified, the current workspace is used.

         base_name(String):
       The base name used to create the unique name.

         workspace{String}:
       The workspace used for creation of the unique name."""
    return gp.createUniqueName(base_name, workspace)

def SaveSettings(file_name):
    """SaveSettings(file_name)

       Saves environment settings to an environment settings file (text stored
       in an Extensible Markup Language [XML] schema). See also LoadSettings on
       how to load environment settings from an XML file.

         file_name(String):
       The XML file to be created that will store the current environment
       settings."""
    return gp.saveSettings(file_name)

def LoadSettings(file_name):
    """LoadSettings(file_name)

       Loads environment settings from an environment settings file (text stored
       in an Extensible Markup Language [XML] schema). See also SaveSettings on
       how to save environment settings.

         file_name(String):
       An existing XML file that contains environment settings."""
    return gp.loadSettings(file_name)

def TestSchemaLock(dataset):
    """TestSchemaLock(dataset)

       Tests if a schema lock can be acquired for a feature class, table, or
       feature dataset. Tools that alter schema will require a schema lock to be
       placed on the input data. The Add Field tool is an example of such a
       tool. If the tool requires a schema lock and is unable to aquire one at
       the time of execution, an appropriate error message is returned. Scripts
       that use such tools should test if a schema lock can be acquired on the
       input data. The TestSchemaLock function will not actually apply a schema
       lock on the input data, but will return a Boolean.

         dataset(String):
       The input data to be tested if a schema lock can be applied."""
    return gp.testSchemaLock(dataset)

def CreateRandomValueGenerator(seed, distribution):
    """CreateRandomValueGenerator(seed, distribution)

       Creates a new random number generator.

         seed(Integer):
       Initializes the random number generator.

         distribution(String):
       The random generation algorithm.

        * ACM599:   ACM collected algorithm 599

        * MERSENNE_TWISTER:   Mersenne Twister mt19937

        * STANDARD_C:   Standard C Rand"""
    return gp.createRandomValueGenerator(seed, distribution)

def IsSynchronous(tool_name):
    """IsSynchronous(tool_name)

       Determines if a tool is running synchronous or asynchronous. When a tool
       is synchronous , the results are automatically returned, but no other
       action may be taken until the tool has completed. All non-server tools
       are synchronous. Server tools may be asynchronous , meaning that once the
       tool has been submitted to the server, other functionality can be run
       without waiting, and the results must be explicitly requested from the
       server.

         tool_name(String):
       The name of the tool to determine if it is synchronous."""
    return gp.isSynchronous(tool_name)

def GetParameterCount(tool_name):
    """GetParameterCount(tool_name)

       Returns a count of the parameter values for the specified tool. If the
       tool is contained in a custom toolbox, use ImportToolbox to access the
       custom tool.

         tool_name(String):
       The name of the tool for which the number of parameters will be returned."""
    return gp.getParameterCount(tool_name)

def GetParameterValue(tool_name, index):
    """GetParameterValue(tool_name, index)

       For a specified tool name, returns the default value of the desired
       parameter.

         tool_name(String):
       The tool name for which the parameter default value will be returned.

         index(Integer):
       Index position of the parameter in the specified tool's parameter list."""
    return gp.getParameterValue(tool_name, index)

def GetParameterInfo(tool_name=None):
    """GetParameterInfo(tool_name)

       Returns a list of parameter objects for a given tool. Commonly used in a
       script tool's ToolValidator class.

         tool_name(String):
       The tool name. Including the toolbox alias will help to resolve any
       conflicts with duplicated tool names. When the GetParameterInfo function
       is used as part of a script tool's ToolValidator class, the tool_name
       argument is optional."""
    return gp.getParameterInfo(tool_name)

def AddFieldDelimiters(datasource, field):
    """AddFieldDelimiters(datasource, field)

       Adds field delimiters to a field name to allow for use in SQL
       expressions.

         datasource(String):
       The field delimiters are based on the data source used.

         field(String):
       The field name to which delimiters will be added.  The field does not
       have to currently exist."""
    return gp.addFieldDelimiters(datasource, field)

def ListPrinterNames():
    """ListPrinterNames()

       Returns a Python list of available printers on the local computer."""
    return gp.listPrinterNames()

def GetSeverity(index):
    """GetSeverity(index)

       Gets the severity code (0, 1, 2) of the specified message by index.

         index(Integer):
       Numeric index position of the message in the stack."""
    return gp.getSeverity(index)

def GetMessageCount():
    """GetMessageCount()

       Returns a numeric count of all the returned messages from the last
       executed command."""
    return gp.messageCount

def GetMaxSeverity():
    """GetMaxSeverity()

       Gets the maximum severity returned from the last executed tool."""
    return gp.maxSeverity

def GetSeverityLevel():
    """GetSeverityLevel()

       Returns the severity level. The severity level is used to control how
       geoprocessing tools throw exceptions."""
    return gp.severityLevel

def SetSeverityLevel(severity):
    """SetSeverityLevel(severity_level)

       Used to control how geoprocessing tools throw exceptions.

         severity_level(Integer):
       The severity level

        * 0:   A tool will not throw an exception, even if the tool produces an
        error or warning.

        * 1:   If a tool produces a warning or an error, it will throw an
        exception.

        * 2:   If a tool produces an error, it will throw an exception. This is
        the default."""
    gp.severityLevel = severity
def GetArgumentCount():
    """GetArgumentCount()

       Returns the number of arguments passed to the script."""
    return gp.parameterCount
def GetLogHistory():
    """GetLogHistory()

       For
       script tools and stand-alone scripts (scripts run outside of an
       ArcGIS application),
       you can determine whether history logging is active using the
       GetLogHistory function.

       The history log file is an Extensible Markup Language (XML) file that
       contains information about each geoprocessing operation. The information
       contained in the log file is essentially the same as that found in the
       Results window."""
    return gp.logHistory
def SetLogHistory(log_history):
    """SetLogHistory(log_history)

       For
       script tools and stand-alone scripts (scripts run outside of an
       ArcGIS application),
       you can enable or disable history logging using the SetLogHistory
       function.

       The history log file is an Extensible Markup Language (XML) file that
       contains information about each geoprocessing operation. The information
       contained in the log file is essentially the same as that found in the
       Results window.

         log_history(Boolean):
       True, to enable geoprocessing logging history and  False, to disable."""
    gp.logHistory = log_history
def FromWKB(byte_array, spatial_reference=None):
    """FromWKB(byte_array)

       Create a new Geometry object from a well-known binary (WKB) string stored
       in a Python bytearray .

         byte_array(Bytearray):
       A WKB string stored in a Python bytearray ."""
    return gp.createObject("geometry", byte_array, None, spatial_reference)
def FromWKT(wkt_string, spatial_reference=None):
    """FromWKT(wkt_string, {spatial_reference})

       Create a new Geometry object from a well-known text (WKT) string.

         wkt_string(String):
       A WKT string.

         spatial_reference{SpatialReference}:
       The spatial reference of the geometry. It can be specified with either a
       SpatialReference object or string equivalent."""
    return gp.createObject("_wkt", wkt_string, spatial_reference)

def AcceptConnections(sde_workspace, accept_connections):
    """AcceptConnections(sde_workspace, accept_connections)

       Allows an administrator to enable or disable the ability of
       nonadministrative users to make connections to an enterprise geodatabase.

         sde_workspace(String):
       The Enterprise geodatabase that will have its connection property
       altered.

       The connection properties specified in the Enterprise Geodatabase must be
       the geodatabase administrator.

         accept_connections(Boolean):
       Boolean value indicating if the geodatabase will accept connections
       (True) or will not accept connections (False)."""
    return gp.acceptConnections(sde_workspace, accept_connections)

def AlterAliasName(table, alias):
    """AlterAliasName(table, alias)

       Updates the alias name for a table or feature class.

         table(String):
       Input table or feature class.

         alias(String):
       The new alias name."""
    return gp.alterAliasName(table, alias)

def LogUsageMetering(code, task_name, num_objects=0, units=0.0):
    """LogUsageMetering(code, task_name, num_objects, units)

       Updates the usage metering for this server tool."""
    return gp.logUsageMetering(code, task_name, num_objects, units)

def CreateGeocodeSDDraft(loc_path, out_sddraft, service_name, server_type='ARCGIS_SERVER', connection_file_path=None, copy_data_to_server=False, folder_name=None, summary=None, tags=None, max_result_size=500, max_batch_size=1000, suggested_batch_size=1000, supported_operations=["GEOCODE","REVERSE_GEOCODE"]):
    """CreateGeocodeSDDraft(loc_path, out_sddraft, service_name, {server_type}, {connection_file_path}, {copy_data_to_server}, {folder_name}, {summary}, {tags}, {max_result_size}, {max_batch_size}, {suggested_batch_size}, {supported_operations})
       Converts an address locator to Service Definition Draft ( .sddraft
       )  files.

         loc_path(String):
       A string that represents the catalog path to the address locator. Valid
       formats for the address locator are locator files (.loc) in a file folder
       or locators in a geodatabase.

         out_sddraft(String):
       A string that represents the path and file name for the output Service
       Definition Draft ( .sddraft ) file.

         service_name(String):
       A string that represents the name of the service. This is the name people
       will see and use to identify the service. The name can only contain
       alphanumeric characters and underscores. No spaces or special characters
       are allowed. The name cannot be more than 120 characters in length.

         server_type{String}:
       A string representing the server type.
       If a connection_file_path parameter is not supplied, then a server_type
       must be provided. If a connection_file_path parameter is supplied, then the
       server_type is taken from the connection file. In this case, you can choose
       FROM_CONNECTION_FILE or skip the parameter entirely.

        * ARCGIS_SERVER:  ArcGIS for Server server type

        * FROM_CONNECTION_FILE: Get the server_type as specified in the
       connection_file_path parameter

         connection_file_path{String}:
       A string that represents the path and file name to the ArcGIS for Server
       connection file  ( .ags ). A new connection file can be created using
       the CreateGISServerConnectionFile function

         copy_data_to_server{Boolean}:
       A Boolean that indicates whether the data referenced in the address
       locator will be copied to the server or not. The copy_data_to_server
       parameter is only used if the server_type is ARCGIS_SERVER and the
       connection_file_path isn't specified. If the connection_file_path is
       specified, then the server's registered data stores are used. For
       example, if the data in the address locator is registered with the server,
       then copy_data_to_server will always be False. Conversely, if the data in
       the address locator is not registered with the server, then
       copy_data_to_server will always be True.

         folder_name{String}:
       A string that represents a folder name to which you want to publish the
       service definition. If the folder does not currently exist, it will be
       created when the service definition is published as a service. The default
       folder is the server root level. 

         summary{String}:
       A string that represents the Item Description Summary.

       Use this parameter to override the user interface summary, or to provide
       a summary if one does not exist. 

         tags{String}:
       A string that represents the Item Description Tags.
       
       Use this parameter to override the user interface tags, or to provide
       tags if they do not exist. To specify mutiple tags, seperate each tag
       with a comma within the string.
         
         max_result_size(Integer):
       The maximum number of candidates returned by the service when geocoding a single address.
         
         max_batch_size(Integer):
       The maximum number of records to be processed in each batch job when performing batch geocoding.

         suggested_batch_size(Integer):
       The recommended number of records to pass in each batch job when performing batch geocoding.
  
         supported_operations(Integer):
       The built-in operations supported by the service. The parameter should be
       specified as a list containing one or more of the following string
       keywords:
       
       * GEOCODE: The service will allow geocoding operations.
       * REVERSE_GEOCODE: The service will allow reverse geocoding operations.
       
       For example, to specify that the service should only support geocoding
       operations and should not allow any reverse geocoding operations, the
       parameter should be specided as ["GEOCODE"]
       """
    import arcgisscripting
    return arcgisscripting._createGeocodeSDDraft(loc_path, out_sddraft, service_name, server_type, connection_file_path, copy_data_to_server, folder_name, summary, tags, max_result_size, max_batch_size, suggested_batch_size, supported_operations)


def CreateGPSDDraft(result, out_sddraft, service_name, server_type="ARCGIS_SERVER", connection_file_path="", copy_data_to_server=True, folder_name=None, summary=None, tags=None, executionType="Asynchronous", resultMapServer=False, showMessages="None", maximumRecords=1000, minInstances=1, maxInstances=2, maxUsageTime=600, maxWaitTime=60, maxIdleTime=1800):
    """CreateGPSDDraft(result, out_sddraft, service_name, server_type="ARCGIS_SERVER", connection_file_path="", copy_data_to_server=True, folder_name=None, summary=None, tags=None, executionType="Asynchronous", resultMapServer=False, showMessages="None", maximumRecords=1000, minInstances=1, maxInstances=2, maxUsageTime=600, maxWaitTime=60, maxIdleTime=1800)"""
    return gp.createGPSDDraft(result, out_sddraft, service_name, server_type, connection_file_path, copy_data_to_server, folder_name, summary, tags, executionType, resultMapServer, showMessages, maximumRecords, minInstances, maxInstances, maxUsageTime, maxWaitTime, maxIdleTime)

def CreateImageSDDraft(raster_or_mosaic_layer, out_sddraft, service_name, server_type="ARCGIS_SERVER", connection_file_path="", copy_data_to_server=False, folder_name=None, summary=None, tags=None):
    """CreateImageSDDraft(raster_or_mosaic_layer, out_sddraft, service_name, server_type="ARCGIS_SERVER", connection_file_path="", copy_data_to_server=False, folder_name=None, summary=None, tags=None)

    Create an image service SDDraft file
    """
    import arcgisscripting
    return arcgisscripting._createimageservicesddraft(raster_or_mosaic_layer, out_sddraft, service_name, server_type, connection_file_path, copy_data_to_server, folder_name, summary, tags)

def ListDataStoreItems(connection_file, datastore_type):
    """ListDataStoreItems(connection_file, datastore_type)"""
    return gp.listDataStoreItems(connection_file, datastore_type)

def ValidateDataStoreItem(connection_file, datastore_type, connection_name):
    """ValidateDataStoreItem(connection_file, datastore_type, connection_name)"""
    return gp.validateDataStoreItem(connection_file, datastore_type, connection_name)

def RemoveDataStoreItem(connection_file, datastore_type, connection_name):
    """RemoveDataStoreItem(connection_file, datastore_type, connection_name)"""
    return gp.removeDataStoreItem(connection_file, datastore_type, connection_name)

def AddDataStoreItem(connection_file, datastore_type, connection_name, server_path, client_path="", hostname=""):
    """AddDataStoreItem(connection_file, datastore_type, connection_name, server_path, {client_path}, {hostname})"""
    return gp.addDataStoreItem(connection_file, datastore_type, connection_name, server_path, client_path, hostname)

@_gptooldoc(None, [[["RasterLayer", "RasterDataset", "FormulatedRaster"], "", "", ""]])
def RasterToNumPyArray(*args, **kwargs):
    """RasterToNumPyArray(in_raster, {lower_left_corner}, {ncols}, {nrows},
       {nodata_to_value})

       Converts a raster to a NumPy array.

         in_raster(Raster):
       The input raster to convert to a NumPy array.

         lower_left_corner{Point}:
       The lower left corner within the in_raster from which to  extract the
       processing block to  convert to an array.
       The x-  and y-values are in map units.

         ncols{Integer}:
       The number of columns from the lower_left_corner in the in_raster to
       convert to the NumPy array.

         nrows{Integer}:
       The number of rows from the lower_left_corner in the in_raster to convert
       to the NumPy array.

         nodata_to_value{Variant}:
       The value to assign the in_raster NoData values in the resulting NumPy
       array. The data type depends on the type of the in_raster .

       If no value is specified, the NoData values in in_raster will be assigned
       the value associated with NoData in in_raster ."""
    return _RasterToNumPyArray(*args, **kwargs)

def NumPyArrayToRaster(*args, **kwargs):
    """NumPyArrayToRaster(in_array, {lower_left_corner}, {x_cell_size},
       {y_cell_size}, {value_to_nodata})

       Converts a NumPy array to a raster.

         in_array(NumPyArray):
       The NumPy array to convert to a raster.

         lower_left_corner{Point}:
       The lower left corner of the output raster to position the NumPy array.
       The X  and Y values are in map units.

         x_cell_size{Double}:
       The cell size in the x direction specified in map units. The input can be
       a specified cell size (type: double) or an input raster.

       When a dataset is input for the x_cell_size , the x cell size of the
       dataset is used for the x cell size for  the output raster.

       If only the x_cell_size is identified and not the y_cell_size, a square
       cell will result with the specified size.

       If neither x_cell_size or y_cell_size are specified, a default of 1.0
       will be used for both the x and y cell size.

         y_cell_size{Double}:
       The cell size in y direction specified in map units. The input can be a
       specified cell size (type: double) or an input raster.

       When a dataset is input for the y_cell_size the y cell size of the
       dataset is used for the y cell size for  the output raster.

       If only the y_cell_size is identified and not the x_cell_size a square
       cell will result with the specified size.

       If neither x_cell_size or y_cell_size are specified, a default of 1.0
       will be used for both the x and y cell size.

         value_to_nodata{Double}:
       The value in the NumPy array to assign to NoData in the output raster.

       If no value is specified for value_to_nodata , there will not be any
       NoData values in the resulting raster."""
    return _NumPyArrayToRaster(*args, **kwargs)
