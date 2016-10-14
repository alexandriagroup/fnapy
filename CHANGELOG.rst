==========
Change log
==========

All notable changes to this project will be documented in this file.
The format is based on `Keep a Changelog`_ and this project adheres to `Semantic Versioning`_.

Unreleased
==========
Added
-----
* Work with sandbox and real account

Changed
-------
* Changed the API for FnapyConnection
* Set a list of eans as an argument in query_pricing

[0.6.0] - 2016-10-07
====================
Changed
-------
* Improved Query class

[0.5.1] - 2016-10-04
====================
Removed
-------
* Really remove BeautifulSoup (bs4) from dependencies

[0.5.0] - 2016-10-04
====================
Removed
-------
* Remove beautifulsoup dependency

Changed
-------
* Improve text extraction from XML

[0.4.3] - 2016-09-29
====================
Changed
-------
* Raise a FnapyPricingError if offers_data is not empty (in update_offers)

[0.4.2] - 2016-09-28
====================
Changed
-------
* Update documentation

[0.4.1] - 2016-09-28
====================
Added
-----
* Implement delete_offers

[0.4.0] - 2016-09-27
====================
Changed
-------
* Use pricing_query (V2)
* Check the connection passed to FnapyManager is a FnapyConnection
* Add a caveat in the README for the requests sent to the sandbox.
* Improve update_offers

Fixed
-----
* Fix Unicode/string confusion bug in Response

[0.2.0] - 2016-09-13
====================

Added
-----
* Support Python 3
* Implement Query class to allow complex queries

Changed
-------
* Update the documentation
* Make the manager authenticate when it is created.
* All the methods return a Response instance
* Store the XML requests as Request instances

Fixed
-----
* Fixed the packaging
* Test the Request and Response classes
* Fix minor things in the constructor of FnapyManager

[0.1.0] - 2016-08-31
====================
Added
-----
* Create the fnapy package

.. _Keep a changelog: http://keepachangelog.com/ 
.. _Semantic Versioning: http://semver.org/
