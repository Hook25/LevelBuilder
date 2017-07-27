from pygame import Color
from json import dumps, loads 

class Tile:
  def __init__(self, ID = 0, Color="", TilePath="", TileImage=None, TileKind=None):
    self.ID = ID
    self.Color = Color
    self.TilePath = TilePath
    self.TileImage = TileImage
    self.TileKind = TileKind
  def to_json(self):
    return dumps(self, default = lambda o: o.__dict__)
  def parse(self, json):
    self.__dict__ = loads(json)

def parseTile(json):
  t = Tile()
  t.parse(json)
  return t


def main():
  saves = open("dumptest.json", "r+w+")
  t = Tile(0, (0,0,0),"",None,"Solid")
  saves.write(t.to_json())
  parseTile(t.to_json())
  saves.close()
 
if __name__ == "__main__":
  main()
