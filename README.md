# scena9\_events

Web application for displaying information about cultural events gathered from various sources.



It uses a python scraper with beautiful soup to parse the HTML data, and then display the information on the localhost using flask in python



3.29.2026



1. It uses the scraper for a html site of a local venue, and have extracted the right title and date. However, the structure of the site is such that the events are contained within the date, and not vice versa. Therefore, I am iterating through all the divs with class="date", extracting the date, and finding events within that date section using class="events". The problem is that this method appends more information after the date, as the class="date" condition might be a little too loose.

