//content communications js
/*
has control over changing the DOM, but cant use chrome apis
*/

// tell event js to highlight icon when on correct page
chrome.runtime.sendMessage({todo: "showPageAction"});


// inject blocker html
function injectBlock(targetPost) {
	console.log("content inject");

	//TODO determine which image/text to use based on response from API
	// construct programatically instead?
	var blocker_html = `
	<div class="bg_filler">
		<div class="content_houser">
			<img class="block_img" src="https://i.imgur.com/zPuiLgy.png" alt="Blocked">
			<p class="block_txt">
				This post has been determined to contain fake news.
			</p>
		</div>
		<div class="btn_houser">
			<button class="read_btn">
				Read Anyway
			</button>
		</div>
	</div>`
	//warnign triangle
	//https://i.imgur.com/Y7dDZmK.png

	//blocky
	//https://i.imgur.com/zPuiLgy.png

	// inject html before comments div
	var mark = targetPost.children(':first-child').children(':first-child').children(':first-child').next().children(':first-child').next();
	$(blocker_html).insertBefore(mark);
}

// remove post contents
function removeContents(targetPost) {
	console.log("removing contents");
	// remove post text (set display='none')
	targetPost.find('div[data-testid="post_message"]').toggle(false); // toggle true to bring back
	// remove post images
	//targetPost.find('a[data-render-location="newsstand"]').toggle(false);
	// remove post videos
	targetPost.find('div.mtm').toggle(false);
	
	// TODO add marking attribute for easy toggling when plugin deactivated
}

// take action on all facebook posts
$(function() {
	console.log("right before live query");
	// run a 'live query' on each post as it's added to DOM
	// TODO: sometimes misses first post?
	$(document).on('DOMNodeInserted', 'div[data-testid="fbfeed_story"]', function() {

		removeContents($(this));

		injectBlock($(this));
		console.log('calls complete');
	});
});




