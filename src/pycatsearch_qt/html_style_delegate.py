from qtpy.QtCore import QModelIndex, QObject, QPersistentModelIndex, QRect, QSize
from qtpy.QtGui import QAbstractTextDocumentLayout, QPainter, QPalette, QTextDocument
from qtpy.QtWidgets import QApplication, QStyle, QStyleOptionViewItem, QStyledItemDelegate

from .utils import the

__all__ = ["HTMLDelegate"]



class HTMLDelegate(QStyledItemDelegate):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._doc: QTextDocument = QTextDocument(self)

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        self.initStyleOption(option, index)
        style: QStyle | None = option.widget.style() if option.widget else QApplication.style()
        if style is None:
            raise RuntimeError("Failed to get style")
        with the(self._doc) as doc:
            doc.clear()
            doc.setHtml(option.text)
            option.text = ""
            style.drawControl(QStyle.ControlElement.CE_ItemViewItem, option, painter)
            ctx: QAbstractTextDocumentLayout.PaintContext = QAbstractTextDocumentLayout.PaintContext()
            text_rect: QRect = style.subElementRect(QStyle.SubElement.SE_ItemViewItemText, option)
            painter.save()
            if option.state & QStyle.StateFlag.State_Selected:
                painter.fillRect(option.rect, option.palette.highlight())
                ctx.palette.setBrush(QPalette.ColorRole.Text, option.palette.highlightedText())
            painter.translate(text_rect.topLeft())
            painter.setClipRect(option.rect.translated(-text_rect.topLeft()))
            painter.translate(0, 0.5 * (option.rect.height() - doc.size().height()))
            doc.documentLayout().draw(painter, ctx)
            painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> QSize:
        options: QStyleOptionViewItem = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        with the(self._doc) as doc:
            doc.clear()
            doc.setHtml(options.text)
            doc.setTextWidth(options.rect.width())
            return QSize(
                round(doc.idealWidth()),
                round(QTextDocument().size().height()),
            )
