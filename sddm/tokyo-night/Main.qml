import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root
    width: 1920
    height: 1080
    color: "#10111c"
    property bool busy: false
    property string feedback: ""
    property bool loginComplete: false
    property date now: new Date()
    property string pendingPower: ""
    readonly property bool wide: width >= 1120 && height >= 720
    readonly property string uiFont: config.font || "Noto Sans"
    readonly property int layoutCount: typeof keyboard !== "undefined" && keyboard.layouts ? keyboard.layouts.length : 0
    readonly property bool capsOn: typeof keyboard !== "undefined" && keyboard.capsLock

    function submit() {
        if (busy || username.text.trim().length === 0 || session.currentIndex < 0)
            return;
        feedback = "";
        busy = true;
        sddm.login(username.text.trim(), password.text, session.currentIndex);
    }
    function requestPower(action) {
        pendingPower = action;
        powerDialog.open();
    }
    Timer { interval: 1000; running: true; repeat: true; onTriggered: root.now = new Date() }
    Connections {
        target: sddm
        function onLoginFailed() {
            root.busy = false;
            root.feedback = qsTr("Could not sign in. Check your credentials and try again.");
            password.text = "";
            password.forceActiveFocus();
        }
        function onLoginSucceeded() {
            root.loginComplete = true;
            password.text = "";
        }
        function onInformationMessage(message) { root.feedback = message; }
    }
    Image {
        anchors.fill: parent
        source: Qt.resolvedUrl(config.background || "background.png")
        fillMode: Image.PreserveAspectCrop
        asynchronous: true
        cache: true
    }
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0; color: "#f210111c" }
            GradientStop { position: 0.48; color: "#bd10111c" }
            GradientStop { position: 1; color: "#5010111c" }
        }
    }
    Row {
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.margins: root.wide ? 48 : 24
        spacing: 12
        Rectangle { width: 8; height: 8; radius: 4; color: "#7aa2f7"; anchors.verticalCenter: parent.verticalCenter }
        Text { text: "A F T E R H O U R S"; color: "#c0caf5"; font.family: root.uiFont; font.pixelSize: 12; font.weight: Font.Medium }
        Text { text: "/  TOKYO NIGHT"; color: "#737aa2"; font.family: root.uiFont; font.pixelSize: 12 }
    }
    Column {
        visible: root.wide
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 52
        anchors.topMargin: 64
        spacing: 4
        Text {
            anchors.right: parent.right
            text: Qt.formatTime(root.now, "HH:mm")
            color: "#c0caf5"; font.family: root.uiFont; font.pixelSize: 76; font.weight: Font.Light
        }
        Text {
            anchors.right: parent.right
            text: Qt.formatDate(root.now, "dddd, d MMMM")
            color: "#a9b1d6"; font.family: root.uiFont; font.pixelSize: 13
        }
    }
    // This card stays usable on smaller laptop panels and high-DPI screens.
    Rectangle {
        id: card
        width: Math.min(390, root.width - 40)
        height: Math.min(root.height - 128, content.implicitHeight + 64)
        x: root.wide ? Math.max(48, Math.round(root.width * 0.08)) : Math.round((root.width - width) / 2)
        y: Math.max(72, Math.round((root.height - height) / 2))
        radius: 0
        color: root.wide ? "transparent" : "#ed161825"
        border.width: 0
        Rectangle { x: 32; y: 0; width: 32; height: 2; color: "#bb9af7"; radius: 1 }
        Flickable {
            anchors.fill: parent
            anchors.margins: 32
            contentHeight: content.implicitHeight
            clip: true
            boundsBehavior: Flickable.StopAtBounds
            ColumnLayout {
                id: content
                width: parent.width
                spacing: 16
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 7
                    Text { text: "S L O W   D O W N .   S I G N   I N ."; color: "#bb9af7"; font.family: root.uiFont; font.pixelSize: 10; font.letterSpacing: 1.8 }
                    Text { text: qsTr("Good to see you."); color: "#c0caf5"; font.family: root.uiFont; font.pixelSize: 30; font.weight: Font.DemiBold }
                    Text { text: qsTr("A little quiet before your next idea."); color: "#a9b1d6"; font.family: root.uiFont; font.pixelSize: 13 }
                }
                Item { Layout.preferredHeight: 4 }
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 7
                    Label { text: qsTr("USERNAME"); color: "#a9b1d6"; font.family: root.uiFont; font.pixelSize: 10; font.letterSpacing: 1.3 }
                    TextField {
                        id: username
                        objectName: "username"
                        Layout.fillWidth: true
                        Layout.preferredHeight: 48
                        text: userModel.lastUser || ""
                        placeholderText: qsTr("Username")
                        color: "#c0caf5"; placeholderTextColor: "#737aa2"
                        font.family: root.uiFont; font.pixelSize: 14
                        leftPadding: 14; rightPadding: 14
                        enabled: !root.busy
                        selectByMouse: true
                        Accessible.name: qsTr("Username")
                        onAccepted: password.forceActiveFocus()
                        background: Rectangle { color: "#1a1b26"; radius: 10; border.width: username.activeFocus ? 2 : 1; border.color: username.activeFocus ? "#7aa2f7" : "#343b58" }
                    }
                }
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 7
                    Label { text: qsTr("PASSWORD"); color: "#a9b1d6"; font.family: root.uiFont; font.pixelSize: 10; font.letterSpacing: 1.3 }
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 8
                        TextField {
                            id: password
                            objectName: "password"
                            Layout.fillWidth: true
                            Layout.preferredHeight: 48
                            placeholderText: qsTr("Enter your password")
                            color: "#c0caf5"; placeholderTextColor: "#737aa2"
                            font.family: root.uiFont; font.pixelSize: 14
                            leftPadding: 14; rightPadding: 14
                            echoMode: reveal.checked ? TextInput.Normal : TextInput.Password
                            passwordCharacter: "●"
                            enabled: !root.busy
                            selectByMouse: true
                            inputMethodHints: Qt.ImhSensitiveData | Qt.ImhNoPredictiveText
                            Accessible.name: qsTr("Password")
                            onAccepted: root.submit()
                            background: Rectangle { color: "#1a1b26"; radius: 10; border.width: password.activeFocus ? 2 : 1; border.color: password.activeFocus ? "#7aa2f7" : "#343b58" }
                        }
                        ThemeButton {
                            id: reveal
                            Layout.preferredWidth: 56
                            Layout.preferredHeight: 48
                            checkable: true
                            text: checked ? qsTr("Hide") : qsTr("Show")
                            font.pixelSize: 11
                            enabled: !root.busy
                            Accessible.name: checked ? qsTr("Hide password") : qsTr("Show password")
                        }
                    }
                }
                Label {
                    visible: root.capsOn
                    text: qsTr("Caps Lock is on")
                    color: "#e0af68"; font.family: root.uiFont; font.pixelSize: 12
                }
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 7
                    Label { text: qsTr("DESKTOP SESSION"); color: "#a9b1d6"; font.family: root.uiFont; font.pixelSize: 10; font.letterSpacing: 1.3 }
                    ComboBox {
                        id: session
                        objectName: "session"
                        Layout.fillWidth: true
                        Layout.preferredHeight: 46
                        model: sessionModel
                        textRole: "name"
                        currentIndex: sessionModel.lastIndex >= 0 ? sessionModel.lastIndex : 0
                        enabled: !root.busy
                        font.family: root.uiFont; font.pixelSize: 13
                        leftPadding: 14
                        rightPadding: 32
                        Accessible.name: qsTr("Desktop session")
                        contentItem: Text { text: session.displayText; font: session.font; color: "#c0caf5"; verticalAlignment: Text.AlignVCenter; elide: Text.ElideRight }
                        indicator: Text { x: session.width - width - 14; y: (session.height - height) / 2; text: "⌄"; color: "#7aa2f7"; font.pixelSize: 17 }
                        background: Rectangle { color: "#202336"; radius: 10; border.width: session.activeFocus ? 2 : 1; border.color: session.activeFocus ? "#7aa2f7" : "#343b58" }
                        delegate: ItemDelegate {
                            width: session.width
                            height: 40
                            highlighted: session.highlightedIndex === index
                            contentItem: Text { text: model.name; color: "#c0caf5"; font.family: root.uiFont; font.pixelSize: 13; verticalAlignment: Text.AlignVCenter }
                            background: Rectangle { color: parent.highlighted ? "#33467c" : "#24283b"; radius: 6 }
                        }
                        popup: Popup {
                            y: session.height + 6
                            width: session.width
                            padding: 6
                            implicitHeight: Math.min(240, popupList.contentHeight + 12)
                            contentItem: ListView { id: popupList; clip: true; implicitHeight: contentHeight; model: session.popup.visible ? session.delegateModel : null; currentIndex: session.highlightedIndex; ScrollIndicator.vertical: ScrollIndicator {} }
                            background: Rectangle { color: "#24283b"; radius: 10; border.color: "#414868" }
                        }
                    }
                }
                ThemeButton {
                    objectName: "login"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 48
                    primary: true
                    text: root.loginComplete ? qsTr("Opening your session…") : root.busy ? qsTr("Signing in…") : qsTr("Sign in  →")
                    enabled: !root.busy && username.text.trim().length > 0 && session.currentIndex >= 0
                    onClicked: root.submit()
                }
                Label {
                    Layout.fillWidth: true
                    visible: root.feedback.length > 0
                    text: root.feedback
                    color: "#f7768e"
                    wrapMode: Text.WordWrap
                    font.family: root.uiFont; font.pixelSize: 12
                    Accessible.role: Accessible.AlertMessage
                }
                Text { text: qsTr("Enter to sign in · Tab to navigate"); color: "#737aa2"; font.family: root.uiFont; font.pixelSize: 10; Layout.alignment: Qt.AlignHCenter }
            }
        }
    }
    Column {
        visible: root.wide
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: 52
        anchors.bottomMargin: 112
        spacing: 8
        Text { anchors.right: parent.right; text: "夜 / AFTER HOURS"; color: "#c0caf5"; font.family: root.uiFont; font.pixelSize: 12; font.letterSpacing: 2 }
        Text { anchors.right: parent.right; text: qsTr("The city slows. Your ideas don't."); color: "#a9b1d6"; font.family: root.uiFont; font.pixelSize: 13 }
    }
    Row {
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: root.wide ? 48 : 12
        spacing: 8
        ThemeButton {
            width: 72; height: 36
            visible: root.layoutCount > 1
            text: root.layoutCount > 1 && keyboard.layouts[keyboard.currentLayout] ? keyboard.layouts[keyboard.currentLayout].shortName.toUpperCase() : ""
            Accessible.name: qsTr("Change keyboard layout")
            enabled: !root.busy
            onClicked: keyboard.currentLayout = (keyboard.currentLayout + 1) % keyboard.layouts.length
        }
        ThemeButton { width: Math.min(86, (root.width - 56) / 4); height: 36; text: qsTr("Sleep"); visible: sddm.canSuspend; enabled: !root.busy; onClicked: sddm.suspend() }
        ThemeButton { width: Math.min(86, (root.width - 56) / 4); height: 36; text: qsTr("Restart"); visible: sddm.canReboot; enabled: !root.busy; onClicked: root.requestPower("restart") }
        ThemeButton { width: Math.min(86, (root.width - 56) / 4); height: 36; text: qsTr("Power off"); danger: true; visible: sddm.canPowerOff; enabled: !root.busy; onClicked: root.requestPower("poweroff") }
    }
    Dialog {
        id: powerDialog
        anchors.centerIn: parent
        width: Math.min(360, root.width - 40)
        modal: true
        closePolicy: Popup.CloseOnEscape
        padding: 24
        background: Rectangle { color: "#24283b"; radius: 16; border.color: "#414868" }
        contentItem: ColumnLayout {
            spacing: 20
            Label { Layout.fillWidth: true; text: root.pendingPower === "restart" ? qsTr("Restart this computer?") : qsTr("Power off this computer?"); color: "#c0caf5"; font.family: root.uiFont; font.pixelSize: 18; wrapMode: Text.WordWrap }
            RowLayout {
                Layout.fillWidth: true
                spacing: 12
                ThemeButton { Layout.fillWidth: true; text: qsTr("Cancel"); onClicked: powerDialog.close() }
                ThemeButton { Layout.fillWidth: true; primary: true; text: qsTr("Confirm"); onClicked: { powerDialog.close(); if (root.pendingPower === "restart") sddm.reboot(); else sddm.powerOff(); } }
            }
        }
    }
    Component.onCompleted: {
        if (username.text.length > 0) password.forceActiveFocus();
        else username.forceActiveFocus();
    }
}
