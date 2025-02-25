"""
This is a module to catch maya control object, get custom attributs and edit them.
@autor : Nathan Boyaval
@Version : 0.0.4
@Update : 2025/02/19
"""
# UI modules
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

import sys

# Script modules
from nb_attribut_control import manage_attr as mattr


def maya_main_windows() :
    '''
    Return maya main window widget as python object
    '''
    maya_main_window = omui.MQtUtil.mainWindow()
    
    # Return int value if current python version is 3 or upper, 
    # otherwise return long
    if int(sys.version[0]) >= 3 :
        return wrapInstance(
                            int(maya_main_window), 
                            QtWidgets.QWidget
                            )
    else :
        return wrapInstance(
                            long(maya_main_window), 
                            QtWidgets.QWidget
                            )
    
class AttributManagerUI (QtWidgets.QDialog) :
    """Main Window class"""
    
    def __init__ (self, parent = maya_main_windows()) -> None :
        super(AttributManagerUI, self).__init__(parent)
        
        self.setWindowTitle("Attribut Manager")
        
        self.create_actions()
        self.create_widgets()
        self.create_layout()
        self.create_connection()
        
    def create_actions (self) -> None :
        """Create action widget"""
        return True
        
    def create_widgets (self) -> None :
        """Create all widget for UI"""
        self.attribut_list = QtWidgets.QListWidget()
        self.up_btn = QtWidgets.QPushButton("Up")
        self.up_btn.setSizePolicy(
                                    QtWidgets.QSizePolicy.Maximum, 
                                    QtWidgets.QSizePolicy.Expanding
                                    )
        self.up_btn.setMaximumWidth(90)
        self.down_btn = QtWidgets.QPushButton("Down")
        self.down_btn.setSizePolicy(
                                    QtWidgets.QSizePolicy.Maximum, 
                                    QtWidgets.QSizePolicy.Expanding
                                    )
        self.add_btn = QtWidgets.QPushButton("Add")
        self.add_btn.setSizePolicy(
                                    QtWidgets.QSizePolicy.Maximum, 
                                    QtWidgets.QSizePolicy.Expanding
                                    )
        self.delete_btn = QtWidgets.QPushButton("Del")
        self.delete_btn.setSizePolicy(
                                    QtWidgets.QSizePolicy.Maximum, 
                                    QtWidgets.QSizePolicy.Expanding
                                    )
        
        self.long_name_le = QtWidgets.QLineEdit()
        self.long_name_le.setPlaceholderText("Long Name")
        self.nice_name_le = QtWidgets.QLineEdit()
        self.nice_name_le.setPlaceholderText("Nice Name")
        self.short_name_le = QtWidgets.QLineEdit()
        self.short_name_le.setPlaceholderText("Short Name")
        
        self.has_max_cb = QtWidgets.QCheckBox()
        self.has_max_cb.setText("Maximum")
        self.has_min_cb = QtWidgets.QCheckBox()
        self.has_min_cb.setText("Minimum")
        self.max_value_float = QtWidgets.QDoubleSpinBox()
        self.min_value_float = QtWidgets.QDoubleSpinBox()
        self.defaut_value_float = QtWidgets.QDoubleSpinBox()
        self.current_value_float = QtWidgets.QDoubleSpinBox()
        
        self.enum_values = QtWidgets.QLineEdit()
        self.enum_values.setPlaceholderText("Enum Values (val1;val2;val3)")
        
        self.visible_cb = QtWidgets.QCheckBox()
        self.visible_cb.setText("Visible")
        self.lock_cb = QtWidgets.QCheckBox()
        self.lock_cb.setText("Locked")
        self.keyable_cb = QtWidgets.QCheckBox()
        self.keyable_cb.setText("Keyable")
        
        self.attribut_combo = QtWidgets.QComboBox()
        
        return True
        
    def create_connection (self) -> None :
        """ Order widgets"""
        return True
        
    def create_layout (self) -> None :
        """ Connect widget to functions"""
        main_layout = QtWidgets.QVBoxLayout(self)
        
        button_layout = QtWidgets.QVBoxLayout()
        button_layout.setSpacing(0)
        button_layout.addWidget(self.up_btn)
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.down_btn)
        
        attribut_layout = QtWidgets.QHBoxLayout()
        attribut_layout.addWidget(self.attribut_list)
        attribut_layout.addLayout(button_layout)
        
        type_layout = QtWidgets.QHBoxLayout()
        type_layout.addWidget(self.attribut_combo)
        type_group = QtWidgets.QGroupBox("Type")
        type_group.setLayout(type_layout)
        
        settings_layout = QtWidgets.QVBoxLayout()
        name_layout = QtWidgets.QGridLayout()
        name_layout.addWidget(QtWidgets.QLabel("Long"))
        name_layout.addWidget(self.long_name_le)
        name_layout.addWidget(QtWidgets.QLabel("Nice"))
        name_layout.addWidget(self.nice_name_le)
        name_layout.addWidget(QtWidgets.QLabel("Short"))
        name_layout.addWidget(self.short_name_le)
        name_group = QtWidgets.QGroupBox("Naming")
        name_group.setLayout(name_layout)
        
        value_layout = QtWidgets.QGridLayout()
        value_layout.addWidget(self.has_min_cb, 0,0)
        value_layout.addWidget(self.min_value_float, 0,1)
        value_layout.addWidget(self.has_max_cb, 1,0)
        value_layout.addWidget(self.max_value_float, 1,1)
        value_layout.addWidget(QtWidgets.QLabel("Defaut"), 2, 0)
        value_layout.addWidget(QtWidgets.QLabel("Current"), 2, 1)
        value_layout.addWidget(self.defaut_value_float, 3, 0)
        value_layout.addWidget(self.current_value_float, 3, 1)
        value_group = QtWidgets.QGroupBox("Value")
        value_group.setLayout(value_layout)
        
        states_layout = QtWidgets.QHBoxLayout()
        states_layout.addWidget(self.visible_cb)
        states_layout.addWidget(self.lock_cb)
        states_layout.addWidget(self.keyable_cb)
        states_group = QtWidgets.QGroupBox("States")
        states_group.setLayout(states_layout)
        
        settings_layout.addWidget(name_group)
        settings_layout.addWidget(value_group)
        settings_layout.addWidget(states_group)
        
        # Create a frame (separator)
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)  # Horizontal line
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)  # Optional: gives a sunken shadow effect        
        
        main_layout.addLayout(attribut_layout)
        main_layout.addWidget(separator)
        main_layout.addWidget(type_group)
        main_layout.addLayout(settings_layout)
        
        return True