module.exports={
    crop: function(req,res){
        const { PythonShell } = require('python-shell');
        PythonShell.run('test.py', null, (err, results) => {
            if (err) throw err;
                console.log(`results: ${results}`);
        });
    }
}
