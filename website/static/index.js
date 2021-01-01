document.getElementById("sendBtn").addEventListener("click",python_bind);

function python_bind() {    
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/send_messages", true); 

    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        // Reponse from ajax 
        if (this.responseText ==="update_screen") {            
            update();
        }
    }
};
    const value = document.getElementById("msg").value;
    const data = {messages:value};
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.send(JSON.stringify(data));
}

function update() {
    fetch('/get_messages')
    .then(function (response) {
        return response.json();
    }).then(function (text) {
        let messages = "";
        for (const msg of text["messages"]) {
            messages += "<br />" + msg;
        }
        document.getElementById("messages_display").innerHTML=messages;        
    });
}
document.onload = update();
function validate(name) {
    if(length(name)>2)
    {
        return true;
    }
    return false;
}