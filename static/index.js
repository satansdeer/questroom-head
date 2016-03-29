"use stict"

countdownActive = true;
var PROGRESS_BAR_TIME_DEFAULT_VALUE = 34 * 1000;
var progressBarTimeTotal = PROGRESS_BAR_TIME_DEFAULT_VALUE;
var progressBarTimeStart = (new Date()).getTime();

requestAnimationFrame(progressBarCountDown)
function WebSocketTest() {
	var messageContainer = document.getElementById("message");
	var progressBar = document.querySelector(".time-left_progress");
	if ("WebSocket" in window) {
		var id = window.location.search.split("?")[1].split("=")[1];
		window.ws = new WebSocket("ws://localhost:8888/socket?Id="+id);

		window.document.title = "cb_" + id;

		ws.onopen = function() {
			messageContainer.innerHTML = "Connected";
		};

		ws.onmessage = function (evt) {
			var received_msg = JSON.parse(evt.data);
			messageContainer.innerHTML = unescape(received_msg.message);

			// rec_mes = messageContainer.innerHTML + " ";
			// for (var value in received_msg) {
			// 	rec_mes = rec_mes + value + " | ";
			// 	console.log("Rec: " + rec_mes);
			// }

			if (received_msg.init) {
				resetProgressBar();
				messageContainer.className = 'message';
				progressBarTimeTotal = PROGRESS_BAR_TIME_DEFAULT_VALUE;
				setLevelIndicators(0);
				setStageIndicators(0, 0);
			}

			if (received_msg.not_a_task) {
				messageContainer.className = 'message green';
			} else {
				messageContainer.className = 'message';
			}


			if(!countdownActive && received_msg.countdown_active){
				countdownActive = received_msg.countdown_active;
				requestAnimationFrame(progressBarCountDown);
			}

			countdownActive = received_msg.countdown_active;
			setProgressVisibility(received_msg.progress_visible);

			resetProgressBar();

			if (received_msg.progress_bar_time) {
				// we received value in sec
				progressBarTimeTotal = received_msg.progress_bar_time * 1000;
			} else {
				progressBarTimeTotal = PROGRESS_BAR_TIME_DEFAULT_VALUE;
			}


			if (received_msg.level) {
				setLevelIndicators(received_msg.level);
				if (received_msg.stage) { setStageIndicators(received_msg.level, received_msg.stage); }
			}
		};

		ws.onclose = function() {
			messageContainer.innerHTML = "Connection is closed...";
			console.log("Connection closed. Reconnecting...");
			setTimeout(function(){
				WebSocketTest();
			}, 3000);
		};
	} else {
		messageContainer.innerHTML = "WebSocket NOT supported by your Browser!";
	}
}

function progressBarCountDown(){
	if(!countdownActive){
		return
	}
	var progressBar = document.querySelector(".time-left_progress");

	var progressBarTimePassed = (new Date()).getTime() - progressBarTimeStart;
	var progressBarValue = 100 - (progressBarTimePassed / progressBarTimeTotal) * 100;

	if(progressBarValue < 0){
		resetProgressBar();
		progressBarValue = 100;
		try{
			var id = window.location.search.split("?")[1].split("=")[1];
			var messageString = "Time end";
			var message = {message: messageString, id: id};
			ws.send(JSON.stringify(message));
		}catch(err){}
	}

	if(countdownActive){
		progressBar.style.width = progressBarValue + '%';
		requestAnimationFrame(progressBarCountDown);
	}
}

function setProgressVisibility(progressBarVisible){
	var progressBar = document.querySelector(".time-left");
	if(progressBarVisible){
		progressBar.style.display = 'block';
	}else{
		progressBar.style.display = 'none';
	}
}

function setLevelIndicators(level){
	var levelIndicators = document.querySelectorAll(".level_indicator");
	for(var i = 0; i < levelIndicators.length; i++){
		if(i < level){
			levelIndicators[i].className = 'level_indicator green';
			if(i == level - 1){ levelIndicators[i].className += ' blinking' }
		} else {
			levelIndicators[i].className = 'level_indicator';
		}
	}
}


function setStageIndicators(level, stage){

	var stage_blocks = document.querySelectorAll(".stage_indicators");
	for (var stage_block_index = 0; stage_block_index < stage_blocks.length; stage_block_index++) {
		if (stage_block_index != level - 1) {
			stage_blocks[stage_block_index].style.visibility = "hidden";
			continue;
		}

		stage_blocks[stage_block_index].style.visibility = "visible";
		var stage_indicators = stage_blocks[stage_block_index].getElementsByClassName("stage_indicator");
		for (var stage_indicator_index = 0; stage_indicator_index < stage_indicators.length; stage_indicator_index++) {

			if (stage_indicator_index < stage - 1) {
				stage_indicators[stage_indicator_index].className = 'stage_indicator green';
			} else if (stage_indicator_index == stage - 1) {
				stage_indicators[stage_indicator_index].className += ' blinking';
			} else {
				stage_indicators[stage_indicator_index].className = 'stage_indicator';
			}
		}
	}
}

function sendButton(event){
	buttonId = event.currentTarget.dataset.id;
	ws.send("Button clicked:"+buttonId);
}

function cretateMessage(messageString, id) {

	var message = {message: messageString, id: id};
	return message;
}

function resetProgressBar() {
	progressBarTimeStart = (new Date()).getTime();

}

function resetProgress(){
	progressValue = 100;
}

document.addEventListener("DOMContentLoaded", function(event) {
	WebSocketTest();
	var progressBar = document.querySelector(".time-left_progress");
	progressBar.addEventListener("webkitTransitionEnd", function(event) {
		// resetProgress();
		resetProgressBar();
		console.log("Reset progress");
		setTimeout(function(){
			progressBar.style.width = '0%';
		}, 1);
		var id = window.location.search.split("?")[1].split("=")[1];
		var messageString = "Time end; at end of index";
		var message = {message: messageString, id: id};
		ws.send(JSON.stringify(message));
	}, false);
});
