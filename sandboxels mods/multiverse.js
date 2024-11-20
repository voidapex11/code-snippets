// this code is coppied from fools24.js, all credit goes to r74n.
// I set up this mod so that you could get the multiverse stuff without the other nonsense from fools24
multiverseTimelines = [];
multiverseIndex = 0;

function saveTimeline() {
    // save at current index
    multiverseTimelines[multiverseIndex] = generateSave(undefined, { keep: ["temp", "color"] });
}
function splitTimeline() {
    saveTimeline();
    var newSave = generateSave(undefined, { keep: ["temp", "color"] });
    // add new timeline one after current
    multiverseTimelines.splice(multiverseIndex + 1, 0, newSave);
    loadTimeline(multiverseIndex + 1);
}
function newTimeline() {
    // add new timeline at end
    saveTimeline();
    clearAll();
    multiverseIndex = multiverseTimelines.length;
    saveTimeline();
    loadTimeline(multiverseIndex);
}
function loadTimeline(i) {
    multiverseIndex = i;
    loadSave(multiverseTimelines[i]);
    document.getElementById("timelineIndex").textContent = i;
}
function nextTimeline() {
    saveTimeline();
    if (multiverseIndex === multiverseTimelines.length - 1) {
        newTimeline();
        return
    }
    loadTimeline(multiverseIndex + 1);
}
function prevTimeline() {
    saveTimeline();
    if (multiverseIndex === 0) {
        return
    }
    loadTimeline(multiverseIndex - 1);
}
function redoTimeline() {
    loadTimeline(multiverseIndex);
}
function deleteTimeline() {
    multiverseTimelines.splice(multiverseIndex, 1);
    if (multiverseIndex === multiverseTimelines.length) {
        multiverseIndex--;
    }
    if (multiverseTimelines.length < 1) {
        newTimeline();
    }
    loadTimeline(multiverseIndex);
}

window.addEventListener("load", function () {
    this.document.getElementById("elementControls").insertAdjacentHTML("afterend", `
        <div style="display:block; padding:5px; font-size:13px">
        <button onclick="location.search = '?fools=false'">Return to Normalcy</button>
        </div>
            `);
    this.document.getElementById("elementControls").insertAdjacentHTML("afterend", `
        <div style="display:block; padding:5px; font-size:13px">
        Timeline-<span id="timelineIndex">0</span>:<button onclick="splitTimeline()">Split</button><button onclick="newTimeline()">New</button><button onclick="prevTimeline()">&lt;</button><button onclick="nextTimeline()">&gt;</button><button onclick="redoTimeline()">Redo</button><button onclick="deleteTimeline()">Delete</button>
        </div>
            `);

})
window.addEventListener("keydown", function (e) {
    if (e.ctrlKey || e.metaKey) {
        return
    }
})