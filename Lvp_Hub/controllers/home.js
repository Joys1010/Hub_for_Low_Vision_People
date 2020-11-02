module.exports = {
    index: function(req,res){
        res.render('../views/index.ejs');
    },
    detailpg: function(req,res){
        // console.log("url url"+req.body);
        res.render('../views/detail.ejs');
    },
    searching : function(req,res){
        console.log("hi");

        var search_category = req.body.search_category;
        var search_word = req.body.search_word;
        var ret = [];
        var json_output = [];
	console.log(search_word);
        console.log(search_category);


        async function crawl_search(input) {
            // var search_word = req.body;
            //console.log(search_word);
            //start = new Date().getTime();
            const {PythonShell} = require('python-shell');

            let options = {
                scriptPath: "./",
                args: [input]
            };

            var mall;
            if (search_category == 'emart') {
                mall = './crawling_server/crawler_emart.py';
            } else if (search_category == 'lotte') {
                mall = './crawling_server/crawler_lotte.py';
            } else if (search_category == 'gmarket') {
                mall = './crawling_server/crawler_gmarket.py';
            }
		else {
	
                mall = './crawling_server/crawler_lotte.py';
            } 
            //for문 돌면서 동기적으로 함수를 실행한다.
            var undefine_error = false;

            // jjeong remeber 크롤러 파일 이마트 참조해서 고치기

	    
            var shopping_json = []
            function mall_crawl() {
                // 동기적 처리를 위한 일~
                return new Promise((resolve, reject) => {
                    try {
                        PythonShell.run(mall, options, (err, results) => {
                            if (err) throw err;
                            for (var i = 0;results!=null && i < results.length; i++) {
                                var a = results[i].split('\'');
                                var data = {
                                    "search": a[1],
                                    "name": a[3],
                                    "price": a[5],
                                    "img_url": a[7],
                                    "detail_url": a[9]
                                }
                                shopping_json.push(data);
                		console.log(data);
                            }
                            json_output.push(shopping_json);
                               // ret.push(results);
                            resolve();
                        });
                    } catch {
                        console.log('error running python code')
                        reject();
                    }
                })

            };
            await mall_crawl();

            function send_render(src){


                res.render('../views/search.ejs', {data : src});

            }
            await send_render(shopping_json);
        }



        //search_word를 기반으로 크롤링 함수로 보낼 예정
        //결과를 search.ejs 에 보낼 것이다.
        crawl_search(search_word);


    }
};

const express = require('express');
const router = express.Router();
