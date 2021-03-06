//content communications js
/*
has control over changing the DOM, but cant use chrome apis
*/

// tell event js to highlight icon when on correct page
chrome.runtime.sendMessage({todo: "showPageAction"});

// tell event js to tell us the initial state of activation
chrome.runtime.sendMessage({todo: "initialLoad"});

// global that holds the activation state of the plugin. Is set via messages from events.js
var activated = true; 

/*
array of IDs of blocked posts; only need to iterate list activating/deactivating
each element when the extension is activated/deactivated
*/
var blockedPosts = [];

/** 
 * Inject blocker html before the Facebook post comments html.
 *
 * @param targetPost - an object containing the target post element
 * @param visibility - Boolean, whether the inject HTML is displayed or not
 * @param confidence - Float, confidence level of the post being fake (0-1 range)
 */
function injectBlock(targetPost, visibility, confidence) {
	// construct HTML to insert to "block" a post. TODO: construct programatically instead?
	var blocker_html1 = `
	<div class="bg_filler" style="display: `
	// set visibility of block
	if (visibility) {
		blocker_html1 += 'block';
	} else {
		blocker_html1 += 'none';
	}

	var blocker_html2 = `;">
		<div class="content_houser">
			<img class="block_img" src="https://i.imgur.com/zPuiLgy.png" alt="Blocked">
			<p class="block_txt">
				This post has been judged to be <b>` + Math.floor(confidence*100) + `%</b> likely to contain fake news.
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
	$(blocker_html1.concat(blocker_html2)).insertBefore(mark);
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
	// post text 
	targetPost.find('div[data-testid="post_message"]').toggle(visibility);
	// post images
	targetPost.find('a[data-render-location="newsstand"]').toggle(visibility);
	// post videos
	targetPost.find('div.mtm').toggle(visibility);
}


/**
 * Retrieve text contents of targetPost, if any. Returns empty string when
 * targetPost contains no text.
 *
 * @param targetPost - a jQuery object containing the post to fetch text from
 * @return - String, the text contents of the post, or empty string
 */
function getPostText(targetPost) {
	var pElem = targetPost.find('p');
	// ensure we found anything
	if (pElem.length) {
		return String(pElem.text());
	} else {
		return '';
	}
}

/**
 * Retrieve the text from targetPost's news banner, if there is
 * one present in targetPost (else empty string).
 *
 * @param targetPost - a jQuery object, containing the HTML to search in
 * @return - String, the contents of the news banner, or empty string
 */
function getNewsText(targetPost) {
	var newsElem = targetPost.find('div.ellipsis');
	// ensure we found anything
	if (newsElem.length) {
		return String(newsElem.parent().parent().next().children().children().text());
	} else {
		// no news banner in this post
		return '';
	}
}

/** 
 * Determine if a post is fake news or not by calling FakeBlock API. The 
 * response is asynchronously handled by a Promise; the target post saved into
 * the array of blocked posts or not once the API responds with the 
 * determination of the post's validity.
 *
 * @param targetPost - a jQuery object containing the target post element
 * @return - None, run for the side-effects
 */
function isFakeNews(targetPost) {
	var newsText = getNewsText(targetPost); 
	var postText = getPostText(targetPost); 

	//tell events script to make API call
	chrome.runtime.sendMessage(
		{todo: "apiCall", text: postText, news: newsText},
		response => {
			// async handling of response
			if (response["fake"]) {
				if (activated) {
					// hide post contents and inject blocky notice
					toggleContents(targetPost, false);
				}
				injectBlock(targetPost, activated, response["confidence"]); 

				// save post as blocked
				blockedPosts.push(targetPost.attr('id'));
			}
		});
}


// catch runtime messages about activation state changes
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	activated = (request.todo === "blockPosts");
	if (!activated) {
		unblockAllPosts();
	} else {
		reblockAllFakePosts();
	}
});


// take action on each facebook post once page loads
$(function() {
	var visitedPosts = {};
	
	// act on each post as it's added to DOM
	// TODO: sometimes misses first post?
	$(document).on('DOMNodeInserted', 'div[data-testid="fbfeed_story"]', function() {
		// dont run on posts that have already been examined
		if (!($(this).attr('id') in visitedPosts)) {

			// mark post as looked at
			visitedPosts[$(this).attr('id')] = true;
			
			isFakeNews($(this)); 
		}
	});

	// set up click event listening for blocked window buttons
	$(document).on('click', '.read_btn', function() { 
		closeBlock($(this));
	});
});





