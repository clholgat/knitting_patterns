

from basic_blocks import *

class DogSweater(KnitBlock):
  def setup(self, neckToTailIn, neckCircumference, neckToFrontLegsIn, legToLegIn, 
               chestCircumferenceIn, neckLengthIn=2, bottomRibbingIn=0, ribbingBlock=None):
    # Constants
    self.neckLengthIn = neckLengthIn

    # Back panel
    self.backLength = 0.9 * neckToTailIn
    self.backWidth = chestCircumferenceIn - legToLegIn
    if bottomRibbingIn > 0:
      self.backRibbing = Trapezoid.fromKnitBlock(ribbingBlock)
      self.backRibbing.setup(bottomRibbingIn, self.backWidth)
    self.backBodyTrap = Trapezoid.fromKnitBlock(self)
    self.backBodyTrap.setup(self.backLength - neckToFrontLegsIn - bottomRibbingIn, 
        self.backWidth)
    self.backNeckTrap = Trapezoid.fromKnitBlock(self)
    self.backNeckTrap.setup(neckToFrontLegsIn, self.backWidth, 0.66 * neckCircumference)

    # Front panel
    self.frontLength = 0.6 * neckToTailIn
    self.frontWidth = legToLegIn
    if bottomRibbingIn > 0:
      self.frontRibbing = Trapezoid.fromKnitBlock(ribbingBlock)
      self.frontRibbing.setup(bottomRibbingIn, self.frontWidth)
    self.frontBodyTrap = Trapezoid.fromKnitBlock(self)
    self.frontBodyTrap.setup(self.frontLength - neckToFrontLegsIn - bottomRibbingIn, 
        self.frontWidth)
    self.frontNeckTrap = Trapezoid.fromKnitBlock(self)
    self.frontNeckTrap.setup(neckToFrontLegsIn, self.frontWidth, 0.33 * neckCircumference)

  def printInstructions(self, startRC=0):
    print "Back panel worked from the bottom up"
    runningRC = 0
    if self.backRibbing:
      self.backRibbing.printCastOn("for 1x1 ribbing")
      runningRC = self.backRibbing.printInstructions(runningRC)
      print "Transfer stitches to main bed"
    else:
      self.backBodyTrap.printCastOn()
    runningRC = self.backBodyTrap.printInstructions(runningRC)
    runningRC = self.backNeckTrap.printInstructions(runningRC)
    print "Scrap off"
    print ""

    runningRC = 0
    print "Front panel worked from the bottom up"
    if self.frontRibbing:
      self.frontRibbing.printCastOn("for 1x1 ribbing")
      runningRC = self.frontRibbing.printInstructions(runningRC)
      print "Transfer stitches to main bed"
    else:
      self.frontBodyTrap.printCastOn()
    runningRC = self.frontBodyTrap.printInstructions(runningRC)
    runningRC = self.frontNeckTrap.printInstructions(runningRC)
    print "Scrap off"
    print ""

    print "Join left shoulder to row " + str(self.frontNeckTrap.lengthRows)
    print "Leave a 3 inch or "+str(int(self.gaugeRows * 3))+"st hole, join rest of seam"
    print ""

    print "Rehang joined neck stitches on the machine for 1x1 ribbing"
    print "Knit "+str(self.neckLengthIn*self.gaugeRows)+" rows"
    print ""

    print "Join neckline ribbing and right shoulder in same manner as left"


if __name__ == "__main__":
  sweater = DogSweater(4, 5.5)
  sweater.setup(16, 10, 5, 4, 17, bottomRibbingIn=2, ribbingBlock=sweater)
  sweater.printInstructions()

