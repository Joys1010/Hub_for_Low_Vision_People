module.exports = {

    searching: function(req,res) {
        console.log("hi search");
        new Search();
        this.keyword = document.querySelector('input[name = "search_word"]');
        this.button = document.querySelector('.btn btn-primary');
        this.form = document.querySelector('.search_joys');
	console.log(keyword)
        console.log(keyword)
    }
}
