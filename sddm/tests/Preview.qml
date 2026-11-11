import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    id: preview
    width: 1920
    height: 1080
    visible: true
    title: "Tokyo Night SDDM preview — mock data only"
    property bool checkFailure: false
    property var config: ({font: "Noto Sans", background: "background.png"})
    property var userModel: ({lastUser: "nightowl", lastIndex: 0})
    property var sessionModel: sessions
    property var keyboard: ({capsLock: false, currentLayout: 0, layouts: []})
    property var sddm: auth
    ListModel {
        id: sessions
        property int lastIndex: 0
        ListElement { name: "COSMIC" }
        ListElement { name: "MangoWC" }
    }
    QtObject {
        id: auth
        property bool canSuspend: true
        property bool canReboot: true
        property bool canPowerOff: true
        property int loginCount: 0
        signal loginFailed()
        signal loginSucceeded()
        signal informationMessage(string message)
        function login(user, password, index) {
            if (user !== "nightowl" || index !== 0) {
                console.error("Unexpected login model values");
                Qt.exit(2);
                return;
            }
            loginCount++;
            Qt.callLater(loginFailed);
        }
        function suspend() { console.log("MOCK: suspend"); }
        function reboot() { console.log("MOCK: reboot"); }
        function powerOff() { console.log("MOCK: power off"); }
    }
    Loader { id: theme; anchors.fill: parent; source: "Main.qml" }
    Timer {
        interval: 1000; running: true; repeat: false
        onTriggered: {
            if (!theme.item) { console.error("Theme did not load"); Qt.exit(2); return; }
            if (preview.checkFailure) {
                theme.item.submit();
                theme.item.submit(); // Busy state must suppress duplicate submissions.
                finish.start();
            } else {
                capture();
            }
        }
    }
    Timer {
        id: finish
        interval: 300
        onTriggered: {
            if (auth.loginCount !== 1 || theme.item.busy || theme.item.feedback.length === 0) {
                console.error("Login failure recovery check failed");
                Qt.exit(2);
            } else {
                console.log("Login submission and failure recovery passed");
                capture();
            }
        }
    }
    function capture() {
        theme.item.grabToImage(function(result) {
            if (!result.saveToFile("preview.png")) { Qt.exit(2); return; }
            console.log("Preview saved");
            Qt.quit();
        });
    }
}
