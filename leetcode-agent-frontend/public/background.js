chrome.runtime.onInstalled.addListener(() => {
  console.log("LeetCode Agent installed.");
});

// Example message listener (frontend <-> background)
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "AUTH_SUCCESS") {
    chrome.storage.local.set({ authed: true }, () => {
      sendResponse({ success: true });
    });
  }
  return true;
});
