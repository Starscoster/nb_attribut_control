lf.maya_obj: str = maya_obj
        self.long_name: str = long_name

        # Create variable and edit them later
        self.nice_name: str = "Attribut 1"
        self.short_name: str = "att1"

        self.parent_attribut: str = ""
        self.child_attribut: str = ""

        self.value: float = 0
        self.defaut_value: float = 0
        self.has_max_value: bool = False
        self.has_min_value: bool = False
        self.enum_list: str = ""
        self.max_value: float = None
        self.min_value: float = None
        
        self.attribute_type: str = "float"
        
        self.in_channel_box: bool = False
        self.keyable: bool = False
        self.locked: bool = False
        
        self.incom_connections: list = []
        self.outcom_connections: list = []


[
    "bool", "long", "short",
    "byte", "char", "float",
    "double", "doubleAngle", "doubleLinear",
    "enum", "matrix", "2 float",
    "3 float", "2 long", "3 long",
    "2 double", "3 double", "2 doubleAngle",
    "3 doubleAngle", "2 doubleLinear", "3 doubleLinear",
    ]