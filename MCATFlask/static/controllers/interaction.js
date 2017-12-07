
//JavaScript stuff

//nlp = window.nlp_compromise;

var messages = [], //array that hold the record of each string in chat
    lastUserMessage = "", //most recent input string from the user
    botMessage = "", //var keeps track of what the chatbot is going to say
    botName = 'MCATutor', //name of the chatbot
    talking = true, //when false the speech function doesn't work
    question_request = false,
    subject = "",
    asking_questions = false,
    index = -1,
    state = 0,
    messageID=0,
    delayInMilliseconds = 350; //.5 second;

window.onload = function() {
	// setup the button click
	document.getElementById("theButton").onclick = function() {
		newEntry();
	};
};

function chatbotResponse() {

	//turns lastUserMessage into JSON object for ajax
	var userMessage = [
    {"input": lastUserMessage}
	];

  if (!asking_questions) {
    // The user is not being quized, operate normally
    // ajax the JSON to the server
    $.ajax({
      type: 'POST',
      url: '/receiver',
      data: JSON.stringify (userMessage),
      success: function(response){
    	  botMessage = response.botResponse;
        question_request = response.question_request;
        if (question_request) {
          subject = response.subject;
          state = 0;
          administerQuestions(subject);
        } else {
          //add the chatbot's name and message to the array messages
          messages.push("<b>" + botName + ":</b> " + botMessage);

          setTimeout(function() {
            addBubble();
            Speech(botMessage);
          }, delayInMilliseconds);
    	    // updateUI();
        }
      },
      contentType: "application/json",
      dataType: 'json'
	    // ajax the JSON to the server
	    //$.post("receiver", cars, function(){
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

      if (state == -1){
        asking_questions = false;
      }
      else {
        asking_questions = true;
      }

      // console.log(botMessage);
    	// updateUI();
      messages.push("<b>" + botName + ":</b> " + botMessage);
    	setTimeout(function() {
        addBubble();
        Speech(botMessage);
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
    //updateUI();
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
    var chatlogClass = "chatlog left";
   }
   else{
    var chatlogClass = "chatlog right";
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

function updateUI(){
  // says the message using the text to speech function written below
  //Speech(lastUserMessage);  //says what the user typed outlou

  //outputs the last few array elements of messages to html
  for (var i = 1; i < messageID; i++) {
    if (messages[messages.length - i])
      document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
  }
}


//text to Speech
//https://developers.google.com/web/updates/2014/01/Web-apps-that-talk-Introduction-to-the-Speech-Synthesis-API
function Speech(say) {
  if ('speechSynthesis' in window && talking) {
    var utterance = new SpeechSynthesisUtterance(say);
    //msg.voice = voices[10]; // Note: some voices don't support altering params
    //msg.voiceURI = 'native';
    //utterance.volume = 1; // 0 to 1
    //utterance.rate = 0.1; // 0.1 to 10
    //utterance.pitch = 1; //0 to 2
    //utterance.text = 'Hello World';
    //utterance.lang = 'en-US';
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
