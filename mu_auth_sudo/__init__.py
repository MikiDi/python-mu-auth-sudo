import os
import logging
import typing
from collections.abc import Mapping

from SPARQLWrapper import SPARQLWrapper, JSON
from flask import request

# https://github.com/mu-semtech/mu-python-template/blob/9ed7afd4e6269567f732cc998632b8575c05b417/helpers.py#L23
logger = logging.getLogger('MU_PYTHON_TEMPLATE_LOGGER')

MU_HEADERS = [
    "MU-SESSION-ID",
    "MU-CALL-ID",
    # "MU-AUTH-ALLOWED-GROUPS", # We'll be using sudo, which overrules these.
    # "MU-AUTH-USED-GROUPS"
]

def sudo_sparql_client(query_type: str,
                       sparql_endpoint: str = None, extra_headers: Mapping[str, str] = None):
                       sparql_client = SPARQLWrapper(sparql_endpoint, returnFormat=JSON)
    if query_type == "update":
        sparql_client.method = "POST"

    # Usual mu headers
    for header in MU_HEADERS:
        if header in request.headers:
            sparql_client.addCustomHttpHeader(header, request.headers[header])

    # sudo header
    sparql_client.addCustomHttpHeader("mu-auth-sudo", "true")

    # extra header
    if extra_headers:
        for header_key, header_val in extra_headers.items():
            sparql_client.addCustomHttpHeader(header_key, header_val)

    return sparql_client

def query_sudo(querystring: str,
               extra_headers: Mapping[str, str] = None,
               sparql_endpoint: str = os.getenv("MU_SPARQL_ENDPOINT")):
    logger.info(querystring)
    sparql_client = sudo_sparql_client("query", sparql_endpoint, extra_headers)
    sparql_client.setQuery(querystring)
    return sparql_client.query().convert()

def update_sudo(querystring: str,
                extra_headers: Mapping[str, str] = None,
                sparql_endpoint: str = os.getenv("MU_SPARQL_UPDATEPOINT")):
    logger.info(querystring)
    sparql_client = sudo_sparql_client("update", sparql_endpoint, extra_headers)
    sparql_client.setQuery(querystring)
    if not sparql_client.isSparqlUpdateRequest():
        logger.warning("The query you're trying to run with 'update_sudo' doesn't look like an update query!\n" + querystring)
    return sparql_client.query()
