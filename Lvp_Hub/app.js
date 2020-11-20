var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var cors = require('cors');
var proxy = require('html2canvas-proxy');

var schedule = require("node-schedule");
const fsExtra = require('fs-extra');

const app = express();
//app.use(cors());
app.use("/search", proxy());
app.use("/detail", proxy());

//일단 주석 처리
var router = require('./routes/routes');

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.engine('html',require('ejs').renderFile)


app.use(logger('dev'));
app.use(express.json({limit : "50mb"}));
app.use(express.urlencoded({ extended: true ,limit : "50mb"}));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(express.static(path.join(__dirname, 'public', 'script')));
app.use(express.static(path.join(__dirname)));
//app.use(express.static(path.join(__dirname,'speaking')));
app.use(express.static(path.join(__dirname,'speaking','search')));
app.use(express.static(path.join(__dirname,'speaking','capture')));
app.use(express.static(path.join(__dirname,'speaking','basic')));

//시간마다 디비 비우기, 파일들 삭제하기

var rule = new schedule.RecurrenceRule();
rule.hour = 3;

const j = schedule.scheduleJob(rule, function(){

  const search = path.join(__dirname,'speaking','search');
  const detail = path.join(__dirname,'speaking','detail');
  const capture = path.join(__dirname,'speaking','capture');
  const captured = path.join(__dirname, 'captured');
  const imgOutput = path.join(__dirname,'controllers','python', 'output');

  var deleted = new Array(search, detail, capture, captured, imgOutput);

  for(var i = 0 ; i < deleted.length ; i++){
    //console.log(deleted[i]);
    fsExtra.emptyDirSync(deleted[i]);
  }
  console.log("deleted");
});

//일단 주석 처리
app.use(router);

app.post(function(req,res,next){
  next();
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
