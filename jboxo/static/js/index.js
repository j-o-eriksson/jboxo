// static/js/index.js

import { DebugForm } from "./debug.js";

function main() {
    console.log(document.querySelector(".debug-card"));
    if (document.querySelector(".debug-card")) {
        const debug = new DebugForm();
        debug.showResponse("");
    }
}

console.log("main");

main();
