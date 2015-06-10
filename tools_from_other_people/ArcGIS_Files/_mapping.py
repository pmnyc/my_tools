# -*- coding: utf-8 -*-
#COPYRIGHT 2012 ESRI
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
from arcpy.arcobjects import mixins
from arcpy.arcobjects._base import _BaseArcObject, passthrough_attr
from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
from arcpy.geoprocessing._base import gp_fixargs
from arcpy.utils import logcall, ArgAdaptor
import logging
import os
class constants(ArgAdaptor):
    """Represents the constants that can be passed into various ExportTo* mapping functions"""
    __args__ = {
        # For add position
        'add_position': {
            'TOP': 'top',
            'AUTO_ARRANGE': 'auto_arrange',
            'BOTTOM': 'bottom'
        },
        # For color mode
        'color_mode': {
            '24-BIT_TRUE_COLOR': 1,
            '8-BIT_PALETTE': 2,
            '8-BIT_GRAYSCALE': 3,
            '1-BIT_MONOCHROME_MASK': 4,
            '1-BIT_MONOCHROME_THRESHOLD': 5
        },
        # For colorspace
        'colorspace': {
            'RGB': 1,
            'CMYK': 2
        },
        # For connection type
        'connection_type': {
            'USE_GIS_SERVICES': 'USE_GIS_SERVICES',
            'ADMINISTER_GIS_SERVICES': 'ADMINISTER_GIS_SERVICES',
            'PUBLISH_GIS_SERVICES': 'PUBLISH_GIS_SERVICES'
        },
        # For dataset option
        'dataset_option': {
            'ALL': 0,
            'SELECTED': 1,
            'USE_RLF': 2,
            'EXTENT': 3,
            'DEFINITION_QUERY': 4
        },
        # For element type
        'element_type': {
            '': '',
            'MAPSURROUND_ELEMENT': 'MAPSURROUND_ELEMENT',
            'DATAFRAME_ELEMENT': 'DATAFRAME_ELEMENT',
            'GRAPHIC_ELEMENT': 'GRAPHIC_ELEMENT',
            'LEGEND_ELEMENT': 'LEGEND_ELEMENT',
            'PICTURE_ELEMENT': 'PICTURE_ELEMENT',
            'TEXT_ELEMENT': 'TEXT_ELEMENT'
        },
        # For encryption
        'encryption': {
            'RC4': 2,
            'AES_V1': 5,
            'AES_V2': 6
        },
        # For gif compression
        'gif_compression': {
            'NONE': 1,
            'RLE': 2,
            'LZW': 3
        },
        # For image compression
        'image_compression': {
            'NONE': 1,
            'RLE': 2,
            'LZW': 3,
            'DEFLATE': 4,
            'JPEG': 5,
            'ADAPTIVE': 6
        },
        # For image quality
        'image_quality': {
            'BEST': 1,
            'BETTER': 2,
            'NORMAL': 3,
            'FASTER': 4,
            'FASTEST': 5
        },
        # For insert position
        'insert_position': {
            'AFTER': 'after',
            'BEFORE': 'before'
        },
        # For layer property
        'layer_property': {
            'DESCRIPTION': 'description',
            'SHOWLABELS': 'showLabels',
            'TIME': 'time',
            'SYMBOLOGY': 'symbology',
            'SYMBOLOGYTYPE': 'symbologyType',
            'SERVICEPROPERTIES': 'serviceProperties',
            'VISIBLE': 'visible',
            'DEFINITIONQUERY': 'definitionQuery',
            'DATASOURCE': 'dataSource',
            'LONGNAME': 'longName',
            'MINSCALE': 'minScale',
            'DATASETNAME': 'datasetName',
            'NAME': 'name',
            'BRIGHTNESS': 'brightness',
            'MAXSCALE': 'maxScale',
            'CONTRAST': 'contrast',
            'TRANSPARENCY': 'transparency',
            'WORKSPACEPATH': 'workspacePath',
            'CREDITS': 'credits',
            'LABELCLASSES': 'labelClasses'
        },
        # For layers attributes
        'layers_attributes': {
            'NONE': 1,
            'LAYERS_ONLY': 2,
            'LAYERS_AND_ATTRIBUTES': 3
        },
        # For msd anti aliasing
        'msd_anti_aliasing': {
            'NONE': 0,
            'FASTEST': 1,
            'FAST': 2,
            'NORMAL': 3,
            'BEST': 4
        },
        # For msd text anti aliasing
        'msd_text_anti_aliasing': {
            'FORCE': 0,
            'NORMAL': 1,
            'NONE': 2
        },
        # For multiple files
        'multiple_files': {
            'PDF_SINGLE_FILE': 0,
            'PDF_MULTIPLE_FILES_PAGE_NAME': 1,
            'PDF_MULTIPLE_FILES_PAGE_INDEX': 2
        },
        # For new workspace type
        'new_workspace_type': {
            'CAD_WORKSPACE': 'CadWorkspaceFactory',
            'TIN_WORKSPACE': 'TinWorkspaceFactory',
            'SDE_WORKSPACE': 'SdeWorkspaceFactory',
            'VPF_WORKSPACE': 'VpfWorkspaceFactory',
            'ARCINFO_WORKSPACE': 'ArcInfoWorkspaceFactory',
            'OLEDB_WORKSPACE': 'OLEDBWorkspaceFactory',
            'ACCESS_WORKSPACE': 'AccessWorkspaceFactory',
            'PCCOVERAGE_WORKSPACE': 'PCCoverageWorkspaceFactory',
            'FILEGDB_WORKSPACE': 'FileGDBWorkspaceFactory',
            'SHAPEFILE_WORKSPACE': 'ShapefileWorkspaceFactory',
            'TEXT_WORKSPACE': 'TextFileWorkspaceFactory',
            'RASTER_WORKSPACE': 'RasterWorkspaceFactory',
            'EXCEL_WORKSPACE': 'ExcelWorkspaceFactory'
        },
        # For old workspace type
        'old_workspace_type': {
            'CAD_WORKSPACE': 'CadWorkspaceFactory',
            'TIN_WORKSPACE': 'TinWorkspaceFactory',
            'SDE_WORKSPACE': 'SdeWorkspaceFactory',
            'VPF_WORKSPACE': 'VpfWorkspaceFactory',
            'NONE': '',
            'ARCINFO_WORKSPACE': 'ArcInfoWorkspaceFactory',
            'OLEDB_WORKSPACE': 'OLEDBWorkspaceFactory',
            'ACCESS_WORKSPACE': 'AccessWorkspaceFactory',
            'PCCOVERAGE_WORKSPACE': 'PCCoverageWorkspaceFactory',
            'FILEGDB_WORKSPACE': 'FileGDBWorkspaceFactory',
            'SHAPEFILE_WORKSPACE': 'ShapefileWorkspaceFactory',
            'TEXT_WORKSPACE': 'TextFileWorkspaceFactory',
            'RASTER_WORKSPACE': 'RasterWorkspaceFactory',
            'EXCEL_WORKSPACE': 'ExcelWorkspaceFactory'
        },
        # For page range type
        'page_range_type': {
            'CURRENT': 'CURRENT',
            'ALL': 'ALL',
            'SELECTED': 'SELECTED',
            'RANGE': 'RANGE'
        },
        # For pdf layout
        'pdf_layout': {
            'DONT_CARE': 0,
            'SINGLE_PAGE': 1,
            'ONE_COLUMN': 2,
            'TWO_COLUMN_LEFT': 3,
            'TWO_COLUMN_RIGHT': 4,
            'TWO_PAGE_LEFT': 5,
            'TWO_PAGE_RIGHT': 6
        },
        # For pdf open view
        'pdf_open_view': {
            'VIEWER_DEFAULT': 0,
            'USE_NONE': 1,
            'USE_THUMBS': 2,
            'USE_BOOKMARKS': 3,
            'FULL_SCREEN': 4,
            'LAYERS': 5,
            'ATTACHMENT': 6
        },
        # For permissions
        'permissions': {
            'EDIT_NOTES': 32,
            'OPEN': 1,
            'SECURE': 2,
            'PRINT': 4,
            'DOC_ASSEMBLY': 1024,
            'EDIT': 8,
            'FILL_AND_SIGN': 256,
            'COPY': 16,
            'ALL_MASTER': 2104,
            'HIGH_PRINT': 2052,
            'ALL': -268435457
        },
        # For picture symbol
        'picture_symbol': {
            'RASTERIZE_BITMAP': 1,
            'RASTERIZE_PICTURE': 2,
            'VECTORIZE_BITMAP': 3
        },
        # For replaceDataSource.workspace type
        'replaceDataSource.workspace_type': {
            'CAD_WORKSPACE': 'CadWorkspaceFactory',
            'TIN_WORKSPACE': 'TinWorkspaceFactory',
            'SDE_WORKSPACE': 'SdeWorkspaceFactory',
            'VPF_WORKSPACE': 'VpfWorkspaceFactory',
            'NONE': '',
            'ARCINFO_WORKSPACE': 'ArcInfoWorkspaceFactory',
            'OLEDB_WORKSPACE': 'OLEDBWorkspaceFactory',
            'ACCESS_WORKSPACE': 'AccessWorkspaceFactory',
            'PCCOVERAGE_WORKSPACE': 'PCCoverageWorkspaceFactory',
            'FILEGDB_WORKSPACE': 'FileGDBWorkspaceFactory',
            'SHAPEFILE_WORKSPACE': 'ShapefileWorkspaceFactory',
            'TEXT_WORKSPACE': 'TextFileWorkspaceFactory',
            'RASTER_WORKSPACE': 'RasterWorkspaceFactory',
            'EXCEL_WORKSPACE': 'ExcelWorkspaceFactory'
        },
        # For rle compression
        'rle_compression': {
            'NONE': 1,
            'RLE': 2
        },
        # For save username password
        'save_username_password': {
            'DO_NOT_SAVE_USERNAME': 0,
            'SAVE_USERNAME': 1
        },
        # For server type
        'server_type': {
            'SPATIAL_DATA_SERVER': 'SPATIAL_DATA_SERVER',
            'FROM_CONNECTION_FILE': '',
            'MY_HOSTED_SERVICES': 'MY_HOSTED_SERVICES',
            'ARCGIS_SERVER': 'ARCGIS_SERVER'
        },
        # For service capabilities
        'service_capabilities': {
            'KML': 'KMLServer',
            'WCS': 'WCSServer',
            'WFS': 'WFSServer',
            'WMS': 'WMSServer',
            'MAPPING': 'MAPPING'
        },
        # For tiff compression
        'tiff_compression': {
            'NONE': 1,
            'JPEG': 2,
            'PACK_BITS': 3,
            'LZW': 4,
            'DEFLATE': 5
        },
        # For version
        'version': {
            '8.3': 83,
            '10.1': 101,
            '10.0': 10,
            '9.2': 92,
            '9.0': 90,
            '9.3': 93
        },
        # For workspace type
        'workspace_type': {
            'CAD_WORKSPACE': 'CadWorkspaceFactory',
            'TIN_WORKSPACE': 'TinWorkspaceFactory',
            'SDE_WORKSPACE': 'SdeWorkspaceFactory',
            'VPF_WORKSPACE': 'VpfWorkspaceFactory',
            'ARCINFO_WORKSPACE': 'ArcInfoWorkspaceFactory',
            'OLEDB_WORKSPACE': 'OLEDBWorkspaceFactory',
            'ACCESS_WORKSPACE': 'AccessWorkspaceFactory',
            'PCCOVERAGE_WORKSPACE': 'PCCoverageWorkspaceFactory',
            'FILEGDB_WORKSPACE': 'FileGDBWorkspaceFactory',
            'SHAPEFILE_WORKSPACE': 'ShapefileWorkspaceFactory',
            'TEXT_WORKSPACE': 'TextFileWorkspaceFactory',
            'RASTER_WORKSPACE': 'RasterWorkspaceFactory',
            'EXCEL_WORKSPACE': 'ExcelWorkspaceFactory'
        }}
class LayoutElement(mixins.LayoutElementSpecializationMixin,_BaseArcObject):
    name = passthrough_attr('name')
    type = passthrough_attr('type')
    elementPositionX = passthrough_attr('elementPositionX')
    elementWidth = passthrough_attr('elementWidth')
    elementPositionY = passthrough_attr('elementPositionY')
    elementHeight = passthrough_attr('elementHeight')
    
class BaseLayerSymbology(mixins.LayerSymbologySpecializationMixin,_BaseArcObject):
    pass
class DataDrivenPages(_BaseArcObject):
    """Provides access to methods and properties for managing the individual pages
       within a map document that has Data Driven Pages  enabled."""
    pageRow = passthrough_attr('pageRow')
    pageCount = passthrough_attr('pageCount')
    currentPageID = passthrough_attr('currentPageID')
    dataFrame = passthrough_attr('dataFrame')
    indexLayer = passthrough_attr('indexLayer')
    selectedPages = passthrough_attr('selectedPages')
    pageNameField = passthrough_attr('pageNameField')
    def refresh(self, *args):
        """DataDrivenPages.refresh()
           
           Refreshes an existing Data Driven Pages series"""
        return convertArcObjectToPythonObject(self._arc_object.refresh(*gp_fixargs((args), True)))
    
    def getPageIDFromName(self, page_name):
        """DataDrivenPages.getPageIDFromName(page_name)
           
           Returns a Data Driven Pages index value based on the name of the page
           
             page_name(String):
           A value in the index layer that corresponds to the Name field that was used to set up Data Driven Pages"""
        return convertArcObjectToPythonObject(self._arc_object.getPageIDFromName(*gp_fixargs((page_name,), True)))
    
    @constants.maskargs
    def exportToPDF(self, out_pdf, page_range_type='ALL', page_range_string='', multiple_files=0, resolution=300, image_quality='BEST', colorspace='RGB', compress_vectors=True, image_compression='DEFLATE', picture_symbol='RASTERIZE_BITMAP', convert_markers=False, embed_fonts=True, layers_attributes='LAYERS_ONLY', georef_info=True, jpeg_compression_quality=80, show_selection_symbology=False):
        """DataDrivenPages.exportToPDF(out_pdf, {page_range_type}, {page_range_string}, {multiple_files}, {resolution}, {image_quality}, {colorspace}, {compress_vectors}, {image_compression}, {picture_symbol}, {convert_markers}, {embed_fonts}, {layers_attributes}, {georef_info}, {jpeg_compression_quality}, {show_selection_symbology})
           
           Exports a specified set of pages to a multipage PDF document for a map document ( .mxd ) that has Data Driven Pages enabled
           
             out_pdf(String):
           A string that represents the path and file name for the output export file.
           
             page_range_type{String}:
           The string value that designates how the pages will be printed, similar to the Pages tab within the ArcMap Export Map dialog box for PDF documents.         
           
            * ALL:   All pages are exported.  
           
            * CURRENT:   The active page is exported.  
           
            * RANGE:   Only pages listed in the page_range_string parameter will be exported.  
           
            * SELECTED:   Selected index layer features/pages are exported.
           
             page_range_string{String}:
           A string that identifies the pages to be printed if the RANGE option in the page_range_type parameter is used (for example, 1, 3, 5-12 ).
           
             multiple_files{String}:
           An option to control how the output PDF is created.  By default, all pages are exported into a single, multipage document.  You can also specify that individual, single-page PDF documents be exported using two different options.   
           
            * PDF_MULTIPLE_FILES_PAGE_NAME: Export  single-page documents using the page name for the output file name. 
           
            * PDF_MULTIPLE_FILES_PAGE_INDEX: Export  single-page documents using the page index value for the output file name. 
           
            * PDF_SINGLE_FILE: Export a multipage document.
           
             resolution{Integer}:
           An integer that defines the resolution of the export file in dots per inch (dpi).
           
             image_quality{String}:
           A string that defines output image quality.         
           
            * BEST:  An output image quality resample ratio of 1  
           
            * BETTER:  An output image quality resample ratio of 2  
           
            * NORMAL:  An output image quality resample ratio of 3  
           
            * FASTER:  An output image quality resample ratio of 4  
           
            * FASTEST:  An output image quality resample ratio of 5
           
             colorspace{String}:
           A string that defines the color space of the export file.         
           
            * CMYK:  Cyan, magenta, yellow, and black color model  
           
            * RGB:  Red, green, and blue color model
           
             compress_vectors{Boolean}:
           A Boolean that controls compression of vector and text portions of the output file. Image compression is defined separately.
           
             image_compression{String}:
           A string that defines the compression scheme used to compress image or raster data in the output file.         
           
            * ADAPTIVE:   Automatically selects the best compression type for each image on the page.   JPEG will be used for large images with many unique colors.  DEFLATE will be used for all other images.  
           
            * JPEG:   A lossy data compression.  
           
            * DEFLATE:   A lossless data compression  
           
            * LZW:   Lempel-Ziv-Welch, a lossless data compression  
           
            * NONE:   Compression not applied  
           
            * RLE:   Run-length encoded compression
           
             picture_symbol{String}:
           A string that defines whether picture markers and picture fills will be converted to vector or rasterized on output.         
           
            * RASTERIZE_BITMAP:   Rasterize layers with bitmap markers/fills.  
           
            * RASTERIZE_PICTURE:   Rasterize layers with any picture markers/fills.  
           
            * VECTORIZE_BITMAP:   Vectorize layers with bitmap markers/fills.
           
             convert_markers{Boolean}:
           A Boolean that controls the conversion of character-based marker symbols to polygons. This allows the symbols to appear correctly if the symbol font is not available or cannot be embedded. However, setting this parameter to True disables font embedding for all character-based marker symbols, which can result in a change in their appearance.
           
             embed_fonts{Boolean}:
           A Boolean that controls the embedding of fonts in an export file. Font embedding allows text and character markers to be displayed correctly when the document is viewed on a computer that does not have the necessary fonts installed.
           
             layers_attributes{String}:
           A string that controls inclusion of PDF layer and PDF object data (attributes) in the export file.         
           
            * LAYERS_ONLY:  Export PDF layers only.  
           
            * LAYERS_AND_ATTRIBUTES:  Export PDF layers and feature attributes.  
           
            * NONE:  No setting is applied.
           
             georef_info{Boolean}:
           A Boolean that enables exporting of coordinate system information for each data frame into the output PDF file.
           
             jpeg_compression_quality{Integer}:
           A number that controls compression quality value when image_compression is set to ADAPTIVE or JPEG. The valid range is 1 to 100.    A jpeg_compression_quality of 100 provides the best quality images but creates large export files.   The recommended range is between 70 and 90.
           
             show_selection_symbology{Boolean}:
           A Boolean that controls whether the selection symbology should be displayed in the output."""
        return convertArcObjectToPythonObject(self._arc_object.exportToPDF(*gp_fixargs((out_pdf, page_range_type, page_range_string, multiple_files, resolution, image_quality, colorspace, compress_vectors, image_compression, picture_symbol, convert_markers, embed_fonts, layers_attributes, georef_info, jpeg_compression_quality, show_selection_symbology), True)))
    
    def printPages(self, printer_name=None, page_range_type='ALL', page_range_string=None, out_print_file=None, ratio=1, show_selection_symbology=False):
        """DataDrivenPages.printPages({printer_name}, {page_range_type}, {page_range_string}, {out_print_file}, {show_selection_symbology})
           
           Prints specific pages from a Data Driven Pages-enabled map document ( .mxd ) to a specified printer
           
             printer_name{String}:
           A string that represents the name of a printer on the local computer.
           
             page_range_type{String}:
           The string value that designates how the pages will be printed, similar to the Pages tab within the ArcMap Export Map dialog box for PDF documents.         
           
            * ALL:   All pages are exported.  
           
            * CURRENT:   The active page is exported.  
           
            * RANGE:   Only pages listed in the page_range_string parameter will be exported.  
           
            * SELECTED:   Selected index layer features/pages are exported.
           
             page_range_string{String}:
           A string that identifies the pages to be printed if the RANGE option in the page_range_type parameter is used (for example, 1, 3, 5-12 ).
           
             out_print_file{String}:
           A path that includes the name of an output print file. The format created is dependent on the printer. If you're using a PostScript printer, the format will be PostScript, and it is recommended that a .ps extension be provided. If you're using a Windows printer, use a .prn extension.
           
             show_selection_symbology{Boolean}:
           A Boolean that controls whether  the selection symbology should be displayed in the output."""
        return convertArcObjectToPythonObject(self._arc_object.printPages(*gp_fixargs((printer_name, page_range_type, page_range_string, out_print_file, ratio, show_selection_symbology), True)))
    
class DataFrame(mixins.LayerIterationMixin,_BaseArcObject):
    """The DataFrame object provides access to many of the data frame properties
       found within a map document ( .mxd ). A reference to the DataFrame object
       is often used as an argument for many functions to filter layers or tables
       within a specific data frame."""
    name = passthrough_attr('name')
    credits = passthrough_attr('credits')
    description = passthrough_attr('description')
    displayUnits = passthrough_attr('displayUnits')
    elementPositionX = passthrough_attr('elementPositionX')
    elementWidth = passthrough_attr('elementWidth')
    elementPositionY = passthrough_attr('elementPositionY')
    elementHeight = passthrough_attr('elementHeight')
    extent = passthrough_attr('extent')
    mapUnits = passthrough_attr('mapUnits')
    rotation = passthrough_attr('rotation')
    referenceScale = passthrough_attr('referenceScale')
    scale = passthrough_attr('scale')
    spatialReference = passthrough_attr('spatialReference')
    geographicTransformations = passthrough_attr('geographicTransformations')
    type = passthrough_attr('type')
    time = passthrough_attr('time')
    def panToExtent(self, extent):
        """DataFrame.panToExtent(extent)
           
           Pans and centers the data frame extent using a new Extent object without changing the data frame's scale
           
             extent(Extent):
           A geoprocessing Extent object"""
        return convertArcObjectToPythonObject(self._arc_object.panToExtent(*gp_fixargs((extent,), True)))
    
    def zoomToSelectedFeatures(self):
        """DataFrame.zoomToSelectedFeatures()
           
           Changes the data frame extent to match the extent of the currently selected features for all layers in a data frame"""
        return convertArcObjectToPythonObject(self._arc_object.zoomToSelectedFeatures(*gp_fixargs((), True)))
    
class DataFrameTime(_BaseArcObject):
    """The DataFrameTime object provides access to time management operations for
       time-enabled layers in a data frame."""
    currentTime = passthrough_attr('currentTime')
    startTime = passthrough_attr('startTime')
    endTime = passthrough_attr('endTime')
    timeWindowUnits = passthrough_attr('timeWindowUnits')
    timeStepInterval = passthrough_attr('timeStepInterval')
    timeWindow = passthrough_attr('timeWindow')
    def resetTimeExtent(self):
        """DataFrameTime.resetTimeExtent()
           
           Resets the time extent to the time window extent of all time-enabled layers in a data frame"""
        return convertArcObjectToPythonObject(self._arc_object.resetTimeExtent(*gp_fixargs((), True)))
    
class GraduatedColorsSymbology(BaseLayerSymbology):
    """The GraduatedColorsSymbology class provides access to different properties
       that allow you to change the appearance of a layer's graduated colors
       symbology."""
    __type_string__ = 'GRADUATED_COLORS'
    classBreakLabels = passthrough_attr('classBreakLabels')
    classBreakValues = passthrough_attr('classBreakValues')
    classBreakDescriptions = passthrough_attr('classBreakDescriptions')
    normalization = passthrough_attr('normalization')
    numClasses = passthrough_attr('numClasses')
    valueField = passthrough_attr('valueField')
    def reclassify(self):
        """GraduatedColorsSymbology.reclassify()
           
           Resets the layer's symbology to the layer's data source information and statistics."""
        return convertArcObjectToPythonObject(self._arc_object.reclassify(*gp_fixargs((), True)))
    
class GraduatedSymbolsSymbology(BaseLayerSymbology):
    """The GraduatedSymbolsSymbology class provides access to different properties
       that allow you to change the appearance of a layer's graduated symbols
       symbology."""
    __type_string__ = 'GRADUATED_SYMBOLS'
    classBreakLabels = passthrough_attr('classBreakLabels')
    classBreakValues = passthrough_attr('classBreakValues')
    classBreakDescriptions = passthrough_attr('classBreakDescriptions')
    normalization = passthrough_attr('normalization')
    numClasses = passthrough_attr('numClasses')
    valueField = passthrough_attr('valueField')
    def reclassify(self):
        """GraduatedSymbolsSymbology.reclassify()
           
           Resets the layer's symbology to the layer's data source information and statistics."""
        return convertArcObjectToPythonObject(self._arc_object.reclassify(*gp_fixargs((), True)))
    
class GraphicElement(LayoutElement):
    """The GraphicElement object provides access to properties that enables its
       repositioning on the page layout as well as methods that allow for
       duplicating and deleting existing graphic elements."""
    isGroup = passthrough_attr('isGroup')
    def clone(self, suffix=None):
        """GraphicElement.clone({suffix})
           
           Provides a mechanism to clone an existing graphic element on a page layout.
           
             suffix{String}:
           An optional string that is used to tag each newly created graphic element.  The new element will get the same element name as the parent graphic plus the suffix value plus a numeric sequencer.  For example, if the parent element name is Line and the suffix value is _copy , the newly cloned elements would be named Line_copy , Line_copy_1 , Line_copy_2 , and so on.  If a suffix is not provided, then the results would look like Line_1 , Line_2 , Line_3 , and so on."""
        return convertArcObjectToPythonObject(self._arc_object.clone(*gp_fixargs((suffix,), True)))
    
    def delete(self):
        """GraphicElement.delete()
           
           Provides a mechanism to delete an existing graphic element on a page layout."""
        return convertArcObjectToPythonObject(self._arc_object.delete(*gp_fixargs((), True)))
    
class LabelClass(_BaseArcObject):
    """Provides access to a layer's label class properties"""
    className = passthrough_attr('className')
    SQLQuery = passthrough_attr('SQLQuery')
    expression = passthrough_attr('expression')
    showClassLabels = passthrough_attr('showClassLabels')
    
class Layer(mixins.LayerIterationMixin,mixins.LayerMixin,mixins.LayerSupportsPropertyMixin,_BaseArcObject):
    """Provides access to layer properties and methods. It can either reference
       layers in a map document ( .mxd ) or layers in a layer ( .lyr ) file."""
    name = passthrough_attr('name')
    credits = passthrough_attr('credits')
    dataSource = passthrough_attr('dataSource')
    datasetName = passthrough_attr('datasetName')
    workspacePath = passthrough_attr('workspacePath')
    visible = passthrough_attr('visible')
    showLabels = passthrough_attr('showLabels')
    labelClasses = passthrough_attr('labelClasses')
    definitionQuery = passthrough_attr('definitionQuery')
    serviceProperties = passthrough_attr('serviceProperties')
    description = passthrough_attr('description')
    transparency = passthrough_attr('transparency')
    brightness = passthrough_attr('brightness')
    contrast = passthrough_attr('contrast')
    isGroupLayer = passthrough_attr('isGroupLayer')
    isFeatureLayer = passthrough_attr('isFeatureLayer')
    isRasterLayer = passthrough_attr('isRasterLayer')
    isRasterizingLayer = passthrough_attr('isRasterizingLayer')
    minScale = passthrough_attr('minScale')
    maxScale = passthrough_attr('maxScale')
    time = passthrough_attr('time')
    symbologyType = passthrough_attr('symbologyType')
    symbology = passthrough_attr('symbology')
    isNetworkAnalystLayer = passthrough_attr('isNetworkAnalystLayer')
    isServiceLayer = passthrough_attr('isServiceLayer')
    def getExtent(self, symbolized_extent=True):
        """Layer.getExtent({symbolized_extent})
           
           Returns a layer's geometric or symbolized extent.
           
             symbolized_extent{Boolean}:
           A value of True will return the layer's symbolized extent; otherwise, it will return the geometric extent.  The symbolized extent takes into account the area the symbology covers so that it does not get cut off by the data frame's boundary."""
        return convertArcObjectToPythonObject(self._arc_object.getExtent(*gp_fixargs((symbolized_extent,), True)))
    
    def getSelectedExtent(self, symbolized_extent=True):
        """Layer.getSelectedExtent({symbolized_extent})
           
           Returns a layer's geometric or symbolized extent for selected features.
           
             symbolized_extent{Boolean}:
           A value of True will return the layer's symbolized extent; otherwise, it will return the geometric extent.  The symbolized extent takes into account the area the symbology covers so that it does not get cut off by the data frame's boundary."""
        return convertArcObjectToPythonObject(self._arc_object.getSelectedExtent(*gp_fixargs((symbolized_extent,), True)))
    
    def replaceDataSource(self, workspace_path="", workspace_type="", dataset_name="", validate=True):
        """Layer.replaceDataSource(workspace_path, workspace_type, {dataset_name}, {validate})
           
           Replaces a data source for a layer in a map document ( .mxd ) or layer ( .lyr ) file.  It also provides the ability to switch workspace types (e.g., replaces a file geodatabase data source with an SDE data source).
           
             workspace_path(String):
           A string that includes the workspace path to the new data or connection file.
           
             workspace_type(String):
           A string keyword that represents the workspace type of the new data.        
           
            * ACCESS_WORKSPACE:   A personal geodatabase or Access workspace 
           
            * ARCINFO_WORKSPACE: An ArcInfo coverage workspace 
           
            * CAD_WORKSPACE: A CAD file workspace  
           
            * EXCEL_WORKSPACE:   An Excel file workspace  
           
            * FILEGDB_WORKSPACE:   A file geodatabase workspace 
           
            * NONE: Used to skip the parameter  
           
            * OLEDB_WORKSPACE:   An OLE database workspace 
           
            * PCCOVERAGE_WORKSPACE: A  PC ARC/INFO Coverage workspace 
           
            * RASTER_WORKSPACE:   A raster workspace  
           
            * SDE_WORKSPACE:   An SDE geodatabase workspace 
           
            * SHAPEFILE_WORKSPACE: A shapefile workspace  
           
            * TEXT_WORKSPACE:   A text file workspace  
           
            * TIN_WORKSPACE:   A TIN workspace  
           
            * VPF_WORKSPACE:   A VPF workspace
           
             dataset_name{String}:
           A string that represents the name of the dataset the way it appears in the new workspace (not the name of the layer in the TOC).  If dataset_name is not provided, the replaceDataSource method will attempt to replace the dataset by finding a table with a the same name as the layer's current dataset property.
           
             validate{Boolean}:
           If  set to True , a workspace will only be updated if the workspace_path value is a valid workspace.  If it is not valid, the workspace will not be replaced.   If set to False , the method will set the source to match the workspace_path , regardless of a valid match.  In this case, if a match does not exist, then the data source would be broken."""
        return convertArcObjectToPythonObject(self._arc_object.replaceDataSource(*gp_fixargs((workspace_path, workspace_type, dataset_name, validate), True)))
    
    def findAndReplaceWorkspacePath(self, find_workspace_path="", replace_workspace_path="", validate=True):
        """Layer.findAndReplaceWorkspacePath(find_workspace_path, replace_workspace_path, {validate})
           
           Finds and replaces a layer's workspace path with a new workspace path.
           
             find_workspace_path(String):
           A string that represents the workspace path or connection file you want to find.  If an empty string is passed, then all workspace paths will be replaced with the replace_workspace_path parameter depending on the value of the validate parameter.
           
             replace_workspace_path(String):
           A string that represents the workspace path or connection file you want to replace.
           
             validate{Boolean}:
           If  set to True , the workspace will only be updated if the replace_workspace_path value is a valid workspace.  If it is not valid, the workspace will not be replaced.   If set to False , the method will set the workspace to match the replace_workspace_path , regardless of a valid match.  In this case, if a match does not exist, then the layer's data source would be broken."""
        return convertArcObjectToPythonObject(self._arc_object.findAndReplaceWorkspacePath(*gp_fixargs((find_workspace_path, replace_workspace_path, validate), True)))
    
    @property
    def isBroken(self, *args):
        return not self._arc_object.valid
    
class LayerTime(_BaseArcObject):
    """The LayerTime object provides access to time management operations for
       time-enabled layers."""
    isTimeEnabled = passthrough_attr('isTimeEnabled')
    startTime = passthrough_attr('startTime')
    endTime = passthrough_attr('endTime')
    startTimeField = passthrough_attr('startTimeField')
    endTimeField = passthrough_attr('endTimeField')
    timeFormat = passthrough_attr('timeFormat')
    timeStepInterval = passthrough_attr('timeStepInterval')
    timeZone = passthrough_attr('timeZone')
    daylightSavings = passthrough_attr('daylightSavings')
    timeOffset = passthrough_attr('timeOffset')
    displayDataCumulatively = passthrough_attr('displayDataCumulatively')
    
class LegendElement(LayoutElement):
    """The LegendElement object provides access to properties and methods that
       enable its repositioning and resizing on the page layout as well as
       modifying its title and  legend items."""
    __type_string__ = 'LEGEND_ELEMENT'
    title = passthrough_attr('title')
    items = passthrough_attr('items')
    parentDataFrameName = passthrough_attr('parentDataFrameName')
    autoAdd = passthrough_attr('autoAdd')
    isOverflowing = passthrough_attr('isOverflowing')
    def adjustColumnCount(self, column_count):
        """LegendElement.adjustColumnCount(column_count)
           
           Provides a mechanism to set the number of columns in a legend.
           
             column_count(Integer):
           An integer that represents the desired number of columns."""
        return convertArcObjectToPythonObject(self._arc_object.adjustColumnCount(*gp_fixargs((column_count,), True)))
    
    def removeItem(self, legend_item_layer, index=0):
        """LegendElement.removeItem(legend_item_layer, {index})
           
           The removeItem method allows you to remove a legend item from a legend on a layout.
           
             legend_item_layer(Layer):
           A reference to a layer that is used in a legend.
           
             index{Long}:
           A single layer can be added into the same legend multiple times.  The index value provides a way to reference a specific legend item.  If you have more than one item and you want to remove all instances, then the removeItem will need to be called multiple times.  By default the first legend item for a layer is removed."""
        return convertArcObjectToPythonObject(self._arc_object.removeItem(*gp_fixargs((legend_item_layer, index), True)))
    
    def updateItem(self, legend_item_layer, legend_item_style_item=None, preserve_style_sizes=False, use_visible_extent=False, show_feature_count=False, use_ddp_extent=False, index=0):
        """LegendElement.updateItem(legend_item_layer, {legend_item_style_item}, {preserve_item_sizes}, {use_visible_extent}, {show_feature_count}, {use_ddp_extent}, {index})
           
           The updateItem method allows you to update  a number of individual properties for a legend item within a legend on a layout.
           
             legend_item_layer(Layer):
           A reference to a layer that is used in a legend.
           
             legend_item_style_item{Object}:
           A reference to a legend item style item that is returned from the ListStyleItems function.  This item must come from the style folder name Legend Items.
           
             preserve_item_sizes{Boolean}:
           A Boolean that controls whether or not the symbol sizes can change if the size of the legend is changed.  If set to True , the sizes authored in the style item will remain unchanged.
           
             use_visible_extent{Boolean}:
           A Boolean that controls if only the features in the data frame's visible extent will be displayed in the legend.
           
             show_feature_count{Boolean}:
           A Boolean that controls if feature counts will be displayed in the legend.
           
             use_ddp_extent{Boolean}:
           A Boolean that controls if only the features within the Data Driven Pages index layer feature will be displayed in the legend.  Data Driven Pages must be enabled.
           
             index{Long}:
           A single layer can be added into the same legend multiple times.  The index value provides a way to reference a specific legend item.  If you have more than one item and you want to remove all instances, then the updateItem method will need to be called multiple times.  By default the first legend item for a layer is updated."""
        return convertArcObjectToPythonObject(self._arc_object.updateItem(*gp_fixargs((legend_item_layer, legend_item_style_item, preserve_style_sizes, use_visible_extent, show_feature_count, use_ddp_extent, index), True)))
    
    def listLegendItemLayers(self):
        """LegendElement.listLegendItemLayers()
           
           Returns a list of Layer object references for every legend item in a legend."""
        return convertArcObjectToPythonObject(self._arc_object.listLegendItemLayers(*gp_fixargs((), True)))
    
class MapDocument(mixins.MapDocumentMethods,_BaseArcObject):
    """Provides access to map document ( .mxd ) properties and methods.  A
       reference to this object is essential for most map scripting operations."""
    filePath = passthrough_attr('filePath')
    title = passthrough_attr('title')
    summary = passthrough_attr('summary')
    author = passthrough_attr('author')
    description = passthrough_attr('description')
    relativePaths = passthrough_attr('relativePaths')
    dateSaved = passthrough_attr('dateSaved')
    datePrinted = passthrough_attr('datePrinted')
    dateExported = passthrough_attr('dateExported')
    activeView = passthrough_attr('activeView')
    credits = passthrough_attr('credits')
    hyperlinkBase = passthrough_attr('hyperlinkBase')
    tags = passthrough_attr('tags')
    activeDataFrame = passthrough_attr('activeDataFrame')
    def save(self):
        """MapDocument.save()
           
           Saves a map document ( .mxd )"""
        return convertArcObjectToPythonObject(self._arc_object.save(*gp_fixargs((), True)))
    
    def saveACopy(self, file_name, version=None):
        """MapDocument.saveACopy(file_name, {version})
           
           Provides an option to save a map document ( .mxd ) to a new file, and optionally, to a previous version.
           
             file_name(String):
           A string that includes the location and name of the output map document ( .mxd ).
           
             version{String}:
           A string that sets the output version number. The default value will use the current version.         
           
            * 10.1:   Version 10.1 
           
            * 10.0: Version 10.0  
           
            * 8.3:   Version 8.3  
           
            * 9.0:   Version 9.0/9.1  
           
            * 9.2:   Version 9.2  
           
            * 9.3:   Version 9.3"""
        if version:
            self._arc_object.saveACopy(file_name, version)
        else:
            self._arc_object.saveACopy(file_name)
    
    def makeThumbnail(self):
        """MapDocument.makeThumbnail()
           
           Creates a map document's ( .mxd ) thumbnail image"""
        return convertArcObjectToPythonObject(self._arc_object.makeThumbnail(*gp_fixargs((), True)))
    
    def deleteThumbnail(self):
        """MapDocument.deleteThumbnail()
           
           Deletes a map document's ( .mxd ) thumbnail image"""
        return convertArcObjectToPythonObject(self._arc_object.deleteThumbnail(*gp_fixargs((), True)))
    
    def replaceWorkspaces(self, old_workspace_path, old_workspace_type, new_workspace_path, new_workspace_type, validate=True):
        """MapDocument.replaceWorkspaces(old_workspace_path, old_workspace_type, new_workspace_path, new_workspace_type, {validate})
           
           Replaces an old workspace with a new workspace for all layers and tables in a map document ( .mxd );  also provides the ability to switch workspace types (for example, replace a file geodatabase data source with an SDE data source).
           
             old_workspace_path(String):
           A string that represents the workspace path or connection file you want to find.    If an empty string is passed, then all workspace paths will be replaced with the new_workspace_path , depending on the value of the validate parameter.
           
             old_workspace_type(String):
           A string keyword that represents the workspace type of the old data to be replaced.  If an empty string is passed, multiple workspaces can be redirected into one workspace.        
           
            * ACCESS_WORKSPACE:   A personal geodatabase or Access workspace 
           
            * ARCINFO_WORKSPACE: An ArcInfo coverage workspace 
           
            * CAD_WORKSPACE: A CAD file workspace  
           
            * EXCEL_WORKSPACE:   An Excel file workspace  
           
            * FILEGDB_WORKSPACE:   A file geodatabase workspace 
           
            * NONE: Used to skip the parameter  
           
            * OLEDB_WORKSPACE:   An OLE database workspace 
           
            * PCCOVERAGE_WORKSPACE: A  PC ARC/INFO Coverage workspace 
           
            * RASTER_WORKSPACE:   A raster workspace  
           
            * SDE_WORKSPACE:   An SDE geodatabase workspace 
           
            * SHAPEFILE_WORKSPACE: A shapefile workspace  
           
            * TEXT_WORKSPACE:   A text file workspace  
           
            * TIN_WORKSPACE:   A TIN workspace  
           
            * VPF_WORKSPACE:   A VPF workspace
           
             new_workspace_path(String):
           A string that represents the new workspace path or connection file.
           
             new_workspace_type(String):
           A string keyword that represents the workspace type  that will replace the old_workspace_type .        
           
            * ACCESS_WORKSPACE:   A personal geodatabase or Access workspace 
           
            * ARCINFO_WORKSPACE: An ArcInfo coverage workspace 
           
            * CAD_WORKSPACE: A CAD file workspace  
           
            * EXCEL_WORKSPACE:   An Excel file workspace  
           
            * FILEGDB_WORKSPACE:   A file geodatabase workspace  
           
            * OLEDB_WORKSPACE:   An OLE database workspace 
           
            * PCCOVERAGE_WORKSPACE: A  PC ARC/INFO Coverage workspace 
           
            * RASTER_WORKSPACE:   A raster workspace  
           
            * SDE_WORKSPACE:   An SDE geodatabase workspace 
           
            * SHAPEFILE_WORKSPACE: A shapefile workspace  
           
            * TEXT_WORKSPACE:   A text file workspace  
           
            * TIN_WORKSPACE:   A TIN workspace  
           
            * VPF_WORKSPACE:   A VPF workspace
           
             validate{Boolean}:
           If  set to True , a workspace will only be updated if the new_workspace_path value is a valid workspace.  If it is not valid, the workspace will not be replaced.   If set to False , the method will set all workspaces to match the new_workspace_path , regardless of a valid match.  In this case, if a match does not exist, then the data sources would be broken."""
        return convertArcObjectToPythonObject(self._arc_object.replaceWorkspaces(*gp_fixargs((old_workspace_path, old_workspace_type, new_workspace_path, new_workspace_type, validate), True)))
    
    def findAndReplaceWorkspacePaths(self, find_workspace_path="", replace_workspace_path="", validate=True):
        """MapDocument.findAndReplaceWorkspacePaths(find_workspace_path, replace_workspace_path, {validate})
           
           Finds old workspace paths and replaces them with new paths for all layers and tables in a map document ( .mxd )
           
             find_workspace_path(String):
           A string that represents the workspace path or connection file you want to find.  If an empty string is passed, then all workspace paths will be replaced with the replace_workspace_path, depending on the value of the validate parameter.
           
             replace_workspace_path(String):
           A string that represents the workspace path or connection file you want to use to replace.
           
             validate{Boolean}:
           If  set to True , a workspace will only be updated if the replace_workspace_path value is a valid workspace.  If it is not valid, the workspace will not be replaced.   If set to False , the method will set all workspaces to match the replace_workspace_path , regardless of a valid match.  In this case, if a match does not exist, then the layer and table's data sources would be broken."""
        return convertArcObjectToPythonObject(self._arc_object.findAndReplaceWorkspacePaths(*gp_fixargs((find_workspace_path, replace_workspace_path, validate), True)))
    
class MapSurround(_BaseArcObject):
    name = passthrough_attr('name')
    position = passthrough_attr('position')
    def setPosition(self, x, y):
        return convertArcObjectToPythonObject(self._arc_object.setPosition(*gp_fixargs((x, y), True)))
    
    def setDimension(self, height, width):
        return convertArcObjectToPythonObject(self._arc_object.setDimension(*gp_fixargs((height, width), True)))
    
class MapSurroundElement(LayoutElement):
    __type_string__ = 'MAPSURROUND_ELEMENT'
    parentDataFrameName = passthrough_attr('parentDataFrameName')
    
class PDFDocument(_BaseArcObject):
    """Allows manipulation of PDF documents, including facilities for merging
       pages, deleting pages, setting document open behavior, adding file
       attachments, and creating or changing document security settings."""
    pageCount = passthrough_attr('pageCount')
    def appendPages(self, pdf_path, password_for_pdf=None):
        """PDFDocument.appendPages(pdf_path, {input_pdf_password})
           
           Appends one PDF document to the end of another
           
             pdf_path(String):
           A string that includes the location and name of the input PDF document to be appended
           
             input_pdf_password{String}:
           A string that defines the master password to a protected file"""
        return convertArcObjectToPythonObject(self._arc_object.appendPages(*gp_fixargs((pdf_path, password_for_pdf), True)))
    
    def insertPages(self, pdf_path, after_page=1, password_for_pdf=None):
        """PDFDocument.insertPages(pdf_path, {before_page_number}, {input_pdf_password})
           
           Allows inserting the contents of one PDF document at the beginning or in between the pages of another  PDFDocument
           
             pdf_path(String):
           A string that includes the location and name of the input PDF document to be inserted.
           
             before_page_number{String}:
           An integer that defines a page number in the currently referenced PDFDocument before which the new page(s) will be inserted.  For example, if the before_page_value is 1, the inserted page will be inserted before all pages.
           
             input_pdf_password{String}:
           A string that defines the master password to a protected file."""
        return convertArcObjectToPythonObject(self._arc_object.insertPages(*gp_fixargs((pdf_path, after_page, password_for_pdf), True)))
    
    def deletePages(self, page_range):
        """PDFDocument.deletePages(page_range)
           
           Provides the ability to delete one or multiple pages within an existing PDF document.
           
             page_range(String):
           A string that defines the page or pages to be deleted.  Delete a single page by passing in a single value as a string (for example, "3" ). Multiple pages can be deleted using a comma between each value (for example, "3, 5, 7" ).  Ranges can also be applied (for example, "1, 3, 5-12" )."""
        return convertArcObjectToPythonObject(self._arc_object.deletePages(*gp_fixargs((page_range,), True)))
    
    def saveAndClose(self, *args):
        """PDFDocument.saveAndClose()
           
           Saves any changes made to the currently referenced PDFDocument"""
        return convertArcObjectToPythonObject(self._arc_object.saveAndClose(*gp_fixargs((args), True)))
    
    @constants.maskargs
    def updateDocProperties(self, pdf_title=None, pdf_author=None, pdf_subject=None, pdf_keywords=None, pdf_open_view=2, pdf_layout=1):
        """PDFDocument.updateDocProperties({pdf_title}, {pdf_author}, {pdf_subject}, {pdf_keywords}, {pdf_open_view}, {pdf_layout})
           
           Allows updating of the PDF document metadata and can also set the certain behaviors that will trigger when the document is opened in Adobe Reader or Adobe Acrobat, such as the initial view mode and the page thumbnails view
           
             pdf_title{String}:
           A string defining the document title, a PDF metadata property.
           
             pdf_author{String}:
           A string defining the document author, a PDF metadata property.
           
             pdf_subject{String}:
           A string defining the document subject, a PDF metadata property.
           
             pdf_keywords{String}:
           A string defining the document keywords, a PDF metadata property.
           
             pdf_open_view{String}:
           A string or number that will define the behavior to trigger when the PDF file is viewed. The default value is USETHUMBS, which will show the Adobe Reader Pages panel automatically when the PDF is opened.         
           
            * VIEWER_DEFAULT:   Uses the application user preference when opening the file  
           
            * USE_NONE:   Displays the document only; does not show other panels  
           
            * USE_THUMBS:   Displays the document plus the Pages panel  
           
            * USE_BOOKMARKS:   Displays the document plus the Bookmarks panel  
           
            * FULL_SCREEN:   Displays the document  in full-screen viewing mode  
           
            * LAYERS:   Displays the document plus the layers panel  
           
            * ATTACHMENT:   Displays the document plus the attachment panel
           
             pdf_layout{String}:
           A string or number that will define the initial view mode to trigger when the PDF file is viewed.         
           
            * DONT_CARE:   Uses the application user preference when opening the file  
           
            * SINGLE_PAGE:   Uses single-page mode  
           
            * ONE_COLUMN:   Uses one-column continuous mode  
           
            * TWO_COLUMN_LEFT:   Uses two-column continuous mode with first page on left  
           
            * TWO_COLUMN_RIGHT:   Uses two-column continuous mode with first page on right  
           
            * TWO_PAGE_LEFT:   Uses two-page mode left  
           
            * TWO_PAGE_RIGHT:   Uses two-page mode right"""
        return convertArcObjectToPythonObject(self._arc_object.updateDocProperties(*gp_fixargs((pdf_title, pdf_author, pdf_subject, pdf_keywords, pdf_open_view, pdf_layout), True)))
    
    @constants.maskargs
    def updateDocSecurity(self, new_master_password, new_user_password='', encryption=2, permissions=-268435457):
        """PDFDocument.updateDocSecurity(new_master_password, {new_user_password}, {encryption}, {permissions})
           
           Provides the mechanism that sets password, encryption, and security restrictions on PDF files.
           
             new_master_password(String):
           A string that defines the master document password. This password is required for appending and inserting pages into a secured PDF.
           
             new_user_password{String}:
           A string that defines the user password needed to open the PDF document for viewing.
           
             encryption{String}:
           A string  that defines the encryption technique used on the PDF.    
           
            * "AES_V1": Uses 128-bit AES encryption (Acrobat 7.0 compatible) 
           
            * "AES_V2": Uses 256-bit AES encryption (Acrobat 9.0 compatible) 
           
            * "RC4": Uses 128-bit RC4 encryption (Acrobat 5.0 compatible)
           
             permissions{String}:
           A string that defines the capabilities restricted by the document security settings. The permissions argument can accept a list of strings describing all the options to be restricted. The document restrictions can be viewed in Adobe Acrobat in the Document Properties Document Restrictions Summary page.         
           
            * "ALL":   Grants all permissions 
           
            * "ALL_MASTER": Grants permissions for COPY, EDIT, EDIT_NOTES, and HIGH_PRINT 
           
            * "COPY": Grants permission to copy information from the document to the clipboard 
           
            * "DOC_ASSEMBLY": Grants permission to perform page insert, delete, and rotate, and allows creation of bookmarks and thumbnails  
           
            * "EDIT":   Grants permission to edit the document in ways other than adding or modifying text notes  
           
            * "EDIT_NOTES":   Grants permission to add, modify, and delete text notes  
           
            * "FILL_AND_SIGN":   Grants permission to fill in or sign existing form or signature fields  
           
            * "HIGH_PRINT":   Grants permission for high-quality printing 
           
            * "OPEN": Grants permission to open or decrypt the document 
           
            * "PRINT": Grants permission to print the document 
           
            * "SECURE": Grants permission  to change the document's security settings"""
        return convertArcObjectToPythonObject(self._arc_object.updateDocSecurity(*gp_fixargs((new_master_password, new_user_password, encryption, permissions), True)))
    
    def attachFile(self, filepath, description=None):
        """PDFDocument.attachFile(file_path, {description})
           
           Attaches files to existing PDF documents  (Attachments are then accessible to users when the PDF file is opened in a PDF viewer application.)
           
             file_path(String):
           A string that includes the location and name of the file to be attached to the PDF document.
           
             description{String}:
           An optional string to be used as a description for the attachment.  The user will see this string when viewing the attachment in a PDF viewer application."""
        return convertArcObjectToPythonObject(self._arc_object.attachFile(*gp_fixargs((filepath, description), True)))
    
class PageLayout(mixins.ImageFileExportMixin,_BaseArcObject):
    orientation = passthrough_attr('orientation')
    units = passthrough_attr('units')
    width = passthrough_attr('width')
    height = passthrough_attr('height')
    dataFrames = passthrough_attr('dataFrames')
    elements = passthrough_attr('elements')
    currentPageName = passthrough_attr('currentPageName')
    printer = passthrough_attr('printer')
    dataDrivenPages = passthrough_attr('dataDrivenPages')
    isDDPEnabled = passthrough_attr('isDDPEnabled')
    def exportToVector(self, *args):
        return convertArcObjectToPythonObject(self._arc_object.exportToVector(*gp_fixargs((args), True)))
    
    def exportToRaster(self, *args):
        return convertArcObjectToPythonObject(self._arc_object.exportToRaster(*gp_fixargs((args), True)))
    
    def createDataFrame(self, *args):
        return convertArcObjectToPythonObject(self._arc_object.createDataFrame(*gp_fixargs((args), True)))
    
    def createTextElement(self, *args):
        return convertArcObjectToPythonObject(self._arc_object.createTextElement(*gp_fixargs((args), True)))
    
    def copyElement(self, *args):
        return convertArcObjectToPythonObject(self._arc_object.copyElement(*gp_fixargs((args), True)))
    
    def printMap(self, printer_name=None, filename=None, ratio=1):
        return convertArcObjectToPythonObject(self._arc_object.printMap(*gp_fixargs((printer_name, filename, ratio), True)))
    
class PictureElement(LayoutElement):
    """Provides access to picture properties that enable the repositioning of a
       picture on the page layout as well as getting and setting its data source."""
    __type_string__ = 'PICTURE_ELEMENT'
    sourceImage = passthrough_attr('sourceImage')
    
class RasterClassifiedSymbology(BaseLayerSymbology,mixins.RasterClassifiedExclusionMixin):
    """The RasterClassifiedSymbology class provides access to different properties
       that allow you to change the appearance of a layer's raster classified
       symbology."""
    __type_string__ = 'RASTER_CLASSIFIED'
    classBreakDescriptions = passthrough_attr('classBreakDescriptions')
    classBreakLabels = passthrough_attr('classBreakLabels')
    classBreakValues = passthrough_attr('classBreakValues')
    normalization = passthrough_attr('normalization')
    numClasses = passthrough_attr('numClasses')
    valueField = passthrough_attr('valueField')
    def reclassify(self):
        """RasterClassifiedSymbology.reclassify()
           
           Resets the layer's symbology to the layer's data source information and statistics."""
        return convertArcObjectToPythonObject(self._arc_object.reclassify(*gp_fixargs((), True)))
    
class StyleGallery(_BaseArcObject):
    classes = passthrough_attr('classes')
    def getItems(self, *args):
        return convertArcObjectToPythonObject(self._arc_object.getItems(*gp_fixargs((args), True)))
    
class StyleItem(_BaseArcObject):
    """Provides access to StyleItem class properties."""
    itemName = passthrough_attr('itemName')
    itemCategory = passthrough_attr('itemCategory')
    styleFolderName = passthrough_attr('styleFolderName')
    
class TableView(mixins.TableViewMixin,_BaseArcObject):
    """Provides access to basic table properties."""
    name = passthrough_attr('name')
    dataSource = passthrough_attr('dataSource')
    workspacePath = passthrough_attr('workspacePath')
    datasetName = passthrough_attr('datasetName')
    definitionQuery = passthrough_attr('definitionQuery')
    def replaceDataSource(self, workspace_path="", workspace_type="", dataset_name="", validate=True):
        """TableView.replaceDataSource(workspace_path, workspace_type, {dataset_name}, {validate})
           
           Replaces a table's data source in a map document ( .mxd ); also provides the ability to switch workspace types (for example, replace a file geodatabase workspace with an SDE workspace).
           
             workspace_path(String):
           A string that includes the workspace path to the new data or connection file.
           
             workspace_type(String):
           A string keyword that represents the workspace type of the new data.        
           
            * ACCESS_WORKSPACE:   A personal geodatabase or Access workspace 
           
            * ARCINFO_WORKSPACE: An ArcInfo coverage workspace 
           
            * CAD_WORKSPACE: A CAD file workspace  
           
            * EXCEL_WORKSPACE:   An Excel file workspace  
           
            * FILEGDB_WORKSPACE:   A file geodatabase workspace 
           
            * NONE: Used to skip the parameter  
           
            * OLEDB_WORKSPACE:   An OLE database workspace 
           
            * PCCOVERAGE_WORKSPACE: A  PC ARC/INFO Coverage workspace 
           
            * RASTER_WORKSPACE:   A raster workspace  
           
            * SDE_WORKSPACE:   An SDE geodatabase workspace 
           
            * SHAPEFILE_WORKSPACE: A shapefile workspace  
           
            * TEXT_WORKSPACE:   A text file workspace  
           
            * TIN_WORKSPACE:   A TIN workspace  
           
            * VPF_WORKSPACE:   A VPF workspace
           
             dataset_name{String}:
           A string that represents the name of the table the way it appears in the new workspace (not the name of the table in the table of contents).  If dataset_name is not provided, the replaceDataSource method will attempt to replace the dataset by finding a table with a the same name as the layer's current dataset property.
           
             validate{Boolean}:
           If  set to True , a workspace will only be updated if the workspace_path value is a valid workspace.  If it is not valid, the workspace will not be replaced.   If set to False , the method will set the workspace to match the workspace_path , regardless of a valid match.  In this case, if a match does not exist, then the data source would be broken."""
        return convertArcObjectToPythonObject(self._arc_object.replaceDataSource(*gp_fixargs((workspace_path, workspace_type, dataset_name, validate), True)))
    
    def findAndReplaceWorkspacePath(self, find_workspace_path="", replace_workspace_path="", validate=True):
        """TableView.findAndReplaceWorkspacePath(find_workspace_path, replace_workspace_path, {validate})
           
           Replaces a table's workspace with a new workspace path
           
             find_workspace_path(String):
           A string that represents the workspace path or connection file you want to find.  If an empty string is passed, then all workspace paths will be replaced with the replace_workspace_path parameter depending on the value of the validate parameter.
           
             replace_workspace_path(String):
           A string that represents the workspace path or connection file you want to use to replace.
           
             validate{Boolean}:
           If  set to True , the workspace will only be updated if the replace_workspace_path value is a valid workspace.  If it is not valid, the workspace will not be replaced.   If set to False , the method will set the workspace to match the replace_workspace_path , regardless of a valid match.  In this case, if a match does not exist, then the table's data source would be broken."""
        return convertArcObjectToPythonObject(self._arc_object.findAndReplaceWorkspacePath(*gp_fixargs((find_workspace_path, replace_workspace_path, validate), True)))
    
    @property
    def isBroken(self, *args):
        return not self._arc_object.valid
    
class TextElement(_BaseArcObject):
    """The TextElement object provides access to properties that enable its
       repositioning on the page layout as well as modifying the text string and
       font size."""
    name = passthrough_attr('name')
    text = passthrough_attr('text')
    type = passthrough_attr('type')
    elementPositionX = passthrough_attr('elementPositionX')
    elementWidth = passthrough_attr('elementWidth')
    elementPositionY = passthrough_attr('elementPositionY')
    elementHeight = passthrough_attr('elementHeight')
    angle = passthrough_attr('angle')
    fontSize = passthrough_attr('fontSize')
    def clone(self, suffix=None):
        """TextElement.clone({suffix})
           
           Provides a mechanism to clone an existing graphic text on a page layout.
           
             suffix{String}:
           An optional string that is used to tag each newly created text element.  The new element will get the same element name as the parent text element plus the suffix value plus a numeric sequencer.  For example, if the parent element name is FieldLabel and the suffix value is _copy , the newly cloned elements would be named FieldLabel_copy , FieldLabel_copy_1 , FieldLabel_copy_2 , and so on.  If a suffix is not provided, then the results would look like FieldLabel_1 , FieldLabel_2 , FieldLabel_3 , and so on."""
        return convertArcObjectToPythonObject(self._arc_object.clone(*gp_fixargs((suffix,), True)))
    
    def delete(self):
        """TextElement.delete()
           
           Provides a mechanism to delete an existing text element on a page layout."""
        return convertArcObjectToPythonObject(self._arc_object.delete(*gp_fixargs((), True)))
    
class TimeUnits(object):
    unknown = 'unknown'
    milliseconds = 'milliseconds'
    seconds = 'seconds'
    minutes = 'minutes'
    hours = 'hours'
    days = 'days'
    weeks = 'weeks'
    months = 'months'
    years = 'years'
    decades = 'decades'
    centuries = 'centuries'
    
class UniqueValuesSymbology(BaseLayerSymbology):
    """The UniqueValuesSymbology class provides access to different properties
       that allow you to change the appearance of a layer's unique value
       symbology."""
    __type_string__ = 'UNIQUE_VALUES'
    classLabels = passthrough_attr('classLabels')
    classValues = passthrough_attr('classValues')
    showOtherValues = passthrough_attr('showOtherValues')
    valueField = passthrough_attr('valueField')
    classDescriptions = passthrough_attr('classDescriptions')
    def addAllValues(self):
        """UniqueValuesSymbology.addAllValues()
           
           Adds all unique values to the symbology."""
        return convertArcObjectToPythonObject(self._arc_object.addAllValues(*gp_fixargs((), True)))
    
for cls in (PictureElement, LegendElement, MapSurroundElement):
    LayoutElement.__type_mapping__[cls.__type_string__.lower()] = cls
for cls in (GraduatedColorsSymbology, GraduatedSymbolsSymbology, 
            UniqueValuesSymbology, RasterClassifiedSymbology):
    BaseLayerSymbology.__type_mapping__[cls.__type_string__.lower()] = cls
del cls
BaseLayerSymbology.__type_mapping__['other'] = None
constants.maskmethods(mixins.ImageFileExportMixin)
constants.maskmethods(mixins.MapDocumentMethods)
constants.maskmethods(mixins.LayerMixin)
constants.maskmethods(mixins.LayerSupportsPropertyMixin)
constants.maskmethods(MapDocument)
constants.maskmethods(Layer)
constants.maskmethods(TableView)
constants.maskmethods(DataDrivenPages)
