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
	$(document).on('DOMNodeInserted', 'div[data-testid="fbfeed_story"]', function() {
		console.log("removing everything");

		// remove post text
		$(this).find('div[data-testid="post_message"]').toggle(false); // toggle true to bring back
		// remove post images
		$(this).find('a[data-render-location="newsstand"]').toggle(false);
		// remove post videos
		$(this).find('div.mtm').toggle(false);
		
		// TODO add marking attribute for easy toggling when plugin deactivated
	});
});

