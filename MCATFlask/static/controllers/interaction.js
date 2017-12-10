
//JavaScript stuff

//nlp = window.nlp_compromise;

var messages = [], //array that hold the record of each string in chat
    lastUserMessage = "", //most recent input string from the user
    botMessage = "", //var keeps track of what the chatbot is going to say
    botName = 'MCATutor', //name of the chatbot
    talking = true, //when false the speech function doesn't work
    question_request = false, // User has asked for a subject
    subject = "",
    asking_questions = false, // User is answering practice questions
    index = -1,
    state = 0,
    messageID=0,
    delayInMilliseconds = 350, //.5 second;
    speech=true, //enabled and disabled by user
    start_exam = false, //User has taken enough questions to build exam
    taking_exam = false;

window.onload = function() {
	// setup the button click
  botMessage = "I am an AI chatbot that would like to help you study for your MCAT exam. I have a collection of questions from subjects including: Biology, Physics, Chemistry, Psychology, and Sociology. What would you like to study today?";
  messages.push("<b>" + botName + ":</b> " + botMessage);
  addBubble();
};

function chatbotResponse() {

	//turns lastUserMessage into JSON object for ajax
	var userMessage = [
    {"input": lastUserMessage,
     "state": state}
	];
  console.log(start_exam);
  if (taking_exam) {
    takeExam();
  } else if (start_exam) {
    state = 0;
    takeExam();
  }
  else if (!asking_questions) {
    // The user is not being quized, operate normally
    // ajax the JSON to the server
    $.ajax({
      type: 'POST',
      url: '/receiver',
      data: JSON.stringify (userMessage),
      success: function(response){
    	  botMessage = response.botResponse;
        question_request = response.question_request;
        start_exam = response.start_exam;
        if (start_exam) {
          state = 0;
          takeExam();
        } else {
          if (question_request) {
            subject = response.subject;
            state = 0;
            administerQuestions(subject);
          } else {
            //add the chatbot's name and message to the array messages
            messages.push("<b>" + botName + ":</b> " + botMessage);

            setTimeout(function() {
              addBubble();
              if (speech) {
                Speech(botMessage);
              }
            }, delayInMilliseconds);
          }
        }
      },
      contentType: "application/json",
      dataType: 'json'
	  });
  }
  else {
    administerQuestions(subject);
  }
}


function administerQuestions(s) {
  question_request = false;
  var userMessage = [
    {"input": lastUserMessage,
     "subject": s,
     "index": index,
     "state": state}
	];

  $.ajax({
    type: 'POST',
    url: '/practice',
    data: JSON.stringify (userMessage),
    success: function(response){
    	botMessage = response.botResponse;
      index = response.index;
      subject = response.subject;
      state = response.state;
      start_exam = response.start_exam;

      if (start_exam){
        state = 0;
        takeExam();
      } else {
        if (state == -1){
          asking_questions = false;
        }
        else {
          asking_questions = true;
        }

        messages.push("<b>" + botName + ":</b> " + botMessage);
    	  setTimeout(function() {
          addBubble();
          if (speech){
            Speech(botMessage);
          }
        }, delayInMilliseconds);
      }
    },
    contentType: "application/json",
    dataType: 'json'
	});

}

function takeExam() {
  console.log("here");
  taking_exam = true;
  var userMessage = [
    {"input": lastUserMessage,
     "state": state}
	];

  $.ajax({
    type: 'POST',
    url: '/exam',
    data: JSON.stringify (userMessage),
    success: function(response){
      console.log("success");
    	botMessage = response.botResponse;
      state = response.state;
      var finished = response.finished;
      console.log(botMessage);

      if (finished) {
        taking_exam = false;
        start_exam = false;
      }

      messages.push("<b>" + botName + ":</b> " + botMessage);
    	setTimeout(function() {
        addBubble();
        if (speech){
          Speech(botMessage);
        }
      }, delayInMilliseconds);
    },
    contentType: "application/json",
    dataType: 'json'
	});
}




//OTHER JSCRIPT STUFF

//It controls the overall input and output
function newEntry() {
  //if the message from the user isn't empty then run
  if (document.getElementById("chatbox").value != "") {

    //pulls the value from the chatbox ands sets it to lastUserMessage
    lastUserMessage = document.getElementById("chatbox").value;

    //sets the chat box to be clear
    document.getElementById("chatbox").value = "";

    //adds the value of the chatbox to the array messages
    messages.push(lastUserMessage);

    addBubble();
    chatbotResponse();

    // stop link reloading the page
    event.preventDefault();

  }
}

//CHANGE CLASS OF CHATLOG FROM LEFT TO RIGHT ONCE CSS IS UPDATED
function addBubble(){
   messageID++;
   var chatlogID = "chatlog" + messageID;
   if (messageID % 2 ==0){
     var chatlogClass = "chatlog right";
   }
   else{
     chatlogClass = "chatlog left";
   }
   var para = document.createElement('p');
   //para.appendChild(message);
   para.setAttribute("id", chatlogID);
   para.setAttribute("class", chatlogClass);
   para.innerHTML = messages[messages.length - 1];
   document.getElementById("chatborder").appendChild(para);

   //automatically scroll to bottom of conversation
   var objDiv = document.getElementById("chatborder");
   objDiv.scrollTop = objDiv.scrollHeight;

}

function changeSpeechSetting(){
  if (speech){
    speech=false;
    document.getElementById("speechToggle").src="../static/images/soundOff.png";
  }
  else{
    speech=true;
    document.getElementById("speechToggle").src="../static/images/soundOn.png";
  }
}

//text to Speech
function Speech(say) {
  if ('speechSynthesis' in window && talking) {
    var utterance = new SpeechSynthesisUtterance(say);
    speechSynthesis.speak(utterance);
  }
}

//runs the keypress() function when a key is pressed
document.onkeypress = keyPress;
//if the key pressed is 'enter' runs the function newEntry()
function keyPress(e) {
  var x = e || window.event;
  var key = (x.keyCode || x.which);
  if (key == 13 || key == 3) {
    //runs this function when enter is pressed
    newEntry();
  }
}

//clears the placeholder text in the chatbox
//this function is set to run when the users brings focus to the chatbox, by clicking on it
function placeHolder() {
  document.getElementById("chatbox").placeholder = "";
}
