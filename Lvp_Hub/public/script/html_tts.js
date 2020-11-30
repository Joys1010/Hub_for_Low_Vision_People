/*
var aud = document.querySelector("#au");
function play_form(){
    aud.playbackRate=0.8
    console.log("for play");
    var playPromise = aud.play();
    if (playPromise !== undefined) {
            playPromise.then(function() {
            }).catch(function(error) {
            });
        }
}*/
var tts_click = false;
function tts_html(){
    tts_click = !tts_click;
    //if(tts_click ==true){
     $('.tts').each(
        function() { 
            var btn_name = $(this).attr('id');
    //$(this
            $(this).hover(
                 function(){
                 console.log(btn_name);
                 if(btn_click){
                 if(btn_name.indexOf('detail')!=-1){
                    btn_name = "detail";
                 }
                aud.setAttribute("src",`./${btn_name}.mp3`);
                 }else{aud.setAttribute("src",`./mouse.mp3`);}
                play_form();
                },
                function(){
                    console.log("off");
                    aud.pause();
                }
            );
        }
     );
    //}
}
async function crawler_tts(){
    console.log("clicked");
    aud.setAttribute("src",`./crawler.mp3`);
    play_form();
}
