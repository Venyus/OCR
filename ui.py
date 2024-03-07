import sys
import fitz
import pytesseract
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QPushButton, QShortcut, QLabel
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QKeySequence
from PyQt5.QtCore import Qt, QRectF
from PIL import Image
import os
import atexit
import pandas as pd
from main import PytorchOcr
from tools.image_processing import Image_Processing

class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.text_sum = []

    def initUI(self):
        self.setGeometry(100, 100, 1800, 1400)
        self.setWindowTitle('PDF Viewer and Text Recognition')

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.pdf_document = None
        self.pdf_page = None
        self.image = None
        self.selection_rect = QRectF()
        self.current_page = 0
        self.drawing = False
        self.start_point = None  # 记录选择框的起始点

        self.view.mousePressEvent = self.mousePressEvent
        self.view.mouseReleaseEvent = self.mouseReleaseEvent
        self.view.mouseMoveEvent = self.mouseMoveEvent

        self.open_button = QPushButton('Open PDF', self)
        self.open_button.clicked.connect(self.openPDF)
        self.open_button.setGeometry(10, 10, 100, 30)

        self.prev_page_button = QPushButton('Previous Page(A)', self)
        self.prev_page_button.clicked.connect(self.previousPage)
        self.prev_page_button.setGeometry(120, 10, 180, 30)
        self.prev_page_button.setEnabled(False)
        shortcut_prev = QShortcut(QKeySequence(Qt.Key_A),self)
        shortcut_prev.activated.connect(self.previousPage)

        self.next_page_button = QPushButton('Next Page(S)', self)
        self.next_page_button.clicked.connect(self.nextPage)
        self.next_page_button.setGeometry(310, 10, 180, 30)
        self.next_page_button.setEnabled(False)
        shortcut_next = QShortcut(QKeySequence(Qt.Key_S),self)
        shortcut_next.activated.connect(self.nextPage)

        self.clear_button = QPushButton('Clear Selection(space)', self)
        self.clear_button.clicked.connect(self.clearSelection)
        self.clear_button.setGeometry(500, 10, 250, 30)
        shortcut_clear = QShortcut(QKeySequence(Qt.Key_Space),self)
        shortcut_clear.activated.connect(self.clearSelection)

        self.delete_button = QPushButton('Delete', self)
        self.delete_button.clicked.connect(self.deleteLast)
        self.delete_button.setGeometry(760, 10, 100, 30)

        self.output_button = QPushButton('Output', self)
        self.output_button.clicked.connect(self.OutputText)
        self.output_button.setGeometry(870, 10, 100, 30)

        self.merge_button = QPushButton('Merge', self)
        self.merge_button.clicked.connect(self.MergeText)
        self.merge_button.setGeometry(980, 10, 100, 30)

        self.show_button = QPushButton('Show', self)
        self.show_button.clicked.connect(self.ShowLast)
        self.show_button.setGeometry(1090, 10, 100, 30)

        self.page_info_label = QLabel(self)
        self.page_info_label.setGeometry(1320, 10, 210, 30)

        self.show()

    def openPDF(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filePath, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        
        self.file_name = os.path.basename(filePath).replace('.pdf','')

        if filePath:
            self.pdf_document = fitz.open(filePath)
            self.loadPage(0)

    def loadPage(self, page_num):
        if self.pdf_document is not None:
            if 0 <= page_num < len(self.pdf_document):
                self.pdf_page = self.pdf_document.load_page(page_num)
                self.current_page = page_num
                self.prev_page_button.setEnabled(page_num > 0)
                self.next_page_button.setEnabled(page_num < len(self.pdf_document) - 1)
                self.renderPage()

            # 更新当前页码和总页数标签
            page_info_text = f"Page {self.current_page + 1} of {len(self.pdf_document)}"
            self.page_info_label.setText(page_info_text)

    def renderPage(self):
        pdf_image = self.pdf_page.get_pixmap(dpi = 180 )
        pdf_image.save("temp.png")
        self.image = QImage("temp.png")

        self.scene.clear()
        pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        self.scene.addItem(pixmap_item)

    def previousPage(self):
        self.loadPage(self.current_page - 1)

    def nextPage(self):
        self.loadPage(self.current_page + 1)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = self.view.mapToScene(event.pos())
            self.drawing = True
            self.update()

    def mouseMoveEvent(self, event):
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_point = self.view.mapToScene(event.pos())
            self.drawing = False
            self.update()

            # 计算出基于两次点击的对角线的矩形
            self.selection_rect = QRectF(self.start_point, self.end_point).normalized()
            self.extractTextFromSelection()

    def paintEvent(self, event):
        if self.selection_rect.isValid():
            painter = QPainter(self.image)
            painter.setPen(QPen(QColor(255, 0, 0), 1, Qt.SolidLine))
            painter.drawRect(self.selection_rect)
            painter.end()

            pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
            self.scene.clear()
            self.scene.addItem(pixmap_item)

    def clearSelection(self):
        self.selection_rect = QRectF()  # 清除选择框
        self.renderPage()  # 重新渲染页面以去除选择框
        self.update()

    def deleteLast(self):
        print('%%%%bef del: ', len(self.text_sum))
        self.text_sum = self.text_sum[:-1]
        print('%%%%aft del: ', len(self.text_sum))

    def MergeText(self):
        print('%%%%bef merge: ', len(self.text_sum))
        temp_text = self.text_sum[-2] + self.text_sum[-1]
        self.text_sum = self.text_sum[:-2]
        self.text_sum.append(temp_text)
        print('%%%%aft merge:', len(self.text_sum))
        print('%%%%merged text: ', temp_text)

    def extractTextFromSelection(self):
        try:
            if self.selection_rect.isValid():
                x = int(self.selection_rect.left())
                y = int(self.selection_rect.top())
                width = int(self.selection_rect.width())
                height = int(self.selection_rect.height())

                selection_image = self.image.copy(x, y, width, height)

                # 将选择的图像对象转换为Pillow的Image对象
                selection_pil_image = Image.fromqimage(selection_image)

                grayed_image_list = image_processed.gray_scale_conver(selection_pil_image, is_save = False)[1]
                split_images = image_processed.split_image(grayed_image_list, is_save = True)
                
                selection_text = ''
                for split_image in split_images:
                    selection_text += ' ' +  recognizer.recognize(split_image)

                print("%%%%Selected Text:", len(self.text_sum)+1)
                print(selection_text)
                self.text_sum.append(selection_text.replace('\n',' '))

        except Exception as e:
            print(f"%%%%Error during text extraction: {str(e)}")

    def OutputText(self):
        df_output = pd.DataFrame(self.text_sum, columns = ['Contents'])
        print('test')
        df_output.to_excel(self.file_name + '.xlsx', index = False)
        print('end')

    def ShowLast(self):
        print('%%%%the last content: ')
        print(self.text_sum[-1])

if __name__ == '__main__':
    '''load the model'''
    model_name = 'CRNN-CAPSTONE_51_980.pth'
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crnn_saved_models', model_name)
    recognizer = PytorchOcr(model_path)

    '''image processing instance'''
    image_processed = Image_Processing()
    
    try:
        app = QApplication(sys.argv)
        viewer = PDFViewer()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {str(e)}")