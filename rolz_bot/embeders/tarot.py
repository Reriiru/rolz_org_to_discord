from discord import Embed, Colour


class TarotEmbeder(Embed):
    def __init__(self, image, username):
        super().__init__(
                        title=image['Name'],
                        type="rich"
                    )

        self.set_image(url=image['Url'])
        self.colour = Colour.teal()
        self.description = image['Description']
        self.add_field(name="Requester", value=username)


class TarotShortEmbeder(Embed):
    def __init__(self, image, username):
        super().__init__(
                title=image['Name'],
                type="rich"
            )

        self.set_image(url=image['Url'])
        self.colour = Colour.teal()
        self.add_field(name="Requester", value=username)