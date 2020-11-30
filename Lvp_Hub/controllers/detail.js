module.exports={
    crop: function(req,res){
        console.log("hi");
      /*
        const { PythonShell } = require('python-shell');
        PythonShell.run('test.py', null, (err, results) => {
            if (err) throw err;
                console.log(`results: ${results}`);
        });*/
        console.log(req.body);
    },
       


    passURL: function(req,res) {
	     
        var detail_url=req.body.detailURL; // 데이터는 여기로 잘 넘어옴
	console.log(req.body.detailURL);
	    var _ocr = detail_url;
	   var for_ocr = _ocr.split('/').reverse()[0];   
	                //console.log(for_ocr);
        async function crawl_detail(img_url){       
            const { PythonShell } = require('python-shell');
           var ret = [];
            let options = {
                scriptPath: "./",
                args: [img_url]
              };
            const mall = ['./crawling_server/crawler_detail_lotte.py','./crawling_server/crawler_emart_detail.py','./crawling_server/crawler_detail_gmarket.py']
            function mall_crawl(img_url){
                var cite = '';
                //url 속 사이트 정보를 가지고 어떤 파이썬 파일을 쓸것인지를결정
                if(img_url.indexOf('lotte')!= -1)
                     cite = mall[0];
                else if( img_url.indexOf('ssg')!= -1)
                     cite = mall[1];
                else if( img_url.indexOf('gmarket')!= -1)
                     cite = mall[2];
                else
                    return;

		    // 동기 방식으로 파이썬 파일 실행 
		    return new Promise((resolve,reject) =>{
			    //yaewon temp	
			    try{
				    PythonShell.run(cite, options, (err, results) => {
					    if (err) throw err;
					    //----------------
					    var essential = [];  
					    var detail_info = [];         //
					    if(results != null && results.length >=3){
						    //console.log(results);

						    ess =results[results.length-1].split('\'');
						    //var essential = [];
						    for(var i=0; i<ess.length;i=i+4){
							    var tmp =[];
							    tmp.push(ess[i+1]);
							    tmp.push(ess[i+3]);
							    essential.push(tmp);

						    }

						    if(results[results.length-2] != "" && results[results.length-2] != null ){

							   var tmp= results[results.length-2];

							    tmp=tmp.replace('[', "");
							    tmp=tmp.replace('[', "");
							    tmp=tmp.replace(/]/g, "");
							    tmp=tmp.replace(/\\t/g, "");
							    tmp=tmp.replace(/\t/g, "");
							    tmp=tmp.replace(/,/g, "");
							    tmp=tmp.replace(/\n/g, "");
							    _tmp = tmp.split("\\n");
							    for (var i=0; i<_tmp.length;i++){
								    __tmp = tmp.split(".");
								    for (var j=0; j< __tmp.length;j++)
								    	detail_info.push(__tmp[j]+".");
							    }
						    }
						    //----------------

						    for(var i=3; results !=null&&i<results.length-2;i++){	
							    var source = {
								    "product_name" : for_ocr,
								    "main_img": results[0],
								    "name" :results[1],
								    "price": results[2],
								    "image" : results[i],
								    "detail_url" : detail_url,
								    "detail_text" : detail_info,
								    "essential" : essential
							    }
							    ret.push(source);
						    }
					    }

                                  	     resolve();  
                    	}); 
		} catch{
                          console.log('error running python code')
                          reject();
                        } })}
            await mall_crawl(img_url); 
	function send_render(src){
             
                //console.log(src);


                res.render('../views/detail.ejs',{detail_data : src});//, {toPrint : result});
              }
              await send_render(ret);
            //확인 용 콘솔
           
        }
         crawl_detail(detail_url);
        // yae
        
    },

    crawl: async function(req,res){
        start = new Date().getTime();
        const { PythonShell } = require('python-shell');
        const ret = [];
        let options = {
            scriptPath: "./",
            args: [input]
        };
        //for문 돌면서 동기적으로 함수를 실행한다.
        const mall = ['crawler_lotte.py','crawler_emart.py','crawler_gmarket.py']
        for( var i=0 ;i<3;i++){
            function mall_crawl(){
                // 동기적 처리를 위한 일~
                return new Promise((resolve,reject) =>{
                    try{
                        PythonShell.run(mall[i], options, (err, results) => {
                            if (err) throw err;
                            ret.push(results);
                            resolve();
                        }); }
                    catch(error){
                        console.log('error running python code')
                        reject();
                    } })};
            await mall_crawl();
        }
        elapsed = new Date().getTime() - start;

        //확인용
        console.log(`소요시간 : ${elapsed}`);
    }
}


