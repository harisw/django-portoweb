var usernameInp = $("#username");
var usernameHead = $("#usernameHeader");
var joinBtn = $("#joinBtn");
var username
var webSocket;
var mapPeers
function webSocketOnMessage(ev){
    var parsedData = JSON.parse(ev.data);
    var msg = parsedData['message'];
    var peerUsername = parsedData['peer'];
    var action = parsedData['action'];

    if(username == peerUsername){
        return;
    }
    var receiver_channel_name = parsedData['message']['receiver_channel_name'];
    if(action == 'new-peer'){
        createOfferer(peerUsername, receiver_channel_name);

        return;
    }
}
$('#joinBtn').click(() => {
    username = usernameInp.val();
    
    if(username == '') return;

    usernameHead.text(username);
    // usernameInp.disable();
    usernameInp.hide();

    // joinBtn.disable();

    var loc = window.location;
    var wsStart = 'ws://';

    if(loc.protocol == 'https:'){
        wsStart = 'wss://';
    }

    var endPoint = wsStart + loc.host + loc.pathname;
    console.log('endpoint: ', endPoint);
    
    webSocket = new WebSocket(endPoint);

    webSocket.addEventListener('open', (e) => {
        console.log('Connection opened');
        sendSignal('new-peer', {});
    });
    webSocket.addEventListener('message', webSocketOnMessage);
    webSocket.addEventListener('closed', (e) => {
        console.log('Connection closed');
    });
    webSocket.addEventListener('error', (e) => {
        console.log('Error: ');
    });
});

var localStream = new MediaStream();
const constraints = {
    'video': true,
    'audio': true
};

const localVideo = document.querySelector('#local-video');

var userMedia = navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
        localStream = stream;
        localVideo.srcObject = localStream;
        localVideo.muted = true;
    }).catch(err => {
        console.log('Error: ', err);
    })
function sendSignal(action, msg){
    var jsonStr = JSON.stringify({
        'peer': username,
        'action': action,
        'message': msg
    });
    webSocket.send(jsonStr);
}

function createOfferer(peerUsername, receiver_channel_name){
    var peer = new RTCPeerConnection(null);

    addLocalTracks(peer);

    var dc = peer.createDataChannel('channel');
    dc.addEventListener('open', () => {
        console.log('Connection opened');
    });
    dc.addEventListener('message', dcOnMessage);

    var remoteVideo = createVideo(peerUsername);
    setOnTrack(peer, remoteVideo);
    mapPeers[peerUsername] = [peer, dc];

    peer.addEventListener('iceconnectionstatechange', () => {
        var iceConnectionState = peer.iceConnectionState;

        if(iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed' ){
            delete mapPeers[peerUsername];

            if(iceConnectionState != 'closed'){
                peer.close();
            }

            removeVideo(remoteVideo);
        }
    })
}

function addLocalTracks(peer){
    localStream.getTracks().forEach(track => {
        peer.addTrack(track, localStream);
    });
    return;
}

var messageList = document.querySelector('#message-list');
function dcOnMessage(event){
    var msg = event.data;
    var li = document.createElement('li');
    li.appendChild(document.createTextNode(msg));
    messageList.appendChild(li);
}

function createVideo(peerUsername){
    var videoContainer = document.querySelector('#videoContainer');

    var remoteVideo = document.createElement('video');
    remoteVideo.id = peerUsername + '-video';
    remoteVideo.autoplay = true;
    remoteVideo.playsInline = true;

    var videoWrapper = document.createElement('div');
    videoContainer.appendChild(videoWrapper);
    videoWrapper.appendChild(remoteVideo);
    return remoteVideo;
}

function setOnTrack(peer, remoteVideo){
    var remoteStream = new MediaStream();
    remoteVideo.srcObject = remoteStream;
    peer.addEventListener('track', async(event) => {
        remoteStream.addTrack(event.track, remoteStream)
    })
}

function removeVideo(video){
    var videoWrapper = video.parentNode;
    videoWrapper.parentNode.removeChild(videoWrapper);
}