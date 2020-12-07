module.exports = {
	index: function(req,res){
		res.render('../views/index.ejs');
	},
	detailpg: function(req,res){
		/* console.log("url url"+req.body); */
		res.render('../views/detail.ejs');
	},
	searching : async function(req,res){
		const dotenv = require("dotenv")
		dotenv.config()

		var search_category = req.body.search_category;
		var search_word = req.body.search_word;
		var ret = [];
		console.log(req.body)

		mongoose = require('mongoose');

		function connect(){
			mongoose.connect(process.env.DB_CONNECT,
			{ useNewUrlParser : true, useUnifiedTopology : true },
			(err) => {
				if(err) return console.error(err);
			});

		}
		
		var checked = new Array();

		function getData(category, word){
			return new Promise((resolve, reject) => {
				connect();
			
				mongoose.connection.on('open', async function() {
					console.log('Mongoose connected.');
					console.log(word);

					/*collection 바꾸는 부분*/
					
					async function test(){
						if(category!=null & category.length <=3){
						for(var i = 0 ; category!=null && i < category.length ; i++){
							connection.db.collection("productData", function(err, collection){
								var cat = category[i];
								collection.find({"search_category": category[i], "search_word":word}).toArray( function(err, data){
	
									if(data === undefined || data.length == []){
										checked.push(cat);
									}
									
								})
							});
						}
					  }else if(category != null){
					  	connection.db.collection("productData", function(err, collection){
								var cat = category;
								collection.find({"search_category": cat, "search_word":word}).toArray( function(err, data){
	
									if(data === undefined || data.length == []){
										checked.push(cat);
									}
									
								})
							});
					  }
					}
					test()
					setTimeout(resolve, 3500)
				});
			});
		}

		function getData2(category, word){
			return new Promise((resolve, reject) => {
				connect();

				mongoose.connection.on('open', function() {
					console.log('Mongoose connected.');
					console.log(word);
					/*collection 바꾸는 부분*/

				 	if(category != null && category.length>3){
					  	connection.db.collection("productData", function(err, collection){
								var cat = category;
								collection.find({"search_category": cat, "search_word":word}).sort({price : 1}).toArray( function(err, data){
									resolve(data);

								})
							});
					  }

					else if(category != null && category.length <=3){
					connection.db.collection("productData", function(err, collection){
						
						collection.find({"search_category": {$in : category}, "search_word":word}).sort({price : 1}).toArray(function(err, data){
							//console.log(data)
							resolve(data);
						})
						
					});
					
					}
					
					
				});
			});
		}
		
		await getData(search_category, search_word);
		
		if(checked !=null && checked.length<=3){
		for(var j = 0 ; checked!=null && j < checked.length ; j++){
			console.log("start")
			await crawl_search(search_word, checked[j]);
			console.log("end")
			}
		}else if(checked !=null){
		var tmp ="";
		for(var j = 0 ; j < checked!=null &&j< checked.length ; j++){

			tmp = tmp+checked[j];
		}
			await crawl_search(search_word, tmp);
		}
		mongoose.connection.close();
		
		let db_data = await getData2(search_category, search_word);
		//console.log(db_data)

		mongoose.connection.close();
		
		data_send(db_data);
		
		async function data_send(db_data) {
			/*yae*/
			var shopping_json = db_data;
			/*data 넣기*/

			function send_render(src){
				if(src === undefined || src.length === 0){
					res.redirect('/error');
				}else res.render('../views/search.ejs', {data : src});
				
			}

			await send_render(shopping_json);
		}

		async function crawl_search(search_word, search_category) {

			console.log(search_category)
			const {PythonShell} = require('python-shell');

			let options = {
				scriptPath: "./",
				args: [search_word]
			};

					var undefine_error = false;

			var shopping_json = []
			function mall_crawl(mall,_category,word) {
				return new Promise((resolve, reject) => {
					try {
						PythonShell.run(mall, options, (err, results) => {
							if (err) throw err;
							for (var i = 0;results!=null && i < results.length; i++) {
								var a = results[i].split('\'');
								var data = {
									"search_category" : _category,
									"search_word" : word,
									"product_name": a[3],
									"price": a[5],
									"image": a[7],
									"detail": a[9],
									"review": a[11]
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
			//await mall_crawl();
	//joys adjusted : check plz

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
			await mall_crawl(mall, search_category,search_word);
			

			function sort_by_key(array, key)
			{
				return array.sort(function(a, b)
					{
						var x = a[key]; var y = b[key];
						return ((x < y) ? -1 : ((x > y) ? 1 : 0));
					});
			}

			/*
			function sortByWins(obj) {
				return Object.keys(obj).sort(function(i, j) {
					return obj[i].review - obj[j].review;
				}).reduce(function (result, key) {
					result[key] = obj[key];
					return result;
				}, {});
			}*/
			/*
			function send_render_c(src){

				//sorting continue...
				//src = sort_by_key(src, 'review');
				res.render('../views/search.ejs', {data : src});

			}
			await send_render_c(shopping_json);
			*/
		}
		/*
		if (db_data ===undefined || db_data.length === 0) {

			crawl_search(search_word,search_category);
		}
		else {
			data_send(db_data);
		}
		*/
	},
	error : function(req,res){
		res.render('../views/nosearch.ejs')
	}
};

const express = require('express');
const { connection } = require('mongoose');
const router = express.Router();
