# -*- coding: utf-8 -*-

from .poppler_backend import PopplerBackend
from .ghostscript_backend import GhostscriptBackend

BACKENDS = {"poppler": PopplerBackend, "ghostscript": GhostscriptBackend}


class ImageConversionBackend(object):
    def __init__(self, backend="poppler", use_fallback=True):
        if backend not in BACKENDS.keys():
            raise ValueError(f"Image conversion backend '{backend}' not supported")

        self.backend = backend
        self.use_fallback = use_fallback
        self.fallbacks = list(filter(lambda x: x != backend, BACKENDS.keys()))

    def convert(self, pdf_path, png_path):
        try:
            converter = BACKENDS[self.backend]()
            converter.convert(pdf_path, png_path)
        except Exception as e:
            import sys

            if not self.use_fallback:
                raise type(e)(
                    f"{str(e)} with image conversion backend '{self.backend}'"
                ).with_traceback(sys.exc_info()[2])
            for fallback in self.fallbacks:
                try:
                    converter = BACKENDS[fallback]()
                    converter.convert(pdf_path, png_path)
                except Exception as e:
                    raise type(e)(
                        f"{str(e)} with image conversion backend '{fallback}'"
                    ).with_traceback(sys.exc_info()[2])
                else:
                    break
