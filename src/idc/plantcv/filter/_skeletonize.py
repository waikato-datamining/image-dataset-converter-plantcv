from typing import List

import numpy as np
from idc.api import ImageClassificationData, ObjectDetectionData, ImageSegmentationData, flatten_list, make_list, \
    safe_deepcopy, array_to_image, ensure_binary, binary_required_info
from plantcv import plantcv as pcv
from seppl.io import Filter


class Skeletonize(Filter):
    """
    Reduces binary objects to 1 pixel wide representations (skeleton).
    """

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

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            image = ensure_binary(item.image, logger=self.logger())
            array_new = pcv.morphology.skeletonize(np.asarray(image).astype(np.uint8))
            item_new = type(item)(image_name=item.image_name,
                                  data=array_to_image(array_new, item.image_format)[1].getvalue(),
                                  metadata=safe_deepcopy(item.get_metadata()),
                                  annotation=safe_deepcopy(item.annotation))
            result.append(item_new)

        return flatten_list(result)
