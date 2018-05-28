document.addEventListener('DOMContentLoaded', function() {

    var websocket_url = 'ws://127.0.0.1:3000';

    var v = window.speechSynthesis.getVoices();

    window.speechSynthesis.onvoicechanged = function() {
        console.log('onvoicechanged');
        var v = window.speechSynthesis.getVoices();
        v.forEach((v, i) => console.log('voices', i, v));
    }

    function getKoreanVoices() {
        var v = window.speechSynthesis.getVoices();
        return v.filter(v => v.lang == 'ko-KR');
    }
    // console.log(getKoreanVoices());

    var ws = new WebSocket(websocket_url);
    ws.onopen = event => {
        // console.log('ws.onopen', event)
        ws.onmessage = function(event) {
            // console.log('ws.onmessage', event)
            var msg = JSON.parse(event.data);
            if (msg.message && msg.message == 'message') {
                console.log('ws message', msg);
                var content = msg.content;
                if (content.tts) {
                    var text = content.tts;
                    var v = window.speechSynthesis.getVoices()
                    console.log('speak', v.length, text);
                    document.querySelector('#tts_message').setAttribute('value', text);
                    utt = new SpeechSynthesisUtterance(text);
                    speechSynthesis.speak(utt);
                }
            }
        }
    }

    window.setInterval(() => {
            console.log('ws connection checking...');
            if (!(ws.readyState == WebSocket.CONNECTING || ws.readyState == WebSocket.OPEN)) {
                console.log('ws not connected', ws.readyState, 'try reconnecting...');
                var onopen_ = ws.onopen;
                ws = new WebSocket(websocket_url);
                ws.onopen = onopen_;
            }
        },
        5000);

})