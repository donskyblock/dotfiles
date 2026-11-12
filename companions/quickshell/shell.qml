import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Io
import Quickshell.Services.Mpris

ShellRoot {
    id: root
    SystemClock { id: clock; precision: SystemClock.Minutes }
    property var player: {
        const players = Mpris.players.values;
        return players.find(p => p.isPlaying) || players[0] || null;
    }
    Variants {
        model: Quickshell.screens
        PanelWindow {
            id: panel
            required property var modelData
            screen: modelData
            anchors { top: true; left: true; right: true }
            margins { top: 8; left: 12; right: 12 }
            implicitHeight: 40
            exclusiveZone: 48
            color: "transparent"
            Rectangle {
                anchors.fill: parent
                color: "#ee1a1b26"
                radius: 12
                border.color: "#414868"
                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 16
                    anchors.rightMargin: 16
                    spacing: 18
                    Text {
                        text: panel.width > 800 ? "AFTER HOURS  /  Tokyo Night" : "AFTER HOURS"
                        color: "#7aa2f7"
                        font { family: "Noto Sans"; pixelSize: 12; bold: true }
                        MouseArea {
                            anchors.fill: parent
                            onClicked: Quickshell.execDetached([Quickshell.env("HOME") + "/.local/bin/after-hours-shell", "launcher"])
                        }
                    }
                    Item { Layout.fillWidth: true }
                    Text {
                        visible: panel.width > 650 && root.player !== null
                        Layout.maximumWidth: Math.max(80, panel.width * 0.3)
                        elide: Text.ElideRight
                        text: root.player ? (root.player.isPlaying ? "▶  " : "Ⅱ  ") + (root.player.trackTitle || "Media") + (root.player.trackArtist ? " · " + root.player.trackArtist : "") : ""
                        color: "#bb9af7"
                        font { family: "Noto Sans"; pixelSize: 12 }
                        MouseArea { anchors.fill: parent; onClicked: { if (root.player && root.player.canTogglePlaying) root.player.togglePlaying(); } }
                    }
                    Item { Layout.fillWidth: true }
                    Text {
                        text: "APPS"
                        color: "#7dcfff"
                        font { family: "Noto Sans"; pixelSize: 12 }
                        MouseArea { anchors.fill: parent; onClicked: Quickshell.execDetached([Quickshell.env("HOME") + "/.local/bin/after-hours-shell", "launcher"]) }
                    }
                    Text {
                        text: Qt.formatDateTime(clock.date, panel.width > 800 ? "ddd d MMM  ·  HH:mm" : "HH:mm")
                        color: "#c0caf5"
                        font { family: "Noto Sans"; pixelSize: 12 }
                    }
                }
            }
        }
    }
}
