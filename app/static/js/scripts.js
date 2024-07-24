$(document).ready(function() {
    $('#send-button').click(function() {
        sendMessage();
    });

    $('#user-input').keypress(function(event) {
        if (event.keyCode === 13) {
            sendMessage();
        }
    });

    function sendMessage() {
        var userInput = $('#user-input').val();
        if (userInput.trim() !== '') {
            appendUserMessage(userInput);
            $('#user-input').val('');
            $.ajax({
                type: 'POST',
                url: '/chatbot',
                contentType: 'application/json',
                data: JSON.stringify({ prompt: userInput }),
                success: function(response) {
                    appendChatbotResponse(response.response);
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        }
    }

    function appendUserMessage(message) {
        $('#chat-box').append('<p>User: ' + message + '</p>');
    }

    function appendChatbotResponse(response) {
        // Remove empty lines after "You:" and "AI:"
        var chatBox = $('#chat-box');
        if (chatBox.children().last().text().startsWith('You:')) {
            chatBox.append('<p>AI: ' + response + '</p>');
        } else {
            chatBox.append('<p>AI: ' + response + '</p><br>');
        }
    }
});
