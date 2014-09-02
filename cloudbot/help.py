from util import hook

@hook.command
def help(inp, notice=None):
    notice("!sf [category] <search term> - Looks up relevant articles from the official symfony docs. Omitted category matches all.")
    notice("!seen <username> - Tells you the last time the given person was seen talking on this channel.")