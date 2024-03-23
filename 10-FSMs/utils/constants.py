from . import vec

RESOLUTION = vec(224, 224)
SCALE = 3
UPSCALED = RESOLUTION * SCALE
settingImage = [[0]*14 for i in range(14)]
EPSILON = 0.01

textMatching = {"tc": (1, 2), "lc": (0, 1), "rc": (2, 1), "bc": (1, 0), "wtl": (
    0, 4), "wbl": (0, 5), "wmt": (1, 4), "wmb": (1, 5), "wtr": (2, 4), "wbr": (2, 5), "h": (1, 3), "v": (3, 1), "c": (3, 3), "dw": (4, 4), "dtr": (1, 6), "dbr": (1, 7), "dt": (2, 6), "db": (2, 7), "dtl": (3, 6), "dbl": (3, 7)}
