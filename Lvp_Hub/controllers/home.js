module.exports = {
	index: function(req,res){
		res.render('../views/index.ejs');
	},
	detailpg: function(req,res){
		/* console.log("url url"+req.body); */
		res.render('../views/detail.ejs');
	},
	searching : async function(req,res){

		var search_category = req.body.search_category;
		var search_word = req.body.search_word;
		var ret = [];

		/*yae 여기 나중에 정식db에서 가져오고 그래야함! */
		/* 1. url 속 db 이름 바꾸기
		 *             2. db collection 맞춰주기, 각 쇼핑몰별로(search_category) */ 
		console.log(search_word);
		mongoose = require('mongoose');
		/*db 이름 바꾸는 부분*/
		mongoose.connect('mongodb+srv://yaewon:yaewon@testcluster.hft0m.mongodb.net/capstone_front_test?retryWrites=true&w=majority',
			{ useNewUrlParser : true, useUnifiedTopology : true },
			(err) => {
				if(err) return console.error(err);
			});

		function getData(category, word){
			return new Promise((resolve, reject) => {
				mongoose.connection.on('open', function() {
					console.log('Mongoose connected.');
					console.log(word);

					/*collection 바꾸는 부분*/
					connection.db.collection("capstone", function(err, collection){
						collection.find({"search_category":category} ,{"search_word":word}).sort("price", 1).toArray(function(err, data){
							/*console.log(data); // it will print your collection data*/
							resolve(data);
						})
					});
				});
			});
		}
		/*가져온 디비 데이터*/
		let db_data = await getData(search_category, search_word);
		console.log(db_data);

		async function data_send(db_data) {
			/*yae*/
			var shopping_json = db_data;
			/*data 넣기*/
			function send_render(src){
				res.render('../views/search.ejs', {data : src});
			}
			await send_render(shopping_json);
		}

		async function crawl_search(input) {

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
			var undefine_error = false;

			var shopping_json = []
			function mall_crawl() {
				return new Promise((resolve, reject) => {
					try {
						PythonShell.run(mall, options, (err, results) => {
							if (err) throw err;
							for (var i = 0;results!=null && i < results.length; i++) {
								var a = results[i].split('\'');
								var data = {
									"search_category" : search_category,
									"search_word" : search_word,
									"product_name": a[3],
									"price": a[5],
									"image": a[7],
									"detail": a[9]
								}
								shopping_json.push(data);
							}
							resolve();
						});
					} catch {
						console.log('error running python code')
						reject();
					}
				})

			};
			await mall_crawl();

			function send_render_c(src){


				res.render('../views/search.ejs', {data : src});

			}
			await send_render_c(shopping_json);
		}

		if (db_data.length === 0) {

			crawl_search(search_word);
		}
		else {
			data_send(db_data);
		}
	}
};

const express = require('express');
const { connection } = require('mongoose');
const router = express.Router();
