import argparse
from typing import List

import numpy as np
from idc.api import ImageClassificationData, ObjectDetectionData, ImageSegmentationData, flatten_list, make_list, \
    safe_deepcopy, array_to_image, ensure_binary, binary_required_info
from plantcv import plantcv as pcv
from seppl.io import Filter
from wai.logging import LOGGING_WARNING


class Skeletonize(Filter):
    """
    Reduces binary objects to 1 pixel wide representations (skeleton).
    """

    def __init__(self, prune: bool = None, size: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param prune: whether to prune the skeleton
        :type prune: bool
        :param size: the size to get pruned off each branch
        :type size: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.prune = prune
        self.size = size

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "skeletonize"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Reduces binary objects to 1 pixel wide representations (skeleton). " + binary_required_info()

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
        parser.add_argument("-p", "--prune", action="store_true", help="Whether to prune the skeleton.")
        parser.add_argument("-s", "--size", type=int, help="The size to get pruned off each branch.", default=50, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.prune = ns.prune
        self.size = ns.size

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.prune is None:
            self.prune = False
        if self.size is None:
            self.size = 1
        if self.size < 1:
            raise Exception("Pruning size must be at least 1, current: %s" % str(self.size))

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            image = ensure_binary(item.image, logger=self.logger())
            array = np.asarray(image).astype(np.uint8)
            array_new = pcv.morphology.skeletonize(array)
            if self.prune:
                array_new, _, _ = pcv.morphology.prune(skel_img=array_new, size=self.size, mask=array)
            item_new = type(item)(image_name=item.image_name,
                                  data=array_to_image(array_new, item.image_format)[1].getvalue(),
                                  metadata=safe_deepcopy(item.get_metadata()),
                                  annotation=safe_deepcopy(item.annotation))
            result.append(item_new)

        return flatten_list(result)
