from __future__ import annotations
from dataclasses import dataclass
from data_structures.linked_stack import LinkedStack
from mountain import Mountain

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        self.path_top.store = None
        self.path_bottom.store = None
        return self.path_follow.store

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""
        return None


    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        ret = TrailSeries(mountain, Trail(self))
        return ret

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        return TrailSplit(Trail(None), Trail(None), Trail(self))



    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        ret = TrailSeries(self.mountain, Trail(TrailSeries(mountain, self.following)))
        return ret

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        ret = TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))
        return ret

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(TrailSeries(mountain, Trail(self.store)))

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        return Trail(TrailSplit(Trail(None), Trail(None), Trail(self.store)))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality.
        Args:
        -personality represents WalkerPersonality obj

        Raises:
        -None

        Returns:
        -None

        Complexity:
        -Worst Case: O(m*(n*comp)*comp), where m is the number of element in the stack and n is the number of path and comp is comparison complexity
        -Best Case: O(m*(n*comp)*comp),where m is the number of element in the stack and n is the number of path and comp is comparison complexity

        -Explantion: assignments, pushing and creating is O(1). calling self.loop_through is O(n*comp) where n is number of path
                    while stack is not empty the loop will continue hence it is O(m) where m is the number of element in the stack and comparison of isinstance is O(comp)
                    and if the trailseries has a path following then it calls the loop_through function which is O(n*comp).
                    suppose is O(m*(n*comp)*comp + (n*comp)) but because of m*(n*comp)*comp has higher upper bound than n*comp so overall the complexity is O(m*(n*comp)*comp)
        """
        current = self.store                                                                #assign self.store to current
        stack = LinkedStack()                                                               #create a linked stack
        stack.push(current.path_follow.store)                                               #push the first stage of split trail to stack
        self.loop_through(current, stack, personality)                                      #call the loop through method to loop through every stage of trail O(n*comp)

        while not stack.is_empty():                                                         #while the stack is not empty
            path = stack.pop()                                                              #pop the path
            if isinstance(path, TrailSeries):                                               #if the path is instance of a TrailSeries
                personality.add_mountain(path.mountain)                                     #then append mountain through path.mountain
                if isinstance(path, TrailSeries) and path.following.store is not None:      #if there is a following trail
                    self.loop_through(path.following.store, stack, personality)             #loop through the following trail and push the chosen path into stack

    def loop_through(self, current: TrailSplit, stack: LinkedStack, personality: WalkerPersonality)-> None:
        """
        Loop through the path based on the personality and push it in a stack

        Args:
        -personality represents WalkerPersonality obj
        -current represents current path
        -stack representing the stack that pushing the path to

        Raises:
        -Attribute error when there is no more path to traverse

        Returns:
        -return to stop the function

        Complexity:
        -Worst Case: O(n*comp), where n is the number of path, comp is comparison complexity
        -Best Case: O(n*comp), where n is the number of path, comp is comparison complexity
        -Explantion: it needs to traverse to the upper path or the lower path based on the personality until it meets an error
        """
        try:
            while current is not None:
                if isinstance(current, TrailSplit):                                         #if the current is instance of TrailSplit
                    if personality.select_branch(current.path_top, current.path_bottom):    #select the branch based on personality
                        current = current.path_top.store                                    #if personality return True, path_top is chosen
                    else:
                        current = current.path_bottom.store                                 #if personaility return false, path_bottom is chosen

                    stack.push(current)                                                     #push current into stack
                    stack.push(current.path_follow.store)                                   #push middle path of every TrailSplit into stack

        except AttributeError:                                                              #if errors occurs -> no more path to walk
            return


    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        mountain = []
        return self.collect_all_mountain_aux(self, mountain)


    def collect_all_mountain_aux(self, trail, mountain)-> list[Mountain]:
        if trail.store is not None:
            if isinstance(trail.store, TrailSeries):
                mountain.append(trail.store.mountain)
                self.collect_all_mountain_aux(trail.store.following, mountain)

            elif isinstance(trail.store, TrailSplit):
                self.collect_all_mountain_aux(trail.store.path_top, mountain)
                self.collect_all_mountain_aux(trail.store.path_bottom,mountain)
                self.collect_all_mountain_aux(trail.store.path_follow, mountain)

        return mountain

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        mountain = []
        all_path = []
        stack = LinkedStack()
        for i in self.collect_all_mountain_aux(self.store.path_follow,[]):
            stack.push(i)
        return self.length_k_paths_aux(self,k,mountain,all_path,stack)

    def length_k_paths_aux(self,trail ,k ,mountain, all_path, stack):
        mountain2 = []
        if len(mountain) == k-1 and len(all_path) < k:
            if stack.peek() not in mountain:
                mountain.append(stack.peek())
            all_path.append(mountain)
            return
        elif trail.store is not None:
            if isinstance(trail.store, TrailSeries) and len(mountain) <k:
                mountain.append(trail.store.mountain)
                self.length_k_paths_aux(trail.store.following,k,mountain,all_path, stack)
            elif isinstance(trail.store, TrailSplit):
                self.length_k_paths_aux(trail.store.path_top,k,[],all_path, stack)
                self.length_k_paths_aux(trail.store.path_bottom, k, mountain2, all_path, stack)
                self.length_k_paths_aux(trail.store.path_follow, k, mountain2, all_path, stack)
                self.length_k_paths_aux(trail.store.path_top, k, mountain, all_path, stack)
                self.length_k_paths_aux(trail.store.path_follow, k, mountain, all_path, stack)
        return all_path


