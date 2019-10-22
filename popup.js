let send_url_button = document.getElementById('send_url_button');

send_url_button.onclick = function(element) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        let url = tabs[0].url;
        chrome.extension.getBackgroundPage().console.log("URL: " + url);

        chrome.runtime.sendMessage({type: 'sendURL', url: url}, (response) => {
            if(response == 'success') {
                send_url_button.style.backgroundColor = '#3aa757';
                chrome.extension.getBackgroundPage().console.log("Sended");
            }
        });
    });
};