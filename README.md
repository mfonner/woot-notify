# Woot-Notify

A script to monitor user-specified deals on woot.com and email them to you.

## Getting Started

Ideally, this is run via a scheduler (like cron) on a cloud server or local machine

### Prerequisites

* [Requests](https://pypi.org/project/requests/) - I enjoy working with this library over httplib and urllib

### Arguments

Required arguments include

* -e for the email address to send matching search results
* -f for the feed to search for. The list of available feeds are documented in woot.py

Optional args

* -s for the sub filter to search on. An example would be Bedding if filtering on the parent of Home. Additional filters can be found on https://developer.woot.com/
* -c for any additional search criteria to filter results with