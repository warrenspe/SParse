"""
    File containing a string parsing class which can accept a grammar and input string to return a dictionary of
    parsed tokens from the string, depending on whether or not the grammar given matches the input string and which
    named tokens exist within the grammar.

    Copyright (C) 2016 Warren Spencer
    warrenspencer27@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Standard imports
import re, sys

# Project imports
import utils._Grammar

# GLOBALS
DEBUG = False # If True will print out debugging info to sys.stderr during a match

class _StringParser(object):

    grammar = None
    stringTokenizer = None
    tokenizerRegexes = [
        '"[^"]*"',
        "'[^']*'",
        '\w+',
        '\S'
    ]

    def __init__(self, grammar, allowSubGrammarDefinitions):
        self.grammar = utils._Grammar.constructGrammar(grammar, allowSubGrammarDefinitions)


    # Internal functions
    def _tokenizeString(self, inputString):
        """
        Tokenizes a string, splitting on whitespace.  Takes quotes and apostrophes into account when splitting tokens.
        Example: "abc def 'g h i' jkl" -> ['abc', 'def', "'g h i'", 'jkl']

        Inputs: inputString - The string to tokenize.

        Outputs: An iterable of tokens.
        """

        return re.findall("(%s)" % "|".join(self.tokenizerRegexes), inputString)


    # User-Level functions
    def match(self, inputString, matchEntirety=True):
        """
        Runs the loaded grammar against a string and returns the output if it matches the input string.

        Inputs: inputString   - The string to parse.
                matchEntirety - A boolean, if True requires the entire string to be matched by the grammar.
                                if False, trailing tokens not matched by the grammar will not cause a match failure.

        Outputs: A dictionary representing the output of parsing if the string matches the grammar, else None.
        """

        tokens = self._tokenizeString(inputString)

        if DEBUG:
            sys.stderr.write("\nInput Tokens:\n\n%s\n\n" % tokens)
            sys.stderr.flush()

        try:
            utils._Grammar.DEBUG = DEBUG
            match, endIdx, output = self.grammar.match(tokens, 0)


        finally:
            utils._Grammar.DEBUG = False

        if match and (not matchEntirety or endIdx == len(tokens)):
            return output[None]


def compile(grammar, allowSubGrammarDefinitions=True):
    """
    Constructs and returns an instance of _StringParser for repeated parsing of strings using the given grammar.
    """

    return _StringParser(grammar, allowSubGrammarDefinitions)


def match(grammar, inputString, matchEntirety=True, allowSubGrammarDefinitions=True):
    """
    Convenience function for performing matches using a grammar against a string.

    Inputs: grammar       - The grammar to use to parse the input string.
            inputString   - The string to be parsed.
            matchEntirety - A boolean, if True requires the entire string to be matched by the grammar.
                                       if False, trailing tokens not matched by the grammar will not
                                                 cause a match failure.
            allowSubGrammarDefinitions - A Boolean, indicating whether or not sub grammar declarations,
                                         (@name: grammar @@), should be processed.  If grammarString has
                                         come from an untrusted source this should be set to False, to
                                         mitigate the potential for a `Billion Laughs` attack.

    Outputs: The result of matching the inputString, if it matches, else None.
    """

    return _StringParser(grammar, allowSubGrammarDefinitions).match(inputString, matchEntirety=matchEntirety)
