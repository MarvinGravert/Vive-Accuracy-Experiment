from decouple import config
import numpy as np

THRESHOLD_FOR_EXCLUSION = config('thresholdForExclusion', cast=float)

TARGET_HOLDER_OFFSET = config('TARGET_HOLDER_OFFSET', cast=float)

LASER2VIVE_ROT_MATRIX_BLACK = config("ROT_LASER2VIVE_BLACK")
LASER2VIVE_ROT_MATRIX_RED = config("ROT_LASER2VIVE_RED")

# VIVE2LASER_ROT_MATRIX_RED = config("ROT_VIVE2LASER_RED")

DATE = config("DATE")
EXPERIMENT_NUMBER = config("EXPERIMENT_NUMBER")

COORDINATE_SYSTEM = config("COORDINATE_SYSTEM")
