// data passing

var currentReceiver = '';
var userInput = $('#user-input');
var sendButton = $('#send-btn');
var msgList = $('#msg-list');
var lastMsgId = '';
var recv = $('#ouser');

function user_on_click()                                // Event on click of username in user list
{
    let selected = event.target;                        // Select element which triggered the event (here username button) 
    $("#user-list *").removeClass("bor-grad");          // Remove active element border if exists
    selected.parentElement.classList.add("bor-grad");   // Add active border to li which triggered the event
    var sel = $.trim(selected.value);                   // Trim string of username passed through buuton value
    setCurrentReceiver(sel);                            // Set recevier
//    console.log("target = ", sel);                  
    document.getElementById("ouser").textContent = sel; // Pass receiver name to card-header to display at top of chat 
//    console.log("currentUser = ", currentUser);
}

function showMsg(msg)
{
    let user = 'other';
    let user_Msg = 'otherMsg';
    const date = new Date(msg.timestamp);
    if (msg.sender === currentUser &&
        msg.receiver === currentReceiver) user = 'current' , user_Msg = 'currentMsg' ;
    {
//        console.log("lastMsgId = ",lastMsgId);
        if(msg.id != lastMsgId)
        {
            const messageItem = `
            <li class="msgWrap">
                <div class="innerCont ${user}">
                    <div class=" ${user_Msg} ${user} ">
                        ${msg.content}
                    </div>
                </div>
                <span class=" ${user} "> ${date.toLocaleString()} </span>
            </li>`;
//            console.log("showMsg ID = ", msg.id);
            $(messageItem).appendTo('#msg-list');
        }
    }
lastMsgId = msg.id;
}

function clearChat()
{
    $('#msg-list li').remove()
//    console.log("Chat cleared");
}

function getChat(receiver)
{
    $.getJSON(`/api/v1/msg/?target=${receiver}`, function (data)
    {
        clearChat();
        msgList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--)
        {
            showMsg(data['results'][i]);
//            console.log("Result =", data['results'][i]);
        }
        msgList.animate({ scrollTop: msgList[0].scrollHeight}, 100);
//        console.log("Loaded old chat messages");
    });
}

function getNewMsg(message)
{
    id = JSON.parse(message).message
    $.getJSON(`/api/v1/msg/${id}/`, function (data) 
    {
        if (data.sender === currentReceiver || (data.receiver === currentReceiver && data.sender == currentUser))
        {
            showMsg(data);
//            console.log("getNewMsg = ",data);
        }
        msgList.animate({ scrollTop: msgList[0].scrollHeight}, 100);
    });
}

function sendMsg(receiver, content)
{
    $.post('/api/v1/msg/', 
    {
        receiver: receiver,
        content: content,
    }).fail(function () 
    {
        alert('Error! Check console!');
    });
}

function setCurrentReceiver(username)
{
    currentReceiver = username;
    getChat(currentReceiver);
    enableInput();
}

function enableInput()
{
    userInput.prop('disabled', false);
    sendButton.prop('disabled', false);
    userInput.focus();
}

function disableInput()
{
    userInput.prop('disabled', true);
    sendButton.prop('disabled', true);
}

$(document).ready(function ()
{
    disableInput();

// Web Socket

var socket = new WebSocket(
    'ws://' + window.location.host +
    '/ws?session_key=${sessionKey}')

userInput.keypress(function (e)
{
    if (e.keyCode == 13)
        sendButton.click();
});

sendButton.click(function ()
{
    if (userInput.val().length > 0)
    {
        sendMsg(currentReceiver, userInput.val());
        userInput.val('');
    }
});

socket.onmessage = function (e)
{
    getNewMsg(e.data);
};
});

/* Filter user in user-list */

$(document).ready(function()
{
    $("#user-search").on("keyup", function() 
    {
      var value = $(this).val().toLowerCase();
      $("#user-list *").filter(function() 
      {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });