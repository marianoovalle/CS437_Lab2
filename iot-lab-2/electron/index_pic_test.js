const { RSA_NO_PADDING } = require('constants');
const { write } = require('fs');

document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65430;
var server_addr = "192.168.1.35";   // the IP address of your Raspberry PI

function receive_picture(){
    const fs = require('fs')
    const net = require('net')
    const client =  net.createConnection({port: 65001, host: server_addr}, () => {
        client.write("12");
    });

    client.on('data', (data) => {
       // var buf = Buffer.from(data, 'base64');
        fs.writeFile('picture.jpg', data, (err) => {
            if (err)
              console.log(err);
            else {
              //console.log("File written successfully\n");
              //console.log("The written has the following contents:");
              //console.log(fs.readFileSync("picture.png", "utf8"));
            }});
        //console.log(data);

        document.getElementById("pics").src="picture.jpg";
        
    })
    
}

function client(){
    
    const net = require('net');
    //var input = document.getElementById("message").value;

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`stop`);
    });
    
    // get the data from the server
    client.on('data', (data) => {
        
        rec_data = JSON.parse(data)
        console.log(rec_data)

        //document.getElementById("bluetooth").innerHTML = rec_data.echo ;
        document.getElementById("temperature").innerHTML = rec_data.temp ;
        document.getElementById("speed").innerHTML = rec_data.speed;
        document.getElementById("distance").innerHTML = rec_data.distance;   
        document.getElementById("direction").innerHTML = rec_data.direction;

        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });


}

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {
    const net = require('net');
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        
    });

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        client.write("forward");
        //send_data("87");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        client.write("reverse");
        //send_data("83");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        client.write("turn_left");
        //send_data("65");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        client.write("turn_right");
        //send_data("68");
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}


// update data for every 50ms
function update_data(){
    setInterval(function(){
        // get image from python server
        client();
    }, 50);
}

function update_picture(){
    setInterval(function(){
        receive_picture();
    }, 4000);
}

update_picture();