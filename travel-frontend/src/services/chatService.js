const API_URL = "http://localhost:5000/chat";

export const sendMessage = async(message) => {
    const response = await fetch(API_URL, {
        method: "POST",
        header: {
            "Content-type":"application/json",
        },
        body:JSON.stringify({message}),
    });


    if (!response.ok){
        throw new Error("Fauled to fetch AI response");
    }

    const data = await response.json();
    return data.response;
;}
