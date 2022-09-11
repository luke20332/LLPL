LLPL




Issues faced:

- IP blocking
It doesnt take a lot of web requests for a rate-driver to ban an IP, this posed an issue when trying to download the HTML file of a license plate.
Workarounds include doing less frequent requests, or using the downloaded document and working with that.
Another workaround is to use IP rotation, however this seems to be a paid service.

To solve this I just downloaded a free VPN provider, and will make HTTP GET requests sparingly.



Structure of the HTML document

The comments are stored in the following format:

<IMAGE HERE>



As we can see, the HTML div element is given an ID, which I will use to single out comments.

