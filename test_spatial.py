import unittest
import numpy as np
from analysis import MapData
from spatial import overlap_clusters

class SpatialTests(unittest.TestCase):
    def test_six_neighbor_clusters_and_mni_coordinates(self):
        a = np.zeros((5, 5, 5)); b = a.copy()
        a[1:3, 1:3, 1:3] = 4; b[1:3, 1:3, 1:3] = 4
        a[4, 4, 4] = b[4, 4, 4] = 4
        affine = np.diag([2, 2, 2, 1])
        x, y = MapData('a', a, affine, ''), MapData('b', b, affine, '')
        mask, rows = overlap_clusters(x, y, threshold=3, min_voxels=2)
        self.assertEqual(int(mask.sum()), 9)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['voxels'], 8)
        self.assertEqual(rows[0]['volume_mm3'], 64)
        self.assertEqual(rows[0]['peak_mni_x'], 2)

if __name__ == '__main__': unittest.main()
