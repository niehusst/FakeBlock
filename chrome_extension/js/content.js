//content communications js
/*
has control over changing the DOM, but cant use chrome apis
*/

// tell event js to highlight icon when on correct page
chrome.runtime.sendMessage({todo: "showPageAction"});


// remove all text and image elements from posts
$(function() {
	console.log("right before live query");
	// run a 'live query' on each post as it's added to DOM
	// TODO: use jquery .each to call hidePostContents on ALL matching elements (use with on somehow?)
	$('div[data-testid="fbfeed_story"]').on('DOMNodeInserted', hidePostContents());
	
});

function hidePostContents() {
	console.log("inside callback");
	//each post has a unique id="hyperfeed_story_id_5d7ce8b3d8d618d30086220"
	//post is enclosed in div: data-testid="fbfeed_story"

	// post text enclosed in div: data-testid="post_message"

	// image may be selectable by following attribute?
	//   a: data-render-location="newsstand"
	//   div: class="uiScaledImageContainer"

	// video may be selectable (where accompanying text was determined bad) with
	//   div: class="mtm"  ???
	console.log(this);
	console.log($(this));

	var postText = $(this).find( $('div[data-testid="post_message"]') );//.toggle(false);

	var postImage = $(this).find('a[data-render-location="newsstand"]').toggle(false);

	var postVid = $(this).find('div.mtm').toggle(false);

	console.log(postText);
	console.log(postVid);
	console.log(postImage);
	
	console.log("printed info?");
	postText.style.display = 'none';
	//document.querySelector('div[data-testid="fbfeed_story"] div[data-testid="post_message"]').style.display = 'none';

	// TODO add marking attribute for easy toggling when plugin deactivated
}