class KeyStruct:
  def __init__(self):
    self.keyStructure = {}

  def add(self, key, property, target):
    self.key = key
    self.property = property
    self.target = target
    self.keyStructure[self.key] = [self.property, self.target]
