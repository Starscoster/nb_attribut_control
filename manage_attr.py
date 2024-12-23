import maya.cmds

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
#                Edit attributs
#######################################################################################################################

def toogle_visible (object_, attribut) -> None :
    """
    Toogle attribut visibility state

    :object_: Maya object with custom attribut
    :attribut: Custom attribut to edit
    :return: None
    """

    if not cmds.getAttr("{}.{}".format(object_, attribut), channelBox=True) :
        cmds.setAttr("{}.{}".format(object_, attribut), channelBox=True)
    
    else :
        cmds.setAttr("{}.{}".format(object_, attribut), channelBox=False)

def toogle_lock (object_, attribut) -> None :
    """
    Toogle attribut lock state

    :object_: Maya object with custom attribut
    :attribut: Custom attribut to edit
    :return: None
    """

    if not cmds.getAttr("{}.{}".format(object_, attribut), lock=True) :
        cmds.setAttr("{}.{}".format(object_, attribut), lock=True)
    
    else :
        cmds.setAttr("{}.{}".format(object_, attribut), lock=False)


def toogle_keyable (object_, attribut) -> None :
    """
    Toogle attribut keyable state

    :object_: Maya object with custom attribut
    :attribut: Custom attribut to edit
    :return: None
    """

    if not cmds.getAttr("{}.{}".format(object_, attribut), keyable=True) :
        cmds.setAttr("{}.{}".format(object_, attribut), keyable=True)
    
    else :
        cmds.setAttr("{}.{}".format(object_, attribut), keyable=False, channelBox=True)

def set_has_maximum_state (control_, attribut, value = False) :
    """
    Set attribut hasMaximumValue state

    :object_: Maya object with custom attribut
    :attribut: Custom attribut to edit
    :value: Bool
    :return: None
    """
    cmds.addAttr("{}.{}".format(control_, attribut), edit = True, hasMaxValue = value)
    
def set_has_minimum_state (control_, attribut, value = False) :
    """
    Set attribut hasMinimumValue state

    :object_: Maya object with custom attribut
    :attribut: Custom attribut to edit
    :value: Bool
    :return: None
    """
    cmds.addAttr("{}.{}".format(control_, attribut), edit = True, hasMinValue = value)
    
def set_maximum_value (control_, attribut, value) :
    """
    Set attribut maxValue

    :object_: Maya object with custom attribut
    :attribut: Custom attribut to edit
    :value: New max value
    :return: None
    """
    cmds.addAttr("{}.{}".format(control_, attribut), edit = True, maxValue = value)
    
def set_minimum_value (control_, attribut, value) :
    """
    Set attribut minValue

    :object_: Maya object with custom attribut
    :attribut: Custom attribut to edit
    :value: New min value
    :return: None
    """
    cmds.addAttr("{}.{}".format(control_, attribut), edit = True, minValue = value)
    
def set_defaut_value (control_, attribut, value) :
    """
    Set attribut dafaut value

    :object_: Maya object with custom attribut
    :attribut: Custom attribut to edit
    :value: New defaut value
    :return: None
    """
    cmds.addAttr("{}.{}".format(control_, attribut), edit = True, defautValue = value)

#######################################################################################################################
#                Edit naming
#######################################################################################################################

def edit_long_name (object_, attribut, new_name) -> None :
    """
    Edit attribut long name
    
    :object_: Maya object with custom attribut
    :attribut: Custom attribut to edit
    :new_name: New attribut name
    :return: New attribut Name
    """
    # Format new_name 
    new_attr_name = format_str_for_long_name(new_name)

    # Rename attribut
    cmds.renameAttr("{}.{}".format(object_, attribut), new_attr_name)

def edit_nice_name (object, attribut, new_nice_name) -> None :
    """
    Edit attribut long name
    
    :object_: Maya object with custom attribut
    :attribut: Custom attribut to edit
    :new_nice_name: New attribut nice name
    :return: New attribut nice Name
    """
    # Format new_name 
    new_attr_name = format_str_for_long_name(new_nice_name)

    # Set new nice name
    cmds.addAttr(object_, ln = attribut, e=True, niceName = new_attr_name)

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

    :object_: maya object
    :return: list of custom attributs in the object or an empty list
    """
    # Get object_ type and create another one
    object_type = cmds.objectType(object_)
    built_in_object = cmds.createNode(obj_type, name = "temp_obj")
    
    # Get both objects attributs
    object_attributs = cmds.listAttr(object_)
    built_in_attributs = cmds.listAttr(built_in_object)

    # Convert list to set. Substract both sets to get custom attributs
    custom_attributs = list(set(object_attributs)-set(built_in_attributs))

    # Delete created object_
    cmds.delete(built_in_object)

    return custom_attributs

def format_str_for_long_name (long_name) -> str :
    """
    Replaces " " by "_" in new attribut name

    :long_name: in name
    :return: formated name
    """
    if " " in long_name :
        new_long_name = long_name.replace(" ", "_")
    else :
        new_long_name = long_name

    return new_long_name

def get_attribut_infos (object_, attribut) :
    """
    Copy custom attributs from an object to another
    
    :object_: Maya object with custom attributs
    :attribut: attribut to copy
    :return: attribut info in dic with keys [
                "value", defaut_value, has_max_value, max_value,
                has_min_value, min_value, attribute_type, categories, in_channel_box, keyable,
                locked, enum_list, parent_attribut, children_attribut, long_name, nice_name,
                "short_name", "incom_connections", "outcom_connections"
                ]
    """
    
    # Combine object and attribut strings
    obj_attribut = "{}.{}".format(object_, attribut)
    
    # Value infos
    value = cmds.getAttr(obj_attribut)
    defaut_value = cmds.attributeQuery(attribut, node = object_, listDefault = True)
    has_max_value = cmds.attributeQuery(attribut, node = object_, maxExists=True)
    has_min_value = cmds.attributeQuery(attribut, node = object_, minExists=True)
    
    if has_max_value :
        max_value = cmds.attributeQuery(attribut, node = object_, maximum=True)
    else : 
        max_value = None

    if has_min_value :
        min_value = cmds.attributeQuery(attribut, node = object_, minimum=True)
    else : 
        min_value = None

    # Attribut parameters  
    attribute_type = cmds.attributeQuery(attribut, node = object_, attributeType = True)
    categories = cmds.attributeQuery(attribut, node = object_, categories = True)
    in_channel_box = cmds.attributeQuery(attribut, node = object_, channelBox = True)
    keyable = cmds.attributeQuery(attribut, node = object_, keyable = True)
    locked = cmds.getAttr(obj_attribut, lock = True)
    
    # Enum string values
    if attribute_type == "enum" :
        enum_list = cmds.attributeQuery(attribut, node = object_, enum_list = True)
    else :
        enum_list = None
    
    # Hierarchie infos
    parent_attribut = cmds.attributeQuery(attribut, node = object_, listParent = True)
    children_attribut = cmds.attributeQuery(attribut, node = object_, listChildren = True)
    
    # Naming Infos
    long_name = cmds.attributeQuery (attribut, node = object_, longName = True)
    nice_name = cmds.attributeQuery (attribut, node = object_, niceName = True)
    short_name = cmds.attributeQuery (attribut, node = object_, shortName = True)

    # Connections info
    incom_connections = cmds.listConnections(obj_attribut, plugs = True, destination = True, source = False)
    outcom_connections = cmds.listConnections(obj_attribut, plugs = True, destination = False, source = True)

    # output dict
    out_dic = {"value" : value,
                "defaut_value" : defaut_value,
                "has_max_value" : has_max_value,
                "max_value" : max_value,
                "has_min_value" : has_min_value,
                "min_value" : min_value,
                "attribute_type" : attribute_type,
                "categories" : categories,
                "in_channel_box" : in_channel_box,
                "keyable" : keyable,
                "locked" : locked,
                "enum_list" : enum_list,
                "parent_attribut" : parent_attribut,
                "children_attribut" : children_attribut,
                "long_name" : long_name,
                "nice_name" : nice_name,
                "short_name" : short_name,
                "incom_connections" : incom_connections,
                "outcom_connections" : outcom_connections}

    return out_dic