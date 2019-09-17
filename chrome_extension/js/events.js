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

// listen for changes in storage (activation switch)
chrome.storage.onChanged.addListener(function(changes, storageName) {
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