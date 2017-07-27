from json import dumps, loads
from Tile import parseTile, Tile
from pygame import Surface, image
from pygame import Color as C
import sys

class Tiler():
  def __init__(self):
    self.Tiles = []
    self.TileSize = 10
  def to_json(self):
    tmp = Tiler()
    tmp.TileSize = self.TileSize
    for val in self.Tiles:
      tmp.Tiles.append(val.to_json())
    return dumps(tmp.__dict__)
  def parse(self, json):
    tmp = loads(json)
    self.TileSize = tmp["TileSize"]
    self.Tiles = []
    for val in tmp["Tiles"]:
      self.Tiles.append(parseTile(val))
  def get_tile_from_color(self, color):
    tmp = None
    for tile in self.Tiles:
      if tile.Color == color:
        tmp = tile
    return tmp

def main():
  if '--help' in sys.argv:
    print "python Tiler.py                                              --> Creates the default tilefile"
    print "python Tiler.py <tilefile.json> <image.bmp> <output.json>    --> Creates the level file"
    print "python Tiler.py <output.json> <file1.json> ... <filen.json>  --> Creates a tilerfile.json from the tile file provided, at least 3 needed"
  elif(len(sys.argv) == 1):
    t = Tiler()
    t.Tiles.append(Tile(0,(0,0,0),"res/ground.png",None,"solid"))
    t.Tiles.append(Tile(1,(255,255,255),"res/sky.png",None,"sky"))
    t.Tiles.append(Tile(0,(255,0,0),"res/grass.png",None,"solid"))
    dum = open("dump.json", "w+")
    dum.write(t.to_json())
    dum.close()
  elif(len(sys.argv) == 4):
    loaded = open(sys.argv[1])
    txt = loaded.read()
    loaded.close()
    trasform_image_to_level(txt,sys.argv[2], sys.argv[3])
  else:
    args = sys.argv
    args = args[1:]
    save_path = args[0]
    args = args[1:]
    save_file = open(save_path)
    t = Tile()
    for p in args:
      tmp = open(p)
      t.Tiles.append(parseTile(tmp.read()))
      tmp.close()
    save_file.write(t.to_json())
    save_file.close()

def trasform_image_to_level(json_tiler,img,output):
  tiler = Tiler()
  tiler.parse(json_tiler)
  img = image.load(img) 
  w,h = img.get_size()
  print w, h, tiler.TileSize
  nw, nh = w*int(tiler.TileSize), h*int(tiler.TileSize)
  print nw, nh
  levelSurface = Surface((int(nw),int(nh)))
  levelMatrix = []
  print "Started loading tiles Image"
  for i in range(0,len(tiler.Tiles)):
    tiler.Tiles[i].TileImage = image.load(tiler.Tiles[i].TilePath)
  print "Done loading tiles Image"
  print "Building the level"
  for y in range(0,h):
    matrixRow = []
    for x in range(0,w):
      c = img.get_at((x,y))
      r, g, b = c.r, c.g, c.b
      tile = tiler.get_tile_from_color([r,g,b])
      matrixRow.append(tile.ID)
      levelSurface.blit(tile.TileImage,(x*tiler.TileSize, y*tiler.TileSize))
    levelMatrix.append(matrixRow)
  print "Done building the level"
  print "Saving"
  outJson = open(output + ".json","w+")
  outJson.write(dumps(levelMatrix))
  outJson.close()
  image.save(levelSurface,output)
  print "Done saving"

if __name__ == '__main__':
  main() 
