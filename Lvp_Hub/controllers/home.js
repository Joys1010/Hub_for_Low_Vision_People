module.exports = {
    index: function(req,res){
        res.render('../views/index.ejs');
    },
    searchpg: function(req,res){
      res.render('../views/search.ejs');
    },
    detailpg : function(req,res){
      res.render('../views/detail.ejs');
    }

};
