var PythonShell = require('python-shell');

$('#connect').on('click', function(){
    PythonShell.run('../test.py', null, (err, results) => {
        if (err) throw err;
        console.log(`results: ${results}`);
      });
});

//alert('hello?');