import os
import logging
from SPARQLWrapper import SPARQLWrapper, JSON

# https://github.com/mu-semtech/mu-python-template/blob/9ed7afd4e6269567f732cc998632b8575c05b417/helpers.py#L23
logger = logging.getLogger('MU_PYTHON_TEMPLATE_LOGGER')

def sudo_sparql_client(extra_headers, sparql_endpoint, query_type):
    if query_type == "query":
        sparql_endpoint = os.getenv("MU_SPARQL_ENDPOINT")
    elif query_type == "update":
        sparql_endpoint = os.getenv("MU_SPARQL_UPDATEPOINT")

    sparql_client = SPARQLWrapper(sparql_endpoint, returnFormat=JSON)

    if query_type == "update":
        sparql_client.method = "POST"

    sparql_client.addCustomHttpHeader("mu-auth-sudo", "true")
    if extra_headers:
        for header_key, header_val in extra_headers.items():
            sparql_client.addCustomHttpHeader(header_key, header_val)

    return sparql_client

def query_sudo(querystring, extra_headers, sparql_endpoint):
    logger.info(querystring)
    sparql_client = sudo_sparql_client(extra_headers, sparql_endpoint, "query")
    sparql_client.setQuery(querystring)
    return sparql_client.query().convert()


def update_sudo(querystring, extra_headers, sparql_endpoint):
    logger.info(querystring)
    sparql_client = sudo_sparql_client(extra_headers, sparql_endpoint, "update")
    sparql_client.setQuery(querystring)
    if not sparql_client.isSparqlUpdateRequest():
        logger.warning("The query you're trying to run with 'update_sudo' doesn't look like an update query!\n" + querystring)
    return sparql_client.query()
