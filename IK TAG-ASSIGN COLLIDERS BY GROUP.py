import c4d

def find_object_by_name_prefix(parent, prefix):
    """Finds an object with a name starting with the given prefix within the specified parent object or its children."""
    if parent.GetName().startswith(prefix):
        return parent
    for child in parent.GetChildren():
        found = find_object_by_name_prefix(child, prefix)
        if found:
            return found
    return None

def find_ik_tag(obj, search_depth=2):
    """Finds an IK tag on the given object or its child joints."""
    print(f"Searching for IK tag on {obj.GetName()}...")
    # Check if the object itself has tags
    for tag in obj.GetTags():
        print(f"Tag type on {obj.GetName()}: {tag.GetType()}")
        if tag.GetType() == 1019561:  # IK tag type ID
            return tag
    # Check children
    if search_depth > 0:
        for child in obj.GetChildren():
            tag = find_ik_tag(child, search_depth - 1)
            if tag:
                return tag
    return None

def main(grp_prefix="GRP_BodyPart", cap_prefix="CAP_BodyPart", ik_prefix="IK_BodyPart"):
    """Finds and processes IK tags in the scene."""
    try:
        # Get all GRP objects in the scene
        grp_objects = [obj for obj in doc.GetObjects() if obj.GetName().startswith(grp_prefix)]
        if not grp_objects:
            print(f"No {grp_prefix} objects found in the scene.")
            return

        cap_objects = []
        ik_objects = []

        # Iterate through GRP objects to find their descendants
        for grp in grp_objects:
            cap = find_object_by_name_prefix(grp, cap_prefix)
            if cap:
                cap_objects.append(cap)
            ik = find_object_by_name_prefix(grp, ik_prefix)
            if ik:
                ik_objects.append(ik)

        if not cap_objects or not ik_objects:
            print(f"{cap_prefix} or {ik_prefix} objects not found as expected in the hierarchy.")
            return

        print(f"Found {len(cap_objects)} CAP objects and {len(ik_objects)} IK objects.")

        # For each IK object
        for ik in ik_objects:
            print(f"Processing {ik.GetName()}...")
            ik_tag = find_ik_tag(ik)

            if not ik_tag:
                print(f"No IK tag found for {ik.GetName()}")
                # Print children of this object
                for child in ik.GetChildren():
                    print(f"  Child of {ik.GetName()}: {child.GetName()} (Type: {child.GetType()})")
                    for tag in child.GetTags():
                        print(f"    Tag on {child.GetName()}: {tag.GetName()} (Type: {tag.GetType()})")
            else:
                print(f"Found IK tag for {ik.GetName()}: Type {ik_tag.GetType()}")
                # Check if dynamics are enabled
                if not ik_tag[c4d.ID_CA_IK_TAG_DYNAMICS_ENABLE]:
                    print(f"Dynamics not enabled on IK tag for {ik.GetName()}. Enabling...")
                    ik_tag[c4d.ID_CA_IK_TAG_DYNAMICS_ENABLE] = True

                # Clear existing colliders and create new InExcludeData
                colliders = c4d.InExcludeData()

                # Find the corresponding CAP object (same number in the name)
                ik_number = ik.GetName().split(ik_prefix)[1]
                corresponding_cap = next((cap for cap in cap_objects if cap.GetName().endswith(ik_number)), None)

                # Add all CAP objects except the corresponding one as colliders
                collider_list = [cap for cap in cap_objects if cap != corresponding_cap]
                for collider in collider_list:
                    colliders.InsertObject(collider, 1)  # 1 means include

                # Set the updated colliders
                ik_tag[c4d.ID_CA_IK_TAG_DYNAMICS_COLLIDERS] = colliders

                print(f"Set {len(collider_list)} colliders for {ik.GetName()}")

        # Display the confirmation message after processing all IK objects
        c4d.gui.MessageDialog("Colliders assigned successfully!")

        c4d.EventAdd()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()