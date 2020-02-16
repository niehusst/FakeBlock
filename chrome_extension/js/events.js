//events handling

// listen for the correct page (facebook.com)
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.todo === "showPageAction") {
		// retrieve all tabs (stored in tabs param) to highlight the extension 
		// icon
		chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
			chrome.pageAction.show(tabs[0].id);
		});
	}
});

// listen for initial page load from content script, send back activation state
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.todo === "initialLoad") {
		// get tabs to have access to the content script id of our target 
		// content script
		chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
			chrome.storage.sync.get(['activated'], function(state) {
				if (!Boolean(state.activated)) {
					chrome.tabs.sendMessage(tabs[0].id,{todo: "showAllPosts"});
				} else {
					chrome.tabs.sendMessage(tabs[0].id, {todo: "blockPosts"});
				}	
			});
		});
	}
});

// listen for messages from content script that contain information for 
// fakeblock API call
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.todo === "apiCall") {
		// make fetch call to FakeBlock API using info scraped from content.js
		const postData = {
			headers: {
				'Accept': "application/json",
				'content-type': "application/json"
			},
			body: JSON.stringify({
				post_text: request.text,
				news_text: request.news
			}),
			method: "POST"
		};
		const apiUrl = 'https://fakeblocker.herokuapp.com/api/fake'

		fetch(apiUrl, postData)
		.then(response => response.json())
		.then(data => sendResponse(data)) // send response back to content.js 
		.catch(error => sendResponse({fake: false})); 

		return true; //respond asynchronously

	}
});