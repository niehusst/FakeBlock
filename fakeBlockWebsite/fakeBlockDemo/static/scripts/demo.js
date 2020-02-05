// demo.js

/**
 * Animate a smooth page scroll on button (id=try-btn) click to its href target
 * Code modified from W3 schools tutorial:
 * https://www.w3schools.com/howto/howto_css_smooth_scroll.asp
 */
$(document).ready(function(){
	// Add smooth scrolling to all links
	$("#try-btn").on('click', function(event) {

		// Make sure this.hash has a value before overriding default behavior
		if (this.hash !== "") {
			// Prevent default anchor click behavior
			event.preventDefault();

			// Store hash
			var hash = this.hash;

			// Using jQuery's animate() method to add smooth page scroll
			// 800 specifies the number of milliseconds animation lasts
			$('html, body').animate({
				scrollTop: $(hash).offset().top
			}, 800, function(){

				// Add hash (#) to URL when done scrolling (mimic click behavior)
				window.location.hash = hash;
			});
		}
	});

});

// set up click event listening for making a post
$(document).on('click', '#make-post', function(event) {
	// grab text from form
	var post_text = $("#posttxt").val();

	if(post_text) {
		// set make-post window to none
		$("#postbody").hide();
		// set posted window to visible
		$("#postedbody").show();

		// put text from form into posted window
		$("#postedtxt").text(post_text);

		// make fetch call to FakeBlock API using post_text
		const postData = {
			headers: {
				'Accept': "application/json",
				'content-type': "application/json"
			},
			body: JSON.stringify({
				post_text: post_text,
				news_text: null
			}),
			method: "POST"
		};
		const apiUrl = 'http://127.0.0.1:8000/api/fake'; //TODO: change to real url after deploy 2 heroku

		fetch(apiUrl, postData)
		.then(response => response.json())
		.then(data => handleAPIResponse(data)) // change status and blocking
		.catch(error => handleAPIResponse({fake: false}));

	}
});

// set up click event listening for blocked window buttons
$(document).on('click', '.read_btn', function() {
	closeBlock($(this));
});


/**
 * Handle the response to the Fakeblock API; unhide the correct status image
 * and block or not block the post based on response.
 * 
 * @param response - Dictionary, the JSON response from the API. Must
 *					 contain the boolean field `fake`. If `fake` is true, 
 *					 it will contain the float field `confidence` (0-1 range).
 * @return - null, run for the side effects					 
 */
function handleAPIResponse(response) {
	// always hide old status image
	$("#status-place-hold").hide();

	if(response.fake) {
		$("#status-negative").show();
		$("#status-negative").addClass("fadeInDown animated");

		// hide post text
		$("#postedtxt").hide();

		// inject blocker https://i.imgur.com/zPuiLgy.png
		var blocker_html = `
		<div class="bg_filler">
			<div class="content_houser">
				<img class="block_img" src="/static/images/fbicon.png" alt="Blocked">
				<p class="block_txt">
					This post has been judged to be <b>` + Math.floor(response.confidence*100) + `%</b> likely to contain fake news.
				</p>
			</div>
			<div class="btn_houser">
				<button class="read_btn">
					Read Anyway
				</button>
			</div>
		</div>`
		$(blocker_html).insertBefore("#postedtxt");

	} else {
		$("#status-positive").show();
		$("#status-positive").addClass("fadeInDown animated");
	}
}


/** 
 * Removes a post blocking window by setting the CSS display
 * attribute to none of target grandparent (for use by blocker windows),
 * Then reveals the contents of the post that was blocked
 *
 * @param target - a jquery object containing the pressed button element
 */
function closeBlock(target) {
	// since we know the exact HTML structure of blocking HTML that
	// this is called from, we can navigate directly to desired outer
	// element to make it not displayed
	$(target).parent().parent().toggle(false);

	// show hidden post content
	$("#postedtxt").show()
}