
from basic_blocks import *

SLEEVE_WRIST_CIRCUMFERENCE = 0.2
SLEEVE_LOWER_LENGTH = 0.5
SLEEVE_ARMPIT_WIDTH = 0.5
ARMPIT_DECREASE = 0.05
SLEEVE_UPPER_HEIGHT = 0.25
SLEEVE_NECK_WIDTH = 0.1

BODY_WIDTH = 0.5
BODY_HEIGHT = 0.5
ARMPIT_WIDTH = 0.4
BODY_UPPER_HEIGHT = 0.25
BODDY_FRONT_NECK_WIDTH = 0.15
BODY_BACK_NECK_WIDTH = 0.1

# Defaults are for front panel
class RaglanBodyPannel(KnitBlock):
  def setup(self, chestCircumferenceIn, bottomRibbingIn=2, ribbingBlock=None,
    bottomLengthPct=0.5, widthPct=0.5, armpitDecreasePct=0.05, upperHeightPct=0.25, 
    neckWidthPct=0.15):

    self.chestCircumference = chestCircumferenceIn
    self.armpitDecreasePct = armpitDecreasePct

    if not ribbingBlock:
      ribbingBlock = self

    remainingBottomLength = bottomLengthPct * chestCircumferenceIn

    if bottomRibbingIn > 0:
      self.bottomRibbing = Trapezoid.fromKnitBlock(ribbingBlock)
      self.bottomRibbing.setup(bottomRibbingIn, chestCircumferenceIn * widthPct)
      remainingBottomLength = remainingBottomLength - bottomRibbingIn

    self.bottom = Trapezoid.fromKnitBlock(self)
    self.bottom.setup(remainingBottomLength,
      chestCircumferenceIn * widthPct)

    self.top = Trapezoid.fromKnitBlock(self)
    self.top.setup(chestCircumferenceIn * upperHeightPct,
      chestCircumferenceIn * (widthPct - (2.0 * armpitDecreasePct)),
      chestCircumferenceIn * neckWidthPct)

  def printInstructions(self, name):
    print "Raglan "+name+" panel"
    runningRC = 0
    if self.bottomRibbing:
      self.bottomRibbing.printCastOn("for 1x1 ribbing")
      runningRC = self.bottomRibbing.printInstructions(runningRC)
      print "Transfer stitches to main bed"
    else:
      self.bottom.printCastOn()
    runningRC = self.bottom.printInstructions(runningRC)

    print "Cast off "+str(self.convertWidth(self.armpitDecreasePct * self.chestCircumference))+" on each side"

    self.top.printInstructions(runningRC)

  def printHalfInstructions(self, side, name="front"):
    print "Raglan cardigan "+name+" "+side+" side"
    runningRC = 0
    if self.bottomRibbing:
      self.bottomRibbing.printHalfCastOn("for 1x1 ribbing")
      runningRC = self.bottomRibbing.printHalfInstructions(runningRC)
      print "Transfer stitches to main bed"
    else:
      self.bottom.printHalfCastOn()
    runningRC = self.bottom.printHalfInstructions(runningRC, side)

    print "Cast off "+str(self.convertWidth(self.armpitDecreasePct * self.chestCircumference))+" on "+side+" side"

    self.top.printHalfInstructions(runningRC, side)

class RaglanCardigan(KnitBlock):
  def setup(self, chestCircumferenceIn):
    self.sleeve = Sleeve.fromKnitBlock(self)
    self.sleeve.setup(chestCircumferenceIn, lowerSleeveWidthPct=0.5, armpitDecreasePct=0.05, upperHeightPct=0.25)

    self.front = RaglanBodyPannel.fromKnitBlock(self)
    self.front.setup(chestCircumferenceIn)

    self.back = RaglanBodyPannel.fromKnitBlock(self)
    self.back.setup(chestCircumferenceIn, neckWidthPct=0.1)

  def printInstructions(self):
    self.sleeve.printInstructions()

    print "\n"

    self.back.printInstructions("back")

    print "\n"

    self.front.printHalfInstructions("left")

    print "\n"

    self.front.printHalfInstructions("right")


if __name__ == "__main__":
  newSleeve = Sleeve(4, 5.5)
  newSleeve.setup(38, lowerSleeveWidthPct=0.5, armpitDecreasePct=0.05, upperHeightPct=0.25)
  newSleeve.printInstructions()

  front = RaglanBodyPannel.fromKnitBlock(newSleeve)
  front.setup(38)
  print "\nWHOLE\n"
  front.printInstructions("front")
  print "\nHALF\n"
  front.printHalfInstructions("left")

  print "\nINTEGRATED\n"

  sweater = RaglanCardigan(4, 5.5)
  sweater.setup(38)
  sweater.printInstructions()
