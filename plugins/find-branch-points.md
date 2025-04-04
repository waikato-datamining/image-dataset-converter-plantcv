# find-branch-points

* accepts: idc.api.ImageClassificationData, idc.api.ObjectDetectionData, idc.api.ImageSegmentationData
* generates: idc.api.ObjectDetectionData

Finds branch points in a skeletonized image and forwards them as object detection annotations. A binary image is required. You can use the 'grayscale-to-binary' for the conversion.

```
usage: find-branch-points [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                          [-N LOGGER_NAME]

Finds branch points in a skeletonized image and forwards them as object
detection annotations. A binary image is required. You can use the 'grayscale-
to-binary' for the conversion.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
```
