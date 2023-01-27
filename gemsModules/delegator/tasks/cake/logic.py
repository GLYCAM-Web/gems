def cake_is_a_lie(cake: bool, color: None) -> str:
    if color is None:
        if cake == True:
            return "You have cake!"
        else:
            return "The cake is a lie!"
    if color == 'bándearg' or color == 'bandearg' or color =='bán dearg' or color == 'ban dearg':
        if cake == True:
            return "Tá cáca milis bándearg agat!"
        else:
            return "Is bréag é an cáca milis bándearg."
    if cake == True:
        return f"You have a {str(color)} cake!"
    else:
        return f"The {str(color)} cake is a lie!"


#print(cake_is_a_lie(cake=False,color='bandearg'))
#print(cake_is_a_lie(cake=True,color='purple'))
