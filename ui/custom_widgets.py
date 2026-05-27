import math

from PyQt6.QtCore import Qt, QTimer, QPointF, QRectF, QSize
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QBrush, QLinearGradient, QRadialGradient, QPainterPath, QIcon, QPolygonF
from PyQt6.QtWidgets import QPushButton, QWidget

# -------------------------------------------------------------
# CUSTOM SIDEBAR BUTTON (Native Vector Drawing)
# -------------------------------------------------------------
class SidebarButton(QPushButton):
    def __init__(self, text, icon_type, parent=None):
        super().__init__(text, parent)
        self.icon_type = icon_type
        self.active = False
        self.setCheckable(True)
        self.setMinimumHeight(46)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.hovered = False
        
    def setActive(self, state):
        self.active = state
        self.setChecked(state)
        self.update()
        
    def enterEvent(self, event):
        self.hovered = True
        self.update()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        super().leaveEvent(event)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        bg_color = QColor(0, 0, 0, 0)
        border_left = False
        text_color = QColor("#64748b")
        icon_color = QColor("#64748b")
        
        if self.active:
            bg_color = QColor(17, 24, 39, 220)
            text_color = QColor("#ffffff")
            icon_color = QColor("#00F2FE")
            border_left = True
        elif self.hovered:
            bg_color = QColor(17, 24, 39, 100)
            text_color = QColor("#f8fafc")
            icon_color = QColor("#00F2FE")
            
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(QRectF(8, 2, width - 16, height - 4), 8, 8)
        
        if border_left:
            grad = QLinearGradient(0, 4, 0, height - 4)
            grad.setColorAt(0.0, QColor("#00F2FE"))
            grad.setColorAt(1.0, QColor("#7F00FF"))
            painter.setBrush(grad)
            painter.drawRoundedRect(QRectF(8, 8, 3, height - 16), 1.5, 1.5)
            
        icon_size = 18
        ix = 22
        iy = (height - icon_size) / 2
        painter.save()
        painter.translate(ix, iy)
        
        pen_icon = QPen(icon_color)
        pen_icon.setWidthF(1.8)
        pen_icon.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen_icon.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen_icon)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        if self.icon_type == "dashboard":
            painter.drawRect(QRectF(0, 0, 7, 7))
            painter.drawRect(QRectF(10, 0, 7, 7))
            painter.drawRect(QRectF(0, 10, 7, 7))
            painter.drawRect(QRectF(10, 10, 7, 7))
        elif self.icon_type == "cpu":
            painter.drawRect(QRectF(3, 3, 12, 12))
            painter.drawRect(QRectF(6, 6, 6, 6))
            # top/bottom pins
            painter.drawLine(7, 0, 7, 3)
            painter.drawLine(11, 0, 11, 3)
            painter.drawLine(7, 15, 7, 18)
            painter.drawLine(11, 15, 11, 18)
            # left/right pins
            painter.drawLine(0, 7, 3, 7)
            painter.drawLine(0, 11, 3, 11)
            painter.drawLine(15, 7, 18, 7)
            painter.drawLine(15, 11, 18, 11)
        elif self.icon_type == "memory":
            painter.drawRect(QRectF(0, 3, 18, 12))
            painter.drawLine(4, 3, 4, 6)
            painter.drawLine(8, 3, 8, 6)
            painter.drawLine(12, 3, 12, 6)
            painter.drawLine(16, 3, 16, 6)
            # bottom connector notches
            painter.drawLine(2, 15, 2, 17)
            painter.drawLine(5, 15, 5, 17)
            painter.drawLine(8, 15, 8, 17)
            painter.drawLine(11, 15, 11, 17)
            painter.drawLine(14, 15, 14, 17)
            painter.drawLine(16, 15, 16, 17)
        elif self.icon_type == "gpu":
            painter.drawRect(QRectF(0, 2, 18, 12))
            painter.drawEllipse(QRectF(6, 4, 8, 8))
            painter.drawLine(2, 14, 6, 16)
            painter.drawLine(10, 14, 12, 14)
        elif self.icon_type == "network":
            painter.drawEllipse(QRectF(0, 0, 18, 18))
            painter.drawEllipse(QRectF(5, 0, 8, 18))
            painter.drawLine(0, 9, 18, 9)
        elif self.icon_type == "energy":
            poly = QPolygonF([
                QPointF(11, 0),
                QPointF(3, 9),
                QPointF(8, 9),
                QPointF(6, 18),
                QPointF(15, 8),
                QPointF(9, 8),
                QPointF(11, 0)
            ])
            painter.drawPolygon(poly)
        elif self.icon_type == "processes":
            painter.drawRect(QRectF(0, 1, 18, 3))
            painter.drawRect(QRectF(0, 7, 18, 3))
            painter.drawRect(QRectF(0, 13, 18, 3))
            painter.drawLine(3, 2, 3, 2)
            painter.drawLine(3, 8, 3, 8)
            painter.drawLine(3, 14, 3, 14)
        elif self.icon_type == "tuneup":
            painter.drawEllipse(QRectF(4, 4, 10, 10))
            painter.drawLine(9, 1, 9, 4)
            painter.drawLine(9, 14, 9, 17)
            painter.drawLine(1, 9, 4, 9)
            painter.drawLine(14, 9, 17, 9)
        elif self.icon_type == "settings":
            painter.drawRect(QRectF(1, 3, 16, 2))
            painter.drawRect(QRectF(1, 9, 16, 2))
            painter.drawRect(QRectF(1, 15, 16, 2))
            painter.drawRect(QRectF(4, 1, 3, 6))
            painter.drawRect(QRectF(11, 7, 3, 6))
            painter.drawRect(QRectF(6, 13, 3, 6))
            
        painter.restore()
        
        painter.setPen(text_color)
        font = QFont("Inter", 10, QFont.Weight.Medium)
        painter.setFont(font)
        painter.drawText(QRectF(52, 0, width - 60, height), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.text())


# -------------------------------------------------------------
# CUSTOM CIRCULAR GAUGE WIDGET
# -------------------------------------------------------------
class CircularGauge(QWidget):
    def __init__(self, parent=None, size=140, title="CPU", color=QColor("#00F2FE"), suffix="%"):
        super().__init__(parent)
        self.setMinimumSize(size, size)
        self.setMaximumSize(size, size)
        self.value = 0.0
        self.target_value = 0.0
        self.title = title
        self.color = color
        self.suffix = suffix
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.animate)
        self.anim_timer.start(16)  # ~60 fps
        
    def setValue(self, val):
        self.target_value = float(val)
        
    def animate(self):
        if abs(self.value - self.target_value) > 0.05:
            self.value += (self.target_value - self.value) * 0.12
            self.update()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        side = min(width, height)
        
        cx = width / 2.0
        cy = height / 2.0
        
        outer_radius = (side * 0.94) / 2.0
        inner_radius = (side * 0.78) / 2.0
        stroke_width = outer_radius - inner_radius
        
        # Track arc (darker blue-slate background)
        pen_bg = QPen(QColor(30, 41, 59, 120))
        pen_bg.setWidthF(stroke_width)
        pen_bg.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_bg)
        
        start_angle = -225 * 16  # start at bottom left
        span_angle = -270 * 16  # sweep clockwise 270 degrees
        
        rect = QRectF(cx - outer_radius + stroke_width/2.0, 
                      cy - outer_radius + stroke_width/2.0, 
                      outer_radius * 2.0 - stroke_width, 
                      outer_radius * 2.0 - stroke_width)
        painter.drawArc(rect, start_angle, span_angle)
        
        # Value arc
        if self.value > 0:
            gradient = QLinearGradient(0, 0, width, height)
            gradient.setColorAt(0.0, self.color)
            hue, sat, val_c, alpha = self.color.getHsv()
            end_color = QColor.fromHsv((hue + 35) % 360, sat, val_c)
            gradient.setColorAt(1.0, end_color)
            
            pen_fg = QPen(QBrush(gradient), stroke_width)
            pen_fg.setWidthF(stroke_width)
            pen_fg.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen_fg)
            
            val_span = -int(270 * (self.value / 100.0) * 16)
            painter.drawArc(rect, start_angle, val_span)
            
        # Draw central text value
        painter.setPen(QColor("#ffffff"))
        font_val = QFont("Inter", int(side * 0.16), QFont.Weight.Bold)
        painter.setFont(font_val)
        val_str = f"{int(round(self.value))}{self.suffix}"
        
        val_rect = QRectF(cx - inner_radius, cy - inner_radius * 0.45, inner_radius * 2.0, inner_radius * 0.8)
        painter.drawText(val_rect, Qt.AlignmentFlag.AlignCenter, val_str)
        
        # Draw small description label below number
        painter.setPen(QColor("#64748b"))
        font_title = QFont("Inter", int(side * 0.08), QFont.Weight.Bold)
        painter.setFont(font_title)
        title_rect = QRectF(cx - inner_radius, cy + inner_radius * 0.25, inner_radius * 2.0, inner_radius * 0.5)
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignCenter, self.title.upper())


# -------------------------------------------------------------
# CUSTOM REAL-TIME GRAPH WIDGET
# -------------------------------------------------------------
class RealTimeGraph(QWidget):
    def __init__(self, parent=None, max_points=60, title="Usage History", color=QColor("#00F2FE")):
        super().__init__(parent)
        self.setMinimumHeight(170)
        self.max_points = max_points
        self.data = [0.0] * max_points
        self.color = color
        self.title = title
        
    def addValue(self, val):
        self.data.pop(0)
        self.data.append(float(val))
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Panel outer card
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(17, 24, 39, 140))
        painter.drawRoundedRect(QRectF(0, 0, width, height), 12, 12)
        
        left_m = 45.0
        right_m = 20.0
        top_m = 35.0
        bottom_m = 25.0
        
        graph_w = width - left_m - right_m
        graph_h = height - top_m - bottom_m
        
        # Grid lines and Y labels (100, 75, 50, 25, 0)
        pen_grid = QPen(QColor(255, 255, 255, 12))
        pen_grid.setStyle(Qt.PenStyle.DashLine)
        pen_grid.setWidthF(1)
        painter.setPen(pen_grid)
        
        font_lbl = QFont("Inter", 8, QFont.Weight.Medium)
        painter.setFont(font_lbl)
        
        for i in range(5):
            y_val = 100 - i * 25
            y_pos = top_m + (i * 0.25) * graph_h
            
            painter.drawLine(QPointF(left_m, y_pos), QPointF(width - right_m, y_pos))
            
            # Label
            painter.setPen(QColor("#64748b"))
            painter.drawText(QRectF(5, y_pos - 8, left_m - 10, 16), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, f"{y_val}%")
            painter.setPen(pen_grid)
            
        if len(self.data) < 2:
            return
            
        pts = []
        for idx, val in enumerate(self.data):
            x = left_m + (idx / (self.max_points - 1)) * graph_w
            val = max(0.0, min(100.0, val))
            y = top_m + (1.0 - val / 100.0) * graph_h
            pts.append(QPointF(x, y))
            
        # 1. Fill gradient region under curve
        path_fill = QPainterPath()
        path_fill.moveTo(left_m, top_m + graph_h)
        for pt in pts:
            path_fill.lineTo(pt)
        path_fill.lineTo(width - right_m, top_m + graph_h)
        path_fill.closeSubpath()
        
        area_grad = QLinearGradient(0, top_m, 0, top_m + graph_h)
        c_from = QColor(self.color.red(), self.color.green(), self.color.blue(), 55)
        c_to = QColor(self.color.red(), self.color.green(), self.color.blue(), 0)
        area_grad.setColorAt(0.0, c_from)
        area_grad.setColorAt(1.0, c_to)
        
        painter.setBrush(area_grad)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path_fill)
        
        # 2. Draw line path with bezier curvature
        pen_line = QPen(self.color)
        pen_line.setWidthF(2.2)
        painter.setPen(pen_line)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        path_line = QPainterPath()
        path_line.moveTo(pts[0])
        for i in range(1, len(pts)):
            xc = (pts[i-1].x() + pts[i].x()) / 2.0
            yc = (pts[i-1].y() + pts[i].y()) / 2.0
            path_line.quadTo(pts[i-1], QPointF(xc, yc))
        path_line.lineTo(pts[-1])
        painter.drawPath(path_line)
        
        # Draw Title
        painter.setPen(QColor("#f8fafc"))
        font_title = QFont("Inter", 10, QFont.Weight.Bold)
        painter.setFont(font_title)
        painter.drawText(QRectF(left_m, 8, graph_w, 20), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.title.upper())


# -------------------------------------------------------------
# CUSTOM SPEED DIAL FOR SPEEDTEST
# -------------------------------------------------------------
class SpeedGauge(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(220, 220)
        self.setMaximumSize(220, 220)
        self.speed = 0.0
        self.target_speed = 0.0
        self.phase = "READY"
        self.color = QColor("#00ff87")
        self.max_scale = 100.0
        
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.animate)
        self.anim_timer.start(16)
        
    def setSpeed(self, speed):
        self.target_speed = float(speed)
        if self.target_speed > self.max_scale:
            if self.target_speed <= 250:
                self.max_scale = 250.0
            elif self.target_speed <= 500:
                self.max_scale = 500.0
            else:
                self.max_scale = 1000.0
                
    def setPhase(self, phase, color):
        self.phase = phase
        self.color = color
        if phase == "READY":
            self.target_speed = 0.0
            self.max_scale = 100.0
        self.update()
        
    def animate(self):
        if abs(self.speed - self.target_speed) > 0.05:
            self.speed += (self.target_speed - self.speed) * 0.1
            self.update()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        side = min(width, height)
        
        cx = width / 2.0
        cy = height / 2.0
        
        outer_radius = (side * 0.94) / 2.0
        inner_radius = (side * 0.78) / 2.0
        stroke_width = outer_radius - inner_radius
        
        # Track arc background
        pen_bg = QPen(QColor(30, 41, 59, 100))
        pen_bg.setWidthF(stroke_width)
        pen_bg.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_bg)
        
        start_angle = -225 * 16
        span_angle = -270 * 16
        rect = QRectF(cx - outer_radius + stroke_width/2.0, 
                      cy - outer_radius + stroke_width/2.0, 
                      outer_radius * 2.0 - stroke_width, 
                      outer_radius * 2.0 - stroke_width)
        painter.drawArc(rect, start_angle, span_angle)
        
        # Draw radial ticks
        pen_tick = QPen(QColor(255, 255, 255, 25))
        pen_tick.setWidthF(1.5)
        painter.setPen(pen_tick)
        
        for i in range(11):
            angle = 135 - i * 27
            rad = math.radians(angle)
            
            x1 = cx + (inner_radius + 2) * math.cos(rad)
            y1 = cy - (inner_radius + 2) * math.sin(rad)
            x2 = cx + (outer_radius - 2) * math.cos(rad)
            y2 = cy - (outer_radius - 2) * math.sin(rad)
            
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
            
            # Draw scale numbers
            val = int((i / 10.0) * self.max_scale)
            xt = cx + (inner_radius - 14) * math.cos(rad)
            yt = cy - (inner_radius - 14) * math.sin(rad)
            
            painter.setPen(QColor("#64748b"))
            font_t = QFont("Inter", 8, QFont.Weight.Medium)
            painter.setFont(font_t)
            painter.drawText(QRectF(xt - 15, yt - 8, 30, 16), Qt.AlignmentFlag.AlignCenter, str(val))
            painter.setPen(pen_tick)
            
        # Value Sweep Arc
        if self.speed > 0:
            gradient = QLinearGradient(0, 0, width, height)
            gradient.setColorAt(0.0, self.color)
            hue, sat, val_c, alpha = self.color.getHsv()
            end_color = QColor.fromHsv((hue + 45) % 360, sat, val_c)
            gradient.setColorAt(1.0, end_color)
            
            pen_fg = QPen(QBrush(gradient), stroke_width)
            pen_fg.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen_fg)
            
            val_span = -int(270 * (self.speed / self.max_scale) * 16)
            painter.drawArc(rect, start_angle, val_span)
            
        # central value numbers
        painter.setPen(QColor("#ffffff"))
        font_val = QFont("Inter", 24, QFont.Weight.ExtraBold)
        painter.setFont(font_val)
        speed_str = f"{self.speed:.1f}" if self.speed > 0 else "0.0"
        painter.drawText(QRectF(cx - 70, cy - 30, 140, 36), Qt.AlignmentFlag.AlignCenter, speed_str)
        
        # Sub-title "Mbps"
        painter.setPen(QColor("#64748b"))
        font_sub = QFont("Inter", 10, QFont.Weight.Bold)
        painter.setFont(font_sub)
        painter.drawText(QRectF(cx - 50, cy + 10, 100, 20), Qt.AlignmentFlag.AlignCenter, "Mbps")
        
        # Active speedtest phase
        painter.setPen(self.color)
        font_ph = QFont("Inter", 9, QFont.Weight.Bold)
        painter.setFont(font_ph)
        painter.drawText(QRectF(cx - 80, cy + 32, 160, 20), Qt.AlignmentFlag.AlignCenter, self.phase.upper())
