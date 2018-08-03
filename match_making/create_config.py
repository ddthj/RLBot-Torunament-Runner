from rlbot.parsing.agent_config_parser import PARTICIPANT_CONFIGURATION_HEADER, PARTICIPANT_CONFIG_KEY, \
    PARTICIPANT_TEAM, PARTICIPANT_LOADOUT_CONFIG_KEY
from rlbot.parsing.custom_config import ConfigObject, ConfigHeader
from rlbot.parsing.match_settings_config_parser import MATCH_CONFIGURATION_HEADER, PARTICIPANT_COUNT_KEY
from rlbot.parsing.rlbot_config_parser import create_bot_config_layout

from gui.player import Player


def create_match_config(players):
    config_object = create_bot_config_layout()
    config_object.set_value(MATCH_CONFIGURATION_HEADER, PARTICIPANT_COUNT_KEY, len(players))

    player_header = config_object.get_header(PARTICIPANT_CONFIGURATION_HEADER)
    for i in range(players):
        add_player_to_config(i, players[i], player_header)
    return config_object


def add_player_to_config(index, player: Player, player_header: ConfigHeader):
    player_header.set_value(PARTICIPANT_CONFIG_KEY, player.get_config_location(), index)
    player_header.set_value(PARTICIPANT_TEAM, player.get_team(), index)
    player_header.set_value(PARTICIPANT_LOADOUT_CONFIG_KEY, player.get_loadout(), index)


def write_config_to_file(file_path, config: ConfigObject):
    with open(file_path, "w") as f:
        f.write(str(config))
