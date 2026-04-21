// emotionlogic.js
// Inlet 0 : list of 6 floats (0.0 – 1.0)
//           order: neutral, sad, fear, happy, disgust, angry
// Outlet 0: R G B ints for colour blend
// Outlet 1: dominant emotion name + percentage string

outlets = 2;

var EMOTIONS = ["neutral", "sad", "fear", "happy", "disgust", "angry"];

var COLORS = [
    [128, 128, 128],
    [ 59, 139, 212],
    [139,  79, 212],
    [249, 203,  66],
    [ 61, 168,  84],
    [226,  75,  74]
];

function list() {
    var probs = arrayfromargs(arguments);
    var r = 0, g = 0, b = 0;
    var maxVal = -1, maxIdx = 0;

    for (var i = 0; i < Math.min(probs.length, EMOTIONS.length); i++) {
        var w = Math.max(0, Math.min(1, probs[i]));
        r += COLORS[i][0] * w;
        g += COLORS[i][1] * w;
        b += COLORS[i][2] * w;
        if (w > maxVal) {
            maxVal = w;
            maxIdx = i;
        }
    }

    outlet(0, Math.round(r), Math.round(g), Math.round(b));
    outlet(1, EMOTIONS[maxIdx] + "  " + Math.round(maxVal * 100) + "%");
}
