import argparse
import numpy as np
from typing import List

from idc.api import ImageClassificationData, ObjectDetectionData, ImageSegmentationData, flatten_list, make_list, \
    safe_deepcopy, array_to_image, ensure_grayscale, grayscale_required_info
from plantcv import plantcv as pcv
from seppl.io import Filter
from wai.logging import LOGGING_WARNING


class Erode(Filter):
    """
    Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel if conditions set in kernel are true, otherwise removes pixel.
    """

    def __init__(self, kernel_size: int = None, num_iterations: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param kernel_size: the kernel size to use
        :type kernel_size: int
        :param num_iterations: the number of iterations to perform
        :type num_iterations: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.kernel_size = kernel_size
        self.num_iterations = num_iterations

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "erode"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel if conditions set in kernel are true, otherwise removes pixel. " + grayscale_required_info()

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageClassificationData, ObjectDetectionData, ImageSegmentationData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ImageClassificationData, ObjectDetectionData, ImageSegmentationData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-k", "--kernel_size", type=int, help="The kernel size, must greater than 1 to have an effect.", default=3, required=False)
        parser.add_argument("-i", "--num_iterations", type=int, help="The number of iterations to perform.", default=1, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.kernel_size = ns.kernel_size
        self.num_iterations = ns.num_iterations

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.kernel_size is None:
            self.kernel_size = 3
        if self.kernel_size < 1:
            raise Exception("Kernel size must be at least 1, current: %s" % str(self.kernel_size))
        if self.num_iterations is None:
            self.num_iterations = 1
        if self.num_iterations < 1:
            raise Exception("# iterations must be at least 1, current: %s" % str(self.num_iterations))

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        # nothing to do?
        if self.kernel_size == 1:
            return flatten_list(make_list(data))

        result = []
        for item in make_list(data):
            image = ensure_grayscale(item.image, logger=self.logger())
            array_new = pcv.erode(np.asarray(image), self.kernel_size, self.num_iterations)
            item_new = type(item)(image_name=item.image_name,
                                  data=array_to_image(array_new, item.image_format)[1].getvalue(),
                                  metadata=safe_deepcopy(item.get_metadata()),
                                  annotation=safe_deepcopy(item.annotation))
            result.append(item_new)

        return flatten_list(result)
