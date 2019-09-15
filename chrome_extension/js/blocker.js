// js for post blocker

//TODO determine which image/text to use based on response from API
var blocker_html = `
<div class="bg_filler">
	<div class="content_houser">
		<img class="block_img" src="../icons/fbWarning.png" alt="Blocked">
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

// inject blocker html
function(targetPost) {

}