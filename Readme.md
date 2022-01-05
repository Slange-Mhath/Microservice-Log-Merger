# Microservice Log Merger (MLM)

## A python script which will merge the different json outputs of Microservices.
Currently our MLM is supporting [Siegfried](https://github.com/richardlehane/siegfried), [Exif](https://github.com/exiftool/exiftool), and more to come. 

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

**-f_key_list**  
This parameter is <strong>mandatory if the mediainfo_log_path parameter is added. </strong> It should be used to specify a file path to a file which should contain the name of those keys from the log, which we want to merge.
Please stick to the recommended file structure specified [here](#key-list).  


Running the script with every optional parameter would look like this:  
```python3 main.py -base_log_path "base_file.json" -sf_log_path "siegfried.log" -exif_log_path "exif.log" -dest_file_path "merged_log.json" -f_keys_to_del_path "key_list.log"```

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



