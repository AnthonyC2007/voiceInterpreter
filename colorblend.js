// colorblend.js
// Inlet 0 : list of 6 floats (probabilities 0.0 – 1.0)
//           order: neutral, sad, fear, happy, disgust, angry
// Outlet 0: three ints  R  G  B  (0 – 255)

var COLORS = [
    [128, 128, 128],   // neutral  – gray
    [ 59, 139, 212],   // sad      – blue
    [139,  79, 212],   // fear     – purple
    [249, 203,  66],   // happy    – yellow
    [ 61, 168,  84],   // disgust  – green
    [226,  75,  74]    // angry    – red
];

function list() {
    var probs = arrayfromargs(arguments);
    var r = 0, g = 0, b = 0;
    for (var i = 0; i < Math.min(probs.length, COLORS.length); i++) {
        var w = Math.max(0, Math.min(1, probs[i]));
        r += COLORS[i][0] * w;
        g += COLORS[i][1] * w;
        b += COLORS[i][2] * w;
    }
    outlet(0, Math.round(r), Math.round(g), Math.round(b));
}
