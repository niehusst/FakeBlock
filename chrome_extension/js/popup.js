//popup
$(function() {
	
	// load persisting activation setting from chrome storage
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
	});
});
