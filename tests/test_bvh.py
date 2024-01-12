import unittest

from bvh import Bvh, BvhNode


class TestBvh(unittest.TestCase):
    def test_file_read(self):
        Bvh.from_file("tests/test_freebvh.bvh")

    def test_empty_root(self):
        mocap = Bvh("")
        self.assertTrue(isinstance(mocap.root, BvhNode))

    def test_tree(self):
        mocap = Bvh.from_file("tests/test_freebvh.bvh")
        self.assertEqual(
            [str(item) for item in mocap.root],
            [
                "HIERARCHY",
                "ROOT mixamorig:Hips",
                "MOTION",
                "Frames: 69",
                "Frame Time: 0.0333333",
            ],
        )

    def test_tree2(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(
            [str(item) for item in mocap.root],
            ["HIERARCHY", "ROOT Hips", "MOTION", "Frames: 455", "Frame Time: 0.033333"],
        )

    def test_filter(self):
        mocap = Bvh.from_file("tests/test_freebvh.bvh")
        self.assertEqual(
            [str(item) for item in mocap.root.filter("ROOT")], ["ROOT mixamorig:Hips"]
        )

    def test_bones(self):
        bones = []
        mocap = Bvh.from_file("tests/test_freebvh.bvh")

        def iterate_joints(joint):
            bones.append(str(joint))
            for child in joint.filter("JOINT"):
                iterate_joints(child)

        iterate_joints(next(mocap.root.filter("ROOT")))
        self.assertEqual(bones[0], "ROOT mixamorig:Hips")
        self.assertEqual(bones[17], "JOINT mixamorig:LeftHandThumb2")
        self.assertEqual(bones[22], "JOINT mixamorig:LeftHandRing1")
        self.assertEqual(bones[30], "JOINT mixamorig:RightForeArm")

    def test_offset(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(
            next(mocap.root.filter("ROOT"))["OFFSET"], ["0.0000", "0.0000", "0.0000"]
        )

    def test_search(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(
            [str(node) for node in mocap.search("JOINT", "LeftShoulder")],
            ["JOINT LeftShoulder"],
        )

    def test_search_single_item(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual([str(node) for node in mocap.search("ROOT")], ["ROOT Hips"])

    def test_search_single_item_joints(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(len(mocap.search("JOINT")), 18)

    def test_joint_offset(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(mocap.joint_offset("RightElbow"), (-2.6865, -25.0857, 1.2959))

    def test_unknown_joint(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        with self.assertRaises(LookupError):
            mocap.joint_offset("FooBar")

    def test_unknown_attribute(self):
        mocap = Bvh.from_file("tests/test_freebvh.bvh")
        with self.assertRaises(IndexError):
            mocap.root["Broken"]

    # def test_nframes_red_light(self):
    #     mocap = Bvh("")
    #     with self.assertRaises(LookupError):
    #         mocap.nframes

    def test_nframes(self):
        mocap = Bvh.from_file("tests/test_freebvh.bvh")
        self.assertEqual(mocap.nframes, 69)

    def test_frame_time(self):
        mocap = Bvh.from_file("tests/test_freebvh.bvh")
        self.assertEqual(mocap.frame_time, 0.0333333)

    def test_nframes2(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(mocap.nframes, 455)

    def test_nframes_with_frames_list(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(mocap.nframes, len(mocap.frames))

    def test_channels(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(
            mocap.joint_channels("LeftElbow"), ["Zrotation", "Xrotation", "Yrotation"]
        )
        self.assertEqual(
            mocap.joint_channels("Hips"),
            [
                "Xposition",
                "Yposition",
                "Zposition",
                "Zrotation",
                "Xrotation",
                "Yrotation",
            ],
        )

    def test_frame_channel(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(mocap.frame_joint_channel(22, "Hips", "Xrotation"), -20.98)
        self.assertEqual(mocap.frame_joint_channel(22, "Chest", "Xrotation"), 17.65)
        self.assertEqual(mocap.frame_joint_channel(22, "Neck", "Xrotation"), -6.77)
        self.assertEqual(mocap.frame_joint_channel(22, "Head", "Yrotation"), 8.47)

    def test_frame_channel_fallback(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(mocap.frame_joint_channel(22, "Hips", "Badrotation", 17), 17)

    # def test_frame_channel2(self):
    #     mocap = Bvh.from_file("tests/test_mocapbank.bvh")
    #     self.assertEqual(
    #         mocap.frame_joint_channel(22, "mixamorig:Hips", "Xposition"), 4.3314
    #     )

    def test_frame_iteration(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        x_accumulator = 0.0
        for i in range(0, mocap.nframes):
            x_accumulator += mocap.frame_joint_channel(i, "Hips", "Xposition")
        self.assertTrue(abs(-19735.902699999995 - x_accumulator) < 0.0001)

    def test_joints_names(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(mocap.get_joints_names()[17], "RightKnee")

    def test_joint_parent_index(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(mocap.joint_parent_index("Hips"), -1)
        self.assertEqual(mocap.joint_parent_index("Chest"), 0)
        self.assertEqual(mocap.joint_parent_index("LeftShoulder"), 3)

    def test_joint_parent(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(mocap.joint_parent("Chest").name, "Hips")

    def test_frame_joint_multi_channels(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        rotation = mocap.frame_joint_channels(
            30, "Head", ["Xrotation", "Yrotation", "Zrotation"]
        )
        self.assertEqual(rotation, [1.77, 13.94, -7.42])

    def test_frames_multi_channels(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        rotations = mocap.frames_joint_channels(
            "Head", ["Xrotation", "Yrotation", "Zrotation"]
        )
        self.assertEqual(len(rotations), mocap.nframes)

    def test_joint_children(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(mocap.joint_direct_children("Chest")[0].name, "Chest2")
        self.assertEqual(mocap.joint_direct_children("Hips")[0].name, "Chest")
        self.assertEqual(mocap.joint_direct_children("Hips")[1].name, "LeftHip")
        self.assertEqual(mocap.joint_direct_children("Hips")[2].name, "RightHip")
        self.assertEqual(mocap.joint_direct_children("RightWrist"), [])

    def test_export(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        raw = mocap.raw_data
        Bvh(raw)

    def test_get_duration(self):
        mocap = Bvh.from_file("tests/test_mocapbank.bvh")
        self.assertEqual(len(mocap), 15167)


if __name__ == "__main__":
    unittest.main()
