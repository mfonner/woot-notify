# Woot-Notify

A script to monitor user-specified deals on woot.com and email them to you.

## Getting Started

Ideally, this is run via a scheduler (like cron) on a machine that can send outbound mail (I'm using port 465 by default)

### Prerequisites

* [Requests](https://pypi.org/project/requests/) - I enjoy working with this library over httplib and urllib

### Environment variables

This script looks for two environment variables:

* WOOT_KEY - The API key to access woot.com. A key can be requested [here](https://forums.woot.com/t/request-developer-api-key/734283)
* EMAIL_KEY - The token used to authenticate to your email provider of choice

### Arguments

Required arguments include

* -e for the email address to send matching search results
* -f for the feed to search for. The list of available feeds are documented in woot.py

Optional args

* -s for the sub filter to search on. An example would be Bedding if filtering on the parent of Home. Additional filters can be found on https://developer.woot.com/
* -c for any additional search criteria to filter results with