<p algin="center"><img src="https://raw.githubusercontent.com/CLARIAH/grlc/master/src/static/grlc_logo_01.png" width="250px"></p>

[![Join the chat at https://gitter.im/grlc](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/grlc/Lobby#)
[![DOI](https://zenodo.org/badge/46131212.svg)](https://zenodo.org/badge/latestdoi/46131212)
[![Build Status](https://travis-ci.org/CLARIAH/grlc.svg?branch=master)](https://travis-ci.org/CLARIAH/grlc)


grlc, the <b>g</b>it <b>r</b>epository <b>l</b>inked data API <b>c</b>onstructor, automatically builds Web APIs using SPARQL queries stored in git repositories. http://grlc.io/

## What is grlc ?
grlc is a lightweight server that takes SPARQL queries (stored in a GitHub repository, local file storage or listed in a URL), and translates them to Linked Data Web APIs. This enables universal access to Linked Data. Users are not required to know SPARQL to query their data, but instead can access a web API.

## Quick tutorial
For a quick usage tutorial check out our wiki walkthrough [here](https://github.com/CLARIAH/grlc/wiki/Quick-tutorial).

## Features
TODO:
 - Move features full list of features to wiki.
 - Proof-read list of features.
 - Point each feature to an example.

- Request parameter mappings into SPARQL: grlc is compliant with [BASIL's convention](https://github.com/the-open-university/basil/wiki/SPARQL-variable-name-convention-for-WEB-API-parameters-mapping) on how to map GET/POST request parameters into SPARQL
- Automatic, user customizable population of parameter values in swagger-ui's dropdown menus via SPARQL triple pattern querying
- Parameter values as enumerations (i.e. closed lists of values that will fill a dropdown in the UI) can now also be specified in the query decorators to save endpoint requests (see [this example](https://github.com/albertmeronyo/lodapi/blob/master/houseType_params.rq))
- Parameter default values can now also be indicated through decorators (see [this example](https://github.com/albertmeronyo/lodapi/blob/master/dbpedia_test.rq))
- URL-based content negotiation: you can request for specific content types by attaching them to the operation request URL, e.g. [http://localhost:8088/CEDAR-project/Queries/residenceStatus_all.csv](http://localhost:8088/CEDAR-project/Queries/residenceStatus_all.csv) will request for results in CSV
- Pagination of API results, as per the `pagination` decorator and [GitHub's API Pagination Traversal](https://developer.github.com/guides/traversing-with-pagination/)
- Docker images in Docker Hub for easy deployment
- Compatibility with [Linked Data Fragments](http://linkeddatafragments.org/) servers, RDF dumps, and HTML+RDFa files
- grlc integrates now [SPARQLTransformer](https://github.com/D2KLab/py-sparql-transformer), allowing the use of queries in JSON (see [this example](https://github.com/albertmeronyo/lodapi/blob/master/dbpedia_test_json.json)).
- Generation of provenance in [PROV](https://www.w3.org/TR/prov-primer/) of both the repo history (via [Git2PROV](https://github.com/IDLabResearch/Git2PROV)) and grlc's activity additions
- Commit-based API versioning that's coherent with the repo versioning with git hashes
- SPARQL endpoint address can be set at the query level, repository level, and now also as a query **parameter**. This makes your APIs endpoint agnostic, and enables for generic and transposable queries!
- CONSTRUCT queries are now mapped automatically to GET requests, accept parameters in the WHERE clause, and return content in ``text/turtle`` or ``application/ld+json``
- INSERT DATA queries are now mapped automatically to POST requests. Support is limited to queries with no WHERE clause, and parameters are always expected to be values for ``g`` (named graph where to insert the data) and ``data`` (with the triples to insert, in ``ntriples`` format). The INSERT query pattern is so far static, as defined in [static.py](https://github.com/CLARIAH/grlc/blob/master/src/static.py#L61). Only tested with Virtuoso.

## Usage

grlc assumes that you have a collection of SPARQL queries as .rq files (like in [this one](https://github.com/CEDAR-project/Queries)). grlc will create an API operation per such a SPARQL query/.rq file. Your queries can include special [decorators](#decorator-syntax) to add extra functionality to your API.

### Query location

grlc can load your query collection from different locations. Each type of location has specific functionality features are accessible via different paths. However all location types produce the same beautiful API's.

#### From a Github repository
> API path: 
`http://grlc-server/api-git/<user>/<repo>`

grlc can build an API from any Github repository, specified by the github user name of the owner and repository name.

For example, assuming your queries are stored on a Github repo: `https://github.com/albertmeronyo/lodapi/`, point your browser to the following location
`http://grlc.io/api-git/albertmeronyo/lodapi/`

grlc can make use of Github version control mechanism to generate an API based on a specific version of queries in the repository. This can be done by including the commit sha in the URL path (`http://grlc-server/api-git/<user>/<repo>/commit/<sha>`), for example: `http://grlc.io/api-git/albertmeronyo/lodapi/commit/321b9c9889128d21e9ae76b1884a81fc50dbf34f`

grlc can also use a subdirectory inside your Github repo. This can be done by including a subdirectory in the URL path (`http://grlc-server/api-git/<user>/<repo>/subdir/<subdir>`) **TODO: include an example.**

#### From local storage
> API path: 
`http://grlc-server/api-local/`

grlc can generate an API from a local directory in the computer where your grlc server runs. You can configure the location of this folder in your [grlc server configuration file](#grlc-server-configuration).
 
#### From a specification file
> API path: 
`http://grlc-server/api-url/?specUrl=<specUrl>`

grlc can generate an API from a yaml specification file accessible on the web.

For example, ssuming your queries are listed on spec file: `https://raw.githubusercontent.com/albertmeronyo/lodapi/master/urls.yml`, point your browser to the following location
`http://grlc.io/api-url?specUrl=https://raw.githubusercontent.com/albertmeronyo/lodapi/master/urls.yml`

**TODO: insert syntax of spec file here or point to section with details of the specification file.**

### Grlc generated API

The API paths of all location types point o the generated swagger-ui style API documentation. On the API documentation page, you can explore available API calls and execute individual API calls.

You can also view the swagger spec of your API, by visiting `<API-path>/spec/`, for example: `http://grlc.io/api-git/albertmeronyo/lodapi/spec/`

### Grlc query execution
When you call an API endpoint, grlc executes the SPARQL query for that endpoint.

There are 4 options to specify your own endpoint:

* Add a `sparql_endpoint` on your [`config.ini`](#grlc-server-configuration)
* Add a `endpoint` parameter to your request: 'http://grlc.io/user/repo/query?endpoint=http://sparql-endpoint/'. You can add a `#+ endpoint_in_url: False` decorator if you DO NOT want to see the `endpoint` parameter in the swagger-ui of your API.
* Add the `#+ endpoint:` [decorator](#`endpoint`).
* Add the URL of the endpoint on a single line in an `endpoint.txt` file within the GitHub repository that contains the queries.

The endpoint call will return the result of executing the query as a json representation of rdflib.query.QueryResult. The format of the response can be modified by using the `#+ transform:` [decorator](#`transform`).

## Decorator syntax
Special decorators are available to make your swagger-ui look nicer and to increase functionality. These are provided as comments at the start of your query file. All decorators start `#+ `, for example:

```SPARQL
#+ decorator_1: decorator value
#+ decorator_1: decorator value

SELECT * WHERE {
  ?s ?p ?o .
}
```
The following is a list of available decorators and their function:

### `summary` 
Creates a summary of your query/operation. Example: `#+ summary: This is the summary of my query/operation`

### `endpoint`
Specifies a query-specific endpoint. Example: `#+ endpoint: http://example.com/sparql`

### `pagination`
Paginates the results in groups of (for example) 100. Example: `#+ pagination: 100`

### `method`
Indicates the HTTP request method (`GET` and `POST` are supported). Example: `#+ method: GET`.

### `tags`
Assign tags to your query/operation. Query/operations with the same tag are grouped together in the swagger-ui. Example:
```
#+ tags:
#+   - firstTag
#+   - secondTag
```

### `enumerate`
Indicates which parameters of your query/operation should get enumerations (and get dropdown menus in the swagger-ui) using the given values from the SPARQL endpoint. For example:
```
#+ enumerate:
#+   - var1
#+   - var2
```
The values for each enumeration variable can also be specified into the query decorators to save endpoint requests and speed up the API generation. For example:
```
#+ enumerate:
#+   - var1:
#+     - value1
#+     - value2
```
Notice that these should be plain variable names without SPARQL/BASIL conventions (so `var1` instead of `?_var1_iri`)

###  `endpoint_in_url`
Allows/disallows the `endpoint` parameter from being provided as a URL parameter (allowed by default). Example:
```
#+ endpoint_in_url: False
```

###  `transform`
Allows  query results to be converted to the specified JSON structure, by using [SPARQLTransformer](https://github.com/D2KLab/py-sparql-transformer) syntax. Example: 
```
#+ transform: {
#+     "key": "?p",
#+     "value": "?o",
#+     "$anchor": "key"
#+   }
```

See examples at [https://github.com/albertmeronyo/lodapi](https://github.com/albertmeronyo/lodapi).

### Example APIs

Check these out:

- http://grlc.io/api/CLARIAH/wp4-queries-hisco/
- http://grlc.io/api/albertmeronyo/lodapi/
- http://grlc.io/api/albertmeronyo/lsq-api

You'll find the sources of these and many more in [GitHub](https://github.com/search?o=desc&q=endpoint+summary+language%3ASPARQL&s=indexed&type=Code&utf8=%E2%9C%93)

Use [this GitHub search](https://github.com/search?q=endpoint+summary+language%3ASPARQL&type=Code&utf8=%E2%9C%93) to see examples from other grlc users.

## Install and run
You can use grlc in different ways: 
 - [Via grlc.io](#grlc.io): you can use the [grlc.io service](https://grlc.io/)
 - [Via Docker](#Docker): you can use the [grlc docker image](https://hub.docker.com/r/clariah/grlc) and start your own grlc server.
 - [Via pip](#Pip): you can install the [grlc Python package](https://pypi.org/project/grlc/) and start your own grlc server or use grlc as a Python library.

More details for each of these options are given below.

### grlc.io
The easiest way to use grlc is by visiting [grlc.io](http://grlc.io/) and using this service to convert SPARQL queries into a RESTful API. Your queries can be [stored on a github repo](#from-a-github-repository) or can be [listed on a specification file](#from-a-specification-file).

### Docker
To run grlc via [docker](https://www.docker.com/), you'll need a working installation of docker. To deploy grlc, just pull the [latest image from Docker hub](https://hub.docker.com/r/clariah/grlc/). :
```bash
docker run -it --rm -p 8088:80 clariah/grlc
```

The docker image allows you to setup several environment variable such as `GRLC_SERVER_NAME` `GRLC_GITHUB_ACCESS_TOKEN` and `GRLC_SPARQL_ENDPOINT`:
```bash
docker run -it --rm -p 8088:80 -e GRLC_SERVER_NAME=grlc.io -e GRLC_GITHUB_ACCESS_TOKEN=xxx -e GRLC_SPARQL_ENDPOINT=http://dbpedia.org/sparql -e DEBUG=true clariah/grlc
```

### Pip
If you want to run grlc locally or use it as a library, you can install grlc on your machine. Grlc is [registered in PyPi](https://pypi.org/project/grlc/) so you can install it using pip.

#### Prerequisites
Grlc has the following requirements:
- Python3
- development files (depending on your OS):
```bash
sudo apt-get install libevent-dev python-all-dev
```

#### pip install
Once the base requirements are satisfied, you can install grlc like this:
```bash
pip install grlc
```

Once grlc is installed, you have several options:
 - [Stand alone server](#Standalone-server)
 - [Using a WSGI server](#Using-a-WSGI-server)
 - [As a python library](#Grlc-library)

#### Standalone server
Grlc includes a command line tool which you can use to start your own grlc server:
```bash
grlc-server
```

#### Using a WSGI server
You can run grlc using a WSGI server such as gunicorn as follows:
```bash
gunicorn grlc.server:app
```

If you want to use your own gunicorn configuration, for example `gunicorn_config.py`:
```python
workers = 5
worker_class = 'gevent'
bind = '0.0.0.0:8088'
```
Then you can run it as:
```bash
gunicorn -c gunicorn_config.py grlc.server:app
```

**Note:** Since `gunicorn` does not work under Windows, you can use `waitress` instead:
```bash
waitress-serve --port=8088 grlc.server:app
```

If you want to run grlc at system boot as a service, you can find example upstart scripts at [upstart/](upstart/grlc-docker.conf)

#### Grlc library
You can use grlc as a library directly from your own python script. See the [usage example](https://github.com/CLARIAH/grlc/blob/master/doc/notebooks/GrlcFromNotebook.ipynb) to find out more.

#### Grlc server configuration
Regardless of how you are running your grlc server, you will need to configure it using the `config.ini` file. Have a look at the [example config file](./config.default.ini) to see how it this file is structured.

The configuration file contains the following variables:
 - `github_access_token` [access token](#github-access-token) to communicate with Github API.
 - `local_sparql_dir` local storage directory where [local queries](#from-local-storage) are located.
 - `server_name` name of the server (e.g. grlc.io)
 - `sparql_endpoint` default SPARQL endpoint
 - `user` and `password` SPARQL endpoint default authentication (if required, specify `'none'` if not required)
 - `debug` enable debug level logging.

##### Github access token
In order for grlc to communicate with GitHub, you'll need to tell grlc what your access token is:

1. Get a GitHub personal access token. In your GitHub's profile page, go to _Settings_, then _Developer settings_, _Personal access tokens_, and _Generate new token_
2. You'll get an access token string, copy it and save it somewhere safe (GitHub won't let you see it again!)
3. Edit your `config.ini` or `docker-compose.yml` as value of the environment variable `GRLC_GITHUB_ACCESS_TOKEN`.

# Contribute!
grlc needs **you** to continue bringing Semantic Web content to developers, applications and users. No matter if you are just a curious user, a developer, or a researcher; there are many ways in which you can contribute:

- File in bug reports
- Request new features
- Set up your own environment and start hacking

Check our [contributing](CONTRIBUTING.md) guidelines for these and more, and join us today!

If you cannot code, that's no problem! There's still plenty you can contribute:

- Share your experience at using grlc in Twitter (mention the handler **@grlcldapi**)
- If you are good with HTML/CSS, [let us know](mailto:albert.merono@vu.nl)

## Related tools
- [SPARQL2Git](https://github.com/albertmeronyo/SPARQL2Git) is a Web interface for editing SPARQL queries and saving them in GitHub as grlc APIs.
- [grlcR](https://github.com/CLARIAH/grlcR) is a package for R that brings Linked Data into your R environment easily through grlc.
- [Hay's tools](https://tools.wmflabs.org/hay/directory/#/showall) lists grlc as a Wikimedia-related tool :-)

## This is what grlc users are saying
- [Flavour your Linked Data with grlc](https://blog.esciencecenter.nl/flavour-your-linked-data-with-garlic-98bfbb358e06), by Carlos Martinez
- [Converting any SPARQL endpoint to an OpenAPI](http://chem-bla-ics.blogspot.com/2018/07/converting-any-sparql-endpoint-to.html) by Egon Willighagen

Quotes from grlc users:
> A cool project that can convert a random SPARQL endpoint into an OpenAPI endpoint

> It enables us to quickly integrate any new API requirements in a matter of seconds, without having to worry about configuration or deployment of the system

> You can store your SPARQL queries on GitHub and then you can run your queries on your favourite programming language (Python, Javascript, etc.) using a Web API (including swagger documentation) just as easily as loading data from a web page

**Contributors:**	[Albert Meroño](https://github.com/albertmeronyo), [Rinke Hoekstra](https://github.com/RinkeHoekstra), [Carlos Martínez](https://github.com/c-martinez)

**Copyright:**	Albert Meroño, VU University Amsterdam  
**License:**	MIT License (see [LICENSE.txt](LICENSE.txt))

## Academic publications

- Albert Meroño-Peñuela, Rinke Hoekstra. “grlc Makes GitHub Taste Like Linked Data APIs”. The Semantic Web – ESWC 2016 Satellite Events, Heraklion, Crete, Greece, May 29 – June 2, 2016, Revised Selected Papers. LNCS 9989, pp. 342-353 (2016). ([PDF](https://link.springer.com/content/pdf/10.1007%2F978-3-319-47602-5_48.pdf))
- Albert Meroño-Peñuela, Rinke Hoekstra. “SPARQL2Git: Transparent SPARQL and Linked Data API Curation via Git”. In: Proceedings of the 14th Extended Semantic Web Conference (ESWC 2017), Poster and Demo Track. Portoroz, Slovenia, May 28th – June 1st, 2017 (2017). ([PDF](https://www.albertmeronyo.org/wp-content/uploads/2017/04/sparql2git-transparent-sparql-4.pdf))
- Albert Meroño-Peñuela, Rinke Hoekstra. “Automatic Query-centric API for Routine Access to Linked Data”. In: The Semantic Web – ISWC 2017, 16th International Semantic Web Conference. Lecture Notes in Computer Science, vol 10587, pp. 334-339 (2017). ([PDF](https://www.albertmeronyo.org/wp-content/uploads/2017/07/ISWC2017_paper_430.pdf))
