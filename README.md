# 2-3 Trees: Applications and Advantages

### Ze Sen Tan and Zhen Ze Ong

This was a group project for a Data Structures & Algorithms class in my Sophomore year of university. It is a basic exploration of the 2-3 Trees data structure, a complex version of binary trees. Looking back, we could have structured the code better and added a proper user interface. The output of the current code is limited to the first two levels of the created 2-3 tree.

Regular binary trees tend to get "unbalanced" after data is inserted or removed. This means that all data are pushed to one side of the binary tree instead of being equally distributed, which increases the time complexity of data retrieval and queries. 2-3 trees do not have this issue because of the way they store data. Nodes that hold data within 2-3 trees can hold up to two values, and they split and merge in a way that maintains a constant balance in the tree. Thus, 2-3 trees are a more effective form of binary trees in databases that constantly update, as the stream of inputs and outputs will not cause an imbalance in the tree.
