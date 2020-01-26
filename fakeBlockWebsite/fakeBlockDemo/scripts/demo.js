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


	$("#make-post").on('click', function(event) {
		// grab text from form
		var post_text = $("#posttxt").val();

		if(post_text) {
			// set make-post window to none
			$("#postbody").hide();
			// set posted window to visible
			$("#postedbody").show();

			// put text from form into posted window
			$("#postedtxt").text(post_text);

			// call api on text

		}
	});
});