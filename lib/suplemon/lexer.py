# -*- encoding: utf-8

import pygments
import pygments.token
import pygments.lexers


class Lexer:
    def __init__(self, app):
        self.app = app
        self.token_map = {
            pygments.token.Comment: "comment",
            pygments.token.Comment.Single: "comment",
            pygments.token.Operator: "keyword",
            pygments.token.Name.Function: "entity.name.function",
            pygments.token.Name.Class: "entity.name.class",
            pygments.token.Name.Tag: "entity.name.tag",
            pygments.token.Name.Attribute: "entity.other.attribute-name",
            pygments.token.Name.Variable: "variable",
            pygments.token.Name.Builtin.Pseudo: "constant.language",
            pygments.token.Literal.String: "string",
            pygments.token.Literal.String.Doc: "string",
            pygments.token.Punctuation: "punctuation",
            pygments.token.Literal.Number: "constant.numeric",
            pygments.token.Name: "entity.name",
            pygments.token.Keyword: "keyword",
            pygments.token.Generic.Deleted: "invalid",
        }

    def lex(self, code, lex):
        """Return tokenified code.

        Return a list of tuples (scope, word) where word is the word to be
        printed and scope the scope name representing the context.

        :param str code: Code to tokenify.
        :param lex: Lexer to use.
        :return:
        """
        if lex is None:
            if not type(code) is str:
                # if not suitable lexer is found, return decoded code
                code = code.decode("utf-8")
            return (("global", code),)

        words = pygments.lex(code, lex)

        scopes = []
        for word in words:
            token = word[0]
            scope = "global"

            if token in self.token_map.keys():
                scope = self.token_map[token]

            scopes.append((scope, word[1]))
        return scopes
