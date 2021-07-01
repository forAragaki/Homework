function ff(a){
    console.log(a);
    var us = "logs/" + a + ".html";
    window.open(us, 'newwindow', 'height=600, width=800, top=30%,left=30%, toolbar=no, menubar=no, scrollbars=no, resizable=no,location=no, status=no');
}

$(function() {
    // new gridjs.Grid({
    //     columns: ["Speaker", "Receiver", "Text",'len','Year','Month','Day',"Details"],
    //     search : true,
    //     sort: true,
    //     pagination: {
    //         limit: 10
    //     },
    //     data: []
    // }).render(document.getElementById("wrapper"));

    $('#bt').on('click', function () {
        // $("#wrapper").empty();
        var $telValue = $('#se').val();
        // console.log($telValue);
        if ($telValue === "") {
            alert('null');
            return;
        }
        var oReq = new XMLHttpRequest();
        url = 'http://127.0.0.1:1234/check?query=' + $telValue;
        oReq.open("GET", url, false); //同步请求
        oReq.setRequestHeader("Content-type", "application/json");
        oReq.send("");
        var reslutData = oReq.responseText;//响应结果

        // console.log(reslutData);
        // reslutData = $.parseJSON( reslutData );
        reslutData = eval('(' + reslutData + ')');
        // console.log(reslutData);
        if('spell' in reslutData){
            var inp = reslutData['spell'];
            for(var insert in inp) {
                $("#lp").append("<li id='cl' style='width: 300px'>" + inp[insert] + "</li>");
            }
        }
        // else{
        console.log(reslutData);
        // reslutData = reslutData['result'];
        if ('result' in reslutData || !('spell' in reslutData)) {
            if ('result' in reslutData){
                reslutData = reslutData['result']
            }
            var listdata = [];
            for (var key in reslutData) {
                var temp = reslutData[key];
                var len = temp['len'];
                var ye = temp['year'];
                var mo = temp['month'];
                var da = temp['day'];
                var sen = temp['sen'];
                // console.log(temp['text']);
                var tt = temp['text'][sen];
                var text = tt[0];
                var sp = tt[1];
                var re = tt[2];
                // var url_key = "log/" + key + ".html";
                var st = `<button onclick=ff(` + key + `)>Details</button>`;
                // var st = `<button onclick=f(` +  text +`)>Details</button>`;
                listdata.push([sp, re, text, len, ye, mo, da, new gridjs.html(st)]);
            }
            new gridjs.Grid({
                columns: ["Speaker", "Receiver", "Text",'len','Year','Month','Day',"Details"],
                search : true,
                sort: true,
                pagination: {
                    limit: 10
                },
                data: listdata
            }).render(document.getElementById("wrapper"));
        }
        // }

    })
});
// new gridjs.Grid({
//     columns: ["Speaker", "Receiver", "Text",'Year','Month','Day',"Details"],
//     search : true,
//     sort: true,
//     pagination: {
//         limit: 10
//     },
//     data: [
//         ["John", "john@example.com", "(353) 01 222 3333"],
//         ["Mark", "mark@gmail.com", "(01) 22 888 4444"],
//         ["Eoin", "eoin@gmail.com", "0097 22 654 00033"],
//         ["Sarah", "sarahcdd@gmail.com", "+322 876 1233"],
//         ["Afshin", "afshin@mail.com", "(353) 22 87 8356"]
//     ]
// }).render(document.getElementById("wrapper"));