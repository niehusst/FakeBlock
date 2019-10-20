//popup window js
$(function() {
	//TODO popup window isn't always available???? maybe replace popup with options page (but that means more front end. bleh.)
	
	// load persisting activation setting from chrome storage into popup html
	chrome.storage.sync.get(['activated', 'notFirstLoad'], function(state) {
		if (state.notFirstLoad) {
			$('#activate_switch').prop('checked', Boolean(state.activated));
		} else {
			// mark activated as true initially
			$('#activate_switch').prop('checked', true);

			// change notFirstLoad, as we have now loaded once
			chrome.storage.sync.set({'activated': true, 'notFirstLoad': true});
		}
	});

	// listen for switch presses
	$('#activate_switch').change(function() {
		// change the state of the activation
		var activationState = $('#activate_switch').prop('checked');

		// set new value in chrome storage
		chrome.storage.sync.set({'activated': activationState});

		// notify content script on storage change
		// get tabs to have access to the content script id of our target content script
		chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
			chrome.storage.sync.get(['activated'], function(state) {
				if (!Boolean(state.activated)) {
					chrome.tabs.sendMessage(tabs[0].id, {todo: "showAllPosts"});
				} else {
					chrome.tabs.sendMessage(tabs[0].id, {todo: "blockPosts"});
				}	
			});
		});
	});
});
