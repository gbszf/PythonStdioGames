# Hacking, by Al Sweigart al@inventwithpython.com
# This game is a clone of the Fallout hacking mini-game.

import random

GARBAGE_CHARS = '~!@#$%^&*()_+-={}[]|;:,.<>?/\\' # The "filler" characters for the board.

# Load the WORDS list from a text file that has a 7-letter word on each line.
with open('sevenletterwords.txt') as dictionaryFile:
    WORDS = dictionaryFile.readlines()
for i in range(len(WORDS)):
    WORDS[i] = WORDS[i].strip().upper()


def getBoard(words):
    assert len(words) == 12
    linesWithWords = random.sample(range(16 * 2), 12)
    memoryAddress = 16 * random.randint(0, 4000)

    board = []
    nextWord = 0
    for i in range(16):
        leftLine = ''
        rightLine = ''
        for j in range(16):
            leftLine += random.choice(GARBAGE_CHARS)
            rightLine += random.choice(GARBAGE_CHARS)

        if i in linesWithWords:
            insertionIndex = random.randint(0, 9)
            leftLine = leftLine[:insertionIndex] + words[nextWord] + leftLine[insertionIndex + 7:]
            nextWord += 1
        if i + 16 in linesWithWords:
            insertionIndex = random.randint(0, 9)
            rightLine = rightLine[:insertionIndex] + words[nextWord] + rightLine[insertionIndex + 7:]
            nextWord += 1

        board.append('0x' + hex(memoryAddress)[2:].zfill(4)           + '  ' + leftLine + '    ' +
                     '0x' + hex(memoryAddress + (16*16))[2:].zfill(4) + '  ' + rightLine)

        memoryAddress += 16

    return '\n'.join(board) # Each string in `board` is joined into one large string to return.


def getPlayerMove(words, tries):
    print('Enter password: (%s tries remaining)' % (tries))
    while True:
        move = input().upper()
        if move in words:
            return move


def getNumberOfMatchingLetters(word1, word2):
    matches = 0
    for i in range(len(word1)):
        if word1[i] == word2[i]:
            matches += 1
    return matches


def getOneWordExcept(blocklist=None):
    if blocklist is None:
        blocklist = []

    while True:
        randomWord = random.choice(WORDS)
        if randomWord not in blocklist:
            return randomWord


def getWords():
    # To make the game fair, we want to only have at most 2 words that have 0 letters in common with the secret password.
    secretPassword = random.choice(WORDS)
    words = [secretPassword]

    # Find two words that have zero matching letters.
    while len(words) < 3: # 3 because the secret password is already in `words`.
        randomWord = getOneWordExcept(words)
        if getNumberOfMatchingLetters(secretPassword, randomWord) == 0:
            words.append(randomWord)

    # Find two words that have 3 matching letters (but give up at 500 tries if not enough can be found).
    for i in range(500):
        if len(words) == 5:
            break

        randomWord = getOneWordExcept(words)
        if getNumberOfMatchingLetters(secretPassword, randomWord) == 3:
            words.append(randomWord)

    # Find seven words that have at least one matching letter (but give up at 500 tries if not enough can be found).
    for i in range(500):
        if len(words) == 12:
            break

        randomWord = getOneWordExcept(words)
        if getNumberOfMatchingLetters(secretPassword, randomWord) != 0:
            words.append(randomWord)

    # Add any random words needed to get 12 words total.
    words.extend(random.sample(WORDS, 12 - len(words)))

    assert len(words) == 12
    return words


def runGame():
    gameWords = getWords()
    gameBoard = getBoard(gameWords)
    secretPassword = random.choice(gameWords)

    print('Find the password in the computer\'s memory:')
    print(gameBoard)
    for triesRemaining in range(4, 0, -1):
        playerMove = getPlayerMove(gameWords, triesRemaining)
        if playerMove == secretPassword:
            print('A C C E S S   G R A N T E D')
            return
        else:
            print('Access Denied (%s/7 correct)' % getNumberOfMatchingLetters(secretPassword, playerMove))
    print('Out of tries. Secret password was %s.' % (secretPassword))


if __name__ == '__main__':
    runGame()