import soundfile as sf
import numpy as np
import os
from os import path
import sys

pathprefix = path.dirname(__file__)

print(__file__)

if pathprefix != "":
    pathprefix = pathprefix + "/"

def buildDict(path):
    dictFile = open(path)

    outDict = {}

    for line in dictFile:
        splitLine = line.split("\t")
        splitPronunciations = splitLine[1].split(", ")
        
        outDict[splitLine[0].lower()] = splitPronunciations[0].replace("\n", "")

    dictFile.close()

    return outDict

def trimUntilInList(workingSyl, listToSearch):
    originalInput = workingSyl
    for i in range(len(workingSyl)):
        if workingSyl in listToSearch:
            return workingSyl 
        else:
            if len(workingSyl) == 1:
                print("TTS!!!!! ERROR: could not resolve segment '" + originalInput + "'.")
                return " "
            #trim one char off right of workingSyl
            workingSyl = workingSyl[:len(workingSyl) - 1]

def searchForFiles(syllable, listToSearch):
    output = []

    workingSyl = syllable

    while len(workingSyl) > 0:
        result = trimUntilInList(workingSyl, listToSearch)
        workingSyl = workingSyl[len(result):]
        result = result.replace(" ", "")
        if len(result) > 0:
            output = output + [result]

    return output

def getPronunciation(query):
    words = query.split(" ")

    pron = ""

    for word in words:
        subwords = searchForFiles(word, dictionary.keys()) #TODO: change the function name lol

        for subword in subwords:
            pron = pron + dictionary[subword]

    return pron

def synthesizeSyllable(phonemeList, stressed):

    firstDone = False
    firstVowelDone = False
    for phoneme in phonemeList:
        path = ""

        if phoneme in consonantList:
            path = "consonant/"
        else:
            if stressed and not firstVowelDone:
                path = path + "stressed/"
            else:
                path = path + "unstressed/"

            firstVowelDone = True

        fullPath = pathprefix +"phonemes/" +path +phoneme +".ogg"

        if os.path.isfile(fullPath):
            audiodata, samplerate = sf.read(fullPath)
        else:
            print("TTS!!!!! ERROR: could not find " +fullPath)
            continue

        if firstDone:
            outputFrames = np.concatenate((outputFrames, audiodata))
        else:
            outputFrames = audiodata
            firstDone = True

    return outputFrames, samplerate

def runTTS(query):
    inputString = getPronunciation(query.lower())     #TODO: option for raw phoneme input
    inputString = inputString.replace("%", "")    #TODO: add support for secondary stress
    inputString = inputString.replace(":", "")      #TODO: add support for syllable length
    inputString = inputString.replace(" ", "")

    thisSyl = ""
    inputString = inputString + "."
    firstDone = False
    stressed = False
    synthesizedOutput = None
    for char in inputString:
        if char != "." and char != '"':
            thisSyl = thisSyl + char
        elif thisSyl != "":

            sylAudio, samplerate = synthesizeSyllable(searchForFiles(thisSyl, combinedList), stressed)

            if firstDone:
                synthesizedOutput = np.concatenate((synthesizedOutput, sylAudio))
            else:
                synthesizedOutput = sylAudio
                firstDone = True

            stressed = False
            thisSyl = ""

        if char == '"':
            stressed = True

    if synthesizedOutput.any() != None:
        sf.write("output.wav", synthesizedOutput, samplerate)


dictionary = buildDict(pathprefix +"cmudict-0.7b-xsampa.txt")

#TODO: load phonemes from zip file because WINDOWS CAN'T TELL THE DIFFERENCE BETWEEN UPPERCASE AND LOWERCASE FILENAMES >:CCCC

consonantList = os.listdir(pathprefix +"phonemes/consonant")
consonantList = list(map(lambda item: item.replace(".ogg", ""), consonantList))

vowelList = os.listdir(pathprefix +"phonemes/stressed") + os.listdir(pathprefix +"phonemes/unstressed")
vowelList = list(map(lambda item: item.replace(".ogg", ""), vowelList))

combinedList = vowelList + consonantList

print("TTS!!!! initialized")

if __name__ == "__main__":
    inputString = sys.argv[1]
    runTTS(inputString)