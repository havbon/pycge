from termcolor import colored
from readchar import readchar
from replit import clear
from pycge.key import KeyStruct

class Game:
  def __init__(self, x_y):
    self.dim = self.x, self.y = x_y

    self.layers = {0: Layer(self.dim)}
    self.backgroundColor = "grey"
    self.eventList = []

  def devDisplay(self):
    renderedBoard = Layer(self.dim)

    for boardIndex in sorted(self.layers.keys()):
      layer = self.layers[boardIndex]

      y = 0
      for row in layer.board:
        x = 0
        for pixel in row:
          if pixel == "#":
            pass

          if pixel != "#":
            renderedBoard.board[y][x] = pixel
          
          #variable pixel is the requested sign
          #if the sign on the rendered version already contains a sign: replace that sign

          #so if pixel is "#", do nothing
          #if pixel != "#", replace renderedBoard with that sign

          x += 1

        y += 1
    self.renderedBoard = renderedBoard
    self.background = colored("  ", self.backgroundColor, attrs = ["reverse"])
    for row in renderedBoard:
      for pixel in row:
        if type(pixel) == Actor:
          print(pixel.rep, end="")

        else:
          print(self.background, end="")
      print()

  def addLayer(self, layerObj, index):
    self.newLayerObj = layerObj
    if self.newLayerObj.dim == self.dim:
      self.layers[index] = self.newLayerObj

  def start(self, keyStructures=None):
    if keyStructures == None:
      keyStructures = KeyStruct()
    self.keyStruct = keyStructures
    self.devDisplay()

    self.key = ""
    while self.key != "x":
      self.key = readchar()
      clear()

      if self.key in self.keyStruct.keyStructure:
        keyActions = self.keyStruct.keyStructure[self.key]

        newLoc = (keyActions[0]().val)

        actor = keyActions[1]

        #remove actor from old loc
        actor.layer.board[actor.y][actor.x] = "#"

        #place actor in new loc
        newLoc = [actor.y+newLoc[1], actor.x+newLoc[0]]

        updateLoc = True

        if actor.hitBox:
          if len(isOverlapping(newLoc[1], newLoc[0], actor, self.layers)) >= 1: 
            hitBoxes = []

            for hitActor in isOverlapping(newLoc[1], newLoc[0], actor, self.layers):
              hitBoxes.append(hitActor.hitBox)
            
            if contains(True, hitBoxes):
              updateLoc = False

            if not contains(True, hitBoxes):
              updateLoc = True
        
        if not actor.hitBox or updateLoc:
          actor.layer.board[newLoc[0]][newLoc[1]] = actor

          #update actors loc
          actor.y, actor.x = newLoc

        else:
          actor.layer.board[actor.y][actor.x] = actor

      #fire events
      for event in self.eventList:
        event.run()

      self.devDisplay()

  def addListener(self, event):
    self.eventList.append(event)

def contains(cond, ls):
  result = False
  for elem in ls:
    if elem == cond:
      result = True
      break

    elif elem != cond:
      pass

  return result

def isOverlapping(x, y, actor, layers):
  overlapping = []

  for layer in layers.values():
    if layer != actor.layer:
      try: layer.board[y][x]
      except: raise Exception("out of bounds")
      if layer.board[y][x] != "#":
        overlapping.append(layer.board[y][x])
        
  return overlapping

class Layer:
  def __init__(self, x_y):
    self.dim = self.x, self.y = x_y
    self.board = []
    while len(self.board) != self.y:
      self.board.append([])
      while len(self.board[-1]) != self.x:
        self.board[-1].append("#")

  def __iter__(self):
    return iter(self.board)

class Actor:
  def __init__(self, color="white"):
    self.rep = colored("  ", color, attrs=["reverse"])
    self.hitBox = True

  def place(self, x, y, layer):
    self.layer = layer
    self.x = x
    self.y = y
    
    try: self.layer.board[y][x]
    except: raise Exception("out of bounds")
    self.layer.board[y][x] = self

class errors:
  dimentionErr = "error, all the layers need to be the same size"

class Event:
  def __init__(self, func):
    self.func = func

  def run(self):
    self.func()

#an event is a script that fires a given function when a condition thats defined by the user is met.