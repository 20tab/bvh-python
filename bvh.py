import re
import copy


class BvhNode:
    def __init__(self, value=[], parent=None):
        self.value = value
        self.children = []
        self.parent = parent
        if self.parent:
            self.parent.add_child(self)

    def add_child(self, item):
        item.parent = self
        self.children.append(item)

    def filter(self, key):
        for child in self.children:
            if child.value[0] == key:
                yield child

    def __iter__(self):
        for child in self.children:
            yield child

    def __getitem__(self, key):
        for child in self.children:
            for index, item in enumerate(child.value):
                if item == key:
                    if index + 1 >= len(child.value):
                        return None
                    else:
                        return child.value[index + 1 :]
        raise IndexError("key {} not found".format(key))

    def __repr__(self):
        return str(" ".join(self.value))

    @property
    def name(self):
        return self.value[1]


class Bvh:
    def __init__(self, data):
        self.data = data
        self.root = BvhNode()
        self.frames = []
        self.tokenize()

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            mocap = cls(f.read())
        return mocap

    def __len__(self):
        return round(self.nframes * 1000 / self.frame_rate)

    def tokenize(self):
        lines = re.split("\n|\r", self.data)
        first_round = [re.split("\\s+", line.strip()) for line in lines[:-1]]
        node_stack = [self.root]
        node = None
        data_start_idx = 0
        for line, item in enumerate(first_round):
            key = item[0]
            if key == "{":
                node_stack.append(node)
            elif key == "}":
                node_stack.pop()
            else:
                node = BvhNode(item)
                node_stack[-1].add_child(node)
            if item[0] == "Frame" and item[1] == "Time:":
                data_start_idx = line
                break
        self.frames = [
            [float(scalar) for scalar in line]
            for line in first_round[data_start_idx + 1 :]
        ]

    def __getitem__(self, x):
        if type(x) is int:
            frames = self.frames[[round(x / (1000 * self.frame_rate))]]
        elif type(x) is slice:
            start_time = x.start if x.start is not None else 0
            end_time = x.stop if x.stop is not None else -1

            start_frame = round(start_time / (1000 * self.frame_rate))
            end_frame = round(end_time / (1000 * self.frame_rate))
            frames = self.frames[start_frame : end_frame : x.step]
        else:
            raise KeyError

        new_bvh = copy.deepcopy(self)
        new_bvh.frames = frames
        return new_bvh

    def search(self, *items):
        found_nodes = []

        def check_children(node):
            if len(node.value) >= len(items):
                failed = False
                for index, item in enumerate(items):
                    if node.value[index] != item:
                        failed = True
                        break
                if not failed:
                    found_nodes.append(node)
            for child in node:
                check_children(child)

        check_children(self.root)
        return found_nodes

    def get_joints(self):
        joints = []

        def iterate_joints(joint):
            joints.append(joint)
            for child in joint.filter("JOINT"):
                iterate_joints(child)

        iterate_joints(next(self.root.filter("ROOT")))
        return joints

    def get_joints_names(self):
        joints = []

        def iterate_joints(joint):
            joints.append(joint.value[1])
            for child in joint.filter("JOINT"):
                iterate_joints(child)

        iterate_joints(next(self.root.filter("ROOT")))
        return joints

    def joint_direct_children(self, name):
        joint = self.get_joint(name)
        return [child for child in joint.filter("JOINT")]

    def get_joint_index(self, name):
        return self.get_joints().index(self.get_joint(name))

    def get_joint(self, name):
        found = self.search("ROOT", name)
        if not found:
            found = self.search("JOINT", name)
        if found:
            return found[0]
        raise LookupError("joint not found")

    def joint_offset(self, name):
        joint = self.get_joint(name)
        offset = joint["OFFSET"]
        return (float(offset[0]), float(offset[1]), float(offset[2]))

    def joint_channels(self, name):
        joint = self.get_joint(name)
        return joint["CHANNELS"][1:]

    def get_joint_channels_index(self, joint_name):
        index = 0
        for joint in self.get_joints():
            if joint.value[1] == joint_name:
                return index
            index += int(joint["CHANNELS"][0])
        raise LookupError("joint not found")

    def get_joint_channel_index(self, joint, channel):
        channels = self.joint_channels(joint)
        if channel in channels:
            channel_index = channels.index(channel)
        else:
            channel_index = -1
        return channel_index

    def frame_joint_channel(self, frame_index, joint, channel, value=None):
        joint_index = self.get_joint_channels_index(joint)
        channel_index = self.get_joint_channel_index(joint, channel)
        if channel_index == -1 and value is not None:
            return value
        return float(self.frames[frame_index][joint_index + channel_index])

    def frame_joint_channels(self, frame_index, joint, channels, value=None):
        values = []
        joint_index = self.get_joint_channels_index(joint)
        for channel in channels:
            channel_index = self.get_joint_channel_index(joint, channel)
            if channel_index == -1 and value is not None:
                values.append(value)
            else:
                values.append(
                    float(self.frames[frame_index][joint_index + channel_index])
                )
        return values

    def frames_joint_channels(self, joint, channels, value=None):
        all_frames = []
        joint_index = self.get_joint_channels_index(joint)
        for frame in self.frames:
            values = []
            for channel in channels:
                channel_index = self.get_joint_channel_index(joint, channel)
                if channel_index == -1 and value is not None:
                    values.append(value)
                else:
                    values.append(float(frame[joint_index + channel_index]))
            all_frames.append(values)
        return all_frames

    def joint_parent(self, name):
        joint = self.get_joint(name)
        if joint.parent == self.root:
            return None
        return joint.parent

    def joint_parent_index(self, name):
        joint = self.get_joint(name)
        if joint.parent == self.root:
            return -1
        return self.get_joints().index(joint.parent)

    @property
    def nframes(self):
        return len(self.frames)

    @property
    def frame_rate(self):
        try:
            return float(next(self.root.filter("Frame")).value[2])
        except StopIteration:
            raise LookupError("frame time not found")

    @property
    def raw_data(self):
        _, root, _, _, _ = self.root
        data = "HIERARCHY\n"

        data, depth = self.write_node(root, data, 0)

        data += "MOTION\n"
        data += f"Frames:\t{self.nframes}\n"
        data += f"Frame Time:\t{self.frame_rate}\n"

        for frame in self.frames:
            data += "\t".join(frame) + "\n"

        return data

    def write_node(self, node, data, depth):
        n_type = node.value[0]

        data += "\t" * depth + "\t".join(node.value) + "\n"
        data += "\t" * depth + "{\n"
        data += "\t" * (depth + 1) + "\t".join(node.children[0].value) + "\n"
        if n_type != "End":
            data += "\t" * (depth + 1) + "\t".join(node.children[1].value) + "\n"
        for child in node.children[2:]:
            depth += 1
            data, depth = self.write_node(child, data, depth)
        data += "\t" * depth + "}\n"
        depth -= 1
        return data, depth

    def export(self, out_f):
        with open(out_f, "w") as f:
            f.write(self.raw_data)
