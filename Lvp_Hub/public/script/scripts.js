var aud = document.querySelector("#au");

// socket에서 count 받아오고, 그 array init 한 담에 tts 끝날때마다 배열 채워주기
var count = 0;
var audioList;

var index = 0;

//socket
var socket = io();
var flag = false;

$('#ocr_select').click((e) => { 
	aud.setAttribute("src", "./wait_capture.mp3");
	play_form();

	flag = true;
	console.log("drag clicked");
	var initialPos_x, initialPos_y;
	var finalPos_x, finalPos_y;

	var dragSpace = new DragSelect({
		
		onDragStart: function(element) {
			initialPos_x = event.pageX;
			initialPos_y = event.pageY;
		},
		onDragMove: function(element){
			finalPos_x = event.pageX;
			finalPos_y = event.pageY;
		}
	});

	
	onmouseup = function(e) {
		dragSpace.stop();
		if(flag){
		aud.pause();
		aud.setAttribute("src", "./wait_capture_ocr.mp3");
		play_form();
		//console.log("initial : ",initialPos_x, " ", initialPos_y );
		//console.log("final :" , finalPos_x, " ", finalPos_y);
		
		
		html2canvas(document.body, {
			proxy: '/search',
			proxy: '/detail',
			x: Math.min(initialPos_x,finalPos_x),
			y: Math.min(initialPos_y,finalPos_y),
			width: Math.abs(finalPos_x-initialPos_x),
			height: Math.abs(finalPos_y-initialPos_y),

		}).then(
		function (canvas) {
			var entireImg = canvas.toDataURL("image/png");
			entireImg = entireImg.replace("data:image/png;base64,", "");

			console.log("html2canvas");

			socket.emit('imgSrc', entireImg);
			
		}) 
		}
	
		/*
		html2canvas(document.body, {
			allowTaint: true,
			useCORS: true,
			useCORS: true,
			x: Math.min(initialPos_x,finalPos_x),
			y: Math.min(initialPos_y,finalPos_y),
			width: Math.abs(finalPos_x-initialPos_x),
			height: Math.abs(finalPos_y-initialPos_y),
			onrendered: function (canvas) {
	
				var entireImg = canvas.toDataURL("image/png");
				entireImg = entireImg.replace("data:image/png;base64,", "");

				console.log("html2canvas");

				socket.emit('imgSrc', entireImg);
			}

		})
		}
		*/
		flag =false; 
	};
	
});
socket.on('captureAudioSrc', data=>{
	const path = data ;
	console.log("capturedAduio");

	aud.setAttribute("src",path);
	play_form();
})

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

var  btn_click = false;
function speak_crawling(){
    aud.setAttribute("src","./crawling.mp3");
    play_form();
}
function play_form(){
	aud.playbackRate=0.8
	console.log("jjeong tts play_form");
    var playPromise = aud.play();
    if (playPromise !== undefined) {
            playPromise.then(function() {
                                                                    // Automatic playback started!
            }).catch(function(error) {
                                                                    // Automatic playback failed.
                                                                    // Show a UI element to let the user manually start playback.
            });
        }
}


/*function tts_btn(){
    btn_click = !btn_click;
    if(btn_click ==true){

        aud.setAttribute("src",'./notice_text_tts.mp3'); // 스페치스바 제거시 - 바꿔~
        play_form();
        $('.detail_and_button').each(function() { 
         //   console.log($(this).attr('id')) ;
            var item_name = $(this).attr('id');
             $(this).hover(
            function(){
		    if(btn_click){
                aud.setAttribute("src","");
                
                var item_content = this.querySelector(".item_detail").textContent;
                console.log(item_content);
                //tts
                var data = { search_word: "lotte" ,contents : item_content, name :item_name};
                socket.emit('textTTS', data);
                socket.on('audioDone', data=>{
					const path = data ;

                	aud.setAttribute("src",path);
					play_form();
					console.log("mouse over");
                })
		    }
            },
            function(){
           
                console.log("off");
                aud.pause();
                
            }

        );
        });
        


       // ;
    }
}*/


function tts_btn(){
	btn_click = !btn_click;
	if(btn_click ==true){

		var title = $('.h2').text().split(":")[1];
		console.log(title);
		aud.setAttribute("src",'./notice_text_tts.mp3'); 
		play_form();
		$('.dyn_tts').each(function() {
			var item_name = "dyn_tts";
			var path ="";
			$(this).hover(
				function(){
					if(btn_click){
						aud.setAttribute("src","");
						var item_content = this.textContent;
						console.log(item_content);
						var data = { search_word: "dyn_tts" ,contents : item_content, name :item_name};
						socket.emit('textTTS', data);
						socket.on('audioDone', data=>{
							path = data ;
							aud.setAttribute("src",path);
							play_form();
							console.log("mouse over");
						})
					}
				},
				function(){
					console.log("off");
					aud.pause();
				}

			);
		});
		$('.detail_and_button').each(function() {
			var item_name = $(this).attr('id');
			$(this).hover(
				function(){
					if(btn_click){
						aud.setAttribute("src","");
						var item_content = this.querySelector(".item_detail").textContent;
						console.log(item_content);
						aud.setAttribute("src","./ding_dong.mp3");
						play_form();
						var data = { search_word: title ,contents : item_content, name :item_name};
						socket.emit('textTTS', data);
						socket.on('audioDone', data=>{
							const path = data ;
							aud.setAttribute("src",path);

							play_form();
							console.log("mouse over");
						})
					}
				},
				function(){

					console.log("off");
					aud.pause();

				}

			);
		});

	}else{
		aud.setAttribute("src",`./end_tts.mp3`);
		play_form();
	}
}





 //joys
var nowZoom = 100;

function zoomIn()
{

	var Page = document.querySelector("body");
	nowZoom = nowZoom + 10;
	if (nowZoom >= 500) nowZoom = 500;
	var zoom = nowZoom + '%';
	Page.style.zoom = zoom;

	return false;
}

function zoomOut()
{
	
	var Page = document.querySelector("body");
	nowZoom = nowZoom - 10;
	if (nowZoom <= 100) nowZoom = 100;
	var zoom = nowZoom + '%';
	Page.style.zoom = zoom;

	return false;
}



/*function zoomIn()
{
	console.log("zoomin");
	  var Page = document.querySelector("body");

	  var zoom = parseInt(Page.style.zoom) + 10 +'%'
	  Page.style.zoom = zoom;
	  return false;
}

function zoomOut()
{

	console.log("zoomout");
	  var Page = document.querySelector("body");
	  var zoom = parseInt(Page.style.zoom) - 10 +'%'
	  Page.style.zoom = zoom;
	  return false;
}*/


/*function init(){
	    in_btn.addEventListener("click",zoomIn);
	    out_btn.addEventListener("click",zoomOut);
}

init();*/











