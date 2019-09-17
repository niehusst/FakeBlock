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
 * @param visibility - Boolean, whether the inject HTML is displayed or not
 */
function injectBlock(targetPost) {
	//TODO determine which image/text to use based on response from API?
	// construct programatically instead? add id attribute??
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
	// TODO make it insert after profile head instead of before comments? not every post has comments (reposts are like 2 posts), but every post does have profile images
	var mark = targetPost.children(':first-child').children(':first-child').children(':first-child').next().children(':first-child').next();
	$(blocker_html).insertBefore(mark);
}

/** 
 * Removes a post blocking window by setting the CSS display
 * attribute to none of target grandparent (for use by blocker windows),
 * Then reveals the contents of the post that was blocked
 *
 * @param target - an object containing the pressed button element
 */
function closeBlock(target) {
	// since we know the exact HTML structure of blocking HTML that
	// this is called from, we can navigate directly to desired outer
	// element to make it not displayed
    $(target).parent().parent().toggle(false);

    // now redisplay the contents of the post
    toggleContents($(target).parent().parent().parent(), true);
}


/*
array of IDs of blocked posts; only need to iterate list activating/deactivating
each element when the extension is activated/deactivated
*/
var blockedPosts = [];

/**
 * For each post marked as blocked, set the display CSS atribute to block,
 * and hiding the post contents.
 */
function reblockAllFakePosts() {
    for(var postNum = 0; postNum < blockedPosts.length; postNum++) {
    	var post = $("#" + blockedPosts[postNum]);
    	toggleContents(post, false);
    	post.find('.bg_filler').toggle(true);
    }
}

/**
 * Set the display CSS atribute on any currently blocked posts to none
 * and reveal the hidden post contents.
 */
function unblockAllPosts() {
	for(var postNum = 0; postNum < blockedPosts.length; postNum++) {
    	var post = $("#" + blockedPosts[postNum]);
    	toggleContents(post, true);
    	post.find('.bg_filler').toggle(false);
    }
}



/** 
 * Remove or reveal contents (image, vid, text) from targetPost via display CSS
 *
 * @param targetPost - an object containing the target post element
 * @param visibility - Boolean, whether the post contents are displayed or not
 */
function toggleContents(targetPost, visibility) {
	// remove post text (set display='none')
	targetPost.find('div[data-testid="post_message"]').toggle(visibility); // toggle true to bring back
	// remove post images
	targetPost.find('a[data-render-location="newsstand"]').toggle(visibility);
	// remove post videos
	targetPost.find('div.mtm').toggle(visibility);
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


//TODO: is it ok that this is just true by default to start with?
// what about when chrome storage has saved false from prev session???
var activated = true; 

// catch runtime messages about activation state changes
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	activated = (request.todo === "blockPosts");
	if (!activated) {
		unblockAllPosts();
	} else { //block posts
		reblockAllFakePosts();
	}
});


// take action on all facebook posts
$(function() {
	var visitedPosts = {};
	
	// run a 'live query' on each post as it's added to DOM
	// TODO: sometimes misses first post?
	$(document).on('DOMNodeInserted', 'div[data-testid="fbfeed_story"]', function() {
		// dont run on posts that have already been examined
		if (!($(this).attr('id') in visitedPosts)) {

			// mark post as looked at
			visitedPosts[$(this).attr('id')] = true;
			
			if (isFakeNews($(this))) {

				// only hide contents of posts if activated
				if (activated) {
					// hide post contents and inject blocky notice
					toggleContents($(this), false);
					injectBlock($(this));
				}

				// save post as blocked
				//TODO unecessary???
				blockedPosts.push($(this).attr('id'));
			}
		}
	});

	// set up click event listening for blocked window buttons
	$(document).on('click', '.read_btn', function() {
		closeBlock($(this));
	});
});





