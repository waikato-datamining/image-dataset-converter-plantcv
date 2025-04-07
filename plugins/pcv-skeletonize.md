# pcv-skeletonize

* accepts: idc.api.ImageClassificationData, idc.api.ObjectDetectionData, idc.api.ImageSegmentationData
* generates: idc.api.ImageClassificationData, idc.api.ObjectDetectionData, idc.api.ImageSegmentationData

Reduces binary objects to 1 pixel wide representations (skeleton). A binary image is required. You can use the 'grayscale-to-binary' for the conversion.

```
usage: pcv-skeletonize [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                       [-N LOGGER_NAME] [--skip] [-p] [-s SIZE]

Reduces binary objects to 1 pixel wide representations (skeleton). A binary
image is required. You can use the 'grayscale-to-binary' for the conversion.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip
  -p, --prune           Whether to prune the skeleton. (default: False)
  -s SIZE, --size SIZE  The size to get pruned off each branch. (default: 50)
```
