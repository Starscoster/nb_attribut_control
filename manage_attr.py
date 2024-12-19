import maya.cmds

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