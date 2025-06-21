import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import yt_dlp
import requests

class YouTubeThumbnailDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Thumbnail Downloader")
        self.setMinimumSize(600, 400)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 타이틀 (가장 위로 이동)
        self.title_label = QLabel("YouTube 썸네일 다운로더")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.insertWidget(0, self.title_label)
        
        # URL input area
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("YouTube URL을 입력하세요")
        url_layout.addWidget(self.url_input)
        
        # Download button
        self.download_btn = QPushButton("썸네일 가져오기")
        self.download_btn.clicked.connect(self.download_thumbnail)
        url_layout.addWidget(self.download_btn)
        layout.addLayout(url_layout)
        
        # Image preview area
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(200)
        layout.addWidget(self.image_label)
        
        # Save button
        self.save_btn = QPushButton("썸네일 저장")
        self.save_btn.clicked.connect(self.save_thumbnail)
        self.save_btn.setEnabled(False)
        layout.addWidget(self.save_btn)
        
        # Download video button
        self.video_btn = QPushButton("다운로드")
        self.video_btn.setMinimumHeight(32)
        self.video_btn.clicked.connect(self.download_video)
        layout.addWidget(self.video_btn)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.thumbnail_url = None
        self.like_count = None
        self.comment_count = None
        self.view_count = None
        # 좋아요/댓글/조회수 라벨 추가
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        self.setStyleSheet("""
            QMainWindow {
                background: #f7f7f7;
            }
            QLabel#TitleLabel {
                font-size: 26px;
                font-weight: bold;
                color: #333;
                margin-bottom: 18px;
            }
            QLineEdit {
                padding: 8px;
                font-size: 15px;
                border: 1.5px solid #bbb;
                border-radius: 6px;
                background: #fff;
            }
            QPushButton {
                background: #1976d2;
                color: #fff;
                font-size: 15px;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 18px;
                margin-left: 8px;
            }
            QPushButton:disabled {
                background: #b0b0b0;
                color: #eee;
            }
            QLabel#ThumbLabel {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background: #fff;
                margin: 18px 0 10px 0;
            }
            QLabel#InfoLabel {
                font-size: 15px;
                color: #1976d2;
                margin-top: 8px;
            }
            QLabel#StatusLabel {
                font-size: 13px;
                color: #d32f2f;
                margin-top: 8px;
            }
        """)
        self.url_input.setMinimumHeight(32)
        self.download_btn.setMinimumHeight(32)
        self.image_label.setObjectName("ThumbLabel")
        self.image_label.setFixedHeight(220)
        self.info_label.setObjectName("InfoLabel")
        self.status_label.setObjectName("StatusLabel")

    def download_thumbnail(self):
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText("URL을 입력해주세요!")
            return
        try:
            ydl_opts = {
                'quiet': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'thumbnail' in info:
                    self.thumbnail_url = info['thumbnail']
                    self.like_count = info.get('like_count', '알 수 없음')
                    self.comment_count = info.get('comment_count', '알 수 없음')
                    self.view_count = info.get('view_count', '알 수 없음')
                    # 썸네일 이미지 다운로드 (requests 사용)
                    response = requests.get(self.thumbnail_url)
                    if response.status_code == 200:
                        pixmap = QPixmap()
                        pixmap.loadFromData(response.content)
                        scaled_pixmap = pixmap.scaled(self.image_label.size(), 
                                                      Qt.AspectRatioMode.KeepAspectRatio,
                                                      Qt.TransformationMode.SmoothTransformation)
                        self.image_label.setPixmap(scaled_pixmap)
                        self.save_btn.setEnabled(True)
                        self.status_label.setText("썸네일을 성공적으로 가져왔습니다!")
                        self.info_label.setText(f"조회수: {self.view_count} / 좋아요: {self.like_count} / 댓글: {self.comment_count}")
                    else:
                        self.status_label.setText("썸네일 이미지를 불러올 수 없습니다.")
                        self.info_label.setText("")
                else:
                    self.status_label.setText("썸네일을 찾을 수 없습니다.")
                    self.info_label.setText("")
        except Exception as e:
            self.status_label.setText(f"에러 발생: {str(e)}")
            self.info_label.setText("")

    def save_thumbnail(self):
        if not self.thumbnail_url:
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "썸네일 저장",
            os.path.expanduser("~/Downloads/thumbnail.jpg"),
            "Images (*.jpg *.jpeg *.png)"
        )
        
        if file_name:
            try:
                # 썸네일 이미지 저장 (requests 사용)
                response = requests.get(self.thumbnail_url)
                if response.status_code == 200:
                    with open(file_name, 'wb') as f:
                        f.write(response.content)
                    self.status_label.setText("썸네일이 성공적으로 저장되었습니다!")
                else:
                    self.status_label.setText("이미지 저장 실패: 다운로드 오류")
            except Exception as e:
                self.status_label.setText(f"저장 중 에러 발생: {str(e)}")

    def download_video(self):
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText("URL을 입력해주세요!")
            return
        self.status_label.setText("영상 다운로드 중...")
        QApplication.processEvents()
        try:
            ydl_opts = {
                'ffmpeg_location': r'C:/Users/USER/ffmpeg-7.1.1-full_build/bin',
                'outtmpl': os.path.join(os.getcwd(), '%(title)s.%(ext)s'),
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'quiet': True,
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.setText("영상 다운로드 완료!")
        except Exception as e:
            self.status_label.setText(f"다운로드 에러: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = YouTubeThumbnailDownloader()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()