var express = require('express'),
    router = express.Router(),
    home = require('../controllers/home'),
    detail = require('../controllers/detail');

router.get('/', home.index);
router.get('/get', detail.crop);

module.exports =router;
