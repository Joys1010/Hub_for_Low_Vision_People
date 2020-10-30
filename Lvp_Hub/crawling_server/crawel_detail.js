
module.exports={
    crawl: async function(req,res){       
        const { PythonShell } = require('python-shell');
        const ret = [];
        let options = {
            scriptPath: "./",
            args: [img_url]
          };
        const mall = ['crawler_detail_lotte.py','crawler_emart_detail.py','crawler_detail_gmarket.py']
        function mall_crawl(img_url){
            var cite = '';
            //url 속 사이트 정보를 가지고 어떤 파이썬 파일을 쓸것인지를결정
            if(img_url.indexOf('lotte')!= -1)
                 cite = mall[0];
            else if( img_url.indexOf('emart')!= -1)
                 cite = mall[1];
            else if( img_url.indexOf('gmarket')!= -1)
                 cite = mall[2];
            else
                return;
            console.log(cite);
            // 동기 방식으로 파이썬 파일 실행 
            return new Promise((resolve,reject) =>{
            try{
            PythonShell.run(cite, options, (err, results) => {
                 if (err) throw err;
                ret.push(results);
                resolve();  
                }); }
                 catch{
                      console.log('error running python code')
                      reject();
                    } })}
        //임의로 url을 던져줌
        var img_url = "https://www.lotteon.com/p/product/LM8809137650063?sitmNo=LM8809137650063_001&mall_no=1&dp_infw_cd=SCH바나나";
        //함수 실행
        await mall_crawl(img_url); 
        //확인 용 콘솔
         console.log(ret);
    }
}