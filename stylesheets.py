ENABLED_STYLESHEET = """
    QPushButton {
        border: 1px solid #007a94;
        border-radius: 6px;
        color:#ffffff;
        background-color: #007a94;
        min-width: 80px;
        }
    QPushButton:pressed {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                  stop: 0 #008aa6, stop: 1 #008aa6);
        }

    QPushButton:flat {
        border: none;
        }
"""
DISABLED_STYLESHEET = """
    QPushButton {
       border: 1px solid #808080;
       border-radius: 6px;
       color:#ffffff;
       background-color: #808080;
       min-width: 80px;
       }
   QPushButton:flat {
       border: none;
       }

"""
NOT_AVAILABLE_STYLESHEET = """
    QPushButton {
       border: 1px solid #808080;
       border-radius: 6px;
       color:#444444;
       background-color: #808080;
       min-width: 80px;
       transparency:0.5;
       }
   QPushButton:flat {
       border: none;
       }

"""