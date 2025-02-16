"""
This is a module to catch maya control object, get custom attributs and edit them.
@autor : Nathan Boyaval
@Version : 0.0.3
@Update : 2025/02/16
"""

import maya.cmds

def is_type (type_) :
    """Custom decorator to check if data is correct type"""
    def decorator (func) :
        def wrapper (*args, **kwargs) :
            if isinstance(args[1], type_) :
                func(*args)
            else :
                raise TypeError (
                    "Incorrect value type ({}); Needs {}, got {}".format(args[0], type_, type(args[1]))
                    )
        return wrapper
    return decorator

attribut_type: list = [
    "bool", "long", "short",
    "byte", "char", "float",
    "double", "doubleAngle", "doubleLinear",
    "enum", "matrix", "2 float",
    "3 float", "2 long", "3 long",
    "2 double", "3 double", "2 doubleAngle",
    "3 doubleAngle", "2 doubleLinear", "3 doubleLinear",
    ]

#######################################################################################################################
#                Utility
#######################################################################################################################

def get_custom_attr_names (object_) -> list :
    """
    Get a maya object custom attributs

    Keywords:
        object_ -- maya object
    
    Returns :
        list of custom attributs in the object or an empty list
    """
    # Get object_ type and create another one
    obj_type = cmds.objectType(object_)
    built_in_object = cmds.createNode(obj_type, name = "temp_obj")
    
    # Get both objects attributs
    object_attributs = cmds.listAttr(object_)
    built_in_attributs = cmds.listAttr(built_in_object)

    # Compare oth lists and get custom attributs
    custom_attributs = list(set(object_attributs)-set(built_in_attributs))

    # Delete built_in_object
    cmds.delete(built_in_object)

    return custom_attributs

class Attribut () :
    """
    New object based on one of maya's object attribut.
    """

    def __init__ (
        self, maya_obj, long_name = "attribut1",
        in_maya = False,
        ) -> object :
        """
        Create class variables.

        Keyword arguments:
            maya_obj -- maya's object that attribut is part of
            long_name -- attribut full name
        Returns:
            None
        """

        self.maya_obj: str = maya_obj
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
        self.max_value: float = 0
        self.min_value: float = 0
        
        self.attribute_type: str = "float"
        
        self.in_channel_box: bool = False
        self.keyable: bool = False
        self.locked: bool = False
        
        self.incom_connections: list = []
        self.outcom_connections: list = []

        if in_maya :
            self.load_maya_attribut()
        else :
            self.edit_nice_name(self.long_name)
            self.edit_short_name(self.long_name)


    def load_maya_attribut (self) -> None :

        obj_attribut = "{}.{}".format(self.maya_obj, self.long_name)

        self.nice_name = cmds.attributeQuery(long_name, node = maya_obj, niceName = True)
        self.short_name = cmds.attributeQuery(long_name, node = maya_obj, shortName = True)
        
        self.parent_attribut = cmds.attributeQuery(long_name, node = maya_obj, listParent = True)
        self.child_attribut = cmds.attributeQuery(long_name, node = maya_obj, listChildren = True)

        self.value = cmds.getAttr(obj_attribut)
        self.defaut_value = cmds.attributeQuery(long_name, node = maya_obj, listDefault = True)
        self.has_max_value = cmds.attributeQuery(long_name, node = maya_obj, maxExists=True)
        self.has_min_value = cmds.attributeQuery(long_name, node = maya_obj, minExists=True)
        self.enum_list = cmds.attributeQuery(long_name, node = maya_obj, listEnum = True)

        # Check if attribut has minimium or maximum value and set self.min_values and self.max_values
        if self.has_max_value :
            self.max_value = cmds.attributeQuery(long_name, node = maya_obj, maximum=True)
        else :
            self.max_value = None
    
        if self.has_min_value :
            self.min_value = cmds.attributeQuery(long_name, node = maya_obj, minimum=True)
        else :
            self.min_value = None
        
        self.attribute_type = cmds.attributeQuery(long_name, node = maya_obj, attributeType = True)
        
        self.in_channel_box = cmds.attributeQuery(long_name, node = maya_obj, channelBox = True)
        self.keyable = cmds.attributeQuery(long_name, node = maya_obj, keyable = True)
        self.locked = cmds.getAttr(obj_attribut, lock = True)
        
        self.incom_connections = cmds.listConnections(obj_attribut, plugs = True, destination = True, source = False)
        self.outcom_connections = cmds.listConnections(obj_attribut, plugs = True, destination = False, source = True)

    #######################################################################################################################
    #                Edit attribut
    #######################################################################################################################
    @is_type(str)
    def edit_long_name (self, new_name) -> None :
        """Edit attribut long name""" 
        self.long_name = new_name.replace(" ", "_")
        self.edit_nice_name(new_name)
        self.edit_short_name(new_name)
        return True

    @is_type(str)
    def edit_nice_name (self, new_nice_name) -> None :
        """Edit attribut nice name"""
        formated_name = new_nice_name.replace("_"," ")
        self.nice_name = formated_name.title()
        return True

    @is_type(str)
    def edit_short_name (self, new_short_name) -> None :
        """Edit attribut short name"""
        no_space = new_short_name.replace(" ","_")
        initial_word = ''.join([word[0] for word in no_space.split("_")])       # Get initial of each word in attribut name
        self.short_name = initial_word
        return True

    #######################################################################################################################
    @is_type(bool)
    def set_has_maximum_state (self, value = False) :
        """Set self.has_max_value"""
        self.has_max_value = value
        return True

    @is_type(bool)   
    def set_has_minimum_state (self, value = False) :
        """Set self.has_min_value"""
        self.has_min_value = value
        return True

    @is_type(float)
    def set_maximum_value (self, value) :
        """Set self.maxValue"""
        self.max_value = value
        return True

    @is_type(float)    
    def set_minimum_value (self, value) :
        """Set self.min_value """
        self.min_value = value
        return True

    @is_type(float)   
    def set_defaut_value (self, value) :
        """Set self.dafaut_value"""
        self.max_value = value
        return True

    #######################################################################################################################
    @is_type(bool)
    def set_visible (self, state) -> None :
        """Set self.in_channel_box"""
        self.in_channel_box = state
        return True

    @is_type(bool)
    def set_lock (self, state) -> None :
        """Set self.locked"""
        self.locked = state
        return True

    @is_type(bool)
    def set_keyable (self, state) -> None :
        """Set self.keyable"""
        self.keyable = state
        return True

    @is_type(str)
    def set_attribut_type (self, new_type) -> bool :
        """Set self.attribut_type"""
        if new_type in attribut_type :
            self.attribute_type = new_type
            return True
        cmds.error ("Unvalid attribut type {}".format(new_type))
        return False

    def commit_attr (self) -> bool :                            
        """Create attribut in maya_object."""

        if self.parent_attribut :
            cmds.addAttr(
                self.maya_obj,
                longName = self.long_name, 
                niceName = self.nice_name,
                shortName = self.short_name, 
                defaultValue = self.defaut_value,
                parent = self.parent_attribut,
                hasMaxValue = self.has_max_value, 
                hasMinValue = self.has_min_value, 
                maxValue = self.max_value,
                minValue = self.min_value, 
                attributeType = self.attribute_type, 
                hidden = self.in_channel_box,
                keyable=self.keyable,
                    )
        else :
            cmds.addAttr(
                self.maya_obj,
                longName = self.long_name, 
                niceName = self.nice_name,
                shortName = self.short_name, 
                defaultValue = self.defaut_value,
                hasMaxValue = self.has_max_value, 
                hasMinValue = self.has_min_value, 
                maxValue = self.max_value,
                minValue = self.min_value, 
                attributeType = self.attribute_type, 
                hidden = self.in_channel_box,
                keyable=self.keyable,
                    )
        # if (self.attribut_type == "long" or
        #     self.attribut_type == "short" or
        #     self.attribut_type == "byte" or
        #     self.attribut_type == "char" or
        #     self.attribut_type == "float" or
        #     self.attribut_type == "double" or
        #     self.attribut_type == "doubleAngle" or
        #     self.attribut_type == "doubleLinear" or
        #     self.attribut_type == "bool"):
        #     # If one of those attribut, do it
        #     cmds.addAttr(
        #         self.maya_obj,
        #         longName = self.long_name, 
        #         niceName = self.nice_name,
        #         shortName = self.short_name, 
        #         parent = self.parent_attribut, 
        #         defautValue = self.defaut_value,
        #         hasMaxValue = self.has_max_value, 
        #         hasMinValue = self.has_min_value, 
        #         maxValue = self.max_value,
        #         minValue = self.min_value, 
        #         attributType = self.attribute_type, 
        #         hidden = self.in_channel_box,
        #         keyable=self.keyable,
        #         )
        
        # # enum attributs
        # elif self.attribut_type == "enum" :
        #     cmds.addAttr(
        #         self.maya_obj,
        #         longName = attribut_name, 
        #         niceName = self.nice_name,
        #         shortName = self.short_name, 
        #         parent = self.parent_attribut,
        #         defautValue = self.defaut_value,
        #         enumName = self.enum_list,
        #         attributType = self.attribute_type, 
        #         hidden = self.in_channel_box,
        #         keyable=self.keyable,
        #         )
        
        # # matrix attibuts
        # elif self.attribut_type == "matrix" :
        #     cmds.addAttr(
        #         self.maya_obj,
        #         longName = attribut_name, 
        #         niceName = self.nice_name,
        #         shortName = self.short_name, 
        #         parent = self.parent_attribut,
        #         attributType = self.attribut_type,
        #         hidden = self.in_channel_box,
        #         keyable=self.keyable,
        #         )

        # combo attributs
        # elif "2" in attribut_type or "3" in attribut_type :

        #     sub_attributs_type = attribut_type[:-1]     # Get attribut types to create
        #     number_of_attr = int(attribut_type[-1])     # Get number of attributs to creates

        #     # Creates combo attribut
        #     cmds.addAttr(object_, longName = attribut_name, at = attribut_type, k=True)

        #     # Create sub attributs
        #     for i in range(number_of_attr) :

        #         # If multiple_attr_flags variable is set, use it otherwise use numbers as suffix
        #         if i <= len(multiple_attr_flags) -1 :
        #             suffix_to_add = multiple_attr_flags[i]
        #         else :
        #             suffix_to_add = i

        #         cmds.addAttr(object_, longName = "{}{}".format(attribut_name, suffix_to_add), at = sub_attributs_type, parent = attribut_name, k=True)
        
        # # If attribut_type don't match supported attributs, raise an error
        # else :
        #     cmds.error("Unvalid attribut type : {}".format(attribut_type))

        cmds.setAttr("{}.{}".format(self.maya_obj, self.long_name), lock = self.locked)
        cmds.setAttr("{}.{}".format(self.maya_obj, self.long_name), self.value)


class MayaObject () :
    """Maya Object as python object"""

    def __init__ (
        self, object_name
        ) -> object :
        self.object_name = object_name
        self.custom_attributs = get_custom_attr_names(object_name)
        self.attributs_dic = {}
        self.create_attributs_class()
        self.custom_attributs_count = len(self.custom_attributs)

    
    def check_attribut(func) :
        """Decorator to check if attribut exists"""
        def wrapper (*args, **kwargs) :
            print ("in decorator")
            attribut_obj = args[0].get_attribut_object(args[1])
            if attribut_obj :
                return func(*args)
            print ("out func")
            return None
        return wrapper

    # Attribut object
    def create_attributs_class (
        self
        ) -> dict :
        """Fil self.attributs_dic"""

        for attr in self.custom_attributs :
            attr_class = Attribut(self.object_name, long_name = attr)
            attr_index = self.custom_attributs.index(attr)
            self.attributs_dic[attr] = {"class" : attr_class, "index" : attr_index}

        return self.attributs_dic

    def get_attribut_object (
        self, attribut
        ) -> None or classmethod:
        """Get attribut class object"""
        try  :
            attribut_class = self.attributs_dic[attribut]["class"]
        except KeyError :
            return None
        return attribut_class
    
    # Edit attributs parameters
    @check_attribut
    def edit_long_name (
        self, attribut, new_name
        ) -> None or str:
        """Edit attribut long name and update class attribut list and dict"""
        self.get_attribut_object(attribut).edit_long_name(new_name)

        # Update class attribut list and dict values
        self.attributs_dic[new_name] = self.attributs_dic.pop(attribut)
        attribut_index = self.custom_attributs.index(attribut)
        self.custom_attributs[attribut_index] = new_name


    @check_attribut
    def edit_nice_name (
        self, attribut, new_nice_name
        ) -> None or str:
        self.get_attribut_object(attribut).edit_nice_name(new_nice_name)

    @check_attribut
    def edit_short_name (
        self, attribut, new_short_name
        ) -> None or str:
        self.get_attribut_object(attribut).edit_short_name(new_short_name)

    @check_attribut
    def set_has_maximum_state (
        self, attribut, value = False
        ) -> None or bool:
        self.get_attribut_object(attribut).set_has_maximum_state(value)
    
    @check_attribut
    def set_has_minimum_state (
        self, attribut, value = False
        ) -> None or bool:
        self.get_attribut_object(attribut).set_has_minimum_state(value)

    @check_attribut
    def set_maximum_value (
        self, attribut, value
        ) -> None or float:
        self.get_attribut_object(attribut).set_maximum_value(value)
    
    @check_attribut
    def set_minimum_value (
        self, attribut, value
        ) -> None or float:
        self.get_attribut_object(attribut).set_minimum_value(value)
    
    @check_attribut
    def set_defaut_value (
        self, attribut, value
        ) -> None or float:
        self.get_attribut_object(attribut).set_defaut_value(value)

    @check_attribut
    def set_visible (
        self, attribut, state
        ) -> None or bool:
        self.get_attribut_object(attribut).set_visible(state)

    @check_attribut
    def set_lock (
        self, attribut, state
        ) -> None or bool :
        self.get_attribut_object(attribut).set_lock(state)

    @check_attribut
    def set_keyable (
        self, attribut, state
        ) -> None or bool :
        self.get_attribut_object(attribut).set_keyable(state)

    @check_attribut
    def set_attribut_type(
        self, attribut, new_type
        ) -> None or bool :
        self.get_attribut_object(attribut).set_attribut_type(new_type)

    # Add and delete attribut
    def add_attribut (
        self, attribut_name
        ) -> tuple :
        """
        Add attribut to class : Creates attribut class, add it in self.attributs_dic
        and in self.custom_attributs

        Keywords : 
            attribut_name -- new attribut name, used as key in self.attribut_dic

        Returns :
            ( 
            self.custom_attributs -- list
            self.attribut_dic -- dict
            self.custom_attributs_count -- int
            )
        """
        if attribut_name not in self.custom_attributs :
            self.custom_attributs.append(attribut_name)
            self.custom_attributs_count += 1

        if attribut_name not in self.attributs_dic.keys() :
            attr_class = Attribut(self.object_name, long_name = attribut_name)
            attribut_index = len(self.custom_attributs) - 1
            self.attributs_dic[attribut_name] = {"class" : attr_class, "index" : attribut_index}
        return (self.custom_attributs, self.attributs_dic, self.custom_attributs_count)

    def delete_attribut (
        self, attribut_name
        ) -> tuple :
        """
        Delete attribut to class, and kill attribut class object

        Keywords : 
            attribut_name -- attribut to delete

        Returns : 
            (
            self.custom_attributs -- list
            self.attribut_dic -- dict
            self.custom_attributs_count -- int
            )
        """
        if attribut_name in self.custom_attributs :
            self.custom_attributs.remove(attribut_name)
            self.custom_attributs_count -= 1
        if attribut_name in self.attributs_dic.keys() :
            class_obj = self.attributs_dic[attribut_name]["class"]
            print ("Deleting attribut {} class".format(attribut_name))
            del class_obj
            try :
                class_obj
            except NameError :
                print("-> deleted")
            else :
                print("-> not deleted")
            self.attributs_dic.pop(attribut_name)
            index = 0
            for attr in self.attributs_dic :
                self.attributs_dic[attr]["index"] = index
                index += 1
        return (self.custom_attributs, self.attributs_dic, self.custom_attributs_count)

    def commit_attributs (self) -> None :
        """Creates all attributs in maya"""
        for attribut in self.custom_attributs :
            is_deleted = self.delete_maya_attribut(attribut)
            if not is_deleted :
                cmds.warning("Attribut {} does not exists".format(attribut))

            attr_class = self.attributs_dic[attribut]["class"]
            attr_class.commit_attr()
            

    def delete_maya_attribut (self, attribut) -> bool :
        """Delete maya object attribut"""
        obj_attr = "{}.{}".format(self.object_name, attribut)
        if cmds.objExists(obj_attr) :
            cmds.deleteAttr (obj_attr)
            return True
        return False

    
    
obj_ = MayaObject("nurbsCircle1")
print (obj_.custom_attributs)
print (obj_.attributs_dic)
obj_.add_attribut("test_bool")
obj_.commit_attributs()