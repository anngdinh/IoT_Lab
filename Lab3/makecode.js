serial.onDataReceived(serial.delimiters(Delimiters.Hash), function () {
    cmd = serial.readUntil(serial.delimiters(Delimiters.Hash))
    if (cmd == "LTrue") {
        basic.showString("L1")
    } else if (cmd == "LFalse") {
        basic.showString("L0")
    } else if (cmd == "PTrue") {
        basic.showString("P1")
    } else if (cmd == "PFalse") {
        basic.showString("P0")
    }
})
let cmd = ""
let delayDefault = 5
let i = delayDefault
let j = delayDefault
basic.forever(function () {
    if (i != 0) {
        i += -1
    } else {
        if (j == delayDefault) {
            serial.writeString("!1:TEMP:" + input.temperature() + "#")
        }
        if (j == 0) {
            serial.writeString("!1:LIGHT:" + input.lightLevel() + "#")
            i = delayDefault
            j = delayDefault
        } else {
            j += -1
        }
    }
    basic.pause(1000)
})
