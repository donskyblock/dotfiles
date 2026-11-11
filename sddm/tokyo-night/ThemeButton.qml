import QtQuick 2.15
import QtQuick.Controls 2.15

Button {
    id: control
    property bool primary: false
    property bool danger: false
    implicitHeight: 46
    hoverEnabled: true
    activeFocusOnTab: true
    font.family: "Noto Sans"
    font.pixelSize: 14
    font.weight: Font.Medium
    Accessible.name: text
    contentItem: Text {
        text: control.text
        font: control.font
        color: !control.enabled ? "#737aa2" : control.primary ? "#16161e" : control.danger ? "#f7768e" : "#c0caf5"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
    background: Rectangle {
        radius: 10
        color: control.primary ? (control.down ? "#7aa2f7" : control.hovered ? "#99b7ff" : "#7aa2f7") : (control.down ? "#33467c" : control.hovered ? "#292e42" : "#202336")
        border.width: control.activeFocus ? 2 : 1
        border.color: control.activeFocus ? "#7dcfff" : control.primary ? "transparent" : "#343b58"
        opacity: control.enabled ? 1 : 0.55
        Behavior on color { ColorAnimation { duration: 120 } }
    }
}
