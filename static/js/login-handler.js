// const ipc = require('electron').ipcRenderer;
// var http = require("http");
// var projectVersion = require("electron").remote.app.getVersion();

let hostName;
let listeningPort;

// window.onload = function () {
//     // check the server connection on load, if server is offline, all interactive elements become disabled
//     let urlParam = (global.location.search).slice(1).split("&");
//     hostName = urlParam[0].split("=")[1];
//     listeningPort = urlParam[1].split("=")[1];

//     disableAllElements();
//     checkServerConnection();
//     $("#server-ip").html(`${hostName}:${listeningPort}`);
//     $("#project-version").html(projectVersion);
// }

document.getElementById('ckb1').onclick = function () {
    // disable the textbox elements on "remember-me" usage
    if(document.getElementById('ckb1').checked == false){
        document.getElementById("txtUsr").disabled = false;
        document.getElementById('txtPwd').disabled = false;
        document.getElementById('txtUsr').value = null;
        document.getElementById('txtPwd').value = null;
    }
}

document.getElementById('btn-login').onclick = function (event) {
    // handle the login action
    event.preventDefault(); // prevent bootstrap default behaviour of reload a page after a form submission

    let txtUser = document.getElementById('txtUsr').value;
    let txtPwd = document.getElementById('txtPwd').value;

    if(document.getElementById('ckb1').checked){
        var credentials = {
            user: txtUser,
            password: txtPwd
        }
        localStorage.setItem('userCredentials', JSON.stringify(credentials)); 
    } else {
        localStorage.clear();
    }
    
    var postData = JSON.stringify({
        'username': txtUser,
        'password': txtPwd
    });
    console.log(postData)

    var postOptions = {
        hostname: hostName,
        port: listeningPort,
        path: "/login",
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            // 'Content-Length': Buffer.byteLength(postData)
        }
    };
    console.log(postOptions)

    // let req = http.request(postOptions, (res) => {
    //     console.log(`STATUS: ${res.statusCode}`);
    //     console.log(`HEADERS: ${JSON.stringify(res.headers)}`);
    //     res.setEncoding('utf8');

    //     res.on('data', (foo) => {
    //         console.log(`incoming data: ${foo}`);

    //         if (res.statusCode == 200) {
    //             ipc.sendSync('entry-accepted', foo);
    //         } else {
    //             $("#lbl").html(
    //                 `<div class="alert alert-danger" role="alert" id="alert-fe">
    //                     ${JSON.parse(foo)["message"]}
    //                 </div>`
    //             );
    //         }
    //     });

    //     res.on('end', () => {
    //         console.log('Response finished.');
    //     });
    // });

    // req.write(postData);
    // req.end();
}

// function checkServerConnection() {
//     // check server connection
//     var getData = JSON.stringify({
//         "ping": "pong"
//     });

//     var getOptions = {
//         hostname: hostName,
//         port: listeningPort,
//         path: "/",
//         method: "GET",
//         headers: {
//             "Content-Type": "application/json",
//             'Content-Length': Buffer.byteLength(getData)
//         }
//     };

//     let req = http.request(getOptions, (res) => {
//         console.log(`STATUS: ${res.statusCode}`);
//         console.log(`HEADERS: ${JSON.stringify(res.headers)}`);
//         res.setEncoding('utf8');

//         res.on('data', (foo) => {
//             console.log(`response: ${foo}`);
//         });

//         res.on('end', () => {
//             console.log('The server is online.');
            
//             if (res.statusCode == 200) {
//                 document.getElementById("server-status").innerHTML = "online";
//                 document.getElementById("server-status").style.color = "green";
//                 enableAllElements();
//                 loadCredentials();
//                 document.getElementById("response-status").innerHTML = "200";
//             }            
//         });
//     });

//     req.on('error', error => {
//         console.log(error);
//         document.getElementById("server-status").innerHTML = "offline";
//         document.getElementById("server-status").style.color = "red";
//     });

//     req.write(getData);
//     req.end();
// }

// function disableAllElements() {
//     // disable all elements
//     var nodes = document.getElementById("main-div").getElementsByTagName('*');

//     for(var i = 0; i < nodes.length; i++){
//         nodes[i].disabled = true;
//     }
// }

// function enableAllElements() {
//     // enable all elements
//     var nodes = document.getElementById("main-div").getElementsByTagName('*');

//     for(var i = 0; i < nodes.length; i++){
//         nodes[i].disabled = false;
//     }
// }

// function loadCredentials() {
//     // load credentials from localStorage variable
//     var credentials = JSON.parse(localStorage.getItem('userCredentials'));
    
//     if(credentials != null){
//         document.getElementById("txtUsr").disabled = true;
//         document.getElementById('txtPwd').disabled = true;
//         document.getElementById('txtUsr').value = JSON.parse(localStorage.getItem('userCredentials'))['user'];
//         document.getElementById('txtPwd').value = JSON.parse(localStorage.getItem('userCredentials'))['password'];
//         document.getElementById('ckb1').checked = true;
//     }
// }

// $("#change-server").click(function () {
//     // change server address to a new ip:port
//     let regExp = new RegExp(/^(localhost|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)):(6553[0-5]|655[0-2][0-9]|65[0-4][0-9][0-9]|6[0-4][0-9][0-9][0-9][0-9]|[1-5](\d){4}|[1-9](\d){0,3})$/);

//     if (!regExp.test($("#server-addr").val())) {
//         // sets the modal style to red-danger
//         $(".modal-content").css({'background': '#f8d7da', 'color': '#721c24', 'border-color': '#f5c6cb'});
//         // update the button style to red-danger
//         $("#modal-button").removeClass("btn-success").addClass("btn-danger");
//         // sets the message according to the back-end
//         $("#transaction-generic-message").html("Please, set a valid server address.");
//         // blocks the access to background content
//         $('#generic-modal').modal('show');
//         $("#server-addr").val("");

//         return;
//     }

//     ipc.sendSync('change-server', $("#server-addr").val());
// });
