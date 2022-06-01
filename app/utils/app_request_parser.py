from http import HTTPStatus
from flask_restx import abort
from flask_restx.reqparse import RequestParser
from werkzeug import exceptions
from flask import request

from config import Config


class AppRequestParser(RequestParser):
    def parse_args(self, req=None, strict=False):
        """
        Parse all arguments from the provided request and return the results as a ParseResult

        :param bool strict: if req includes args not in parser, throw 400 BadRequest exception
        :return: the parsed results as :class:`ParseResult` (or any class defined as :attr:`result_class`)
        :rtype: ParseResult
        """
        if req is None:
            req = request

        result = self.result_class()

        # A record of arguments not yet parsed; as each is found
        # among self.args, it will be popped out
        req.unparsed_arguments = (
            dict(self.argument_class("").source(req)) if strict else {}
        )
        error = ""
        for arg in self.args:
            value, found = arg.parse(req, True)
            if isinstance(value, ValueError):
                error = list(found.values())[0]
                found = None
                break
            if found or arg.store_missing:
                result[arg.dest or arg.name] = value
        if error:
            abort(HTTPStatus.BAD_REQUEST, error, status=Config.ERROR_STATUS)

        if strict and req.unparsed_arguments:
            arguments = ", ".join(req.unparsed_arguments.keys())
            msg = "Unknown arguments: {0}".format(arguments)
            abort(HTTPStatus.BAD_REQUEST, msg, status=Config.ERROR_STATUS)

        return result
