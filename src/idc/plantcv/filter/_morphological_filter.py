import abc

import numpy as np
from PIL import Image

from build.lib.idc.api import ensure_binary
from idc.api import flatten_list, make_list, \
    safe_deepcopy, array_to_image, ensure_grayscale
from seppl.io import Filter

REQUIRED_FORMAT_ANY = "any"
REQUIRED_FORMAT_BINARY = "binary"
REQUIRED_FORMAT_GRAYSCALE = "grayscale"


class MorphologicalFilter(Filter, abc.ABC):
    """
    Ancestor for morphological filters.
    """

    def _nothing_to_do(self, data) -> bool:
        """
        Checks whether there is nothing to do, e.g., due to parameters.

        :param data: the data to process
        :return: whether nothing needs to be done
        :rtype: bool
        """
        return False

    def _required_format(self) -> str:
        """
        Returns what input format is required for applying the filter.

        :return: the type of image
        :rtype: str
        """
        return REQUIRED_FORMAT_ANY

    def _ensure_correct_format(self, image: Image.Image) -> Image.Image:
        """
        Ensures that the image is in the right format.

        :param image: the image to check
        :type image: Image.Image
        :return: the image with the correct format
        :rtype: Image.Image
        """
        req_format = self._required_format()
        if req_format == REQUIRED_FORMAT_ANY:
            return image
        elif req_format == REQUIRED_FORMAT_BINARY:
            return ensure_binary(image, self.logger())
        elif req_format == REQUIRED_FORMAT_GRAYSCALE:
            return ensure_grayscale(image, self.logger())
        else:
            raise Exception("Unsupported required format: %s" % req_format)

    def _apply_filter(self, array: np.ndarray) -> np.ndarray:
        """
        Applies the morphological filter to the image and returns the numpy array.

        :param array: the image the filter to apply to
        :type array: np.ndarray
        :return: the filtered image
        :rtype: np.ndarray
        """
        raise NotImplementedError()

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        # nothing to do?
        if self._nothing_to_do(data):
            return data

        result = []
        for item in make_list(data):
            image = self._ensure_correct_format(item.image)
            array = np.asarray(image).astype(np.uint8)
            array_new = self._apply_filter(array)
            item_new = type(item)(image_name=item.image_name,
                                  data=array_to_image(array_new, item.image_format)[1].getvalue(),
                                  metadata=safe_deepcopy(item.get_metadata()),
                                  annotation=safe_deepcopy(item.annotation))
            result.append(item_new)

        return flatten_list(result)
