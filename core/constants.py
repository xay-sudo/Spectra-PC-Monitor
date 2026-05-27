import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# -------------------------------------------------------------
# GLOBAL STYLING SYSTEM (Premium Solid Deep Space Dark Mode)
# -------------------------------------------------------------
QSS_STYLING = """
QMainWindow {
    background-color: #04060a;
}

QWidget#main_container {
    background-color: #080c14;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
}

QWidget#sidebar {
    background-color: #0c0f17;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    border-top-left-radius: 16px;
    border-bottom-left-radius: 16px;
}

QPushButton#mac_close {
    background-color: #ff5f56;
    border: none;
    border-radius: 7px;
    width: 14px;
    height: 14px;
    min-width: 14px;
    min-height: 14px;
    color: #4c0002;
    font-family: "Courier New", monospace;
    font-size: 10px;
    font-weight: bold;
    text-align: center;
    line-height: 14px;
}
QPushButton#mac_close:hover {
    background-color: #ff7e76;
    color: #4c0002;
}

QPushButton#mac_min {
    background-color: #ffbd2e;
    border: none;
    border-radius: 7px;
    width: 14px;
    height: 14px;
    min-width: 14px;
    min-height: 14px;
    color: #5c3e00;
    font-family: "Courier New", monospace;
    font-size: 10px;
    font-weight: bold;
    text-align: center;
    line-height: 14px;
}
QPushButton#mac_min:hover {
    background-color: #ffdb4d;
    color: #5c3e00;
}

QPushButton#mac_max {
    background-color: #27c93f;
    border: none;
    border-radius: 7px;
    width: 14px;
    height: 14px;
    min-width: 14px;
    min-height: 14px;
    color: #004c05;
    font-family: "Courier New", monospace;
    font-size: 9px;
    font-weight: bold;
    text-align: center;
    line-height: 14px;
}
QPushButton#mac_max:hover {
    background-color: #44e55b;
    color: #004c05;
}

QLabel#app_title {
    color: #ffffff;
    font-size: 16px;
    font-weight: 900;
    letter-spacing: 2px;
}

QLabel#app_subtitle {
    color: #00F2FE;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 3px;
}

QFrame#card {
    background-color: #0c0f17;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
}

QFrame#card:hover {
    border: 1px solid rgba(0, 242, 254, 0.2);
    background-color: #121724;
}

QLabel#card_title {
    color: #94a3b8;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
}

QLabel#card_value {
    color: #ffffff;
    font-size: 22px;
    font-weight: 700;
}

QLabel#card_unit {
    color: #64748b;
    font-size: 12px;
    font-weight: 500;
}

QLabel#stat_label {
    color: #94a3b8;
    font-size: 11px;
    font-weight: 500;
}

QLabel#stat_value {
    color: #f1f5f9;
    font-size: 11px;
    font-weight: 600;
}

QProgressBar {
    border: none;
    border-radius: 4px;
    background-color: #121724;
    height: 8px;
    text-align: right;
    color: transparent;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00f2fe, stop:1 #4facfe);
    border-radius: 4px;
}

QScrollBar:vertical {
    border: none;
    background: #04060a;
    width: 6px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #121724;
    min-height: 20px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: #1e293b;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}

QPushButton#action_btn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00F2FE, stop:1 #00ff87);
    color: #040810;
    font-size: 11px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 1px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 10px 24px;
}

QPushButton#action_btn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00ff87, stop:1 #60efff);
    border: 1px solid #ffffff;
}

QPushButton#action_btn:disabled {
    background: #0f131d;
    border: 1px solid rgba(255, 255, 255, 0.03);
    color: #475569;
}

QTableWidget {
    background-color: #080c14;
    border: 1px solid rgba(255, 255, 255, 0.05);
    gridline-color: rgba(255, 255, 255, 0.03);
    border-radius: 8px;
    font-size: 11px;
}

QTableWidget::item {
    padding: 8px;
    background-color: transparent;
}

QTableWidget::item:selected {
    background-color: rgba(0, 242, 254, 0.15);
    color: #ffffff;
}

QHeaderView::section {
    background-color: #0c0f17;
    color: #64748b;
    padding: 8px;
    font-weight: 800;
    font-size: 9px;
    text-transform: uppercase;
    border: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

QLineEdit#search_input {
    background-color: #0c0f17;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    color: #ffffff;
    font-size: 11px;
    font-weight: 500;
    padding: 8px 16px;
}

QLineEdit#search_input:focus {
    border: 1px solid #00F2FE;
}
"""
