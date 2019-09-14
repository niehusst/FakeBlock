//content communications js

// tell event page to highlight icon on correct page
chrome.runtime.sendMessage({todo: "showPageAction"});