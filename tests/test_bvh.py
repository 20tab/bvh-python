import unittest
from bvh import Bvh, BvhNode


class TestBvh(unittest.TestCase):

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

    def test_offset(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual(next(mocap.root.filter('ROOT'))['OFFSET'], ['0.0000', '0.0000', '0.0000'])

    def test_search(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual([str(node) for node in mocap.search('JOINT', 'LeftShoulder')], ['JOINT LeftShoulder'])

    def test_search_single_item(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual([str(node) for node in mocap.search('ROOT')], ['ROOT Hips'])

    def test_search_single_item_joints(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual(len(mocap.search('JOINT')), 18)

    def test_joint_offset(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual(mocap.joint_offset('RightElbow'), (-2.6865, -25.0857, 1.2959))

    def test_unknown_joint(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        with self.assertRaises(LookupError):
            mocap.joint_offset('FooBar')

    def test_unknown_attribute(self):
        with open('tests/test_freebvh.bvh') as f:
            mocap = Bvh(f.read())
        with self.assertRaises(IndexError):
            mocap.root['Broken']

    def test_nframes_red_light(self):
        mocap = Bvh('')
        with self.assertRaises(LookupError):
            mocap.nframes

    def test_nframes(self):
        with open('tests/test_freebvh.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual(mocap.nframes, 69)

    def test_frame_time(self):
        with open('tests/test_freebvh.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual(mocap.frame_time, 0.0333333)

    def test_nframes2(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual(mocap.nframes, 455)

    def test_nframes_with_frames_list(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual(mocap.nframes, len(mocap.frames))

    def test_channels(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual(mocap.joint_channels('LeftElbow'), ['Zrotation', 'Xrotation', 'Yrotation'])
        self.assertEqual(mocap.joint_channels('Hips'), ['Xposition', 'Yposition', 'Zposition', 'Zrotation', 'Xrotation', 'Yrotation'])

    def test_frame_channel(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual(mocap.frame_joint_channel(22, 'Hips', 'Xrotation'), -20.98)
        self.assertEqual(mocap.frame_joint_channel(22, 'Chest', 'Xrotation'), 17.65)
        self.assertEqual(mocap.frame_joint_channel(22, 'Neck', 'Xrotation'), -6.77)
        self.assertEqual(mocap.frame_joint_channel(22, 'Head', 'Yrotation'), 8.47)

    def test_frame_channel(self):
        with open('tests/test_freebvh.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual(mocap.frame_joint_channel(22, 'mixamorig:Hips', 'Xposition'), 4.3314)

    def test_frame_iteration(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        x_accumulator = 0.0
        for i in range(0, mocap.nframes):
            x_accumulator += mocap.frame_joint_channel(i, 'Hips', 'Xposition') 
        self.assertTrue(abs(-19735.902699999995 - x_accumulator) < 0.0001)

    def test_joints_names(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual(mocap.get_joints_names()[17], 'RightKnee')

    def test_joint_parent_index(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual(mocap.joint_parent_index('Hips'), -1)
        self.assertEqual(mocap.joint_parent_index('Chest'), 0)
        self.assertEqual(mocap.joint_parent_index('LeftShoulder'), 3)

    def test_joint_parent(self):
        with open('tests/test_mocapbank.bvh') as f:
            mocap = Bvh(f.read())
        self.assertEqual(mocap.joint_parent('Chest').name, 'Hips')


if __name__ == '__main__':
    unittest.main()

