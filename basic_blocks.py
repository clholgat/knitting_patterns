
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
  KNIT_WITH_HALF_CHANGE = "Knit {} row(s) {} one stitch on the {} every {} rows to {} stitches"

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
    self._printCastOn(self.startWidthSt, extra)

  def printHalfCastOn(self, extra=None):
    self._printCastOn(self.startWidthSt / 2, extra)

  def _printCastOn(self, width, extra):
    print self.RC_STRING.format(0)
    print self.CAST_ON_STRING.format(width, extra)

  def printInstructions(self, startRC=0):
    return self._printInstructions(startRC, self.endWidthSt)
    
  def printHalfInstructions(self, startRC=0, side="Right"):
    return self._printInstructions(startRC, self.endWidthSt / 2, side=side)

  def _printInstructions(self, startRC, endWidthSt, side=None):
    if self.isSquare:
      print self.KNIT_STRING.format(self.lengthRows)
    elif not side:
      print self.KNIT_WITH_CHANGE.format(self.lengthRows, self.change, self.cadence, endWidthSt)
    else:
      print self.KNIT_WITH_HALF_CHANGE.format(self.lengthRows, self.change, side, self.cadence, endWidthSt)

    rc = int(self.totalRC + startRC)
    print self.RC_STRING.format(int(self.totalRC + startRC))
    return rc


# Defaults are for a set in sleeve
class Sleeve(KnitBlock):
  def setup(self, chestCircumferenceIn, cuffRibbingIn=2, ribbingBlock=None, 
    wristCircumferencePct=0.2, lowerLengthPct=0.5, lowerSleeveWidthPct=0.35, armpitDecreasePct=0.025,
    upperWidthPct=0.1, upperHeightPct=0.2):

    self.chestCircumference = chestCircumferenceIn
    self.armpitDecreasePct = armpitDecreasePct
    if not ribbingBlock:
      ribbingBlock = self

    upperSleeveLength = upperHeightPct * chestCircumferenceIn
    remainingLowerSleeveLength = lowerLengthPct * chestCircumferenceIn

    if cuffRibbingIn > 0:
      self.cuffRibbing = Trapezoid.fromKnitBlock(ribbingBlock)
      self.cuffRibbing.setup(cuffRibbingIn, chestCircumferenceIn * wristCircumferencePct)
      remainingLowerSleeveLength = remainingLowerSleeveLength - cuffRibbingIn

    # The next logical step is to build out the body of the sleeve
    # but we won't know how long it is until we get the end done.
    lowerSleeveTopHeight = chestCircumferenceIn * armpitDecreasePct
    self.lowerSleeveTop = Trapezoid.fromKnitBlock(self)
    self.lowerSleeveTop.setup(lowerSleeveTopHeight, chestCircumferenceIn * lowerSleeveWidthPct)
    remainingLowerSleeveLength = remainingLowerSleeveLength - lowerSleeveTopHeight

    self.lowerSleeve = Trapezoid.fromKnitBlock(self)
    self.lowerSleeve.setup(remainingLowerSleeveLength, 
      chestCircumferenceIn * wristCircumferencePct,
      chestCircumferenceIn * lowerSleeveWidthPct)

    upperSleeveWidthPct = lowerSleeveWidthPct - (2.0 * armpitDecreasePct)
    self.upperSleeve = Trapezoid.fromKnitBlock(self)
    self.upperSleeve.setup(upperSleeveLength, 
      chestCircumferenceIn * upperSleeveWidthPct,
      chestCircumferenceIn * upperWidthPct)

  def printInstructions(self):
    print "Sleeve worked bottom up, make 2"
    runningRC = 0
    if self.cuffRibbing:
      self.cuffRibbing.printCastOn("for 1x1 ribbing")
      runningRC = self.cuffRibbing.printInstructions(runningRC)
      print "Transfer stitches to main bed"
    else:
      self.lowerSleeve.printCastOn()
    runningRC = self.lowerSleeve.printInstructions(runningRC)

    print "Cast off "+str(self.convertWidth(self.armpitDecreasePct * self.chestCircumference))+" on each side"

    runningRC = self.upperSleeve.printInstructions(runningRC)
