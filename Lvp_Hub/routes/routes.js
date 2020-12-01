
var express = require('express'),

    router = express.Router(),
    home = require('../controllers/home'),
    detail = require('../controllers/detail');

//수정했음
router.get('/', home.index);
//search 랑 detail도 물품 id 값에 따라 바뀌도록 해야됨... 나중에 post로 바꿔야할듯
//router.get('/search',home.searchpg);

router.post('/get', detail.crop);

//이거가 검색페이지에서 하나 눌렀을때 상세로 url 넘겨주는 걸로 합시다
//router.post('/passURL',detail.passURL);
//router.get('/detail',home.detailpg);

//router.get('/detail', detail.passURL)
router.post('/detail', detail.passURL);

router.post('/search',home.searching);

router.get('/error', home.error);
module.exports =router;
