Task 1: Trail creation and

Edit methods

• As indicated in the A2 specification, please make sure you read the slide “what is trail”. You should know that the trail is implemented using the
concept of linked structure. Here’s a couple of important points:
• A trailstore must be placed/stored inside a trail. e.g. you can’t have
trailsplit.following point to a trailsplit or trailseries or none. Thus its
either point to Trail(TrailSeries()) or Trail(TrailSplit()) or Trail(None).
Same goes for trailsplit.path_top, path_bottom, or path_follow.
• A mountain can only be part of a trailseries.
• Most importantly, in a trailsplit, both path_top and path_bottom will
eventually lead to / connected to path_follow. Note that “eventually” means it may not be directly linked. For example, path_top may point
to one or more trail first before finally point to the path_follow. This particularly important when you want to traverse the trails. (i.e.
deciding which trail to go next)

Task 1: Trail creation and

Edit methods

• Now that you (hopefully) have understood what a trail is and how it is structured, in
task 1 you need to complete the implementation of Trail, TrailSeries and TrailSplit. If
you refer back to our linked list implementation, we use Node and link it. You can
think of Trail as a Node that need to be updated in order to make it as part of a
particular trails set.
• That said, this task is all about updating the link and content of the trail, trailseries,
and trailsplit!
• When implementing the method, remember that you are working on an instance of
that particular class and most importantly, as stated in the specification, you should
return a new (or the old) instance. What this means, you should not update the
instance. For example:
• There should not be any update statement such as self.following = None,
self.mountain = mountain, self.store = None, self.path_top = None, etc.
• Thus it should be either returning new instance (e.g. return TrailSeries(....) or old
instance (e.g. return self.following)

Task 2: Traversing Trails with

Terrific Tricks

• By the time you start this task, you should have completed
Task 1.

• In this task, you only need to complete one method called
follow_path.

• It is basically a method that will traverse the trails starting
from the particular instance. That is, the starting trail
should be self.store.

• You also need to implement this method using a loop
(iterative based) use appropriate ADT to assist the
process.

Task 2: Traversing Trails with

Terrific Tricks

• Input of follow_path is WalkerPersonality instance. Note that
WalkerPersonality has been fully implemented and thus you
just need to use it. e.g. call personality.add_mountain() or
personality.select_branch() accordingly.

• The important key about WalkerPersonality implementation
is that if select_branch() returns True means you should
follow the top brach, if it returns False, you should follow the
bottom branch.

• Knowledge about how the path_follow works under
TrailSeries would be useful here.

Task 3: Double Keyed Table

• This task is sort of taking a break from the Mountain
Climber application! You task is to implement a new type of
hashtable and it has nothing to do with the Trails. (although
you may choose to use it in later task, but the
implementation of Double Keyed Table should not be
specific to Trails).

• As per the specification, double keyed table uses linear
probing to handle collision.

• For each data to insert, there will be 2 keys and 1 value.
The first key will decide where in the top level table the low
level table is located, and the second key will then decide
where the value will be stored.

Task 3: Double Keyed Table

• Here’s some important points:

• The low level table should be just an instance of LinearProbeTable
whereas the top level table is an array.

• the top level table should store the first key and instance of low level
table. For example, when inserting key1, key2, value1, if key1
hashed into position 3, then key1 and instance of low level table
should be stored in position 3 of the top level table. and if key2
hashed into position 5, then key2 and value1 should be stored in
position 5 of low level table.

• iter_keys and iter_values must return an iterator object which can
be used by the for item in x loop or next() method to return all
key1,key2,value pair of the double keyed table. Thus you would
need to implement an iterator class or generator.

Task 4: Infinite Depth Hash

Table

• This task is also has nothing to do with the Trails. Similar to
double keyed table, although you may choose to use this
infinite depth hash table in later task, but your implementation
of infinite depth hash table should not be specific to Trails.

• Infinite depth hash table is not using linear probe to handle
collision. Instead, it handle collision by creating new subtable
at the next level and reinsert both new data and the existing
data. if a subtable already exist at that position, it will attempt
to insert the new data at the subtable. This process of nesting
subtable continues until there’s an empty position the subtable
at one of the level.

• the size of the main table is the same with all its subtable at all
level which is 27.

Task 4: Infinite Depth Hash

Table

• Here’s some important points:
• At every table (main or subtable), it will either store a pair of key and value
or a pair of key and instance of subtable.
• Basically when a table store a pair of key1 and instance of subtable, the
instance of subtable will store all keys starts with key1.
• Except the main table, all subtable must at least have two pair of data
stored. That is, if after deleting one data pair the subtable only contains
one pair of data, the subtable at this particular level should be deleted
and the last pair should reinserted at its parent table (at the previous level)
and the same process applies unless the parent is the main table.
• for example: using the sample in the A2 sheet, deleting mine, it will
trigger reinsertion of mining into the main table since mining will be the
only pair in the current subtable, and all its parent subtable will only
have one pair until it reaches the main table.

Task 5: Mountain Organiser

• In this task, you will continue to work on the trails! You need
to complete the implementation of two methods under the
mountain organiser class. Here’s some important point:

• The mountain organiser keep a list of mountains in sorted
by its rank (from lowest to highest). The rank is based on
the length.

• If two or more mountain having the same length, it will be
ranked based lexicographical order of its name.

• In the two method that you need to implement, you can
use (and modify) the provided algorithm

Task 6: Mountain Manager

• This is the last task you need to do to make the Mountain
Climber app’s graph view to function properly. The
MountainManager class need to have an ADT to store the
mountain. The ADT required would be hashtable (hence
choose between LinearProbeTable, DoubleKeyedTable or
Infinite Depth Hash Table). Here’s some important point:

• By using the chosen ADT to store the mountain, you
should be able to filter the mountain by difficulty.

• In the group_by_difficulty() method, you should return a
sorted list of the mountains by its difficulty.

Task 7: More Trail methods

• In this last task, we aim to write more method to manipulate the
trails as follows:

• collect_all_mountains method basically will collect all mountains
starting from the trail instance where this method called. i.e.
starting from self.store.

• length_k_paths method basically will return a list of all possible
path with the size of k starting from the trail instance where this
method is called. i.e. starting from self.store. Unlike the
follow_path you previously implemented where it just follow one
possible path (either following top or bottom branch), in
length_k_paths, you will need to explore all possible path and if
in that path you found k number of mountains, add that list of k
mountains in the returned list. You are allowed to use a recursive
approach combined with the help of appropriate ADT.
