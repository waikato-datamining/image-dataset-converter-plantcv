import argparse
import numpy as np
from typing import List

from idc.api import ImageClassificationData, ObjectDetectionData, ImageSegmentationData, flatten_list, make_list, \
    safe_deepcopy, array_to_image, ensure_binary, binary_required_info
from plantcv import plantcv as pcv
from seppl.io import Filter
from wai.logging import LOGGING_WARNING


class Fill(Filter):
    """
    Identifies objects and fills objects that are less than the specified 'size' in pixels.
    """

    def __init__(self, size: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param size: the minimum object area size
        :type size: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.size = size

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "pcv-fill"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Identifies objects and fills objects that are less than the specified 'size' in pixels. " + binary_required_info()

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
        parser.add_argument("-s", "--size", type=int, help="The minimum object area size in pixels.", default=1, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.size = ns.size

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.size is None:
            self.size = 1
        if self.size < 1:
            raise Exception("Minimum object area size must be at least 1, current: %s" % str(self.size))

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            image = ensure_binary(item.image, logger=self.logger())
            array_new = pcv.fill(np.asarray(image).astype(np.uint8), self.size)
            item_new = type(item)(image_name=item.image_name,
                                  data=array_to_image(array_new, item.image_format)[1].getvalue(),
                                  metadata=safe_deepcopy(item.get_metadata()),
                                  annotation=safe_deepcopy(item.annotation))
            result.append(item_new)

        return flatten_list(result)
