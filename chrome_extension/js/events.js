//events handling

// listen for the correct page (facebook.com)
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

	if (request.todo === "showPageAction") {
		// retrieve all tabs (stored in tabs param) to highlight the extension icon
		chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
			chrome.pageAction.show(tabs[0].id);
		});
	}

});