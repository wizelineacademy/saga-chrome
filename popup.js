let send_url_button = document.getElementById('send_url_button');
//Adds functionality to the button
send_url_button.onclick = function(element) {
    //Get current tab of the button
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        let url = tabs[0].url;
        chrome.extension.getBackgroundPage().console.log("URL: " + url);
        //Send the URL and set the button backgrond color as green if succeded
        chrome.runtime.sendMessage({type: 'sendURL', url: url}, (response) => {
            if(response == 'success') {
                send_url_button.style.backgroundColor = '#3aa757';
                chrome.extension.getBackgroundPage().console.log("Sended");
            }
        });
    });
};