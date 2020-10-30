const aud = document.querySelector("#au");

// socket에서 count 받아오고, 그 array init 한 담에 tts 끝날때마다 배열 채워주기
var count = 0;
var audioList;

var index = 0;


//socket
var socket = io();
$('#ocr_all').on('click', function(){

	    var count = 0;
           	     //yae
	    //  var name = $("#product_name").text();

	    var name_tmp;// = $(".img_url").text();//split("/").reverse()[0];
	    var img=[];
	    $(".img_url").each(function() {  
		img.push(this.src);
		count++;
		name_tmp = this.src;
	    });
	//jjeong
	    var name = name_tmp.split("/").reverse()[0];

	    console.log(name);
	
	    var data = {count : count, img_url: img, product_name: name};
	    socket.emit('ocrSource', data);
	    aud.setAttribute("src",'./wait_ocr.mp3');
	   aud.play();
	});

socket.on('arrCount', data=>{
	console.log(data);
	count = data;
	audioList = new Array;
})

socket.on('audioSource', data=>{
	audioList.push(data);
	//jjeong
	//audioList.sort();
	console.log(audioList);
})

socket.on('ocrData', data=>{
	socket.emit('tts', data);
})








// a = 경로가 들어있는 배열
function fn_up(){
	if(index < audioList.length){
		aud.setAttribute("src",audioList[index++]);
	  	aud.play();
		console.log(index);
	}else{
		alert("out of range");

	}
}
function fn_down(){
	if(index <= 0){
		alert("out of range");
	}else{
		aud.setAttribute("src",audioList[index--]);
		aud.play();
		console.log(index);
	}
}

function init(){
	document.addEventListener('keydown', function (event) {
		if( audioList != null  && audioList.length != 0){
			switch(event.which) {
			      case 37: // left
				      fn_down();
				      break;
			      case 39: // right
				      fn_up();
				      break;
			     case 32:
					aud.pause();
					break;
				      default: return; // exit this handler for other keys
				  }
		}
		event.preventDefault();
	}); // prevent the default action (scroll / move caret)

}

init();

