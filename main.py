from memory.short_term import ShortTermMemory
from memory.linguistic import LinguisticMemory

from senses.hearing import Hearing

from processing import MainProcessor

from actions.printSoundEvents import printer
from actions.outputSound import speaker


if __name__ == '__main__':
    st_mem = ShortTermMemory()
    ling_mem = LinguisticMemory()

    hearing = Hearing(st_mem=st_mem, rate=16000)
    hearing.launch()

    mainProcessor = MainProcessor(st_mem=st_mem, ling_mem=ling_mem)
    mainProcessor.launch()

    """
    ### Actions ###

    SEPrinter = printer(st_mem=st_mem)
    SEPrinter.launch()

    audioSpeaker = speaker(st_mem=st_mem, channels=1, rate=16000)
    audioSpeaker.launch()
    """
