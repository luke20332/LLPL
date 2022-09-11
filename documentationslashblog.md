LLPL




Issues faced:

- IP blocking
It doesnt take a lot of web requests for a rate-driver to ban an IP, this posed an issue when trying to download the HTML file of a license plate.
Workarounds include doing less frequent requests, or using the downloaded document and working with that.
Another workaround is to use IP rotation, however this seems to be a paid service.

To solve this I just downloaded a free VPN provider, and will make HTTP GET requests sparingly.



Structure of the HTML document

The comments are stored in the following format, and begin at line 320:


</div><div id='c267920' comment-id='267920' itemprop='comment' class='comment' itemscope itemtype='http://schema.org/Comment'><span class='plate'><a href='/H982FKL'>H982 FKL</a></span>
<meta itemprop='about' content='H982FKL'/><span style='float: right; margin-top: -10px; font-size: x-small; font-weight: bold;'>
<span class='name name-not-verified' itemprop='author'>Michael Jackson</span><span class='date' itemprop='dateCreated'>2021-10-01 23:21:48</span></span>
<br/><br/><span class='text' itemprop='text'>My friend Chester had this car since 1993
<br/>
</span>	<div class="commentControls">



As we can see, the HTML div element is given an ID, which I will use to single out comments.

We will parse the page by selecting a specific element by its ID.

in HTML, every element can have an id attribute assigned, making it identifiable. For us, each comment is of the form 'cXXXXXX', x being a number.
The 4th ID is the first comment.

every comment is wrapped in a div element with the class 'comment'