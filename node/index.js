var express = require('express');
var app = express();
var router = require('./router/routes');


app.set('views', __dirname + '/view')
app.set('view engine', 'ejs');
app.engine('html', require('ejs').renderFile);

app.use(router);

var server = app.listen(3000, function(){
    console.log("Express server has started on port 3000")
});

