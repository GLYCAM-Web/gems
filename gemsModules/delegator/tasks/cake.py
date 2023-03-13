def execute(cake: bool, color: None) -> str:
    """ Return info about a cake
    >>> print(execute(cake=True,color='ban dearg'))
    Tá cáca milis bándearg agat!
    >>> print(execute(cake=False,color='bandearg'))
    Is bréag é an cáca milis bándearg!
    >>> print(execute(cake=True,color='purple'))
    You have a purple cake!
    >>> print(execute(cake=False,color='exploding'))
    The exploding cake is a lie!
    """
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
