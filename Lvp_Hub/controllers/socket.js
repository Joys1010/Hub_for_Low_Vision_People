const SocketIO = require('socket.io');
var Mutex = require('async-mutex').Mutex;
const mutex = new Mutex();
var fs = require('fs');
const { PythonShell } = require('python-shell');
const { stringify } = require('querystring');

module.exports = (server, app) =>{

    const io = SocketIO(server);
	app.set('io', io);
	
	
    io.on('connection', socket=>{

	   socket.on('imgSrc', async function(imgSrc){

		console.log("test button clicked");
        //console.log(req.body.imgSrc);
        var base64Data = imgSrc;
        
        require("fs").writeFile("./captured/out.png", base64Data, 'base64', function(err) {
            console.log(err);
        });

        console.log("OCR gogo");
		const vision = require('@google-cloud/vision');
				
		// Creates a client
		const client = new vision.ImageAnnotatorClient();
				
		var fileName = './captured/out.png'
		const [result] = await client.textDetection(fileName);
		const detections = result.textAnnotations;
					

        if(detections[0] != undefined){
            //console.log(detections[0]['description']);
            var ttsData = { option: "capture", contents: detections[0]['description'] };
			const fs = require('fs');
			const util = require('util');
			const textToSpeech = require('@google-cloud/text-to-speech');
			const projectId='refreshing-mark-222309';
			const keyfile='./My First Project-a0591a3611f6.json'; //---1) 
			const client =  new textToSpeech.TextToSpeechClient({
			projectId:projectId,
			keyFilename:keyfile
			});

			//폴더 만들어주기
			const makeFolder = (dir)=>{  
			if(!fs.existsSync(dir)){  
			fs.mkdirSync(dir);    
			}                         
			}                           
		
			var ttsData = JSON.parse(JSON.stringify(ttsData));
			
			const contents = ttsData.contents;
			//console.log(contents);
			const request = {
			input: {text: contents},
			voice: {languageCode: 'ko-KR', ssmlGender: 'FEMALE'},
			audioConfig: {audioEncoding: 'MP3'}
			};

			var path;
			try{
			const [response] = await client.synthesizeSpeech(request);
			
			// Write the binary audio content to a local file
			const w_File = util.promisify(fs.writeFile);
			var folder_name;
				folder_name = `./speaking/capture`
				makeFolder(folder_name);
				output_name =ttsData.name;
				path = `${folder_name}/${detections[0]['description'][0]}.mp3`;
			
				//file exists
				await w_File(path, response.audioContent, 'binary');
			
			}catch(err){
			return;
			}
			socket.emit('captureAudioSrc', path);

        }

	   })

	socket.on('textTTS',async function(data){
		searchData = JSON.parse(JSON.stringify(data));
		var ttsData = { option: "_search", search_word:searchData.search_word, img_url:"NULL", name:searchData.name, contents: searchData.contents };
			const fs = require('fs');
			const util = require('util');
			const textToSpeech = require('@google-cloud/text-to-speech');
			const projectId='refreshing-mark-222309';
			const keyfile='./My First Project-a0591a3611f6.json'; //---1) 
			const client =  new textToSpeech.TextToSpeechClient({
			projectId:projectId,
			keyFilename:keyfile
			});

			//폴더 만들어주기
			const makeFolder = (dir)=>{  
				if(!fs.existsSync(dir)){  
				fs.mkdirSync(dir);    
				}                         
			}                           
		
			var ttsData = JSON.parse(JSON.stringify(ttsData));
			
			const search_word =ttsData.search_word;
			const contents = ttsData.contents;
			const request = {
				input: {text: contents},
				voice: {languageCode: 'ko-KR', ssmlGender: 'FEMALE'},
				audioConfig: {audioEncoding: 'MP3'}
			};

			var path;
			try{
			const [response] = await client.synthesizeSpeech(request);
			
			// Write the binary audio content to a local file
			const w_File = util.promisify(fs.writeFile);
			var folder_name, output_name;
			folder_name = `./speaking/search/${search_word}`
			makeFolder(folder_name);
			output_name =ttsData.name;
			path = `${folder_name}/${output_name}.mp3`;
			//if (!(fs.existsSync(path))) {
				//file exists
				await w_File(path, response.audioContent, 'binary');
			//}
			}catch(err){
				return;
			}
			socket.emit('audioDone', path);
	});

        socket.on('ocrSource', async function(data){
            console.log("Socket.on - ocrSource(server)");
			imgSegData = JSON.parse(JSON.stringify(data));
			
			product_name = imgSegData.product_name;
	    	var argPython = [imgSegData.count, imgSegData.img_url];

            //data 안에 src들 들어있다.
            //나중에 포문으로 감싸야댐

            let options = {
                mode: 'text',
                pythonOptions: ['-u'], // get p/rint results in real-time
                args: argPython
            };
            
            PythonShell.run('./controllers/python/imgSeg.py', options, async function(err, results){
				if (err) throw err;
			
				console.log(`results: ${results}`);
				
				var savedPath = results[0];

				var results = results.splice(1, results.length);
				
				var maxCount = results.length;	
				socket.emit('arrCount', parseInt(results[maxCount-1]));

				for(var cur = 0; cur < maxCount ; cur++){
					if(cur == 0){
						for(var imgName = parseInt(results[cur]) ; imgName > 0; imgName--){
					//OCR 돌린다.
		                    console.log(imgName+"th OCR");
							const vision = require('@google-cloud/vision');
				
							// Creates a client
							const client = new vision.ImageAnnotatorClient();
				
							var fileName = savedPath+'Img'+imgName+'.jpg'
							const [result] = await client.textDetection(fileName);
							const detections = result.textAnnotations;
					

                    		if(detections[0] != undefined){
		    	    			console.log(detections[0]['description']);
			    				var ttsData = { option: "detail", search_word:"NULL", img_url:product_name, name:imgName, contents: detections[0]['description'] };

								// mp3 파일로 저장
								const fs = require('fs');
								const util = require('util');
								const textToSpeech = require('@google-cloud/text-to-speech');
							
								const projectId='refreshing-mark-222309';
								const keyfile='./My First Project-a0591a3611f6.json'; //---1) 

								const client =  new textToSpeech.TextToSpeechClient({
												projectId:projectId,
												keyFilename:keyfile
								});

								//폴더 만들어주기
								const makeFolder = (dir)=>{  
									if(!fs.existsSync(dir)){  
										fs.mkdirSync(dir);    
									}                         
			    				}                           
			
								var ttsData = JSON.parse(JSON.stringify(ttsData));
								
								const option =ttsData.option;
								const search_word =ttsData.search_word;
								const img_url = ttsData.img_url;
								const contents = ttsData.contents;
								const name = ttsData.name;

								const request = {
									input: {text: contents},
									voice: {languageCode: 'ko-KR', ssmlGender: 'FEMALE'},
									audioConfig: {audioEncoding: 'MP3'},
								};

			    				var path;
			    try{
				const [response] = await client.synthesizeSpeech(request);
				
				// Write the binary audio content to a local file
				const w_File = util.promisify(fs.writeFile);
				
				//jjeong
				// 검색어 별로 저장 공간 분리 : 없으면 폴더 만들어 버려~
				var folder_name, output_name;
				//검색어 페이지 인 경우
				//speaking  ->search -> 검색어 -> 이름 :  세부_url + 각_id_이름 
				if(option == 'search'){
				    folder_name = `./speaking/search/${search_word}`
				    makeFolder(folder_name);
				    output_name = detail_url +'_'+name;
				}
				//세부 페이지인 경우
				//speaking  ->detail -> 세부_url-> 이름 :  각_id_이름
				else if(option == 'detail'){
				    folder_name = `./speaking/detail/${img_url}`
				    makeFolder(folder_name);
				    output_name = name;
				}                                                              
				else return;                                                  
				
				// 경로 정해주기 
				path = `${folder_name}/${output_name}.mp3`;  

				if (!(fs.existsSync(path))) {
				    //file exists
				    await w_File(path, response.audioContent, 'binary');
				    console.log('Audio content written to file: output.mp3'); 
				}
				
			    }catch(err){
				console.error('ERROR:', err);
				return;
			    }

			    socket.emit('audioSource', path);

                    }

				}
			}else{
				for(var imgName = parseInt(results[cur]) ; imgName > parseInt(results[cur-1]) ; imgName--){
					//OCR 돌린다.
                   console.log(imgName+"th OCR");
                    const vision = require('@google-cloud/vision');
        
                    // Creates a client
                    const client = new vision.ImageAnnotatorClient();
        
                    var fileName = savedPath+'Img'+imgName+'.jpg'
                    const [result] = await client.textDetection(fileName);
                    const detections = result.textAnnotations;
		    

                    if(detections[0] != undefined){

		    	    console.log(detections[0]['description']);
			    var ttsData = { option: "detail", search_word:"NULL", img_url:product_name, name:imgName, contents: detections[0]['description'] };

			    // mp3 파일로 저장
			    const fs = require('fs');
			    const util = require('util');
			    const textToSpeech = require('@google-cloud/text-to-speech');
			
			    const projectId='refreshing-mark-222309';
			    const keyfile='./My First Project-a0591a3611f6.json'; //---1) 
			    const client =  new textToSpeech.TextToSpeechClient({
				projectId:projectId,
				keyFilename:keyfile
			    });

			    //폴더 만들어주기
			    const makeFolder = (dir)=>{  
			    if(!fs.existsSync(dir)){  
				fs.mkdirSync(dir);    
				}                         
			    }                           
			
			    var ttsData = JSON.parse(JSON.stringify(ttsData));
				
			    const option =ttsData.option;
			    const search_word =ttsData.search_word;
			    const img_url = ttsData.img_url;
			    const contents = ttsData.contents;
			    const name = ttsData.name;

			    const request = {
				input: {text: contents},
				voice: {languageCode: 'ko-KR', ssmlGender: 'FEMALE'},
				audioConfig: {audioEncoding: 'MP3'},
			    };

			    var path;
			    try{
				const [response] = await client.synthesizeSpeech(request);
				
				// Write the binary audio content to a local file
				const w_File = util.promisify(fs.writeFile);
				
				//jjeong
				// 검색어 별로 저장 공간 분리 : 없으면 폴더 만들어 버려~
				var folder_name, output_name;
				//검색어 페이지 인 경우
				//speaking  ->search -> 검색어 -> 이름 :  세부_url + 각_id_이름 
				if(option == 'search'){
				    folder_name = `./speaking/search/${search_word}`
				    makeFolder(folder_name);
				    output_name = detail_url +'_'+name;
				}
				//세부 페이지인 경우
				//speaking  ->detail -> 세부_url-> 이름 :  각_id_이름
				else if(option == 'detail'){
				    folder_name = `./speaking/detail/${img_url}`
				    makeFolder(folder_name);
				    output_name = name;
				}                                                              
				else return;                                                  
				
				// 경로 정해주기 
				path = `${folder_name}/${output_name}.mp3`;  

				if (!(fs.existsSync(path))) {
				    //file exists
				    await w_File(path, response.audioContent, 'binary');
				    console.log('Audio content written to file: output.mp3'); 
				}
				
			    }catch(err){
				console.error('ERROR:', err);
				return;
			    }

			    socket.emit('audioSource', path);

                    }
				}
				
			}
			
			
		}
		//yae
		//socket.emit('arrCount', results[0]);
			
		
//                for( var i = results[0] ; i >= 1; i--){
//                    console.log(i+"th OCR");
//                    const vision = require('@google-cloud/vision');
//        
//                    // Creates a client
//                    const client = new vision.ImageAnnotatorClient();
//        
//                    var fileName = './controllers/python/output/Img'+i+'.jpg'
//                    const [result] = await client.textDetection(fileName);
//                    const detections = result.textAnnotations;
//		    
//
//                    if(detections[0] != undefined){
//
//		    	    console.log(detections[0]['description']);
//			    var ttsData = { option: "detail", search_word:"NULL", img_url:product_name, name:i, contents: detections[0]['description'] };
//
//			    // mp3 파일로 저장
//			    const fs = require('fs');
//			    const util = require('util');
//			    const textToSpeech = require('@google-cloud/text-to-speech');
//			
//			    const projectId='refreshing-mark-222309';
//			    const keyfile='./My First Project-a0591a3611f6.json'; //---1) 
//			    const client =  new textToSpeech.TextToSpeechClient({
//				projectId:projectId,
//				keyFilename:keyfile
//			    });
//
//			    //폴더 만들어주기
//			    const makeFolder = (dir)=>{  
//			    if(!fs.existsSync(dir)){  
//				fs.mkdirSync(dir);    
//				}                         
//			    }                           
//			
//			    var ttsData = JSON.parse(JSON.stringify(ttsData));
//				
//			    const option =ttsData.option;
//			    const search_word =ttsData.search_word;
//			    const img_url = ttsData.img_url;
//			    const contents = ttsData.contents;
//			    const name = ttsData.name;
//
//			    const request = {
//				input: {text: contents},
//				voice: {languageCode: 'ko-KR', ssmlGender: 'FEMALE'},
//				audioConfig: {audioEncoding: 'MP3'},
//			    };
//
//			    var path;
//			    try{
//				const [response] = await client.synthesizeSpeech(request);
//				
//				// Write the binary audio content to a local file
//				const w_File = util.promisify(fs.writeFile);
//				
//				//jjeong
//				// 검색어 별로 저장 공간 분리 : 없으면 폴더 만들어 버려~
//				var folder_name, output_name;
//				//검색어 페이지 인 경우
//				//speaking  ->search -> 검색어 -> 이름 :  세부_url + 각_id_이름 
//				if(option == 'search'){
//				    folder_name = `./speaking/search/${search_word}`
//				    makeFolder(folder_name);
//				    output_name = detail_url +'_'+name;
//				}
//				//세부 페이지인 경우
//				//speaking  ->detail -> 세부_url-> 이름 :  각_id_이름
//				else if(option == 'detail'){
//				    folder_name = `./speaking/detail/${img_url}`
//				    makeFolder(folder_name);
//				    output_name = name;
//				}                                                              
//				else return;                                                  
//				
//				// 경로 정해주기 
//				path = `${folder_name}/${output_name}.mp3`;  
//
//				if (!(fs.existsSync(path))) {
//				    //file exists
//				    await w_File(path, response.audioContent, 'binary');
//				    console.log('Audio content written to file: output.mp3'); 
//				}
//				
//			    }catch(err){
//				console.error('ERROR:', err);
//				return;
//			    }
//
//			    socket.emit('audioSource', path);
//
//                    }
//                }
//              
//              
      	    });
        })
        
        socket.on('tts', async function(data){
            console.log(data);
            // 태그 속 내용 (바로바로) 읽어주기

            // mp3 파일로 저장
            const fs = require('fs');
            const util = require('util');
            const textToSpeech = require('@google-cloud/text-to-speech');
        
            const projectId='refreshing-mark-222309';
            const keyfile='./My First Project-a0591a3611f6.json'; //---1) 
            const client =  new textToSpeech.TextToSpeechClient({
                projectId:projectId,
                keyFilename:keyfile
            });

            //폴더 만들어주기
            const makeFolder = (dir)=>{  
            if(!fs.existsSync(dir)){  
                fs.mkdirSync(dir);    
                }                         
            }                           
        
            var ttsData = JSON.parse(JSON.stringify(data));
                
            const option =ttsData.option;
            const search_word =ttsData.search_word;
            const img_url = ttsData.img_url.split('/');
            const contents = ttsData.contents;
            const name = ttsData.name;

            const request = {
                input: {text: contents},
                voice: {languageCode: 'ko-KR', ssmlGender: 'FEMALE'},
                audioConfig: {audioEncoding: 'MP3'},
            };

            var path;
            try{
                const [response] = await client.synthesizeSpeech(request);
                
                // Write the binary audio content to a local file
                const w_File = util.promisify(fs.writeFile);
                
                //jjeong
                // 검색어 별로 저장 공간 분리 : 없으면 폴더 만들어 버려~
                var folder_name, output_name;
                //검색어 페이지 인 경우
                //speaking  ->search -> 검색어 -> 이름 :  세부_url + 각_id_이름 
                if(option == 'search'){
                    folder_name = `./speaking/search/${search_word}`
                    makeFolder(folder_name);
                    output_name = detail_url +'_'+name;
                }
                //세부 페이지인 경우
                //speaking  ->detail -> 세부_url-> 이름 :  각_id_이름
                else if(option == 'detail'){
                    folder_name = `./speaking/detail/${img_url}`
                    makeFolder(folder_name);
                    output_name = name;
                }                                                              
                else return;                                                  
                
                // 경로 정해주기 
                path = `${folder_name}/${output_name}.mp3`;  

                if (!(fs.existsSync(path))) {
                    //file exists
                    await w_File(path, response.audioContent, 'binary');
                    console.log('Audio content written to file: output.mp3'); 
                }
                
            }catch(err){
                console.error('ERROR:', err);
                return;
            }
            // TTS File 재생 
            //console.log(data);
            time = 0;
            //const path = `./speaking/output.mp3`;
            const release = await mutex.acquire();

            try {
                var player = require('play-sound')(opts = {});

                //const speakPath = `./speaking/${req.body.id}.mp3`;
                
                const getMP3Duration = require('get-mp3-duration');
                const buffer = fs.readFileSync(path);
                const duration = getMP3Duration(buffer);

                time = duration;

                player.play(path, function(err){
                    if (err) throw err;
            });
            } finally {
                setTimeout(function() {
                release();
                }, time);
            }
            
        });
        
        
    });

    
	async function savetts(data){
		    // 태그 속 내용 (바로바로) 읽어주기

		 	}

};
