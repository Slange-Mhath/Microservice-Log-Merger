# Microservice Log Merger (MLM)

## A python script which will merge the different json outputs of Microservices.
Currently our MLM is supporting [Siegfried](https://github.com/richardlehane/siegfried), [Exif](https://github.com/exiftool/exiftool), and more to come. 

## USAGE

`git clone https://github.com/Slange-Mhath/Microservice-Log-Merger`

### Merging only the base output with the Siegfried output:

`python3 main.py -base_log_path "my_base_file_.json" -sf_log "my-siegfried_output.log"  -dest "my_finally_merged_file.json"`


**-base_log_path**  
Specify the path to the base log file which should be enriched with the Siegfried log. Please ensure that your file follows the example structure specified [here](#base_file).  
**-sf_log**  
Specify the Siegfried file which should be merged into the base log. Please ensure that your file follows the example structure specified [here](#siegfried-output).  
**-dest**  
Specify the file path to the file where the merged output should be written to. 

### Optional parameters:

The MLM currently supports [Exif](https://github.com/exiftool/exiftool) as well. To add the Exif tool output to the merged file add the following parameters.  

**-exif**  
Specify the Exif file which should be added as key to the merged log. Please ensure that your file follows the example structure specified [here](#exif-output).

**-f_keys_to_delete**  
This is again an optional parameter. It can be used to specify a file path to a file which can contain different key names to delete them from the Exif log file to decrease verbosity. Please stick to the recommended file structure specified [here](#keys-to-delete).  


Running the script with every optional parameter would look like this:  
```python3 main.py -base_log_path "base_file.json" -sf_log "siegfried.log" -exif "exif.log" -dest "merged_log.json" -f_keys_to_del "key_list.log"```

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
### Keys to Delete 

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



