
from enum import Enum
import math

# RC multiplier for multicolor jaquard
class KnitType(Enum):
  STOCKINETTE = 1
  TWO_COLOR_JACQUARD = 2
  THREE_COLOR_JACQUARD = 3

class KnitBlock:
  RC_STRING = "RC{:03d}"
  CAST_ON_STRING = "Cast on {} {}"
  KNIT_STRING = "Knit {} row(s)"
  KNIT_WITH_CHANGE = "Knit {} row(s) {} one stitch each side every {} rows to {} stitches"

  def __init__(self, gaugeSt, gaugeRows, knitType=KnitType.STOCKINETTE, easePct=1):
    self.gaugeSt = gaugeSt
    self.gaugeRows = gaugeRows
    self.knitType = knitType
    self.easePct = easePct

  @classmethod
  def fromKnitBlock(cls, knitBlock):
    return cls(knitBlock.gaugeSt, knitBlock.gaugeRows, knitBlock.knitType)

  def convertWidth(self, widthIn):
    return int(round(widthIn * self.gaugeSt * self.easePct))

  def convertLength(self, lengthIn):
    return int(round(lengthIn * self.gaugeRows))

class Trapezoid(KnitBlock):
  def setup(self, lengthIn, startWidthIn, endWidthIn=-1):
    if endWidthIn == -1:
      endWidthIn = startWidthIn

    # Sizing
    self.startWidthSt = self.convertWidth(startWidthIn)
    self.endWidthSt = self.convertWidth(endWidthIn)
    self.lengthRows = self.convertLength(lengthIn)

    # Ecoutremont
    self.totalRC = self.lengthRows * self.knitType.value
    self.isSquare = self.startWidthSt == self.endWidthSt

    if not self.isSquare:
      self.change = "increasing" if self.startWidthSt < self.endWidthSt else "decreasing"

      # Decreasing one stitch each side
      delta = float(abs(self.startWidthSt - self.endWidthSt)) / 2.0 + 1
      self.cadence = int(math.floor(float(self.totalRC) / float(delta)))

  def printCastOn(self, extra=None):
    print self.RC_STRING.format(0)
    print self.CAST_ON_STRING.format(self.startWidthSt, extra)

  def printInstructions(self, startRC=0):
    if self.isSquare:
      print self.KNIT_STRING.format(self.lengthRows)
    else:
      print self.KNIT_WITH_CHANGE.format(self.lengthRows, self.change, self.cadence, self.endWidthSt)
    rc = int(self.totalRC + startRC)
    print self.RC_STRING.format(int(self.totalRC + startRC))
    return rc