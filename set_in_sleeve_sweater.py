
from basic_blocks import *


if __name__ == "__main__":

  newSleeve = Sleeve(7, 22)
  newSleeve.setup(40, cuffRibbingIn=2, ribbingBlock=cuff)
  newSleeve.printInstructions()
