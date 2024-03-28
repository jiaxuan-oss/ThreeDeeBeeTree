Task 1: Methods on BSTs

• In this task, you will be asked to complete as well update an existing
BST implementation.

• Part 1: You need to complete get_minimal and get_successor method
so that it will complete the existing delete_aux() implementation. Refer
to the week 10 pre-reading material on the idea of get_successor
implementation for the purpose of deleting a node.

• Part 2: You are ask to update some method in the BST implementation
so that you can implement Part 3 efficiently. Basically, you need to
modify insert_aux and delete_aux so that during insert and delete,
each node will have subtree_size count. subtree_size is basically the
number of node inside that particular subtree. Thus when you are
accessing a node, you should know how many node are there in the
subtree where that node is the root. if a node doesn't have a child, that
node will have subtree_size 1. (only that node basically)

Task 1: Methods on BSTs

• Part 3: This is the main part of Task 1 where you need to
implement kth_smallest(k, node) method. Its basically a tree
recursive algorithm to search for kth smallest value inside a
sub tree of the give node. Referring to the example in the A3
specification, when calling kth_smallest(2, node-85), it will return node-85 itself because a sub tree with node-85 as its
root only has one child and that child node have a key of 80.
Thus node-80 will be the 1st smallest and 85 will be 2nd
smallest. since k=2, 85 will be returned. if we call
kth_smallest(1, node-85), it will return node-80 since k=1.

• If the given k is bigger than the node’s subtree_size, its up to
you to return None or raise an error. (currently there’s no
mention about how this should be handled in the specification)

Task 2: Ratio elements

• In this task, you need to choose the appropriate ADT to implement
the Percentile class. The main method that you need to implement
is ratio(). ratio is a method that will return the points inside the
percentile object that is higher than x% of the points but smaller
than y% of the element. Using the example given in the
specification, if the percentile objects contains the following
points: [4, 9, 14, 15, 16, 82, 87, 91, 92, 99]

• for ratio(13,10) means bigger than 13% of the points and
smaller than 42% of the points. Thus, 13/100 * 10 (number of
points in the example above) is 1.3, if we round up, basically
bigger than 2 of the smallest points (which is 4 and 9) and
10/100 * 10 is 1 thus less than 1 of the largest points (which is
99), hence it will return [14,15,16,82,87,91,92]

Task 3: ThreeDeeBeeTree

• In this task, you are asked to implement a new type of Tree ADT called
ThreeDeeBeeTree. Its not a binary tree since it can have up to 8 children.
• You could either have 8 individual child pointer or by having the children
as a list of BeeNode where the index of where each child should sit in the
list will depends on the key (point) of the child - based on the octant. For
example, you could have the the first octant (as index 0) when all point of the child is bigger than the parent’s point.
• The key of a BeeNode will be the point (e.g. using the 5 points example
in the specification, (5,-6,7) is the key of the root.
• Still using the example, point (6,0,10) is the child of point (5,-6,7) that sit
at the first octant (using example above) because 6>5, 0>-6, and 10>7.
• Remember to update subtree_size when inserting a new point/node. - in
a similar way as you implement it in the BST of task 1.

Task 4: Balancing Bees

• The main idea of this task is we want to balance a ThreeDeeBeeTree. But
instead of ensuring the ThreeDeeBeeTree always balance whenever we
insert a new point/node, you are asked to write a function called
make_ordering() which will basically to order the given list of points so
that when we insert that points into the ThreeDeeBeeTree one by one, the
resulted ThreeDeeBeeTree structure will be ‘balanced’.

• As stated in the specification, the definition of ‘balanced’ in
ThreeDeeBeeTree is for any node in the ThreeDeeBeeTree, splitting it's
children by those with a negative offset of one of the three axis and those
with a positive offset of the same axis must have a size ratio of at most
1:7 (Or both sides have at most 17 nodes). - Important to note that ‘ratio
1:7’ here is not the same with percentile ratio(1,7).
• See the hint provided in the specification. Your main challenge is to find
the right ‘a’ value to pass to percentile ratio(a,a) for checking the valid x,
y and z indices. You may use the size ratio info above to find the right ‘a’ value.

Task 4: Balancing Bees

• the function make_ordering() is an independent function
and not part of the ThreeDeeBeeTree class. see the test
case for an example of how we can use the
make_ordering() function to make sure we create a
balanced ThreeDeeBeeTree when we insert the list
produced by make_ordering().

• Similar to the make_balanced() method in Week10 Applied
Optional (which the solution is now available), you can use
recursive approach for make_ordering()

Task 5: Sweeping through

beehives

• This is an optional (and rather complicated) task and won’t
be marked (even you implement it correctly). Do it only if
you have time and for the sake of fulfilling your curiosity and
harnessing your problem solving skill!

Task 6: Barry B. Benson's

Best Beehive

• In this task, you need to complete the implementation of BeehiveSelector
class which basically will act as a container to the beehive object. You need
to chose suitable ADT as the data structure behind the BeehiveSelector.

• You need to implement 3 method (other than __init__) inside the
BeehiveSelector class, namely add_beehive, set_all_beehives, and
harvest_best_beehives.
• The method harvest_best_beehives basically will get the ‘best’ beehive from
the ADT and return the emerald value of that beehives. As per the
specification, emerald can be calculated by getting the min between honey
capacity and honey volume and multiply it with the nutrient factor.
• Since it is stated that the creator will often pick up and put down
beehives and assuming the selected ‘best’ beehive will be ‘consumed’,
thus if the consumed value is still less than that beehives volume, you
need to put back that beehive (with reduced volume) into the ADT.
