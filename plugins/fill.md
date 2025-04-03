# fill

* accepts: idc.api.ImageClassificationData, idc.api.ObjectDetectionData, idc.api.ImageSegmentationData
* generates: idc.api.ImageClassificationData, idc.api.ObjectDetectionData, idc.api.ImageSegmentationData

Identifies objects and fills objects that are less than the specified 'size' in pixels. A binary image is required. You can use the 'grayscale-to-binary' for the conversion.

```
usage: fill [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
            [-s SIZE]

Identifies objects and fills objects that are less than the specified 'size'
in pixels. A binary image is required. You can use the 'grayscale-to-binary'
for the conversion.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -s SIZE, --size SIZE  The minimum object area size in pixels. (default: 1)
```
