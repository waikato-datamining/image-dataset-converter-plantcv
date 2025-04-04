from typing import List

import numpy as np
from idc.api import ImageClassificationData, ObjectDetectionData, ImageSegmentationData, flatten_list, make_list, \
    safe_deepcopy, array_to_image, ensure_binary, binary_required_info
from plantcv import plantcv as pcv
from seppl.io import Filter
from wai.common.adams.imaging.locateobjects import LocatedObject, LocatedObjects


class FindTips(Filter):
    """
    Find tips in a skeletonized image and forwards them as object detection annotations.
    """

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "find-tips"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Finds tips in a skeletonized image and forwards them as object detection annotations. " + binary_required_info()

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
        return [ObjectDetectionData]

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
            array_new = pcv.morphology.find_tips(array)
            locations = np.where(array_new > 0)
            lobjs = LocatedObjects()
            for y, x in zip(locations[0], locations[1]):
                meta = {"type": "tip"}
                lobj = LocatedObject(int(x), int(y), 1, 1, **meta)
                lobjs.append(lobj)
            item_new = ObjectDetectionData(image_name=item.image_name,
                                           data=array_to_image(array_new, item.image_format)[1].getvalue(),
                                           metadata=safe_deepcopy(item.get_metadata()),
                                           annotation=lobjs)
            result.append(item_new)

        return flatten_list(result)
