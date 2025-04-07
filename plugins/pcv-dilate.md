# pcv-dilate

* accepts: idc.api.ImageClassificationData, idc.api.ObjectDetectionData, idc.api.ImageSegmentationData
* generates: idc.api.ImageClassificationData, idc.api.ObjectDetectionData, idc.api.ImageSegmentationData

Performs morphological 'dilation' filtering. Adds pixel to center of kernel if conditions set in kernel are true. A grayscale image is required. You can use the 'rgb-to-grayscale' for the conversion.

```
usage: pcv-dilate [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                  [-N LOGGER_NAME] [--skip] [-k KERNEL_SIZE]
                  [-i NUM_ITERATIONS]

Performs morphological 'dilation' filtering. Adds pixel to center of kernel if
conditions set in kernel are true. A grayscale image is required. You can use
the 'rgb-to-grayscale' for the conversion.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip
  -k KERNEL_SIZE, --kernel_size KERNEL_SIZE
                        The kernel size, must greater than 1 to have an
                        effect. (default: 3)
  -i NUM_ITERATIONS, --num_iterations NUM_ITERATIONS
                        The number of iterations to perform. (default: 1)
```
