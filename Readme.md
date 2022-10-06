# Microservice Log Merger (MLM)

## A python script which will merge the different json outputs of Microservices.
Currently our MLM is supporting [Siegfried](https://github.com/richardlehane/siegfried), [Exif](https://github.com/exiftool/exiftool), and more to come. 


## Requirements

This tool is developed and tested on Python 3.9

- SQLAlchemy
  ```python -m pip install SQLAlchemy```
  
- Memory-profiler
  ```python -m pip install memory-profiler```

- Psycopg2
  ```python -m pip install psycopg2-binary``

### Database:

The MLM uses the postgresql db, which should be set up like this:

- Create database mlmdb
- Create user mlm with encrypted password
- Grant all privileges (or transfer ownership) on database mlmdb to mlm
- On Linux adjust ```/var/lib/pgsql/data/pg_hba.conf``` at the bottom to allow verification via password rather than ident or trust


## USAGE

`git clone https://github.com/Slange-Mhath/Microservice-Log-Merger`

### Merging only the base output with the Siegfried output:

`python3 main.py -base_log_path "my_base_file_.json" -sf_log_path "my-siegfried_output.log"  -dest_file_path "my_finally_merged_file.json"`


**-base_log_path**  
Specify the path to the base log file which should be enriched with the Siegfried log. Please ensure that your file follows the example structure specified [here](#base_file).  
**-sf_log_path**  
Specify the Siegfried file which should be merged into the base log. Please ensure that your file follows the example structure specified [here](#siegfried-output).  
**-dest_file_path**  
Specify the file path to the file where the merged output should be written to. 

### Optional parameters:

The MLM currently supports [Exif](https://github.com/exiftool/exiftool), and [Mediainfo](https://mediaarea.net/en/MediaInfo) as well. To add the Exif tool output to the merged file add the following parameters.  

**-pdf_analyser_log_path**

Identify if PDF files are images and attach the information in the output. Please ensure that your file follows the example structure specified [here](#pdf-analyser-log-output).

**-occurrence_of_keys**

To display a statistic which fields and how often they occur in the merged log set this to True (-occurrence_of_keys "True"). Otherwise the default value will be False and thus the statistic not calculated or shown.

**-exif_log_path**  
Specify the Exif file which should be added as key to the merged log. Please ensure that your file follows the example structure specified [here](#exif-output).

**-f_key_list**  
This parameter is <strong>mandatory if the exif_log_path parameter is added. </strong> It should be used to specify a file path to a file which should contain the name of those keys from the log, which we want to merge.
Please stick to the recommended file structure specified [here](#key-list).  

To add the Mediainfo output to the merged file use the following parameters: 

**-mediainfo_log_path**  
Specify the Exif file which should be added as key to the merged log. Please ensure that your file follows the example structure specified [here](#exif-output).

**-jpylyzer_log_path**  
Specify the Jpylzer file which should be added as key to the merged log. Please ensure that your file follows the example structure specified [here](#jpylyzer-output).


**-f_key_list**  
This parameter is <strong>mandatory if the mediainfo_log_path parameter is added. </strong> It should be used to specify a file path to a file which should contain the name of those keys from the log, which we want to merge.
Please stick to the recommended file structure specified [here](#key-list).  


Running the script with every optional parameter would look like this:  
```python3 main.py -base_log_path "base_file.json" -sf_log_path "siegfried.log" -exif_log_path "exif.log" -mediainfo_log "mediainfo.log" -jpylyzer_log "jpylyzer.log -dest_file_path "merged_log.json" -f_keys_to_del_path "key_list.log"```

## File structures

### base_file
```json
{"files": [
        {"timestamp": "2021-06-03T11:06:26+0100",
         "file": {"inode": "155", "mode": "664", "gid": "1004",
                  "uid": "1004", "size": "204800",
                  "mtime": "2020-01-18T16:51:03+0000",
                  "path": "my/path",
                  "hash": {
                      "sha512": "6d9990",
                      "sha1": "ff"}}}
    ]}
```

### Siegfried Output
```json
{
   "siegfried":"1.9.1",
   "scandate":"2021-06-28T12:40:03+01:00",
   "signature":"default.sig",
   "created":"2020-10-06T19:13:40+02:00",
   "identifiers":[
      {
         "name":"pronom",
         "details":"DROID_SignatureFile_V97.xml; container-signature-20201001.xml"
      }
   ],
   "files":[
      {
         "filename":"/my_path",
         "filesize":42,
         "modified":"2020-01-18T16:51:03Z",
         "errors":"",
         "matches":[
            {
               "ns":"pronom",
               "id":"UNKNOWN",
               "format":"",
               "version":"",
               "mime":"",
               "basis":"",
               "warning":"no match"
            }
         ]
      }
   ]
}
```

### Pdf Analyser log Output
```json
{ "test_pdfs/602351290.pdf": 
    {"isText": true, "tool_version_info": "\nPyMuPDF 1.19.1: Python bindings for the MuPDF 1.19.0 library.\nVersion date: 2021-10-23 00:00:01.\nBuilt for Python 3.9 on darwin (64-bit).\n"}, 
  "test_pdfs/A+study+of+the+Middle+English+treatises+on+grammar+(Part+2+-+file+1)": 
    {"isText": false, "tool_version_info": "\nPyMuPDF 1.19.1: Python bindings for the MuPDF 1.19.0 library.\nVersion date: 2021-10-23 00:00:01.\nBuilt for Python 3.9 on darwin (64-bit).\n"}, 
  "test_pdfs/chapter+3+-+chapter+4": {"isText": false, "tool_version_info": "\nPyMuPDF 1.19.1: Python bindings for the MuPDF 1.19.0 library.\nVersion date: 2021-10-23 00:00:01.\nBuilt for Python 3.9 on darwin (64-bit).\n"}
}
```


### Exif Output
```json
[{
  "SourceFile": "my_path",
  "ExifToolVersion": 29.09,
  "FileName": "my_file.zip",
  "Directory": "/my_path/my_file.zip",
  "FileSize": "3893 KiB",
  "FileModifyDate": "2018:03:14 23:09:34+00:00",
  "FileAccessDate": "2018:03:14 23:09:34+00:00",
  "FileInodeChangeDate": "2018:03:14 23:09:34+00:00",
  "FilePermissions": "rw-rw-r--",
  "FileType": "ZIP",
  "FileTypeExtension": "zip",
  "MIMEType": "application/zip",
  "ZipRequiredVersion": 20,
  "ZipBitFlag": 0,
  "ZipCompression": "Deflated",
  "ZipModifyDate": "2017:01:04 12:21:36",
  "ZipCRC": "0xaaf21001",
  "ZipCompressedSize": 1720,
  "ZipUncompressedSize": 4132,
  "ZipFileName": "my_file.m",
  "Warning": "[minor] Use the Duplicates option to extract tags for all 7 files"
},
{
  "SourceFile": "/my_other_file",
  "ExifToolVersion": 14.16,
  "FileName": "Belinda_Blinked.xlsx",
  "Directory": "/my_file_path/my_other_file",
  "FileSize": "1080 KiB",
  "FileModifyDate": "2018:03:14 18:57:25+00:00",
  "FileAccessDate": "2018:03:14 18:57:25+00:00",
  "FileInodeChangeDate": "2018:03:14 18:57:25+00:00",
  "FilePermissions": "rw-r--r--",
  "FileType": "XLSX",
  "FileTypeExtension": "xlsx",
  "MIMEType": "",
  "ZipRequiredVersion": 20,
  "ZipBitFlag": "0x0006",
  "ZipCompression": "Deflated",
  "ZipModifyDate": "1980:01:01 00:00:00",
  "ZipCRC": "0x78c4a176",
  "ZipCompressedSize": 448,
  "ZipUncompressedSize": 4226,
  "ZipFileName": "[Content_Types].xml",
  "PreviewImage": "(Binary data 29920 bytes, use -b option to extract)",
  "Application": "Microsoft Macintosh Excel",
  "DocSecurity": "None",
  "ScaleCrop": "No",
  "HeadingPairs": ["Worksheets",23],
  "TitlesOfParts": ["Key","1_self(re)discovery","2_likecomfortableself","3_Timeout","4_Transitions"],
  "Company": "",
  "LinksUpToDate": "No",
  "SharedDoc": "No",
  "HyperlinksChanged": "No",
  "AppVersion": 14.0300,
  "Creator": "Rocky Flintstone",
  "LastModifiedBy": "Rocky Flintstone",
  "CreateDate": "2016:03:11 15:17:02Z",
  "ModifyDate": "2016:05:23 09:53:07Z"
}]
```

### Mediainfo

```json
[{
        "media": {
            "@ref": "./window_one.jpg",
            "track": [{
                    "@type": "General",
                    "Count": "331",
                    "StreamCount": "1",
                    "StreamKind": "General",
                    "StreamKind_String": "General",
                    "StreamKindID": "0",
                    "ImageCount": "1",
                    "Image_Format_List": "JPEG",
                    "Image_Format_WithHint_List": "JPEG",
                    "Image_Codec_List": "JPEG",
                    "CompleteName": "./window_one.jpg",
                    "FolderName": ".",
                    "FileNameExtension": "window_one.jpg",
                    "FileName": "window_one",
                    "FileExtension": "jpg",
                    "Format": "JPEG",
                    "Format_String": "JPEG",
                    "Format_Extensions": "h3d jpeg jpg jpe jps mpo",
                    "Format_Commercial": "JPEG",
                    "InternetMediaType": "image/jpeg",
                    "FileSize": "11162",
                    "FileSize_String": "10.9 KiB",
                    "FileSize_String1": "11 KiB",
                    "FileSize_String2": "11 KiB",
                    "FileSize_String3": "10.9 KiB",
                    "FileSize_String4": "10.90 KiB",
                    "StreamSize": "0",
                    "StreamSize_String": "0.00 Byte (0%)",
                    "StreamSize_String1": " Byte0",
                    "StreamSize_String2": "0.0 Byte",
                    "StreamSize_String3": "0.00 Byte",
                    "StreamSize_String4": "0.000 Byte",
                    "StreamSize_String5": "0.00 Byte (0%)",
                    "StreamSize_Proportion": "0.00000",
                    "File_Modified_Date": "UTC 2021-01-31 15:12:31",
                    "File_Modified_Date_Local": "2021-01-31 15:12:31"
                },
                {
                    "@type": "Image",
                    "Count": "124",
                    "StreamCount": "1",
                    "StreamKind": "Image",
                    "StreamKind_String": "Image",
                    "StreamKindID": "0",
                    "Format": "JPEG",
                    "Format_String": "JPEG",
                    "Format_Commercial": "JPEG",
                    "InternetMediaType": "image/jpeg",
                    "Width": "461",
                    "Width_String": "461 pixels",
                    "Height": "252",
                    "Height_String": "252 pixels",
                    "ColorSpace": "YUV",
                    "ChromaSubsampling": "4:4:4",
                    "BitDepth": "8",
                    "BitDepth_String": "8 bits",
                    "Compression_Mode": "Lossy",
                    "Compression_Mode_String": "Lossy",
                    "StreamSize": "11162",
                    "StreamSize_String": "10.9 KiB (100%)",
                    "StreamSize_String1": "11 KiB",
                    "StreamSize_String2": "11 KiB",
                    "StreamSize_String3": "10.9 KiB",
                    "StreamSize_String4": "10.90 KiB",
                    "StreamSize_String5": "10.9 KiB (100%)",
                    "StreamSize_Proportion": "1.00000"
                }
            ]
        }
    },
    {
        "media": {
            "@ref": "/ORA4/PRD/REVIEW/ff/85/03/ff85037813a09ea793b4bc2d860324d65184c20f",
            "track": [{
                    "@type": "General",
                    "Count": "331",
                    "StreamCount": "1",
                    "StreamKind": "General",
                    "StreamKind_String": "General",
                    "StreamKindID": "0",
                    "ImageCount": "1",
                    "Image_Format_List": "JPEG",
                    "Image_Format_WithHint_List": "JPEG",
                    "Image_Codec_List": "JPEG",
                    "CompleteName": "./window_two.jpg",
                    "FolderName": ".",
                    "FileNameExtension": "window_two.jpg",
                    "FileName": "window_two",
                    "FileExtension": "jpg",
                    "Format": "JPEG",
                    "Format_String": "JPEG",
                    "Format_Extensions": "h3d jpeg jpg jpe jps mpo",
                    "Format_Commercial": "JPEG",
                    "InternetMediaType": "image/jpeg",
                    "FileSize": "9535",
                    "FileSize_String": "9.31 KiB",
                    "FileSize_String1": "9 KiB",
                    "FileSize_String2": "9.3 KiB",
                    "FileSize_String3": "9.31 KiB",
                    "FileSize_String4": "9.312 KiB",
                    "StreamSize": "0",
                    "StreamSize_String": "0.00 Byte (0%)",
                    "StreamSize_String1": " Byte0",
                    "StreamSize_String2": "0.0 Byte",
                    "StreamSize_String3": "0.00 Byte",
                    "StreamSize_String4": "0.000 Byte",
                    "StreamSize_String5": "0.00 Byte (0%)",
                    "StreamSize_Proportion": "0.00000",
                    "File_Modified_Date": "UTC 2021-01-31 15:13:09",
                    "File_Modified_Date_Local": "2021-01-31 15:13:09"
                },
                {
                    "@type": "Image",
                    "Count": "124",
                    "StreamCount": "1",
                    "StreamKind": "Image",
                    "StreamKind_String": "Image",
                    "StreamKindID": "0",
                    "Format": "JPEG",
                    "Format_String": "JPEG",
                    "Format_Commercial": "JPEG",
                    "InternetMediaType": "image/jpeg",
                    "Width": "461",
                    "Width_String": "461 pixels",
                    "Height": "252",
                    "Height_String": "252 pixels",
                    "ColorSpace": "YUV",
                    "ChromaSubsampling": "4:4:4",
                    "BitDepth": "8",
                    "BitDepth_String": "8 bits",
                    "Compression_Mode": "Lossy",
                    "Compression_Mode_String": "Lossy",
                    "StreamSize": "9535",
                    "StreamSize_String": "9.31 KiB (100%)",
                    "StreamSize_String1": "9 KiB",
                    "StreamSize_String2": "9.3 KiB",
                    "StreamSize_String3": "9.31 KiB",
                    "StreamSize_String4": "9.312 KiB",
                    "StreamSize_String5": "9.31 KiB (100%)",
                    "StreamSize_Proportion": "1.00000"
                }
            ]
        }
    }
]
```


### Jpylyzer

```json

{
  "jpylyzer": {
    "toolInfo": {
      "toolName": "jpylyzer",
      "toolVersion": "2.1.0"
    },
    "file": [
      {
        "fileInfo": {
          "fileName": "relax.jp2",
          "filePath": "/ORA/PRD/DATA/ora_var/fedora/objects/2008/0520/10/26/uuid_7a79f51b-509f-476f-b1d0-1466dbfd9c78",
          "fileSizeInBytes": 16298,
          "fileLastModified": "2022-01-18T11:45:43.227749"
        },
        "statusInfo": {
          "success": "True"
        },
        "isValid": "True",
        "tests": "",
        "properties": {
          "signatureBox": "",
          "fileTypeBox": {
            "br": "jp2",
            "minV": 0,
            "cL": "jp2"
          },
          "jp2HeaderBox": {
            "imageHeaderBox": {
              "height": 300,
              "width": 400,
              "nC": 3,
              "bPCSign": "unsigned",
              "bPCDepth": 8,
              "c": "jpeg2000",
              "unkC": "yes",
              "iPR": "no"
            },
            "colourSpecificationBox": {
              "meth": "Restricted ICC",
              "prec": 0,
              "approx": 0,
              "icc": {
                "profileSize": 278,
                "preferredCMMType": "",
                "profileVersion": "2.2.0",
                "profileClass": "Input Device Profile",
                "colourSpace": "RGB",
                "profileConnectionSpace": "XYZ",
                "dateTimeString": "2001/01/01, 00:00:00",
                "profileSignature": "acsp",
                "primaryPlatform": "",
                "embeddedProfile": "no",
                "profileCannotBeUsedIndependently": "no",
                "deviceManufacturer": "",
                "deviceModel": "",
                "transparency": "Transparent",
                "glossiness": "Glossy",
                "polarity": "Positive",
                "colour": "Colour",
                "renderingIntent": "Perceptual",
                "connectionSpaceIlluminantX": 0.9642,
                "connectionSpaceIlluminantY": 1,
                "connectionSpaceIlluminantZ": 0.8249,
                "profileCreator": "",
                "profileID": 0,
                "tag": [
                  "rTRC",
                  "gTRC",
                  "bTRC",
                  "rXYZ",
                  "gXYZ",
                  "bXYZ"
                ],
                "description": ""
              }
            },
            "resolutionBox": {
              "captureResolutionBox": {
                "vRcN": 9289,
                "vRcD": 32768,
                "hRcN": 9289,
                "hRcD": 32768,
                "vRcE": 4,
                "hRcE": 4,
                "vRescInPixelsPerMeter": 2834.78,
                "hRescInPixelsPerMeter": 2834.78,
                "vRescInPixelsPerInch": 72,
                "hRescInPixelsPerInch": 72
              }
            }
          },
          "contiguousCodestreamBox": {
            "siz": {
              "lsiz": 47,
              "rsiz": "ISO/IEC 15444-1",
              "xsiz": 400,
              "ysiz": 300,
              "xOsiz": 0,
              "yOsiz": 0,
              "xTsiz": 400,
              "yTsiz": 300,
              "xTOsiz": 0,
              "yTOsiz": 0,
              "numberOfTiles": 1,
              "csiz": 3,
              "ssizSign": [
                "unsigned",
                "unsigned",
                "unsigned"
              ],
              "ssizDepth": [
                8,
                8,
                8
              ],
              "xRsiz": [
                1,
                1,
                1
              ],
              "yRsiz": [
                1,
                1,
                1
              ]
            },
            "cod": {
              "lcod": 12,
              "precincts": "default",
              "sop": "no",
              "eph": "no",
              "order": "LRCP",
              "layers": 12,
              "multipleComponentTransformation": "yes",
              "levels": 5,
              "codeBlockWidth": 64,
              "codeBlockHeight": 64,
              "codingBypass": "no",
              "resetOnBoundaries": "no",
              "termOnEachPass": "no",
              "vertCausalContext": "no",
              "predTermination": "no",
              "segmentationSymbols": "no",
              "transformation": "5-3 reversible",
              "precinctSizeX": [
                32768,
                32768,
                32768,
                32768,
                32768,
                32768
              ],
              "precinctSizeY": [
                32768,
                32768,
                32768,
                32768,
                32768,
                32768
              ]
            },
            "qcd": {
              "lqcd": 19,
              "qStyle": "no quantization",
              "guardBits": 1,
              "epsilon": [
                10,
                11,
                11,
                12,
                11
              ]
            },
            "com": {
              "lcom": 14,
              "rcom": "ISO/IEC 8859-15 (Latin)",
              "comment": "Kakadu-3.2"
            },
            "ppmCount": 0,
            "plmCount": 0,
            "tileParts": {
              "tilePart": {
                "sot": {
                  "lsot": 10,
                  "isot": 0,
                  "psot": 15809,
                  "tpsot": 0,
                  "tnsot": 1
                },
                "pltCount": 0,
                "pptCount": 0
              }
            }
          },
          "compressionRatio": 22.09
        }
      },
      {
        "fileInfo": {
          "fileName": "sample1.jp2",
          "filePath": "/Users/sebastianlange/Documents/Oxford/work/Micorservices/jpylyzer/sample1.jp2",
          "fileSizeInBytes": 670265,
          "fileLastModified": "2022-10-04T10:54:06.873575"
        },
        "statusInfo": {
          "success": "True"
        },
        "isValid": "True",
        "tests": "",
        "properties": {
          "signatureBox": "",
          "fileTypeBox": {
            "br": "jp2",
            "minV": 0,
            "cL": "jp2"
          },
          "jp2HeaderBox": {
            "imageHeaderBox": {
              "height": 3701,
              "width": 2717,
              "nC": 3,
              "bPCSign": "unsigned",
              "bPCDepth": 8,
              "c": "jpeg2000",
              "unkC": "yes",
              "iPR": "no"
            },
            "colourSpecificationBox": {
              "meth": "Enumerated",
              "prec": 0,
              "approx": 0,
              "enumCS": "sRGB"
            }
          },
          "uuidInfoBox": {
            "uuidListBox": {
              "nU": 2,
              "uuid": [
                "6a706a70-6a70-6a70-6a70-6a706a706a70",
                "61626162-6162-6162-6162-616261626162"
              ]
            },
            "urlBox": {
              "version": 0,
              "loc": "http://www.openplanetsfoundation.org/"
            }
          },
          "xmlBox": {
            "xmpmeta": {
              "RDF": {
                "Description": [
                  {
                    "format": "image/jpeg"
                  },
                  {
                    "ColorSpace": 65535,
                    "NativeDigest": "256,257,258,259,262,274,277,284,530,531,282,283,296,301,318,319,529,532,306,270,271,272,305,315,33432;7EF15F60B74B2599BAEDB6749C30991A",
                    "PixelXDimension": 2717,
                    "PixelYDimension": 3701
                  },
                  {
                    "ColorMode": 3,
                    "History": ""
                  },
                  {
                    "BitsPerSample": {
                      "Seq": {
                        "li": 8
                      }
                    },
                    "Compression": 1,
                    "ImageLength": 3701,
                    "ImageWidth": 2717,
                    "NativeDigest": "256,257,258,259,262,274,277,284,530,531,282,283,296,301,318,319,529,532,306,270,271,272,305,315,33432;7EF15F60B74B2599BAEDB6749C30991A",
                    "Orientation": 1,
                    "PhotometricInterpretation": 2,
                    "PlanarConfiguration": 1,
                    "ResolutionUnit": 2,
                    "SamplesPerPixel": 4,
                    "Software": "Adobe Photoshop CS3 Windows",
                    "XResolution": "72/1",
                    "YCbCrSubSampling": "1 1",
                    "YResolution": "72/1"
                  },
                  {
                    "CreateDate": "2008-07-19T16:14:14-07:00",
                    "CreatorTool": "Adobe Photoshop CS3 Windows",
                    "MetadataDate": "2008-07-19T16:14:14-07:00",
                    "ModifyDate": "2008-07-19T16:14:14"
                  },
                  {
                    "DerivedFrom": {
                      "instanceID": "uuid:AC48AD726754DD11BA6DEACED58C77FA"
                    },
                    "DocumentID": "uuid:6200E56DE155DD118C3CED023B237FE5",
                    "InstanceID": "uuid:6300E56DE155DD118C3CED023B237FE5"
                  }
                ]
              }
            }
          },
          "contiguousCodestreamBox": {
            "siz": {
              "lsiz": 47,
              "rsiz": "ISO/IEC 15444-1",
              "xsiz": 2717,
              "ysiz": 3701,
              "xOsiz": 0,
              "yOsiz": 0,
              "xTsiz": 1024,
              "yTsiz": 1024,
              "xTOsiz": 0,
              "yTOsiz": 0,
              "numberOfTiles": 12,
              "csiz": 3,
              "ssizSign": [
                "unsigned",
                "unsigned",
                "unsigned"
              ],
              "ssizDepth": [
                8,
                8,
                8
              ],
              "xRsiz": [
                1,
                1,
                1
              ],
              "yRsiz": [
                1,
                1,
                1
              ]
            },
            "cod": {
              "lcod": 18,
              "precincts": "user defined",
              "sop": "yes",
              "eph": "yes",
              "order": "RPCL",
              "layers": 6,
              "multipleComponentTransformation": "yes",
              "levels": 5,
              "codeBlockWidth": 64,
              "codeBlockHeight": 64,
              "codingBypass": "no",
              "resetOnBoundaries": "no",
              "termOnEachPass": "no",
              "vertCausalContext": "no",
              "predTermination": "no",
              "segmentationSymbols": "yes",
              "transformation": "9-7 irreversible",
              "precinctSizeX": [
                128,
                128,
                128,
                128,
                256,
                256
              ],
              "precinctSizeY": [
                128,
                128,
                128,
                128,
                256,
                256
              ]
            },
            "qcd": {
              "lqcd": 35,
              "qStyle": "scalar expounded",
              "guardBits": 2,
              "mu": [
                1816,
                1770,
                1770,
                1724,
                1792
              ],
              "epsilon": [
                13,
                13,
                13,
                13,
                12
              ]
            },
            "com": {
              "lcom": 17,
              "rcom": "ISO/IEC 8859-15 (Latin)",
              "comment": "Jpylyzer demo"
            },
            "ppmCount": 0,
            "plmCount": 0,
            "tileParts": {
              "tilePart": [
                {
                  "sot": {
                    "lsot": 10,
                    "isot": 0,
                    "psot": 67161,
                    "tpsot": 0,
                    "tnsot": 1
                  },
                  "pltCount": 0,
                  "pptCount": 0
                },
                {
                  "sot": {
                    "lsot": 10,
                    "isot": 1,
                    "psot": 99064,
                    "tpsot": 0,
                    "tnsot": 1
                  },
                  "pltCount": 0,
                  "pptCount": 0
                },
                {
                  "sot": {
                    "lsot": 10,
                    "isot": 2,
                    "psot": 36130,
                    "tpsot": 0,
                    "tnsot": 1
                  },
                  "pltCount": 0,
                  "pptCount": 0
                },
                {
                  "sot": {
                    "lsot": 10,
                    "isot": 3,
                    "psot": 56048,
                    "tpsot": 0,
                    "tnsot": 1
                  },
                  "pltCount": 0,
                  "pptCount": 0
                },
                {
                  "sot": {
                    "lsot": 10,
                    "isot": 4,
                    "psot": 140022,
                    "tpsot": 0,
                    "tnsot": 1
                  },
                  "pltCount": 0,
                  "pptCount": 0
                },
                {
                  "sot": {
                    "lsot": 10,
                    "isot": 5,
                    "psot": 24008,
                    "tpsot": 0,
                    "tnsot": 1
                  },
                  "pltCount": 0,
                  "pptCount": 0
                },
                {
                  "sot": {
                    "lsot": 10,
                    "isot": 6,
                    "psot": 46691,
                    "tpsot": 0,
                    "tnsot": 1
                  },
                  "pltCount": 0,
                  "pptCount": 0
                },
                {
                  "sot": {
                    "lsot": 10,
                    "isot": 7,
                    "psot": 62671,
                    "tpsot": 0,
                    "tnsot": 1
                  },
                  "pltCount": 0,
                  "pptCount": 0
                },
                {
                  "sot": {
                    "lsot": 10,
                    "isot": 8,
                    "psot": 26306,
                    "tpsot": 0,
                    "tnsot": 1
                  },
                  "pltCount": 0,
                  "pptCount": 0
                },
                {
                  "sot": {
                    "lsot": 10,
                    "isot": 9,
                    "psot": 45614,
                    "tpsot": 0,
                    "tnsot": 1
                  },
                  "pltCount": 0,
                  "pptCount": 0
                },
                {
                  "sot": {
                    "lsot": 10,
                    "isot": 10,
                    "psot": 38428,
                    "tpsot": 0,
                    "tnsot": 1
                  },
                  "pltCount": 0,
                  "pptCount": 0
                },
                {
                  "sot": {
                    "lsot": 10,
                    "isot": 11,
                    "psot": 25064,
                    "tpsot": 0,
                    "tnsot": 1
                  },
                  "pltCount": 0,
                  "pptCount": 0
                }
              ]
            }
          },
          "compressionRatio": 45.01
        }
      }
    ]
  }
}

```



### Key list

This file contains the superficial keys. Please specify one key name per line.
```
HyperlinksChanged
LastModifiedBy
LinksUpToDate
```

## Note for future development

This script uses dict comprehensions. It basically looks for matching keys in both logs and adds them together. 
Therefore its important that the matching_key parameters in the different functions are existent in the respective log file and specified correctly.
Out of convenience we are currently using the filename for this matching key. However it is important to mention that the name of the key where the filename is stored might be different.
E.g. our base file stores the filename under ***path*** while Siegfried uses ***filename*** and Exif ***SourceFile***.



