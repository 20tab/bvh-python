import unittest
from bvh import Bvh, BvhNode


class TestBvh(unittest.TestCase):

    """
    def test_get_format_need_more(self):
        mp3 = Mpg123()
        with self.assertRaises(Mpg123.NeedMoreException):
            mp3.get_format()
    """

    def test_file_read(self):
        with open('tests/test_freebvh.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual(len(mocap.data), 98838)

    def test_empty_root(self):
        mocap = Bvh('')
        self.assertTrue(isinstance(mocap.root, BvhNode))

    def test_tree(self):
        with open('tests/test_freebvh.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual([str(item) for item in mocap.root], ['HIERARCHY', 'ROOT mixamorig:Hips', 'MOTION', 'Frames: 69', 'Frame Time: 0.0333333'])

    def test_tree2(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual([str(item) for item in mocap.root], ['HIERARCHY', 'ROOT Hips', 'MOTION', 'Frames: 455', 'Frame Time: 0.033333'])

    def test_filter(self):
        with open('tests/test_freebvh.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual([str(item) for item in mocap.root.filter('ROOT')], ['ROOT mixamorig:Hips'])

    def test_bones(self):
        bones = []
        with open('tests/test_freebvh.bvh') as f:
            mocap = Bvh(f.read())
        def iterate_joints(joint):
            bones.append(str(joint))
            for child in joint.filter('JOINT'):
                iterate_joints(child)
        iterate_joints(next(mocap.root.filter('ROOT')))
        self.assertEqual(bones[0], 'ROOT mixamorig:Hips')
        self.assertEqual(bones[17], 'JOINT mixamorig:LeftHandThumb2')
        self.assertEqual(bones[22], 'JOINT mixamorig:LeftHandRing1')
        self.assertEqual(bones[30], 'JOINT mixamorig:RightForeArm')
        

if __name__ == '__main__':
    unittest.main()

