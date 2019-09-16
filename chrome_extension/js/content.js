//content communications js
/*
has control over changing the DOM, but cant use chrome apis
*/

// tell event js to highlight icon when on correct page
chrome.runtime.sendMessage({todo: "showPageAction"});


/** 
 * Inject blocker html before the comments html
 *
 * @param targetPost - an object containing the target post element
 */
function injectBlock(targetPost) {

	//TODO determine which image/text to use based on response from API?
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
	// TODO make it insert after profile head instead of before comments? not every post has comments (reposts are like 2 posts)
	var mark = targetPost.children(':first-child').children(':first-child').children(':first-child').next().children(':first-child').next();
	$(blocker_html).insertBefore(mark);
}

/** 
 * Remove contents (image, vid, text) from targetPost
 *
 * @param targetPost - an object containing the target post element
 */
function removeContents(targetPost) {
	console.log("removing contents");
	// remove post text (set display='none')
	targetPost.find('div[data-testid="post_message"]').toggle(false); // toggle true to bring back
	// remove post images
	targetPost.find('a[data-render-location="newsstand"]').toggle(false);
	// remove post videos
	targetPost.find('div.mtm').toggle(false);
	
	// TODO add marking attribute for easy toggling when plugin deactivated
}

/** 
 * Determine if a post is fake news or not by calling APIs
 *
 * @param targetPost - an object containing the target post element
 * @return - Boolean, TODO: change this to include information about which tool determined fake?
 */
function isFakeNews(targetPost) {
	//TODO: call APIs
	return Math.round(Math.random());
}

// take action on all facebook posts
$(function() {
	console.log("right before live query");
	// run a 'live query' on each post as it's added to DOM
	// TODO: sometimes misses first post?
	var visitedPosts = {};
	$(document).on('DOMNodeInserted', 'div[data-testid="fbfeed_story"]', function() {
		// dont run on posts that have already been examined
		if (!($(this).attr('id') in visitedPosts)) {

			// mark post as looked at
			visitedPosts[$(this).attr('id')] = true;
			
			if (isFakeNews($(this))) {
				removeContents($(this));
				injectBlock($(this));
			}
		}
	});
});




