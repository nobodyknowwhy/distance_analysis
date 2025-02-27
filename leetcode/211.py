class WordDictionary(object):


    def __init__(self):
        self.words = []

    def addWord(self, word):
        """
        :type word: str
        :rtype: None
        """
        self.words.append(word)

    def search(self, word):
        """
        :type word: str
        :rtype: bool
        """
        import re
        if re.match(word + '$', ' '.join(self.words)):
            return 'true'
        else:
            return 'false'