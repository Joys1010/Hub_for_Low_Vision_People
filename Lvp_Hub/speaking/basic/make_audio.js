async function make_audio(name,content){

    const fs = require('fs');
    const util = require('util');
    const textToSpeech = require('@google-cloud/text-to-speech');
    const projectId='refreshing-mark-222309';
    const keyfile='./My First Project-a0591a3611f6.json'; //---1) 
    const client =  new textToSpeech.TextToSpeechClient({
    projectId:projectId,
    keyFilename:keyfile
    });

    const contents =content;
    const request = {
    input: {text: contents},
    voice: {languageCode: 'ko-KR', ssmlGender: 'FEMALE'},
    audioConfig: {audioEncoding: 'MP3'}
    };
    var path= name;
    try{
    const [response] = await client.synthesizeSpeech(request);
    
    // Write the binary audio content to a local file
    const w_File = util.promisify(fs.writeFile);
   
    
    if (!(fs.existsSync(path))) {
        //file exists
        await w_File(path, response.audioContent, 'binary');
    }
    }catch(err){
    return;
    }
}
function init(){

    make_audio("in_btn.mp3","글자 음성 변환기 시작, 읽고 싶은 글자위에 마우스를 올려주세요.");
    make_audio("out_btn.mp3","글자 음성 변환기 종료.");

}
init();
