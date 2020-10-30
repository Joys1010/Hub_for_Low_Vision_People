const Searchng = Search.prototype;

function Search() {
    this.keyword = document.querySelector('input[name = "search_word"]');
    this.button = document.querySelector('.btn btn-primary');
    this.form = document.querySelector('.search_joys');

}

new Search();

Searching.Crawling = function() {
    this.form.addEventListener('submit', e => {

    let keyword = this.keyword.value;

    //crawl(keyword, );
    console.log(keyword);

    });
}