# Chillie-C4D-Scripts
C4d Scripts

Purpose:
This Python script is designed to automatically assign colliders to IK tags in a Cinema 4D scene, based on a specific naming convention for GRP, CAP, and IK objects. It assumes that the scene is structured with GRP objects containing CAP and IK objects, and that these objects have names that follow a consistent pattern (e.g., "GRP_BodyPart1", "CAP_BodyPart1", "IK_BodyPart1").

How it works:

Finds GRP objects: The script searches for all objects in the scene that start with the specified grp_prefix (default: "GRP_BodyPart").
Finds CAP and IK objects: For each GRP object, it searches for child objects that start with the specified cap_prefix and ik_prefix (defaults: "CAP_BodyPart" and "IK_BodyPart").
Assigns colliders: For each IK object, it finds the corresponding CAP object (based on the number in their names) and assigns all other CAP objects as colliders to the IK tag.
Enables dynamics: If the IK tag's dynamics are not enabled, it enables them.
Usage:

Open your Cinema 4D scene.
Copy and paste the script into the Python console.
Run the script by pressing Enter.
Customization:
If you need to customize the script for different naming conventions or specific use cases, you can modify the following parameters in the main function:

grp_prefix: The prefix for GRP objects.
cap_prefix: The prefix for CAP objects.
ik_prefix: The prefix for IK objects.
Additional Notes:

The script assumes that the scene is structured in a specific way. If your scene has a different structure, you might need to adjust the script accordingly.
If you encounter any errors or unexpected behavior, please provide more details about your scene and the specific issue you're facing.
Example:
If your scene has objects named "GRP_Arm", "CAP_Arm1", "CAP_Arm2", and "IK_Arm1", the script will assign "CAP_Arm2" as a collider to the "IK_Arm1" tag.
