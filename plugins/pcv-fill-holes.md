# pcv-fill-holes

* accepts: idc.api.ImageClassificationData, idc.api.ObjectDetectionData, idc.api.ImageSegmentationData
* generates: idc.api.ImageClassificationData, idc.api.ObjectDetectionData, idc.api.ImageSegmentationData

Flood fills holes in a binary image. A binary image is required. You can use the 'grayscale-to-binary' for the conversion.

```
usage: pcv-fill-holes [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                      [-N LOGGER_NAME] [--skip] [-a {both,image,annotations}]

Flood fills holes in a binary image. A binary image is required. You can use
the 'grayscale-to-binary' for the conversion.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -a {both,image,annotations}, --apply_to {both,image,annotations}
                        Where to apply the filter to. (default: image)
```
