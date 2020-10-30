var input = "청소기";
module.exports={
    crawl: async function(req,res){
      start = new Date().getTime();
        const { PythonShell } = require('python-shell');
        const ret = [];
        let options = {
            scriptPath: "./",
            args: [input]
          };
          //for문 돌면서 동기적으로 함수를 실행한다.
        const mall = ['crawler_lotte.py','crawler_emart.py','crawler_gmarket.py']
          for( var i=0 ;i<3;i++){
            function mall_crawl(){
                    // 동기적 처리를 위한 일~
                        return new Promise((resolve,reject) =>{
                            try{
                           PythonShell.run(mall[i], options, (err, results) => {
                            if (err) throw err;
                            ret.push(results);
                            resolve();  
                        }); }
                    catch{
                      console.log('error running python code')
                      reject();
                    } })};
                    await mall_crawl();    
        }
        elapsed = new Date().getTime() - start;

        //확인용
        console.log(`소요시간 : ${elapsed}`);
    }
}


