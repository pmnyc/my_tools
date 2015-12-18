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
"""The Server toolbox contains tools to manage ArcGIS Server map and globe caches.
It also contains tools that simplify data extraction through the server and
facilitate printing from a web application."""
__all__ = ['DeleteGlobeServerCache', 'ManageGlobeServerCacheTiles', 'SendEmailWithZipFileAttachment', 'ExtractDataTask', 'ExtractDataAndEmailTask', 'ExtractData', 'UploadServiceDefinition', 'StageService', 'SignInToPortal', 'SignOutFromPortal', 'ExportWebMap', 'ConvertMapServerCacheStorageFormat', 'CreateMapServerCache', 'DeleteMapServerCache', 'ExportMapServerCache', 'GenerateMapServerCacheTilingScheme', 'ImportMapServerCache', 'ManageMapServerCacheScales', 'ManageMapServerCacheTiles', 'ManageMapServerCacheStatus']
__alias__ = u'server'
from arcpy.geoprocessing._base import gptooldoc, gp, gp_fixargs
from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject

# Caching toolset
@gptooldoc('ConvertMapServerCacheStorageFormat_server', None)
def ConvertMapServerCacheStorageFormat(input_service=None, num_of_caching_service_instances=None):
    """ConvertMapServerCacheStorageFormat_server(input_service, {num_of_caching_service_instances})

        Converts the storage of a map or image service cache between the exploded
        format and the compact format. The tool converts the format in place, meaning it
        does not make a copy of the existing format of the cache. Instead, it creates
        the new format of the cache in the same cache folder and deletes the old
        format.Make a backup of your cache before running this tool if you think you
        might want
        to go back to the old format.

     INPUTS:
      input_service (Image Service / MapServer):
          The map or image service whose cache format you want to convert.This is a string
          containing both the server and service information. To see how
          to construct this string, open ArcCatalog, select your service in the Catalog
          tree, and note the text in the Location toolbar. Then change the backslashes to
          forward slashes, for example, GIS Servers/arcgis on MYSERVER
          (admin)/USA.MapServer.
      num_of_caching_service_instances {Long}:
          The total number of instances of the System/CachingTools service that you want
          to dedicate toward running this tool. You can increase the maximum number of
          instances per machine of the System/CachingTools service using the Service
          Editor window available through an administrative connection to ArcGIS Server.
          Ensure your server machines can support the chosen number of instances."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ConvertMapServerCacheStorageFormat_server(*gp_fixargs((input_service, num_of_caching_service_instances), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('CreateMapServerCache_server', None)
def CreateMapServerCache(input_service=None, service_cache_directory=None, tiling_scheme_type=None, scales_type=None, num_of_scales=None, dots_per_inch=None, tile_size=None, predefined_tiling_scheme=None, tile_origin=None, scales=None, cache_tile_format=None, tile_compression_quality=None, storage_format=None):
    """CreateMapServerCache_server(input_service, service_cache_directory, tiling_scheme_type, scales_type, num_of_scales, dots_per_inch, tile_size, {predefined_tiling_scheme}, {tile_origin}, {scales;scales...}, {cache_tile_format}, {tile_compression_quality}, {storage_format})

        Creates the tiling scheme and preparatory folders for a map or image service
        cache. After running this tool, run Manage Map Server Cache Tiles to add tiles
        to the cache.

     INPUTS:
      input_service (Image Service / MapServer):
          The map or image service to be cached.This is a string containing both the
          server and service information. To see how
          to construct this string, open ArcCatalog, select your service in the Catalog
          tree, and note the text in the Location toolbar. Then change the backslashes to
          forward slashes, for example, GIS Servers/arcgis on MYSERVER
          (admin)/USA.MapServer.
      service_cache_directory (String):
          The parent directory for the cache. This must be a registered ArcGIS Server
          cache directory.
      tiling_scheme_type (String):
          Choose to use a NEW or PREDEFINED tiling scheme. You can define a new tiling
          scheme with this tool or browse to a predefined tiling scheme file (.xml). A
          predefined scheme can be created by running the Generate Map Server Cache Tiling
          Scheme tool.

          * NEW—You will define a new tiling scheme using the various other parameters in
          this tool to define scale levels, image format, storage format, and so on. This
          is the default.

          * PREDEFINED—You will specify a tiling scheme .xml file that already exists on
          disk. You can create a tiling scheme file using the Generate Map Server Cache
          Tiling Scheme tool.
      scales_type (String):
          Specify how you will define the scales for the tiles.

          * STANDARD—Autogenerates the scales based on the number defined in the Number of
          Scales (num_of_scales in Python) parameter. It will use levels that increase or
          decrease by half from 1:1,000,000 and will start with a level closest to the
          extent of the source map document. For example, if the source map document has
          an extent of 1:121,000,000 and three scale levels are defined, the map service
          will create a cache with scale-levels at 1:128,000,000; 1:64,000,000; and
          1:32,000,000. This is the default.

          * CUSTOM—Permits the cache designer to enter any scales desired.
      num_of_scales (Long):
          The number of scale levels to create in the cache. This option is disabled if
          you create a custom list of scales.
      dots_per_inch (Long):
          The dots per inch of the intended output device. If a DPI is chosen that does
          not match the resolution of the output device, the scale of the map tile will
          appear incorrect. The default value is 96.
      tile_size (String):
          The width and height of the cache tiles in pixels. The default is 256 by 256.
          For the best balance between performance and manageability, avoid deviating from
          standard widths of 256 by 256 or 512 by 512.

          * 128 x 128—128 by 128 pixels

          * 256 x 256—256 by 256 pixels

          * 512 x 512—512 by 512 pixels

          * 1024 x 1024—1024 by 1024 pixels
      predefined_tiling_scheme {File}:
          Path to a predefined tiling scheme file (usually named conf.xml).
      tile_origin {Point}:
          The origin (upper left corner) of the tiling scheme in the coordinates of the
          spatial reference of the source map document. The extent of the source map
          document must be within (but does not need to coincide) with this region.
      scales {Value Table}:
          Scale levels available for the cache. These are not represented as fractions.
          Instead, use 500 to represent a scale of 1:500, and so on.
      cache_tile_format {String}:
          Choose either PNG, PNG8, PNG24, PNG32, JPEG, or MIXED file format for the tiles
          in the cache. PNG8 is the default.

          * PNG—Creates PNG format with varying bit depths. The bit depths are optimized
          according to the color variation and transparency values in a tile.

          * PNG8—A lossless, 8-bit color, image format that uses an indexed color palette
          and an alpha table. Each pixel stores a value (0–255) that is used to look up
          the color in the color palette and the transparency in the alpha table. 8-bit
          PNGs are similar to GIF images and enjoy the best support for transparent
          background by most web browsers.

          * PNG24—A lossless, three-channel image format that supports large color
          variations (16 million colors) and has limited support for transparency. Each
          pixel contains three 8-bit color channels and the file header contains the
          single color that represents the transparent background. The color representing
          the transparent background color can be set in ArcMap. Versions of Internet
          Explorer less than version 7 do not support this type of transparency. Caches
          using PNG24 are significantly larger than those using PNG8 or JPEG and will take
          more disk space and require greater bandwidth to serve clients.

          * PNG32—A lossless, four-channel image format that supports large color
          variations (16 million colors) and transparency. Each pixel contains three 8-bit
          color channels and one 8-bit alpha channel that represents the level of
          transparency for each pixel. While the PNG32 format allows for partially
          transparent pixels in the range from 0 to 255, the ArcGIS Server cache
          generation tool only writes fully transparent (0) or fully opaque (255) values
          in the transparency channel. Caches using PNG32 are significantly larger than
          the other supported formats and will take more disk space and require greater
          bandwidth to serve clients.

          * JPEG—A lossy, three-channel image format that supports large color variations
          (16 million colors) but does not support transparency. Each pixel contains three
          8-bit color channels. Caches using JPEG provide control over output quality and
          size.

          * MIXED—Creates PNG 32 anywhere that transparency is detected (in other words,
          anywhere that the data frame background is visible). Creates JPEG for the
          remaining tiles. This keeps the average file size down while providing you with
          a clean overlay on top of other caches.
      tile_compression_quality {Long}:
          Enter a value between 1 and 100 for the JPEG compression quality. The default
          value is 75 for JPEG tile format and zero for other formats.Compression is
          supported only for JPEG format. Choosing a higher value will
          result in a larger file size with a higher-quality image. Choosing a lower value
          will result in a smaller file size with a lower-quality image.
      storage_format {String}:
          Determines the storage format of tiles.

          * COMPACT—Group tiles into large files called bundles. This storage format is
          more efficient in terms of storage and mobility.

          * EXPLODED—Store each tile as a separate file."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.CreateMapServerCache_server(*gp_fixargs((input_service, service_cache_directory, tiling_scheme_type, scales_type, num_of_scales, dots_per_inch, tile_size, predefined_tiling_scheme, tile_origin, scales, cache_tile_format, tile_compression_quality, storage_format), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('DeleteGlobeServerCache_server', None)
def DeleteGlobeServerCache(service=None, Layer=None):
    """DeleteGlobeServerCache_server(service, Layer;Layer...)

        Deletes a layer or layers of an existing globe service cache and all tiles in
        them.

     INPUTS:
      service (GlobeServer):
          The globe service whose layer caches you want to delete.This is a string
          containing both the server and service information. To see how
          to construct this string, open ArcCatalog, select your service in the Catalog
          tree, and note the text in the Location toolbar. Then change the backslashes to
          forward slashes, for example, GIS Servers/arcgis on MYSERVER
          (admin)/Seattle.GlobeServer.
      Layer (String):
          The layers in the globe service whose caches will be deleted. All layers of the
          service are included by default. If a layer is excluded the layer's cache will
          not be deleted."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DeleteGlobeServerCache_server(*gp_fixargs((service, Layer), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('DeleteMapServerCache_server', None)
def DeleteMapServerCache(input_service=None, num_of_caching_service_instances=None):
    """DeleteMapServerCache_server(input_service, {num_of_caching_service_instances})

        Deletes an existing map or image service cache, including all associated files
        on disk.Parameters have changed for this tool at version 10.1. Models and
        scripts
        written prior to 10.1 that use this tool will need to be modified to work in
        10.1.

     INPUTS:
      input_service (Image Service / MapServer):
          The map or image service whose cache will be deleted.This is a string containing
          both the server and service information. To see how
          to construct this string, open ArcCatalog, select your service in the Catalog
          tree, and note the text in the Location toolbar. Then change the backslashes to
          forward slashes, for example, GIS Servers/arcgis on MYSERVER
          (admin)/USA.MapServer.
      num_of_caching_service_instances {Long}:
          The total number of instances of the System/CachingTools service that you want
          to dedicate toward running this tool. You can increase the maximum number of
          instances per machine of the System/CachingTools service using the Service
          Editor window available through an administrative connection to ArcGIS Server.
          Ensure your server machines can support the chosen number of instances.The
          Delete Map Server Cache tool requires a minimum of two instances to run
          successfully."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DeleteMapServerCache_server(*gp_fixargs((input_service, num_of_caching_service_instances), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('ExportMapServerCache_server', None)
def ExportMapServerCache(input_service=None, target_cache_path=None, export_cache_type=None, copy_data_from_server=None, storage_format_type=None, scales=None, num_of_caching_service_instances=None, area_of_interest=None, export_extent=None, overwrite=None):
    """ExportMapServerCache_server(input_service, target_cache_path, export_cache_type, copy_data_from_server, storage_format_type, scales;scales..., {num_of_caching_service_instances}, {area_of_interest}, {export_extent}, {overwrite})

        Exports tiles from a map or image service cache as a cache dataset or as a tile
        package to a folder on disk. The tiles can either be imported into other caches
        or they can be accessed from ArcGIS for Desktop or mobile devices as a raster
        dataset, independently from their parent service.

     INPUTS:
      input_service (Image Service / MapServer):
          The map or image service whose cache tiles will be exported.This is a string
          containing both the server and service information. To see how
          to construct this string, open ArcCatalog, select your service in the Catalog
          tree, and note the text in the Location toolbar. Then change the backslashes to
          forward slashes, for example, GIS Servers/arcgis on MYSERVER
          (admin)/USA.MapServer.
      target_cache_path (Folder):
          The folder into which the cache will be exported. This folder does not have to
          be a registered server cache directory. The ArcGIS Server account must have
          write access to the target cache folder. If the server account cannot be granted
          write access to the destination folder but the ArcGIS for Desktop client has
          write access to it,  then choose the Copy data from server parameter.
      export_cache_type (String):
          Choose to export cache as a Cache Dataset or a Tile Package. Tile packages are
          suitable for ArcGIS Runtime and ArcGIS Mobile deployments.

          * CACHE_DATASET—Map or image service cache that is generated using ArcGIS
          Server. Usable in ArcMap and by ArcGIS Server map or image services. This is the
          default.

          * TILE_PACKAGE—A single compressed file where the cache dataset is added as a
          layer and consolidated so that it can be shared easily. Usable in ArcGIS for
          Desktop, as well as in ArcGIS Runtime and mobile applications.
      copy_data_from_server (Boolean):
          Set this option to COPY_DATA if the ArcGIS Server account cannot be granted
          write access to the target folder and the ArcGIS for Desktop client has write
          access to it. The software exports the tiles in the server output directory
          before moving them to the target folder.

          * COPY_DATA—Tiles are placed in the server output directory, then moved to the
          target folder. The ArcGIS for Desktop client must have write access to the
          target folder.

          * DO_NOT_COPY—Tiles are exported directly into the target folder. The ArcGIS
          Server account must have write access to the target folder. This is the default.
      storage_format_type (String):
          The storage format of the exported cache.

          * COMPACT—Tiles are grouped in bundle files to save space on disk and allow for
          faster copying of caches. This is the default, if Export cache type
          (export_cache_type in Python) is Tile package.

          * EXPLODED—Each tile is stored as an individual file (in the way caches were
          always stored prior to ArcGIS Server 10).
      scales (Double):
          A list of scale levels at which tiles will be exported.
      num_of_caching_service_instances {Long}:
          The total number of instances of the System/CachingTools service that you want
          to dedicate toward running this tool. You can increase the maximum number of
          instances per machine of the System/CachingTools service using the Service
          Editor window available through an administrative connection to ArcGIS Server.
          Ensure your server machines can support the chosen number of instances.
      area_of_interest {Feature Set}:
          An area of interest (polygon) that spatially constrains where tiles are
          exported from the cache. This can be a feature class, or it can be a feature
          that you interactively define in ArcMap. This parameter is useful if you want to
          export irregularly shaped areas, as the tool clips the cache dataset at pixel
          resolution.If you do not specify an area of interest, the full extent of the map
          is
          exported.
      export_extent {Extent}:
          A rectangular extent defining the tiles to be exported. By default the extent
          is set to the full extent of the map service into which you are importing. Note
          the optional parameter on this tool Area of Interest that allows you to
          alternatively import using a polygon. It is recommended not to provide values
          for both the parameters for a job. If values are provided for both parameters,
          the Area of Interest takes precedence over Import Extent
      overwrite {Boolean}:
          * OVERWRITE—The export replaces all pixels in the area of interest, effectively
          overwriting tiles in the destination cache with tiles from the originating
          cache.

          * MERGE—When the tiles are imported, transparent pixels in the originating cache
          are ignored by default. This results in a merged or blended image in the
          destination cache. This is the default behavior."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ExportMapServerCache_server(*gp_fixargs((input_service, target_cache_path, export_cache_type, copy_data_from_server, storage_format_type, scales, num_of_caching_service_instances, area_of_interest, export_extent, overwrite), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('GenerateMapServerCacheTilingScheme_server', None)
def GenerateMapServerCacheTilingScheme(map_document=None, data_frame=None, tile_origin=None, output_tiling_scheme=None, num_of_scales=None, scales=None, dots_per_inch=None, tile_size=None):
    """GenerateMapServerCacheTilingScheme_server(map_document, data_frame, tile_origin, output_tiling_scheme, num_of_scales, scales;scales..., dots_per_inch, tile_size)

        Generates an XML tiling scheme file that defines the scale levels, tile
        dimensions, and other properties for a map service cache. This tool is useful
        when creating a tiling scheme to use in multiple caches. You can load the tiling
        scheme file when you create a cache in ArcGIS for Desktop or ArcGIS Server
        Manager, or you can run Create Map Server Cache and pass in the tiling scheme
        file as a parameter.A tiling scheme describes how clients should reference the
        tiles in a cache and
        is a mapping between the spatial reference of the source map document and the
        tiling grid. The tiling grid uses a level of detail (scales), row, and column
        reference scheme. The scheme also defines the scale levels (levels of detail) at
        which the cache has tiles, the size of the tiles in pixels, and the screen
        resolution for which the tiles are intended to be most commonly displayed. A
        tiling scheme is needed to generate a map cache.

     INPUTS:
      map_document (File):
          The source map document to be used for the tiling scheme.
      data_frame (String):
          The data frame to be used for the tiling scheme.
      tile_origin (Point):
          The upper left corner of the tiling scheme, in coordinates of the spatial
          reference of the source data frame.
      num_of_scales (Long):
          Number of scale levels in the tiling scheme.
      scales (Value Table):
          Scale levels to include in the tiling scheme. These are not represented as
          fractions. Instead, use 500 to represent a scale of 1:500, and so on.
      dots_per_inch (Long):
          The dots per inch of the intended output device. If a DPI is chosen that does
          not match the resolution of the output device, the scale of the map tile will
          appear incorrect. The default value is 96.
      tile_size (String):
          The width and height of the cache tiles in pixels. The default is 256 by 256.
          For the best balance between performance and manageability, avoid deviating from
          standard dimensions of 256 by 256 or 512 by 512.

          * 128 x 128—128 by 128 pixels

          * 256 x 256—256 by 256 pixels

          * 512 x 512—512 by 512 pixels

          * 1024 x 1024—1024 by 1024 pixels

     OUTPUTS:
      output_tiling_scheme (File):
          Path and file name of the tiling scheme file to create."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.GenerateMapServerCacheTilingScheme_server(*gp_fixargs((map_document, data_frame, tile_origin, output_tiling_scheme, num_of_scales, scales, dots_per_inch, tile_size), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('ImportMapServerCache_server', None)
def ImportMapServerCache(input_service=None, source_cache_type=None, source_cache_dataset=None, source_tile_package=None, upload_data_to_server=None, scales=None, num_of_caching_service_instances=None, area_of_interest=None, import_extent=None, overwrite=None):
    """ImportMapServerCache_server(input_service, source_cache_type, {source_cache_dataset}, {source_tile_package}, {upload_data_to_server}, {scales;scales...}, {num_of_caching_service_instances}, {area_of_interest}, {import_extent}, {overwrite})

        Imports tiles from a folder on disk into a map or image service cache. The
        source folder can be a child of a registered server cache directory, a folder
        into which a cache has been previously exported, or a tile package (.tpk).The
        target service must have the same tiling scheme and the storage format as the
        source cache.

     INPUTS:
      input_service (Image Service / MapServer):
          The map or image service into which tiles will be imported.This is a string
          containing both the server and service information. To see how
          to construct this string, open ArcCatalog, select your service in the Catalog
          tree, and note the text in the Location toolbar. Then change the backslashes to
          forward slashes, for example, GIS Servers/arcgis on MYSERVER
          (admin)/USA.MapServer.
      source_cache_type (String):
          Choose to import cache from a CACHE_DATASET or TILE_PACKAGE to a cached map or
          image service running on the server.

          * CACHE_DATASET—Map or image service cache that is generated using ArcGIS
          Server. Usable in ArcMap and by ArcGIS Server map or image services.

          * TILE_PACKAGE—A single compressed file where the cache dataset is added as a
          layer and consolidated so that it can be shared easily. Usable in ArcGIS for
          Desktop, as well as in ArcGIS Runtime and mobile applications.
      source_cache_dataset {Raster Dataset}:
          The path to the cache folder matching the data frame name. You do not have to
          enter a registered server cache directory; in fact, most of the time you'll
          enter a location on disk where tiles have been previously exported. This
          location should be accessible to the ArcGIS Server account. If the ArcGIS Server
          account cannot be granted access to this location set the upload_data_to_server
          to UPLOAD_DATA.
      source_tile_package {File}:
          The path to the tile package (.tpk) that will be imported. This location should
          be accessible to the ArcGIS Server account. When importing a tile package file
          to a cached map/image service, the upload_data_to_server parameter is ignored as
          it will be automatically be set to UPLOAD_DATA.
      upload_data_to_server {Boolean}:
          Set this parameter to UPLOAD_DATA if the ArcGIS Server account does not have
          read access to the source cache. The tool will upload the source cache to the
          ArcGIS Server uploads directory before moving it to the ArcGIS Server cache
          directory.

          * UPLOAD_DATA—Tiles are placed in the server uploads directory, then moved to
          the server cache directory. This is by default enabled when storage_format_type
          is TILE_PACKAGE.

          * DO_NOT_UPLOAD—Tiles are imported directly into the server cache directory. The
          ArcGIS Server account must have read access to the source cache.
      scales {Double}:
          A list of scale levels at which tiles will be imported.
      num_of_caching_service_instances {Long}:
          The total number of instances of the System/CachingTools service that you want
          to dedicate toward running this tool. You can increase the maximum number of
          instances per machine of the System/CachingTools service using the Service
          Editor window available through an administrative connection to ArcGIS Server.
          Ensure your server machines can support the chosen number of instances.
      area_of_interest {Feature Set}:
          A rectangular extent defining the tiles to be imported into the cache. By
          default the extent is set to the full extent of the map service into which you
          are importing. Note the optional parameter on this tool Area Of Interest that
          allows you to spatially constrain the tiles imported using an irregular shape.
          If values are provided for both parameters, the Area Of Interest takes
          precedence over Import Extent.
      import_extent {Extent}:
          An area of interest polygon that spatially constrains where tiles are imported
          into the cache. This can be a feature class, or it can be a feature that you
          interactively define in ArcMap. This parameter is useful if you want to import
          tiles for irregularly shaped areas, as the tool clips the cache dataset which
          intersects the polygon at pixel resolution and then import it to the service
          cache directory.If you do not provide a value for this parameter, the value of
          the Import Extent
          parameter will be used. The default is to use the full extent of the map.
      overwrite {Boolean}:
          * OVERWRITE—The import replaces all pixels in the area of interest, effectively
          overwriting tiles in the destination cache with tiles from the originating
          cache.

          * MERGE—When the tiles are imported, transparent pixels in the originating cache
          are ignored by default. This results in a merged or blended image in the
          destination cache. This is the default behavior."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ImportMapServerCache_server(*gp_fixargs((input_service, source_cache_type, source_cache_dataset, source_tile_package, upload_data_to_server, scales, num_of_caching_service_instances, area_of_interest, import_extent, overwrite), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('ManageGlobeServerCacheTiles_server', None)
def ManageGlobeServerCacheTiles(service=None, in_layers=None, update_mode=None, num_of_caching_service_instances=None, area_of_interest=None, ignore_status=None, update_extent=None):
    """ManageGlobeServerCacheTiles_server(service, in_layers;in_layers..., update_mode, {num_of_caching_service_instances}, {area_of_interest}, {ignore_status}, {update_extent})

        Creates and updates tiles in an existing globe service cache. This tool is used
        to create new tiles or to replace missing tiles, overwrite outdated tiles, or
        add new tiles. All these actions can be defined by rectangular extents or by a
        polygon feature class. When creating new tiles, you can choose whether to create
        only empty tiles or re-create all tiles.   Parameters have changed for this tool
        at version 10.1. Models and scripts written prior to 10.1 that use this tool
        will need to be modified to work in 10.1.

     INPUTS:
      service (GlobeServer):
          The globe service whose cache tiles you want to update.This is a string
          containing both the server and service information. To see how
          to construct this string, open ArcCatalog, select your service in the Catalog
          tree, and note the text in the Location toolbar. Then change the backslashes to
          forward slashes, for example, GIS Servers/arcgis on MYSERVER
          (admin)/Seattle.GlobeServer.
      in_layers (Value Table):
          Rectangular extent at which tiles should be created or deleted, depending on the
          value of the update_mode parameter. You can type the extent values or choose an
          extent from an existing data source.
      update_mode (String):
          The layers to include in the cache.For each layer, you need to provide a
          level_from, which is the level of detail
          at which you would like to begin caching the layer, and a level_to, which is the
          level of detail at which you would like to end caching the layer. If the
          smallest and largest levels of detail are used for level_from and level_to,
          respectively, a full cache will be built for the layer.
      num_of_caching_service_instances {Long}:
          Choose a mode for updating the cache. The two modes are:

          * RECREATE_EMPTY_TILES—Only tiles that are empty will be created. Existing tiles
          will be left unchanged.

          * RECREATE_ALL_TILES—All tiles, including existing tiles, will be replaced.
          Additionally, new tiles will be added if a layer's data extent has changed or
          new layers have been added to the globe service and listed in this tool.
      area_of_interest {Feature Set}:
          The total number of instances of the System/CachingTools service that you want
          to dedicate toward running this tool. You can increase the maximum number of
          instances per machine of the System/CachingTools service using the Service
          Editor window available through an administrative connection to ArcGIS Server.
          Ensure your server machines can support the chosen number of instances.
      ignore_status {Boolean}:
          Defines an area of interest to constrain where tiles will be created or deleted.
          This can be a feature class, or it can be a feature that you interactively
          define in ArcMap. This parameter is useful if you want to manage tiles for
          irregularly shaped areas. It's also useful in situations where you want to
          precache some areas and leave less-visited areas uncached.
      update_extent {Extent}:
          This parameter allows you to track the status of your caching if you are
          creating tiles based on feature class boundaries (see the update_feature_class
          parameter).

          * TRACK_STATUS—The feature class' Cached field is read (and created if it
          doesn't exist yet). Features containing No or null in this field are cached and
          will contain Yes when caching has completed for the feature. Features already
          marked Yes in this field are not cached.

          * DO_NOT_TRACK_STATUS—The feature class' Cached field is ignored and tiles are
          created for all features in the feature class."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ManageGlobeServerCacheTiles_server(*gp_fixargs((service, in_layers, update_mode, num_of_caching_service_instances, area_of_interest, ignore_status, update_extent), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('ManageMapServerCacheScales_server', None)
def ManageMapServerCacheScales(input_service=None, scales=None):
    """ManageMapServerCacheScales_server(input_service, scales;scales...)

        Updates the scale levels in an existing cached map or image service. Use this
        tool to add new scales or delete existing scales from a cache.

     INPUTS:
      input_service (Image Service / MapServer):
          The map or image service for which you want to add or remove cache scales.This
          is a string containing both the server and service information. To see how
          to construct this string, open ArcCatalog, select your service in the Catalog
          tree, and note the text in the Location toolbar. Then change the backslashes to
          forward slashes, for example, GIS Servers/arcgis on MYSERVER
          (admin)/USA.MapServer.
      scales (Value Table):
          The scale values to be included in the updated tiling scheme.You must specify
          existing scale values if you want to keep them. Any existing
          scale levels you do not specify in this tool will be permanently deleted. For
          example, if you have four existing scales and you wish to add two scales, make
          sure your final list has a total of six scales."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ManageMapServerCacheScales_server(*gp_fixargs((input_service, scales), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('ManageMapServerCacheStatus_server', None)
def ManageMapServerCacheStatus(input_service=None, manage_mode=None, scales=None, num_of_caching_service_instances=None, report_folder=None, area_of_interest=None, report_extent=None):
    """ManageMapServerCacheStatus_server(input_service, manage_mode, {scales;scales...}, {num_of_caching_service_instances}, {report_folder}, {area_of_interest}, {report_extent})

        Manages internal data kept by the server about the built tiles in a map or image
        service cache.

     INPUTS:
      input_service (Image Service / MapServer):
          The map or image service for which the status will be modified.This is a string
          containing both the server and service information. To see how
          to construct this string, open ArcCatalog, select your service in the Catalog
          tree, and note the text in the Location toolbar. Then change the backslashes to
          forward slashes, for example, GIS Servers/arcgis on MYSERVER
          (admin)/USA.MapServer.
      manage_mode (String):
          The scale levels for which the status will be modified. This parameter is only
          applicable when building a custom status using the REPORT_BUNDLE_STATUS option
          for the manage_mode parameter.
      scales {Double}:
          * DELETE_CACHE_STATUS—Deletes the status information used by the server.

          * REBUILD_CACHE_STATUS—Deletes, then rebuilds the status information used by the
          server.

          * REPORT_BUNDLE_STATUS—Creates status information in a new file geodatabase
          named Status.gdb in a folder you specify in the Output Folder parameter. This
          option is used when you want to create a custom status report for a particular
          area of interest or set of scales.
      num_of_caching_service_instances {Long}:
          The total number of instances of the System/CachingTools service that you want
          to dedicate toward running this tool. You can increase the maximum number of
          instances per machine of the System/CachingTools service using the Service
          Editor window available through an administrative connection to ArcGIS Server.
          Ensure your server machines can support the chosen number of instances.This tool
          uses three instances by default, if that many are available. Using a
          larger number of instances with this tool may cause the operation to slow down.
      report_folder {Folder}:
          Output folder for the Status.gdb. This parameter is only applicable when
          building a custom status using the REPORT_BUNDLE_STATUS option.The account
          running ArcGIS for Desktop needs write access to this folder.This folder must
          not already have a Status.gdb in it.
      area_of_interest {Feature Set}:
          A rectangular extent defining the area for which the status will be built. This
          parameter is only applicable when building a custom status using the
          REPORT_BUNDLE_STATUS option.Note that the Area Of Interest parameter allows you
          to specify an area of
          interest that is nonrectangular.
      report_extent {Extent}:
          An area of interest (polygon) that determines what geography the status report
          will cover. This can be a feature class, or it can be a feature that you
          interactively define in ArcMap. This parameter is only applicable when building
          a custom status using the REPORT_BUNDLE_STATUS option."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ManageMapServerCacheStatus_server(*gp_fixargs((input_service, manage_mode, scales, num_of_caching_service_instances, report_folder, area_of_interest, report_extent), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('ManageMapServerCacheTiles_server', None)
def ManageMapServerCacheTiles(input_service=None, scales=None, update_mode=None, num_of_caching_service_instances=None, area_of_interest=None, update_extent=None, wait_for_job_completion=None):
    """ManageMapServerCacheTiles_server(input_service, scales;scales..., update_mode, {num_of_caching_service_instances}, {area_of_interest}, {update_extent}, {wait_for_job_completion})

        Creates and updates tiles in an existing map or image service cache. This tool
        is used to create new tiles, replace missing tiles, overwrite outdated tiles,
        and delete tiles.

     INPUTS:
      input_service (Image Service / MapServer):
          The map or image service whose cache tiles you want to update.This is a string
          containing both the server and service information. To see how
          to construct this string, open ArcCatalog, select your service in the Catalog
          tree, and note the text in the Location toolbar. Then change the backslashes to
          forward slashes, for example, GIS Servers/arcgis on MYSERVER
          (admin)/USA.MapServer.
      scales (Double):
          The scale levels at which you will create or delete tiles when running this
          tool, depending on the Update Mode.
      update_mode (String):
          The mode for updating the cache.

          * RECREATE_EMPTY_TILES—Only tiles that are empty will be created. Existing tiles
          will be left unchanged.

          * RECREATE_ALL_TILES—Existing tiles will be replaced and new tiles will be added
          if the extent has changed.

          * DELETE_TILES —Tiles will be deleted from the cache. The cache folder structure
          will not be deleted. If you wish to delete the entire cache, including the
          folder structure, use the Delete Map Server Cache tool.
      num_of_caching_service_instances {Long}:
          The total number of instances of the System/CachingTools service that you want
          to dedicate toward running this tool. You can increase the maximum number of
          instances per machine of the System/CachingTools service using the Service
          Editor window available through an administrative connection to ArcGIS Server.
          Ensure your server machines can support the chosen number of instances.
      area_of_interest {Feature Set}:
          Rectangular extent at which to create or delete tiles, depending on the value of
          the update_mode parameter. It is not recommended you provide values for both
          update_extent and area_of_interest. If values for both parameters are provided,
          the value of area_of_interest will be used.
      update_extent {Extent}:
          Defines an area of interest to constrain where tiles will be created or deleted.
          This can be a feature class, or it can be a feature that you interactively
          define in ArcMap. This parameter is useful if you want to manage tiles for
          irregularly shaped areas. It's also useful in situations where you want to pre-
          cache some areas and leave less-visited areas uncached.If you do not provide a
          value for this parameter, the default is to use the full
          extent of the map.
      wait_for_job_completion {Boolean}:
          This parameter allows you to watch the progress of the cache job running on the
          server.

          * WAIT—This tool will continue to run in ArcGIS for Desktop while the cache job
          runs on ArcGIS for Server or ArcGIS Online. With this option, you can request
          detailed progress reports at any time and view the geoprocessing messages as
          they appear. This is the default option. It is recommended that you use this
          option in Python scripts.

          * DO_NOT_WAIT—The geoprocessing tool will submit the job to the server, allowing
          you to perform other geoprocessing tasks in ArcGIS for Desktop or even close
          ArcGIS for Desktop. This option is used when you choose to build a cache
          automatically at the time you publish the service, and you can also set this
          option on any other cache that you build. To track the status of the cache job,
          open ArcGIS for Desktop, right-click the service in the Catalog window, and
          click View Cache Status. You can also use the URL provided in the tool result
          message.This option is not available if the Status.gdb file geodatabase is not
          present in the service's cache directory."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ManageMapServerCacheTiles_server(*gp_fixargs((input_service, scales, update_mode, num_of_caching_service_instances, area_of_interest, update_extent, wait_for_job_completion), True)))
        return retval
    except Exception, e:
        raise e


# Data Extraction toolset
@gptooldoc('ExtractData_server', None)
def ExtractData(Layers_to_Clip=None, Area_of_Interest=None, Feature_Format=None, Raster_Format=None, Spatial_Reference=None, Custom_Spatial_Reference_Folder=None, Output_Zip_File=None):
    """ExtractData_server(Layers_to_Clip;Layers_to_Clip..., Area_of_Interest, Feature_Format, Raster_Format, Spatial_Reference, {Custom_Spatial_Reference_Folder}, Output_Zip_File)

        Extracts selected layers in the specified area of interest to a specific format
        and spatial reference.  The extracted data is then written to a zip file.This
        script tool is not intended for general use. This tool is intended
        specifically for the use of a data extraction geoprocessing service such as the
        Extract Data Task and Extract Data and Email Task model tools, or a clip and
        ship geoprocessing service such as the Geoprocessing service example: Clip And
        Ship. If you are only looking for simple tools to subset feature data, look in
        the Extract toolset or at the Clip tool.

     INPUTS:
      Layers_to_Clip (Layer):
          The layers to be clipped. Layers must be feature or raster layers in the table
          of contents of ArcMap. Layer files (.lyr files) do not work for this parameter.
      Area_of_Interest (Feature Set):
          One or more polygons by which the layers will be clipped.
      Feature_Format (String):
          The format in which the output features will be delivered. The string provided
          should be formatted as follows:

          *  Name or format - Short Name - extension (if any)
          The hyphen between the components is required, as well as the spaces around the
          hyphen.For example:

          * File Geodatabase - GDB - .gdb

          * Shapefile - SHP - .shp

          * Autodesk AutoCAD - DXF_R2007 - .dxf

          * Autodesk AutoCAD - DWG_R2007 - .dwg

          * Bentley Microstation Design (V8) - DGN_V8 - .dgn
           Internally, this tool uses the Export to CAD tool to convert data to the .dgn,
          .dwg, and .dxf CAD formats. The list of short names supported includes DGN_V8,
          DWG_R14, DWG_R2000, DWG_R2004, DWG_R2005, DWG_R2006, DWG_R2007, DWG_R2010,
          DXF_R14, DXF_R2000, DXF_R2004, DXF_R2005, DXF_R2006, DXF_R2007, and
          DXF_R2010.Exporting to nondefault formats is supported using the Quick Export
          tool and
          that requires the Data Interoperability extension be installed. The Data
          Interoperability extension is not installed by default with ArcGIS for Desktop
          or ArcGIS for Server.
      Raster_Format (String):
          The format in which the output raster datasets will be delivered. The string
          provided should be formatted as follows:

          * Name of format - Short Name - extension (if any)
          Any of the following strings will work:

          * Esri GRID - GRID

          * File Geodatabase - GDB - .gdb

          * ERDAS IMAGINE - IMG - .img

          * Tagged Image File Format - TIFF - .tif

          * Portable Network Graphics - PNG - .png

          * Graphic Interchange Format - GIF - .gif

          * Joint Photographics Experts Group - JPEG - .jpg

          * Joint Photographics Experts Group - JPEG - .jp2

          * Bitmap - BMP - .bmp
          Some of the above raster formats have limitations and not all data can be
          converted to the format. For a list of formats and their limitations, see
          Supported raster dataset file formats.
      Spatial_Reference (String):
          The spatial reference of the output data delivered by the tool.For standard Esri
          spatial references, the name you provide here should be the
          name of the desired coordinate system. This name corresponds to the name of the
          spatial reference's projection file. Alternatively, you can use the Well Known
          ID (WKID) of the coordinate system.For example:

          * Sinusoidal (world)

          * WGS 1984 Web Mercator

          * NAD 1983 HARN StatePlane Oregon North FIPS 3601

          * WGS 1984 UTM Zone 11N

          * 102003

          * 54001

          * If you want the output to have the same coordinate system as the input, then
          use the string Same As Input.
          For any custom projection, the name specified should be the name of the custom
          projection file (without extension). The location of the custom projection files
          should be specified in the Custom_Spatial_Reference_Folder parameter.
      Custom_Spatial_Reference_Folder {Folder}:
          The location of any custom projection file or files referenced in the Spatial
          Reference parameter. This is only necessary if the custom projection file is not
          in the default installation Coordinate System folder.

     OUTPUTS:
      Output_Zip_File (File):
          The zip file that will contain the extracted data."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ExtractData_server(*gp_fixargs((Layers_to_Clip, Area_of_Interest, Feature_Format, Raster_Format, Spatial_Reference, Custom_Spatial_Reference_Folder, Output_Zip_File), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('ExtractDataAndEmailTask_server', None)
def ExtractDataAndEmailTask(Layers_to_Clip=None, Area_of_Interest=None, Feature_Format=None, Raster_Format=None, To=None):
    """ExtractDataAndEmailTask_server(Layers_to_Clip;Layers_to_Clip..., Area_of_Interest, Feature_Format, Raster_Format, To)

        Extracts the data in the specified layers and area of interest to the selected
        format and spatial reference, zips the data, and emails it to the specified
        address. This tool can be used to create a Data Extraction geoprocessing
        service. This tool is intended primarily for use as a part of a geoprocessing
        service.
        When using this tool as a part of a geoprocessing service, copy the tool into a
        custom toolbox, edit the model, and reconfigure it as necessary. It is important
        to note that this tool will not work unless you open and edit the model (as
        described below) before publishing the model as a service.

     INPUTS:
      Layers_to_Clip (Layer):
          The layers to be clipped. Layers must be feature or raster layers in the table
          of contents of ArcMap. Layer files (.lyr files) do not work for this parameter.
      Area_of_Interest (Feature Set):
          One or more polygons by which the layers will be clipped.
      Feature_Format (String):
          The format in which the output features will be delivered. The string provided
          should be formatted as follows:

          *  Name or format - Short Name - extension (if any)
          The hyphen between the components is required, as well as the spaces around the
          hyphen.For example:

          * File Geodatabase - GDB - .gdb

          * Shapefile - SHP - .shp

          * Autodesk AutoCAD - DXF_R2007 - .dxf

          * Autodesk AutoCAD - DWG_R2007 - .dwg

          * Bentley Microstation Design (V8) - DGN_V8 - .dgn
           Internally, this tool uses the Export to CAD tool to convert data to the .dgn,
          .dwg, and .dxf CAD formats. The list of short names supported includes DGN_V8,
          DWG_R14, DWG_R2000, DWG_R2004, DWG_R2005, DWG_R2006, DWG_R2007, DWG_R2010,
          DXF_R14, DXF_R2000, DXF_R2004, DXF_R2005, DXF_R2006, DXF_R2007, and
          DXF_R2010.Exporting to nondefault formats is supported using the Quick Export
          tool and
          that requires the Data Interoperability extension be installed. The Data
          Interoperability extension is not installed by default with ArcGIS for Desktop
          or ArcGIS for Server.
      Raster_Format (String):
          The format in which the output raster datasets will be delivered. The string
          provided should be formatted as follows:

          * Name of format - Short Name - extension (if any)
          Any of the following strings will work:

          * Esri GRID - GRID

          * File Geodatabase - GDB - .gdb

          * ERDAS IMAGINE - IMG - .img

          * Tagged Image File Format - TIFF - .tif

          * Portable Network Graphics - PNG - .png

          * Graphic Interchange Format - GIF - .gif

          * Joint Photographics Experts Group - JPEG - .jpg

          * Joint Photographics Experts Group - JPEG - .jp2

          * Bitmap - BMP - .bmp
          Some of the above raster formats have limitations and not all data can be
          converted to the format. For a list of formats and their limitations, see
          Supported raster dataset file formats.
      To (String):
          The email address of the recipient.This tool will be able to email to this
          address if and only if the SMTP server
          has been configured within this model."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ExtractDataAndEmailTask_server(*gp_fixargs((Layers_to_Clip, Area_of_Interest, Feature_Format, Raster_Format, To), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('ExtractDataTask_server', None)
def ExtractDataTask(Layers_to_Clip=None, Area_of_Interest=None, Feature_Format=None, Raster_Format=None, Output_Zip_File=None):
    """ExtractDataTask_server(Layers_to_Clip;Layers_to_Clip..., Area_of_Interest, Feature_Format, Raster_Format, Output_Zip_File)

        Extracts the selected layers in the specified area of interest to the selected
        formats and spatial reference, then returns all the data in a zip file.This tool
        is intended primarily for use as part of a geoprocessing service. When
        using this tool as part of a geoprocessing service, copy the tool into a custom
        toolbox, edit the model, and reconfigure it as necessary. For step-by-step
        instructions on how to make, use, and configure a geoprocessing service using
        this tool, see Geoprocessing service example: Clip And Ship.

     INPUTS:
      Layers_to_Clip (Layer):
          The layers to be clipped. Layers must be feature or raster layers in the table
          of contents of ArcMap. Layer files (.lyr files) do not work for this parameter.
      Area_of_Interest (Feature Set):
          One or more polygons by which the layers will be clipped.
      Feature_Format (String):
          The format in which the output features will be delivered. The string provided
          should be formatted as follows:

          *  Name or format - Short Name - extension (if any)
          The hyphen between the components is required, as well as the spaces around the
          hyphen.For example:

          * File Geodatabase - GDB - .gdb

          * Shapefile - SHP - .shp

          * Autodesk AutoCAD - DXF_R2007 - .dxf

          * Autodesk AutoCAD - DWG_R2007 - .dwg

          * Bentley Microstation Design (V8) - DGN_V8 - .dgn
           Internally, this tool uses the Export to CAD tool to convert data to the .dgn,
          .dwg, and .dxf CAD formats. The list of short names supported includes DGN_V8,
          DWG_R14, DWG_R2000, DWG_R2004, DWG_R2005, DWG_R2006, DWG_R2007, DWG_R2010,
          DXF_R14, DXF_R2000, DXF_R2004, DXF_R2005, DXF_R2006, DXF_R2007, and
          DXF_R2010.Exporting to nondefault formats is supported using the Quick Export
          tool and
          that requires the Data Interoperability extension be installed. The Data
          Interoperability extension is not installed by default with ArcGIS for Desktop
          or ArcGIS for Server.
      Raster_Format (String):
          The format in which the output raster datasets will be delivered. The string
          provided should be formatted as follows:

          * Name of format - Short Name - extension (if any)
          Any of the following strings will work:

          * Esri GRID - GRID

          * File Geodatabase - GDB - .gdb

          * ERDAS IMAGINE - IMG - .img

          * Tagged Image File Format - TIFF - .tif

          * Portable Network Graphics - PNG - .png

          * Graphic Interchange Format - GIF - .gif

          * Joint Photographics Experts Group - JPEG - .jpg

          * Joint Photographics Experts Group - JPEG - .jp2

          * Bitmap - BMP - .bmp
          Some of the above raster formats have limitations and not all data can be
          converted to the format. For a list of formats and their limitations, see
          Supported raster dataset file formats.

     OUTPUTS:
      Output_Zip_File (File):
          The zip file that will contain the extracted data."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ExtractDataTask_server(*gp_fixargs((Layers_to_Clip, Area_of_Interest, Feature_Format, Raster_Format, Output_Zip_File), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('SendEmailWithZipFileAttachment_server', None)
def SendEmailWithZipFileAttachment(To=None, From=None, Subject=None, Text=None, Zip_File=None, Max_File_Size__MB_=None, SMTP_Email_Server=None, User=None, Password=None):
    """SendEmailWithZipFileAttachment_server(To, From, Subject, Text, Zip_File, Max_File_Size__MB_, SMTP_Email_Server, {User}, {Password})

        Emails a file to an email address using an SMTP email server.This tool is
        primarily intended for use as a part of a Clip and Email/Data
        Extraction geoprocessing service. To this end, this script tool is contained in
        the Extract Data and Email Task model tool and is primarily intended for use by
        that model.

     INPUTS:
      To (String):
          The email address of the recipient.
      From (String):
          The email address of the sender.
      Subject (String):
          The text in the subject line of the email.
      Text (String):
          The body text of the email.
      Zip_File (File):
          The file to be attached to the email.
      Max_File_Size__MB_ (Long):
          The maximum allowable size of an attachment.If you don't know what to use for
          Max File Size, check the attachment size limit
          of your SMTP mail server and the recipient email provider.
      SMTP_Email_Server (String):
          The SMTP email server that will deliver the email.
      User {String}:
          The user which will log in to the SMTP email server.
      Password {String}:
          The user password used to connect to the SMTP email server (if necessary)."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.SendEmailWithZipFileAttachment_server(*gp_fixargs((To, From, Subject, Text, Zip_File, Max_File_Size__MB_, SMTP_Email_Server, User, Password), True)))
        return retval
    except Exception, e:
        raise e


# Printing toolset
@gptooldoc('ExportWebMap_server', None)
def ExportWebMap(Web_Map_as_JSON=None, Output_File=None, Format=None, Layout_Templates_Folder=None, Layout_Template=None):
    """ExportWebMap_server(Web_Map_as_JSON, Output_File, {Format}, {Layout_Templates_Folder}, {Layout_Template})

        This tool takes the state of a web application (for example, included services,
        layer visibility settings, and client-side graphics) and returns a printable
        page layout or basic map of the specified area of interest.The input for Export
        Web Map is a piece of text in JavaScript object notation
        (JSON) format describing the layers, graphics, and other settings in the web
        map. The JSON must be structured according to the ExportWebMap specification in
        the ArcGIS Help.This tool is shipped with ArcGIS Server to support web services
        for printing,
        including the preconfigured service named PrintingTools. The ArcGIS web APIs for
        JavaScript, Flex and Silverlight use the PrintingTools service to generate
        images for simple map printing.

     INPUTS:
      Web_Map_as_JSON (String):
          A JSON representation of the state of the map to be exported as it appears in
          the web application. See the ExportWebMap specification in the ArcGIS Help to
          understand how this text should be formatted. The ArcGIS web APIs (for
          JavaScript, Flex, Silverlight, etc.) allow developers to easily get this JSON
          string from the map.
      Format {String}:
          The format in which the map image for printing will be delivered. The following
          strings are accepted.For example:

          * PNG8 ( default if the parameter is left blank )

          * PDF

          * PNG32

          * JPG

          * GIF

          * EPS

          * SVG

          * SVGZ
      Layout_Templates_Folder {Folder}:
          Full path to the folder where map documents (.MXDs) to be used as Layout
          Templates are located. The default location is
          <install_directory>\Templates\ExportWebMapTemplates.
      Layout_Template {String}:
          Either a name of a template from the list or the keyword MAP_ONLY. When MAP_ONLY
          is chosen or an empty string is passed in, the output map does not contain any
          page layout surroundings (for example title, legends, scale bar, and so forth)

     OUTPUTS:
      Output_File (File):
          Output file name. The extension of the file depends on the output file format."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ExportWebMap_server(*gp_fixargs((Web_Map_as_JSON, Output_File, Format, Layout_Templates_Folder, Layout_Template), True)))
        return retval
    except Exception, e:
        raise e


# Publishing toolset
@gptooldoc('SignInToPortal_server', None)
def SignInToPortal(username=None, password=None, portal_url=None):
    """SignInToPortal_server(username, password, portal_url)

        Allows you to sign in to portals. If you are publishing to an ArcGIS Online
        portal you need to be signed in to ArcGIS Online in order to publish. For those
        organizations that would like to use ArcGIS Online behind the firewall or in
        their own private cloud, there is a version that you can install and use on your
        own computer networks. It is called Portal for ArcGIS.

     INPUTS:
      username (String):
          The esri global account user name.
      password (Encrypted String):
          The esri global account password.
      portal_url (String):
          The URL for the ArcGIS Online portal for which you want to make a connection.
          For example, http://www.arcgis.com/. The forward slash at the end of the URL
          must be included. The default value is URL for the ArcGIS portal currently
          chosen for the user."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.SignInToPortal_server(*gp_fixargs((username, password, portal_url), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('SignOutFromPortal_server', None)
def SignOutFromPortal():
    """SignOutFromPortal_server()

        Signs out from the portal that you are currently signed in to. For those
        organizations that would like to use ArcGIS Online behind the firewall or in
        their own private cloud, there is a version that you can install and use on your
        own computer networks. It is called Portal for ArcGIS."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.SignOutFromPortal_server(*gp_fixargs((), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('StageService_server', None)
def StageService(in_service_definition_draft=None, out_service_definition=None):
    """StageService_server(in_service_definition_draft, out_service_definition)

        Stages a service definition. A staged service definition (.sd) file contains
        all the necessary information needed to publish a GIS service, including data
        that must be copied to the server because it does not appear in the server's
        data store.

     INPUTS:
      in_service_definition_draft (File):
          Input draft service definition. Service definition drafts can be created using
          ArcGIS for Desktop. See the help topic About draft services for more
          information. You can also use the arcpy.mapping function CreateMapSDDraft to
          create draft service definitions.Once staged, the input draft service definition
          is deleted.

     OUTPUTS:
      out_service_definition (File):
          Resulting service definition. The default is to write the service definition to
          the same directory as the draft service definition"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.StageService_server(*gp_fixargs((in_service_definition_draft, out_service_definition), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('UploadServiceDefinition_server', None)
def UploadServiceDefinition(in_sd_file=None, in_server=None, in_service_name=None, in_cluster=None, in_folder_type=None, in_folder=None, in_startupType=None, in_override=None, in_my_contents=None, in_public=None, in_organization=None, in_groups=None):
    """UploadServiceDefinition_server(in_sd_file, in_server, {in_service_name}, {in_cluster}, {in_folder_type}, {in_folder}, {in_startupType}, {in_override}, {in_my_contents}, {in_public}, {in_organization}, {in_groups;in_groups...})

        Uploads and publishes a GIS service to a specified GIS server based on a staged
        service definition (.sd) file.

     INPUTS:
      in_sd_file (File):
          The service definition (.sd) contains all the information needed to publish a
          GIS service.
      in_server (ServerConnection):
          You can use ArcGIS for Server connections listed under the GIS Servers node in
          the Catalog window, or you can navigate to a different folder where you might
          have server connection files stored.If you are connecting to ArcGIS Online, make
          sure you type My Hosted Services
          for the server connection with each word capitalized and a space between each
          word.
      in_service_name {String}:
          Use this to override the service name currently specified in the service
          definition with a new name.
      in_cluster {String}:
          Use this if you want to change the cluster to which the service has been
          assigned. You must choose from clusters that are available on the specified
          server.
      in_folder_type {String}:
          Folder type is used to determine the source for the folder. The default is to
          get a folder from the service definition. You can also choose to get a list of
          folders already existing on the specified server, or you can specify a new
          folder to be created once you publish this service.

          * NEW—Use this to create a new folder.

          * EXISTING—Use this to specify a folder that exists on the server.

          * FROM_SERVICE_DEFINITION—Use the folder already specified in the service
          definition. This is the default.
      in_folder {String}:
          Use this to specify the folder for the service. The default is to use the folder
          specified in the service definition. If you chose the NEW folder type, you use
          this parameter to enter a new folder name. If you chose the EXISTING folder
          type, you can choose from the existing folders on the server.
      in_startupType {Boolean}:
          Use this to determine the start/stop state of the service immediately after
          publishing.

          * STARTED—The service starts immediately after publishing.

          * STOPPED—The service does not start after publishing. You will have to start
          the service manually.
      in_override {Boolean}:
          Use this parameter if you want to override the sharing properties set in the
          service definition. These properties define if, and how, you are sharing your
          service with ArcGIS Online. Sharing your service with ArcGIS Online exposes it
          for others to use.

          * OVERRIDE_DEFINITION—Override the sharing properties set in the service
          definition with new values.

          * USE_DEFINITION—The sharing properties currently set in the service definition
          will be used when the service is published. This is the default.
          You must be logged in to ArcGIS Online in order to override sharing properties.
      in_my_contents {Boolean}:
          All shared services are available through My Contents. Even if you only want to
          share with a specific group in your organization, the service will also be
          shared through My Contents.

          * SHARE_ONLINE—Shares the service on ArcGIS Online. The service will be listed
          under My Content.

          * NO_SHARE_ONLINE—The service will not be shared on ArcGIS Online and will be
          inaccessible to other ArcGIS Online users and clients on the web.
          You must be logged in to ArcGIS Online in order to override sharing properties.
      in_public {Boolean}:
          Choose whether or not your service will be available to the public.

          * PUBLIC—Share the service with the public.

          * PRIVATE—Do not share the service with the public.
          You must be logged in to ArcGIS Online in order to override sharing properties.
      in_organization {Boolean}:
          You can share your service with your organization.

          * SHARE_ORGANIZATION—Share the service with your organization.

          * NO_SHARE_ORGANIZATION—Do not share the service with your organization.
          You must be logged in to ArcGIS Online in order to override sharing properties.
      in_groups {String}:
          A list of group names with which to share the service.You must be logged in to
          ArcGIS Online in order to override sharing properties."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.UploadServiceDefinition_server(*gp_fixargs((in_sd_file, in_server, in_service_name, in_cluster, in_folder_type, in_folder, in_startupType, in_override, in_my_contents, in_public, in_organization, in_groups), True)))
        return retval
    except Exception, e:
        raise e


# End of generated toolbox code
del gptooldoc, gp, gp_fixargs, convertArcObjectToPythonObject