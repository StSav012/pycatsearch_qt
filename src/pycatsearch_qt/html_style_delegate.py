from qtpy.QtCore import QModelIndex, QPersistentModelIndex, QRect, QSize
from qtpy.QtGui import QAbstractTextDocumentLayout, QPainter, QPalette, QTextDocument
from qtpy.QtWidgets import QApplication, QStyle, QStyleOptionViewItem, QStyledItemDelegate

__all__ = ["HTMLDelegate"]


class HTMLDelegate(QStyledItemDelegate):
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
        doc: QTextDocument = QTextDocument(self)
        doc.setHtml(option.text)
        option.text = ""
        style.drawControl(QStyle.ControlElement.CE_ItemViewItem, option, painter)
        ctx: QAbstractTextDocumentLayout.PaintContext = QAbstractTextDocumentLayout.PaintContext()
        if option.state & QStyle.StateFlag.State_Selected:
            ctx.palette.setBrush(QPalette.ColorRole.Text, option.palette.highlightedText())
        text_rect: QRect = style.subElementRect(QStyle.SubElement.SE_ItemViewItemText, option)
        painter.save()
        painter.translate(text_rect.topLeft())
        painter.setClipRect(option.rect.translated(-text_rect.topLeft()))
        painter.translate(0, 0.5 * (option.rect.height() - doc.size().height()))
        doc.documentLayout().draw(painter, ctx)
        painter.restore()
        doc.deleteLater()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> QSize:
        options: QStyleOptionViewItem = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        doc: QTextDocument = QTextDocument(self)
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        size: QSize = QSize(
            round(doc.idealWidth()),
            round(QTextDocument().size().height()),
        )
        doc.deleteLater()
        return size
