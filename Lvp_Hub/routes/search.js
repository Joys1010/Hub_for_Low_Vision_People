//첫화면에서 두번째 화면으로 넘어가는거 처리하기 위한 router

var express = require('express');
var router = express.Router();

router.get('/', (req,res,next) => {
    res.render('../views/index');
});



