import re

class BvhNode:

   def __init__(self, value=None, parent=None):
       self.value = value
       self.children = []
       self.parent = parent
       if self.parent:
           self.parent.add_child(self)

   def add_child(self, item):
       item.parent = self
       self.children.append(item)

   def get_property_value(self, key):
       for child in self.children:
           if key == child.value[0]:
               return child.value[1:]
       return None

   def filter(self, key):
       for child in self.children:
           if child.value[0] == key:
               yield child

   def __iter__(self):
       for child in self.children:
           yield child

   def __repr__(self):
       return str(' '.join(self.value))


class Bvh:

   def __init__(self, data):
       self.data = data
       self.root = BvhNode()
       self.frames = []
       self.tokenize()

   def tokenize(self):
       first_round = []
       accumulator = ''
       for char in self.data:
           if char not in ('\n', '\r'):
               accumulator += char
           else:
               if accumulator:
                   first_round.append(re.split('\\s+', accumulator.strip()))
                   accumulator = ''
       node_stack = [self.root]
       frame_time_found = False
       for item in first_round:
           if frame_time_found:
               self.frames.append(item)
               continue
           key = item[0]
           if key == '{':
               node_stack.append(node)
           elif key == '}':
               node_stack.pop()
           else:
               node = BvhNode(item)
               node_stack[-1].add_child(node)
           if item[0] == 'Frame' and item[1] == 'Time:':
               frame_time_found = True
