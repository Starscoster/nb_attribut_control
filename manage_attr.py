"""
This is a module to catch maya control object, get custom attributs and edit them.
@autor : Nathan Boyaval
@Version : 0.0.1
@Update : 2025/02/10
"""
# Tester les class objet et attribut. Tester l'edition de long_name, le try excet pour les type des variables

import maya.cmds


def is_type (type_) :
    """Custom decorator to check if data is correct type"""
    def decorator (func) :
        def wrapper (*args, **kwargs) :
            if isinstance(args[1], type_) :
                func(*args)
            else :
                raise TypeError (
                    "Incorrect value type ({}); Needs {}, got {}".format(args[0], type_, args[1])
                    )
        return wrapper
    return decorator

#######################################################################################################################
#                Create, delete, copy attribut
#######################################################################################################################

def create_attribut (object_, attribut_name,
                    attribut_type = None,
                    attribut_short_name = None, 
                    attribut_nice_name = None, 
                    attribut_min = None, 
                    attribut_max = None, 
                    attribut_defaut = 0, 
                    enum_values="",
                    multiple_attr_flags = ["X", "Y", "Z"]) -> None :
                        
    """
    Create a new attribut to a node. 
    
    :object_: maya object to add attribut to
    :attribut_name: attribut long name
    :attribut_type: attribut type : bool, long, short, byte, char, float, double, doubleAngle, doubleLinear, enum, matrix, long2, long3, short2, short3, double2, double3, float2, float3
    :attribut_short_name: attribut short name to display in node editor
    :attribut_nice_name: attribut name to display in outliner
    :attribut_min: attribut minimum value
    :attribut_max: attribut maximum value
    :attribut_defaut: attribut default value
    :enum_values: enum values to set in enumName parameter
    :multiple_attr_flags: list of 3 strings to add at the end of combo attr
    :return: None
    """

    # bool attributs
    if attribut_type == "bool" :        
        cmds.addAttr(object_, longName = attribut_name, at = attribut_type, k=True)

    # long, short, byte, char, float, double, doubleAngle, doubleLinear attributs
    elif attribut_type == "long" or attribut_type == "short" or attribut_type == "byte" or attribut_type == "char" or attribut_type == "float" or attribut_type == "double" or attribut_type == "doubleAngle" or attribut_type == "doubleLinear":
        cmds.addAttr(object_, longName = attribut_name, at = attribut_type, defaultValue = attribut_defaut, k=True)
    
    # enum attributs
    elif attribut_type == "enum" :
        cmds.addAttr(object_, longName = attribut_name, at = attribut_type, enumName = enum_values, k=True)
    
    # matrix attibuts
    elif attribut_type == "matrix" :
        cmds.addAttr(object_, longName = attribut_name, at = attribut_type)

    # combo attributs
    elif "2" in attribut_type or "3" in attribut_type :

        sub_attributs_type = attribut_type[:-1]     # Get attribut types to create
        number_of_attr = int(attribut_type[-1])     # Get number of attributs to creates

        # Creates combo attribut
        cmds.addAttr(object_, longName = attribut_name, at = attribut_type, k=True)

        # Create sub attributs
        for i in range(number_of_attr) :

            # If multiple_attr_flags variable is set, use it otherwise use numbers as suffix
            if i <= len(multiple_attr_flags) -1 :
                suffix_to_add = multiple_attr_flags[i]
            else :
                suffix_to_add = i

            cmds.addAttr(object_, longName = "{}{}".format(attribut_name, suffix_to_add), at = sub_attributs_type, parent = attribut_name, k=True)
    
    # If attribut_type don't match supported attributs, raise an error
    else :
        cmds.warning("Unvalid attribut type : {}".format(attribut_type))

def delete_attribut (object_, attribut) -> None :
    """
    Delete a custom attribut

    :object_: Maya object with custom attribut
    :attribut: Custom attribut to delete
    :return: None
    """
    cmds.deleteAttr("{}.{}".format(object_, attribut))

#######################################################################################################################
#                Utility
#######################################################################################################################

def get_attr_names (object_) -> list :
    """
    Get a list of all attributs of an object
    
    :object_: maya object
    :return: list of object attributs
    """
    return cmds.listAttr(object_)

def get_custom_attr_names (object_) -> list :
    """
    Get a maya object custom attributs

    Keywords:
        object_ -- maya object
    
    Returns :
        list of custom attributs in the object or an empty list
    """
    # Get object_ type and create another one
    object_type = cmds.objectType(object_)
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
        self, maya_obj, long_name
        ) -> object :
        """
        Create class variables.

        Keyword arguments:
            maya_obj -- maya's object that attribut is part of
            long_name -- attribut full name
        Returns:
            None
        """

        self.maya_obj = maya_obj
        self.long_name = long_name

        obj_attribut = "{}.{}".format(maya_obj, self.long_name)

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
        self.nice_name = formated_name
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


class MayaObject () :
    """Maya Object as python object"""

    def __init__ (
        self, object_name
        ) -> object :
        self.object_name = object_name
        self.custom_attributs = get_custom_attr_names(object_name)
        self.attributs_dic = {}

    def create_attributs_class (
        self
        ) -> dict :
        """Fil self.attributs_dic"""

        for attr in self.custom_attributs :
            attr_class = Attribut(self.object_name, long_name = attr)
            attr_index = self.custom_attributs.index(attr)
            self.attributs_dic[attr] = {"class" : attr_class, "index" : attr_index}

        return True

    def get_attribut_object (
        self, attribut
        ) -> None :
        """Get attribut class object"""

        try  :
            attribut_class = self.attributs_dic[attribut]["class"]
        except KeyError :
            return None
        return attribut_class


    def edit_long_name (self, attribut, new_name) -> None :
        """Edit attribut long name"""
        attribut_obj = self.get_attribut_object(attribut)
        if attribut_obj :
            attribut_obj.edit_long_name(new_name)
        return True

    def edit_nice_name (self, attribut, new_nice_name) -> None :
        """Edit attribut nice name"""
        formated_name = new_nice_name.replace("_"," ")
        self.nice_name = formated_name
        return True

    def edit_short_name (self, attribut, new_short_name) -> None :
        """Edit attribut short name"""
        no_space = new_short_name.replace(" ","_")
        initial_word = ''.join([word[0] for word in no_space.split("_")])       # Get initial of each word in attribut name
        self.short_name = initial_word
        return True

    def set_has_maximum_state (self, attribut, value = False) :
        """Set self.has_max_value"""
        self.has_max_value = value
        return True
 
    def set_has_minimum_state (self, attribut, value = False) :
        """Set self.has_min_value"""
        self.has_min_value = value
        return True

    def set_maximum_value (self, attribut, value) :
        """Set self.maxValue"""
        self.max_value = value
        return True
   
    def set_minimum_value (self, attribut, value) :
        """Set self.min_value """
        self.min_value = value
        return True
  
    def set_defaut_value (self, attribut, value) :
        """Set self.dafaut_value"""
        self.max_value = value
        return True

    def set_visible (self, attribut, state) -> None :
        """Set self.in_channel_box"""
        self.in_channel_box = state
        return True

    def set_lock (self, attribut, state) -> None :
        """Set self.locked"""
        self.locked = state
        return True

    def set_keyable (self, attribut, state) -> None :
        """Set self.keyable"""
        self.keyable = state
        return True
    
attr = Attribut("nurbsCircle1", "test")
attr.edit_long_name("new_test_name")