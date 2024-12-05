import React from 'react';
import Message from './Message';
import CahtInput from './CjatInput';

const ChatWindow = ({messages, onSendMessage}) => {

    return (
        <div className="chat-window">
            <div className="message-list">
                {messages.map((msg) => (
                    <Message key={msg.id} sender={msg.sender} text={msg.text} />

                ))}
            </div>
            <ChatInput onSendMessage={onSendMessage} />
        </div>
    );
};

export default ChatWindow;


