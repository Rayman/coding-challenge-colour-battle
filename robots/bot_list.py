import importlib

from robots.short_sighted_steve import ShortSightedSteve

RamboTheRando = importlib.import_module("robots.coding-challenge-bot-template.rambo_the_rando").RamboTheRando
DanielsRobot = importlib.import_module("robots.DanielsRobot.Daniels_Bot").Daniels_Bot
JorikAtilla = importlib.import_module("robots.jorik.atilla").AtillaTheAttacker
TheCluelessAfrican = importlib.import_module("robots.jp.The_no_clue_African").TheCluelessAfrican
BigAssBot = importlib.import_module("robots.mahmoud.big_ass_bot").BigAssBot
ch34tsRus = importlib.import_module("robots.lewie.ch34tsRus").ch34tsRus
Aslan = importlib.import_module("robots.hakan.aslan").Aslan
RickbrandtVanRijn = importlib.import_module("robots.rick.RickbrandtVanRijn").RickbrandtVanRijn
Vector = importlib.import_module("robots.ishu.vector").Vector
Greedy = importlib.import_module("robots.rayman.greedy").Greedy
id10plus_bot = importlib.import_module("robots.tim.id10+_bot").id10plus_bot
ShortSpanDog = importlib.import_module("robots.felipe.short_span_dog").ShortSpanDog
LearoundoDaVinci = importlib.import_module("robots.hein-leo.learoundo_da_vinci").LearoundoDaVinci
RapidRothko = importlib.import_module("robots.jorik.rapid").RapidRothko
Abra = importlib.import_module("robots.rayman.search_min").Abra
Kadabra = importlib.import_module("robots.rayman.search_min").Kadabra
Furbot = importlib.import_module("robots.furbot.furbot").FurBot
LeonardoDaVidi = importlib.import_module("robots.bram.leonardo_da_vidi").LeonardoDaVidi

# Add new bots to the bottom of this list
# to maintain the same colours as much as possible
BotList = [
    Furbot,
    LeonardoDaVidi,
    DanielsRobot,
    JorikAtilla,
    TheCluelessAfrican,
    BigAssBot,
    ch34tsRus,
    Aslan,
    RickbrandtVanRijn,
    Vector,
    # Greedy,
    Abra, # Replaces Greedy so that visible colours remain the same
    id10plus_bot,
    ShortSpanDog,
    LearoundoDaVinci,
    RapidRothko,
    Kadabra,

    # These should always be last
    RamboTheRando,
    ShortSightedSteve,
]