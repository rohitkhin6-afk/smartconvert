"""Application-wide Qt style sheet."""

APP_STYLE = """
QWidget {
    color: #e8ecf7;
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 14px;
}
QMainWindow, QWidget#AppRoot, QScrollArea, QWidget#ScrollContent {
    background: #0b0d14;
}
QScrollArea { border: none; }
QScrollBar:vertical {
    width: 8px; background: transparent; margin: 4px 1px;
}
QScrollBar::handle:vertical { background: #34394d; border-radius: 4px; min-height: 28px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

QFrame#Sidebar { background: #11141e; border-right: 1px solid #232738; }
QLabel#LogoMark {
    background: #7357ff; color: white; border-radius: 11px;
    font-size: 19px; font-weight: 800;
}
QLabel#LogoTitle { color: #ffffff; font-size: 20px; font-weight: 750; }
QLabel#LogoCaption, QLabel#SidebarFooter { color: #72798f; font-size: 11px; }
QPushButton#NavButton {
    background: transparent; border: none; border-radius: 10px;
    color: #949bb0; text-align: left; padding: 12px 16px;
    font-size: 13px; font-weight: 600;
}
QPushButton#NavButton:hover { background: #1b1e2c; color: #f5f6fb; }
QPushButton#NavButton[active="true"] {
    background: #24213c; color: #bcaeff; border-left: 3px solid #8067ff;
}

QLabel#Eyebrow { color: #8f7cff; font-size: 11px; font-weight: 800; letter-spacing: 2px; }
QLabel#PageTitle { color: #ffffff; font-size: 31px; font-weight: 800; }
QLabel#PageSubtitle { color: #8b91a5; font-size: 14px; }
QLabel#SecurityPill {
    background: #151a26; color: #8f97ac; border: 1px solid #272c3d;
    border-radius: 14px; padding: 7px 12px; font-size: 11px; font-weight: 600;
}

QFrame#UploadCard {
    background: #131722; border: 2px dashed #4b426f; border-radius: 20px;
}
QFrame#UploadCard[dragActive="true"] { background: #1c1930; border-color: #8c75ff; }
QLabel#UploadIcon {
    background: #292344; color: #aa98ff; border: 1px solid #463b71;
    border-radius: 30px; font-size: 29px; font-weight: 500;
}
QLabel#UploadTitle { color: #f7f7fb; font-size: 20px; font-weight: 750; }
QLabel#MutedText { color: #777f95; font-size: 12px; }
QLabel#FileName { color: #ffffff; font-size: 17px; font-weight: 700; }
QLabel#FileMeta { color: #9da4b8; font-size: 12px; }
QLabel#ErrorLabel {
    background: #321c29; color: #ff9ab5; border: 1px solid #633046;
    border-radius: 8px; padding: 8px 13px; font-size: 12px;
}
QPushButton#BrowseButton {
    background: #755cff; color: white; border: none; border-radius: 10px;
    padding: 12px 25px; font-size: 13px; font-weight: 750;
}
QPushButton#BrowseButton:hover { background: #8871ff; }
QPushButton#BrowseButton:pressed { background: #654de7; }
QLabel#FormatChip {
    color: #8f96aa; background: #1c202d; border: 1px solid #2b3041;
    border-radius: 7px; padding: 5px 9px; font-size: 10px; font-weight: 700;
}

QLabel#SectionTitle { color: #f5f6fa; font-size: 17px; font-weight: 750; }
QLabel#SectionHint { color: #737b90; font-size: 12px; }
QFrame#ConverterCard, QFrame#BottomCard {
    background: #141822; border: 1px solid #252a3a; border-radius: 14px;
}
QFrame#ConverterCard:hover { background: #191d2a; border-color: #55487d; }
QLabel#CardIcon {
    background: #28223e; color: #ad9cff; border-radius: 10px;
    font-size: 20px; font-weight: 700;
}
QLabel#CardTitle { color: #f3f4f9; font-size: 14px; font-weight: 750; }
QLabel#CardDescription { color: #777f94; font-size: 11px; }
QLabel#Arrow { color: #666e83; font-size: 17px; }
QLabel#StatusBadge {
    color: #8edbc0; background: #152b28; border: 1px solid #244c43;
    border-radius: 10px; padding: 4px 9px; font-size: 10px; font-weight: 700;
}
QProgressBar {
    background: #242837; border: none; border-radius: 4px; height: 8px;
    color: transparent;
}
QProgressBar::chunk { background: #765fff; border-radius: 4px; }
QLabel#EmptyIcon { color: #4d5468; font-size: 23px; }
QLabel#EmptyText { color: #747c90; font-size: 11px; }
"""
