import tempfile
import unittest
from pathlib import Path
import numpy as np
import nibabel as nib
from analysis import load_map, compare, validate_grid

class AnalysisTests(unittest.TestCase):
    def test_overlap_and_provenance(self):
        with tempfile.TemporaryDirectory() as d:
            a = np.zeros((3, 3, 3)); b = np.zeros_like(a)
            a[0, 0, 0] = a[1, 1, 1] = 4
            b[0, 0, 0] = b[2, 2, 2] = 4
            paths = [Path(d) / x for x in ('a.nii.gz', 'b.nii.gz')]
            for path, data in zip(paths, (a, b)):
                nib.save(nib.Nifti1Image(data, np.eye(4)), str(path))
            x, y = [load_map(p) for p in paths]
            result = compare(x, y, [3])[0]
            self.assertEqual(result['shared_voxels'], 1)
            self.assertAlmostEqual(result['jaccard'], 1/3)
            self.assertAlmostEqual(result['dice'], .5)
            self.assertEqual(len(x.sha256), 64)
            y.affine[0, 3] = 2
            with self.assertRaises(ValueError): validate_grid([x, y])

if __name__ == '__main__': unittest.main()
