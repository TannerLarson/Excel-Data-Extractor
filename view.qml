import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Window 2.2
import QtQuick.Controls.Styles 1.4

ApplicationWindow {
    title: qsTr("Top Sales Finder")
    visible: true
    height: minimumHeight
    width: minimumWidth
    minimumHeight: colFilterBoxes.height + colCombos.height + 20
    minimumWidth: screen.width * 0.45
    font.pixelSize: screen.height * 0.014

    property var myData: { "region": "", "vertical": "", "vendor": "", "solution": "", "sort": "Total Price",
        "outType": "Text", "numLines": 1, "xlFiles": "", "ssdType": { "optane": false, "nand": false },
        "segment": { "client": false, "dc": false, "iot": false}, "status": {"wApproved": false,
        "wSubmitted": false, "pending": false, "cancelled": false, "lost": false }}

    Column {
        id: colCombos
        x: 15
        y: 10
        spacing: 13
        ComboBox {
            id: comboRegion
            Label {
                text: "Region"
                font.pixelSize: screen.height * 0.010
            }
            width: inOut.x - 30
            model: ListModel {
                id: modelRegion
                ListElement { text: "Ignore" }
                ListElement { text: "ASMO" }
                ListElement { text: "APJ" }
                ListElement { text: "EMEA" }
                ListElement { text: "PRC" }
                ListElement { text: "Blank" }
            }
            onCurrentTextChanged: myData.region = currentText
        }

        ComboBox {
            id: comboVertical
            Label {
                text: "Vertical Market"
                font.pixelSize: screen.height * 0.010
            }
            width: inOut.x - 30
            model: ListModel {
                id: modelVertical
                ListElement { text: "Ignore" }
                ListElement { text: "Automation/Building Management" }
                ListElement { text: "Cloud Service Providers" }
                ListElement { text: "Comms Service Providers" }
                ListElement { text: "Education" }
                ListElement { text: "Energy (Oil & Gas, Utilities, Solar & Wind)" }
                ListElement { text: "Enterprise" }
                ListElement { text: "Financial Services" }
                ListElement { text: "Government" }
                ListElement { text: "Health and Life Sciences" }
                ListElement { text: "Manufacturing" }
                ListElement { text: "Retail" }
                ListElement { text: "Transportation" }
                ListElement { text: "Undefined" }
            }
            onCurrentTextChanged: myData.vertical = currentText
        }

        ComboBox {
            id: comboVendor
            Label {
                text: "Vendor Group"
                font.pixelSize: screen.height * 0.010
            }
            width: inOut.x - 30
            model: ListModel {
                id: modelVendor
                ListElement { text: "Ignore" }
                ListElement { text: "Cisco System" }
                ListElement { text: "DELL" }
                ListElement { text: "HP" }
                ListElement { text: "Huawei" }
                ListElement { text: "Lenovo" }
                ListElement { text: "Supermicro" }
                ListElement { text: "Acer" }
                ListElement { text: "Asus" }
                ListElement { text: "Cray" }
                ListElement { text: "Quanta" }
                ListElement { text: "Samsung" }
                ListElement { text: "ZT Systems" }
                ListElement { text: "Others" }
                ListElement { text: "Blank" }
            }
            onCurrentTextChanged: myData.vendor = currentText
        }

        ComboBox {
            id: comboSolution
            Label {
                text: "Solution"
                font.pixelSize: screen.height * 0.010
            }
            width: inOut.x - 30
            model: ListModel {
                id: modelSolution
                ListElement { text: "Ignore" }
                ListElement { text: "vSAN" }
                ListElement { text: "Ceph" }
                ListElement { text: "CAS/Caching" }
                ListElement { text: "Cloud Storage" }
                ListElement { text: "Database" }
                ListElement { text: "EDA" }
                ListElement { text: "HPC" }
                ListElement { text: "Hyperflex" }
                ListElement { text: "IMDT" }
                ListElement { text: "Nutanix" }
                ListElement { text: "Others" }
                ListElement { text: "Unknown" }
            }
            onCurrentTextChanged: myData.solution = currentText
        }
    }

    Column {
        id: colFilterBoxes
        x: 15
        y: 210
        width: 240

        Row {
            id: categories
            spacing: font.pixelSize * 2

            Column {

                Column {
                    width: 99
                    height: 137
                    Label { text: "Product Segment"}
                    CheckBox {
                        id: checkbClient
                        checked: false
                        text: qsTr("Client")
                        onCheckedChanged: myData.segment.client = checked
                        }

                    CheckBox {
                        id: checkbDC
                        checked: false
                        text: qsTr("Data Center")
                        onCheckedChanged: myData.segment.dc = checked
                    }
                    CheckBox {
                        id: checkbIoT
                        checked: false
                        text: qsTr("IoT")
                        onCheckedChanged: myData.segment.iot = checked
                    }
                }

                Column {
                    id: status
                    width: 125
                    height: 223
                    Label { text: "Status"}
                    CheckBox {
                        id: checkbWApproved
                        checked: false
                        text: qsTr("Win Approved")
                        onCheckedChanged: myData.status.wApproved = checked
                        }

                    CheckBox {
                        id: checkbWSubmitted
                        checked: false
                        text: qsTr("Win Submitted")
                        onCheckedChanged: myData.status.wSubmitted = checked
                    }
                    CheckBox {
                        id: checkbPending
                        checked: false
                        text: qsTr("Pending")
                        onCheckedChanged: myData.status.pending = checked
                    }
                    CheckBox {
                        id: checkbCanceled
                        checked: false
                        text: qsTr("Cancelled")
                        onCheckedChanged: myData.status.cancelled = checked
                    }
                    CheckBox {
                        id: checkbLost
                        checked: false
                        text: qsTr("Lost")
                        onCheckedChanged: myData.status.lost = checked
                    }
                }
            }

            Column {
                spacing: 15

                Column {
                    width: 88
                    height: 90
                    Label { text: "Drive type:"}
                    CheckBox {
                        id: checkbOptane
                        checked: false
                        text: qsTr("Optane")
                        transformOrigin: Item.Center
                        tristate: false
                        onCheckedChanged: myData.ssdType.optane = checked
                    }

                    CheckBox {
                        id: checkbNand
                        checked: false
                        text: qsTr("NAND")
                        onCheckedChanged: myData.ssdType.nand = checked
                    }
                }

                ButtonGroup {
                    id: bgSortBy
                    buttons: cSortBy.children
                    onClicked: myData.sort = checkedButton.text
                }

                Column {
                    id: cSortBy
                    Label {
                        text: "Sort by: "
                    }

                    RadioButton {
                        text:qsTr("Total Price")
                        checked: true
                    }

                    RadioButton {
                        text:qsTr("Quantity")
                    }
                }

                ButtonGroup {
                    id: bgOutputType
                    buttons: colOutputType.children
                    onClicked: myData.outType = checkedButton.text
                }

                Column {
                    id: colOutputType

                    Label {
                        text: "Output type: "
                    }

                    RadioButton {
                        checked :true
                        text:qsTr("Text")
                    }

                    RadioButton {
                        text:qsTr(".xlsx")
                    }

                    RadioButton {
                        text:qsTr(".csv")
                    }
                }

            }
        }

        Row {
            width: categories.width - 30
            height: 50
            spacing: 5

            Text {
                text: qsTr("Top")
                anchors.verticalCenter: parent.verticalCenter
            }

            SpinBox {
                id: sbNumOpIds
                from: 1
                to: 10000
                editable: true
                anchors.verticalCenter: parent.verticalCenter
                onValueModified: myData.numLines = value
                width: parent.width
            }
        }
    }

    Column {
        id: inOut
        x: categories.width + font.pixelSize + 10
        y: 10
        width: parent.width - categories.width - 40
        height: parent.height - 70
        spacing: 10

        Rectangle {
            height: 100
            width: parent.width
            color: "#dedede"

            ScrollView {
                y: 0
                clip: true
                anchors.fill: parent
                width: parent.width
                height: parent.height

                TextEdit {
                    id: tEditXLDocuments
                    width: parent.width
                    height: parent.height
                    text: qsTr("Enter path to the desired .xlsx files, one path per line, from most to least recent")
                    selectByMouse: true
                    onEditingFinished: myData.xlFiles = text
                    font.pointSize: 8
                }
            }
        }

        Rectangle {
            id: recOutput
            color: "#dedede"
            width: parent.width
            height: parent.height * 0.8 - 15

            ScrollView {
                width: parent.width
                height: parent.height
                anchors.fill: parent
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
                clip: true
                font.pointSize: 9

                ListView {
                    id: output
                    model: myModel
                    width: parent.width
                    height: parent.height
                    delegate: TextEdit {
                        text: model.display
                        readOnly: true
                        selectByMouse: true
                    }
                }
            }
        }
    }




    Row {
        id: buttons
        x: inOut.x + inOut.width - 210
        y: inOut.y + inOut.height + 10
        spacing: 10

        Button {
            id: butReset
            text: qsTr("Reset")
            onClicked: {
                comboRegion.currentIndex = 0
                comboVertical.currentIndex = 0
                comboVendor.currentIndex = 0
                comboSolution.currentIndex = 0
                sbNumOpIds.value = 1
                bgSortBy.buttons[0].checked = true
                bgOutputType.buttons[0].checked = true
                checkbOptane.checked = false
                checkbNand.checked = false
                checkbClient.checked = false
                checkbDC.checked = false
                checkbIoT.checked = false
                checkbCanceled.checked = false
                checkbLost.checked = false
                checkbWApproved.checked = false
                checkbWSubmitted.checked = false
                checkbPending.checked = false
                tEditXLDocuments.text = "Enter path to the desired .xlsx files, one path per line, from most to least recent"
            }
        }

        Button {
            id: butSubmit
            text: qsTr("Submit")
            onClicked: {
                bridge.setData(myData.region, myData.vertical, myData.vendor,
                                   myData.solution, myData.sort, myData.outType,
                                   myData.numLines, myData.xlFiles, myData.ssdType.optane,
                                   myData.ssdType.nand, myData.segment.client,
                                   myData.segment.dc, myData.segment.iot, myData.status.wSubmitted,
                                   myData.status.wApproved, myData.status.pending,
                                   myData.status.lost, myData.status.cancelled)
                bridge.printValues()
                bridge.getData()
            }
        }
    }
}
