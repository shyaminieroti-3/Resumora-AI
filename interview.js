async function generateQuestions() {

    const role = document.getElementById("role").value;

    const response = await fetch("http://127.0.0.1:5000/interview", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            role: role
        })

    });

    const data = await response.json();

    document.getElementById("questionBox").innerHTML =
        "<pre>" + data.questions + "</pre>";

}


async function submitAnswer() {

    const answer = document.getElementById("answer").value;

    if (answer.trim() === "") {

        alert("Please type your answer.");

        return;

    }

    const response = await fetch("http://127.0.0.1:5000/feedback", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            answer: answer
        })

    });

    const data = await response.json();

    document.getElementById("feedback").innerHTML =
        "<pre>" + data.feedback + "</pre>";

}