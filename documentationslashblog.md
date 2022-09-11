LLPL




Issues faced:

- IP blocking
It doesnt take a lot of web requests for a rate-driver to ban an IP, this posed an issue when trying to download the HTML file of a license plate.
Workarounds include doing less frequent requests, or using the downloaded document and working with that.
Another workaround is to use IP rotation, however this seems to be a paid service.

To solve this I just downloaded a free VPN provider, and will make HTTP GET requests sparingly.



Structure of the HTML document

The comments are stored in the following format:



'<div id='c281976' comment-id='281976' itemprop='comment' class='comment' itemscope itemtype='http://schema.org/Comment'><span class='plate'><a href='/H982FKL'>H982 FKL</a></span>
<meta itemprop='about' content='H982FKL'/><span style='float: right; margin-top: -10px; font-size: x-small; font-weight: bold;'>
<span class='name name-not-verified' itemprop='author'>Respectable driver</span><span class='date' itemprop='dateCreated'>2022-04-03 00:03:56</span></span>
<br/><br/><span class='text' itemprop='text'>Yes</span>	<div class="commentControls">

		  <button onclick="showCommentForm(281976); return false;" class="btn btn-mini btn-inverse respond"><i class="icon-comment icon-white"></i> Reply</button>

		  <meta itemprop="upvoteCount" content="1"/>

	  <meta itemprop="downvoteCount" content="0"/>

	 

	  <div style="float: right">

		<a title="Report comment" href="#" onclick="zglosKomentarz(281976); return false;" style="margin-right: 10px;"><i class="icon-ban-circle icon-white"></i></a>

				Rate this comment:

		<a title="Rate this comment" href="#" onclick="glosujKomentarz(281976, 1); return false;"><div class="plusMinus plus">+</div></a>

		<div class="plusMinus voteCount positive">1</div>

		<a title="Rate this comment" href="#" onclick="glosujKomentarz(281976, -1); return false;"><div class="plusMinus minus">-</div></a>

	  </div>

	  <div style="clear: both"></div>

				</div>'

As we can see, the HTML div element is given an ID, which I will use to single out comments.

