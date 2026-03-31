# Super Rigid Skin Tool

> Helps with rigid skinning by applying uniform skin weights to selected vertices.

---

## 🖼️ Preview

![Preview](/Maya/SuperRigidSkinTool/SuperRigidSkinTool_Preview.png)

## 🧩 Features

- Apply a rigid skin to selected vertices
- Convert any selection type to vertex selection
- Unlock joints

## 🛠️ How to use

1. Select faces, edges or vertices of a skinned mesh
2. *(Optional)* If the selection type is not vertices, use **Convert Selection to Vertices**
3. Save the selection with **Get Vertex Selection**
4. Select a joint and save it with **Get Joint Selection**
5. *(Optional)* If step 4 prints the "Locked Joint" warning, use **Unlock Joint**
6. *(Optional)* Change the **Paint Value** if you don't want a fully rigid skin
7. **Apply Skin** will set the skin weight of every vertex bound to the selected joint to the Paint Value

## ⚙️ Technicalities

- Vertices need to be bound to the joint with a skin cluster (if a joint is missing, a warning will trigger asking to "Add Influence")
- The "Normalize Weights" attribute of the skin cluster will automatically be set to "Interactive"