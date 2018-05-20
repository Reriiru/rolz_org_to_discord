from discord import Embed, Colour


class TwitterEmbeder(Embed):
    FORMAT_STRINGS = {
        "hydra": '`Hail Hydra!`',
        "shitpost": '*flings a shitty picture*',
        "pesel": '**Have a pesel!**',
        "neko_string": '*shamelesly ripping off features*'
    }

    def __init__(self, image, type):
        super().__init__(
                        title="Nice things are here!",
                        type="rich"
                    )
        self.colour = Colour.purple()
        self.description = self.FORMAT_STRINGS[type]
        self.set_image(url=image)
