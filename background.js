
chrome.runtime.onInstalled.addListener(function() {
    console.log("Hello world from the background script");
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
      chrome.declarativeContent.onPageChanged.addRules([{
        conditions: [new chrome.declarativeContent.PageStateMatcher({
          pageUrl: {urlContains: 'https'},
        })
        ],
            actions: [new chrome.declarativeContent.ShowPageAction()]
      }]);
    });
  });
// Your web app's Firebase configuration
var firebaseConfig = {
    apiKey: "AIzaSyD9U71Vd71rsuqN2sZxXiROcXoBFfSckrY",
    authDomain: "chrome-saga.firebaseapp.com",
    databaseURL: "https://chrome-saga.firebaseio.com",
    projectId: "chrome-saga",
    storageBucket: "",
    messagingSenderId: "70424170722",
    appId: "1:70424170722:web:9c9fa60b5d5e4569470ebb"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
app_db = firebase.database();
chrome.runtime.onMessage.addListener((msg, sender, response) => {
    switch (msg.type) {
      case 'sendURL':
        app_db.ref('pages').push({
            url : msg.url,
            });
        //app_db.ref().child("pages").set({ value: msg.url });
        response('success');
        break;
      default:
        response('unknown request');
        break;
    }
  });


