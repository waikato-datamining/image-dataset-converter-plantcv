# pcv-erode

* accepts: idc.api.ImageClassificationData, idc.api.ObjectDetectionData, idc.api.ImageSegmentationData
* generates: idc.api.ImageClassificationData, idc.api.ObjectDetectionData, idc.api.ImageSegmentationData

Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel if conditions set in kernel are true, otherwise removes pixel. A grayscale image is required. You can use the 'rgb-to-grayscale' for the conversion.

```
usage: pcv-erode [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [-N LOGGER_NAME] [--skip] [-a {both,image,annotations}]
                 [-o {as-is,binary,grayscale,rgb}] [-k KERNEL_SIZE]
                 [-i NUM_ITERATIONS]

Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel
if conditions set in kernel are true, otherwise removes pixel. A grayscale
image is required. You can use the 'rgb-to-grayscale' for the conversion.

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
  -o {as-is,binary,grayscale,rgb}, --output_format {as-is,binary,grayscale,rgb}
                        The image format to generate as output. (default: as-
                        is)
  -k KERNEL_SIZE, --kernel_size KERNEL_SIZE
                        The kernel size, must greater than 1 to have an
                        effect. (default: 3)
  -i NUM_ITERATIONS, --num_iterations NUM_ITERATIONS
                        The number of iterations to perform. (default: 1)
```
