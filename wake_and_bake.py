import maya.cmds as cmds

def wake_n_bake(joint_prefix_field, join_name_field):
    joint_prefix = cmds.textField(joint_prefix_field, query=True, text=True)
    joint_name = cmds.textField(join_name_field, query=True, text=True)

    # Get selected objects
    selected_objects = cmds.ls(selection=True, type='transform')

    joint_data = []

    joint_count = 0

    # Start and End frame
    start_frame = cmds.playbackOptions(query=True, minTime=True)
    end_frame = cmds.playbackOptions(query=True, maxTime=True)

    for obj in selected_objects:
        # Get center
        center = cmds.objectCenter(obj, gl=True)
        
        # Deselect
        cmds.select(clear=True)

        new_joint_name = joint_prefix + joint_name + "_" + str(joint_count)

        # Create a joint at the center
        joint = cmds.joint(position=center,name=new_joint_name)

        # Parent shite
        constraint = cmds.parentConstraint(obj, joint)
        
        joint_data.append([joint, obj, constraint])

        joint_count += 1
        
    # Get all the joints   
    joints = [data[0] for data in joint_data]
            
    # Select all joints
    cmds.select(joints)

    # Bake n wake!
    cmds.bakeResults(joints, t=(start_frame, end_frame), simulation=True)

    # Cleanup shite
    for data in joint_data:
        cmds.delete(data[2])
        cmds.cutKey(data[1], clear=True)
        cmds.skinCluster(data[0], data[1])
    


# Create window and layout
window = cmds.window(title="Joint Simulation - Wake 'n Bake", widthHeight=(400, 250))
cmds.columnLayout(adjustableColumn=True)

# Joint Prefix
cmds.text(label="Joint Prefix:")
joint_prefix_field = cmds.textField(text="j_")

cmds.separator(style='none', height=10)

# Joint Name
cmds.text(label="Joint Name: ( Will auto add numbers behind the name )")
join_name_field = cmds.textField(text="joint")

cmds.separator(style='none', height=40)

cmds.button(label="Wake 'n Bake!", command=lambda x: wake_n_bake(joint_prefix_field, join_name_field))

# Show the window
cmds.showWindow(window)