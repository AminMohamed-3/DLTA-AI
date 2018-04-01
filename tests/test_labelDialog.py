try:
    from PyQt5 import QtCore
    from PyQt5 import QtWidgets
except ImportError:
    from PyQt4 import QtCore
    from PyQt4 import QtGui as QtWidgets

from labelme import labelDialog


def test_LabelQLineEdit(qtbot):
    list_widget = QtWidgets.QListWidget()
    list_widget.addItems([
        'cat',
        'dog',
        'person',
    ])
    widget = labelDialog.LabelQLineEdit()
    widget.setListWidget(list_widget)
    qtbot.addWidget(widget)

    # key press to navigate in label list
    item = widget.list_widget.findItems('cat', QtCore.Qt.MatchExactly)[0]
    widget.list_widget.setCurrentItem(item)
    assert widget.list_widget.currentItem().text() == 'cat'
    qtbot.keyPress(widget, QtCore.Qt.Key_Down)
    assert widget.list_widget.currentItem().text() == 'dog'

    # key press to enter label
    qtbot.keyPress(widget, QtCore.Qt.Key_P)
    qtbot.keyPress(widget, QtCore.Qt.Key_E)
    qtbot.keyPress(widget, QtCore.Qt.Key_R)
    qtbot.keyPress(widget, QtCore.Qt.Key_S)
    qtbot.keyPress(widget, QtCore.Qt.Key_O)
    qtbot.keyPress(widget, QtCore.Qt.Key_N)
    assert widget.text() == 'person'


def test_LabelDialog_addLabelHistory(qtbot):
    labels = ['cat', 'dog', 'person']
    widget = labelDialog.LabelDialog(labels=labels, sort_labels=True)
    qtbot.addWidget(widget)

    widget.addLabelHistory('bicycle')
    assert widget.labelList.count() == 4
    widget.addLabelHistory('bicycle')
    assert widget.labelList.count() == 4
    item = widget.labelList.item(0)
    assert item.text() == 'bicycle'


def test_LabelDialog_popUp(qtbot):
    labels = ['cat', 'dog', 'person']
    widget = labelDialog.LabelDialog(labels=labels, sort_labels=True)
    qtbot.addWidget(widget)

    # popUp(text='cat')

    def interact():
        qtbot.keyClick(widget.edit, QtCore.Qt.Key_P)  # enter 'p' for 'person'
        qtbot.keyClick(widget.edit, QtCore.Qt.Key_Enter)
        qtbot.keyClick(widget.edit, QtCore.Qt.Key_Enter)

    QtCore.QTimer.singleShot(500, interact)
    text = widget.popUp('cat')
    assert text == 'person'

    # popUp()

    def interact():
        qtbot.keyClick(widget.edit, QtCore.Qt.Key_Enter)
        qtbot.keyClick(widget.edit, QtCore.Qt.Key_Enter)

    QtCore.QTimer.singleShot(500, interact)
    text = widget.popUp()
    assert text == 'person'

    # popUp() + key_Up

    def interact():
        qtbot.keyClick(widget.edit, QtCore.Qt.Key_Up)  # 'person' -> 'dog'
        qtbot.keyClick(widget.edit, QtCore.Qt.Key_Enter)
        qtbot.keyClick(widget.edit, QtCore.Qt.Key_Enter)

    QtCore.QTimer.singleShot(500, interact)
    text = widget.popUp()
    assert text == 'dog'
