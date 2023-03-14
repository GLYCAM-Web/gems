from typing import Protocol
from typing import Union

class cake_data(Protocol):
    cake : bool
    color : Union[str,None]

def execute(cake_data) -> str:
    """ Return info about a cake
    >>> class cake():
    ...     cake : bool = True
    ...     color : str = 'ban dearg'
    >>> the_cake = cake()
    >>> print(execute(the_cake))
    Tá cáca milis bándearg agat!
    >>> the_cake.cake = False
    >>> the_cake.color = 'bandearg'
    >>> print(execute(the_cake))
    Is bréag é an cáca milis bándearg!
    >>> the_cake.cake = True
    >>> the_cake.color = 'purple'
    >>> print(execute(the_cake))
    You have a purple cake!
    >>> the_cake.cake = False
    >>> the_cake.color = 'exploding'
    >>> print(execute(the_cake))
    The exploding cake is a lie!
    """

    color = cake_data.color
    cake = cake_data.cake
    if color is None:
        if cake == True:
            return "You have cake!"
        else:
            return "The cake is a lie!"
    if color == 'bándearg' or color == 'bandearg' or color =='bán dearg' or color == 'ban dearg':
        if cake == True:
            return "Tá cáca milis bándearg agat!"
        else:
            return "Is bréag é an cáca milis bándearg!"
    if cake == True:
        return f"You have a {str(color)} cake!"
    else:
        return f"The {str(color)} cake is a lie!"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
