from ..base import BaseObject, Collection


class Group(Collection):
    """Group of objects.

    A Group object is a collection of objects.
    """

    def __init__(self, objects: list[Collection | BaseObject] | None = None):
        """Create a Group object."""
        super().__init__()
        if objects:
            for obj in objects:
                self.add_object(obj)

    def _create_objects(self) -> None:
        """Create objects for the group."""
