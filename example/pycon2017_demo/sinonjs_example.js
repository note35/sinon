define([
    "doh/runner",
    "dojo/node!sinon",
    "dojo/node!child_process"
], function(doh, sinon, child_process) {

    sinon.config = {
        useFakeTimers: false
    };

    tests = {
        "001: spies(): function called times check": function() {
            var spy = sinon.spy(myObj, "print");
            myObj.print(expected_string);
            sinon.assert.calledOnce(spy);
            spy.restore();
        },

        "002: spies(): function called with check": function() {
            var spy = sinon.spy(myObj, "print");
            myObj.print(expected_string);
            sinon.assert.calledWith(spy, expected_string);
            spy.restore();
        },
    }

    function setUp(){
        // Define global object
        expected_string = "some string";

        myObj = {
            tmp: false,
            print: function(s){
                //console.log("myObj.print: " + s);
            }
        };

        myAsync = {
            delay: function(callback){
                spawn = child_process.spawnSync;
                ok = spawn( "./tests/async.sh" );
                callback(ok.stdout.toString());
            }
        };
    }

    var wrapped = [];
    for(var name in tests){
        wrapped.push({
            name: name,
            setUp: setUp,
            runTest: tests[name]
        })
    }

    doh.register("SinonTest", wrapped);
});
