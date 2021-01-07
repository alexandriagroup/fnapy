.. _changelog:

Change log
==========

All notable changes to this project will be documented in this file.
The format is based on `Keep a Changelog`_ and this project adheres to
`Semantic Versioning`_.


[1.3.0] - 2021-01-07
--------------------
Changed
*******
* Change the argument for `query_pricing` to allow to specify any combination of code types
  and keep compatibility with the old version (a list of EANs when the code type is not specified)

[1.2.0] - 2021-01-07
--------------------
Changed
*******
* Allow more code types in `query_pricing` (not only Ean)

Fixed
*****
* Update the sandbox URL

[1.1.10] - 2020-06-23
---------------------
Fixed
*****
* Fix the encoding (raw bytes returned in FNAC responses not encoded in UTF8?)

[1.1.9] - 2019-06-11
--------------------
Fixed
*****
* Fix the encoding

[1.1.8] - 2019-03-13
--------------------
Fixed
*****
* Fix some tests and fixtures

Changed
*******
* Allow to send tracking information in orders_update (by rafaurl)

[1.1.7] - 2018-11-06
--------------------
Fixed
*****
* Prevent possible vulnerabilities due to requests<=2.19.1 (CVE-2018-18074)

Changed
*******
* Use pipenv for development
* FnapyResponseError is raised for invalid responses

[1.1.6] - 2017-04-26
--------------------
Fixed
*****
* Fix error when the content of a response is an empty string

[1.1.5] - 2017-01-12
--------------------
Fixed
*****
* Fix another utf-8 problem (from miss encoding xml)

[1.1.4] - 2017-01-12
--------------------
Fixed
*****
* Fix ``to_unicode``.

[1.1.3] - 2016-12-28
--------------------
Fixed
*****
* Fix ``extract_text``.


[1.1.2] - 2016-10-24
--------------------
Changed
*******
* No more tests in the package
* Display a message when no EAN is passed to ``query_pricing``.


[1.1.1] - 2016-10-21
--------------------
Changed
*******
* Display a message when the limit of EANs is reached in ``query_pricing``.

Fixed
*****
* Fix ``parse_xml``


[1.1.0] - 2016-10-17
--------------------
Changed
*******
* Display a log rather than raise a ``FnapyPricingError`` when a list of EANs is
  provided


[1.0.1] - 2016-10-17
--------------------
Fixed
*****
* Fixed bug in ``FnapyConnection``: when ``credentials`` is provided and if
  sandbox is False, a ``FnapyConnectionError`` is raised.


[1.0.0] - 2016-10-14
--------------------
Added
*****
* Working with sandbox or real account is now possible

Changed
*******
* ``FnapyConnection`` now accepts credentials dictionary or sandbox boolean
* ``query_pricing`` now accepts a list of EANs


[0.6.0] - 2016-10-07
--------------------
Added
*****
* In the ``Query`` class, added the ``was`` method to handle the states (especially
  the states of orders)


[0.5.1] - 2016-10-04
--------------------
Removed
*******
* Really remove ``BeautifulSoup`` (bs4) from the dependencies


[0.5.0] - 2016-10-04
--------------------
Removed
*******
* Remove ``BeautifulSoup`` dependency

Changed
*******
* Improve the text extraction from XML


[0.4.3] - 2016-09-29
--------------------
Changed
*******
* In ``update_offers``, ``FnapyUpdateOfferError`` is raised if: 
    - ``offer_reference`` and at least one of the optional parameters (except
      ``product_reference``) are not provided
    - ``offers_data`` is empty


[0.4.2] - 2016-09-28
--------------------
Changed
*******
* Update documentation


[0.4.1] - 2016-09-28
--------------------
Added
*****
* Implement ``delete_offers``


[0.4.0] - 2016-09-27
--------------------
Changed
*******
* Use pricing_query (V2)
* Check the connection passed to ``FnapyManager`` is a ``FnapyConnection``
* Add a caveat in the README for the requests sent to the sandbox.
* Improve ``update_offers``

Fixed
*****
* Fix Unicode/string confusion bug in ``Response``


[0.2.0] - 2016-09-13
--------------------
Added
*****
* Support Python 3
* Implement the ``Query`` class to allow complex queries
* Added new classes for requests and responses 
  (respectively ``Request`` and ``Response``)

Changed
*******
* Update the documentation
* Make the manager authenticate when it is created.
* All the methods return a ``Response`` instance
* Store the XML requests as ``Request`` instances

Fixed
*****
* Fixed the packaging
* Fix minor things in the constructor of ``FnapyManager``


[0.1.0] - 2016-08-31
--------------------
Added
*****
* Create the ``fnapy`` package

.. _Keep a changelog: http://keepachangelog.com/ 
.. _Semantic Versioning: http://semver.org/
