from mcdreforged.api.all import *
from typing import cast

def on_load(server: PluginServerInterface, prev):
    server.register_help_message('!!head [player] [个数]', '获取指定玩家的头颅,支持同时获取多个。当count未指定时，默认值为1。本插件支持全版本。')
    builder = SimpleCommandBuilder()
    builder.command("!!head",                   parsar)
    builder.command("!!head <player>",          parsar)
    builder.command("!!head <player> <count>",  parsar)
    builder.arg("player", Text)
    builder.arg("count", lambda count: Integer(count).at_min(1))
    builder.register(server)


def execute(_source: CommandSource, _owner: str, _player: str, _count: int) -> None:
    version = Version(ServerInterface.get_instance().get_server_information().version)
    ver_mapping = {
        (Version("1.20.5+"), None): 2,
        (Version("1.13"), Version("1.20.5")): 1,
        (None, Version("1.13")): 0
    }
    val = next(
        (
            value for (min_ver, max_ver), value in ver_mapping.items()
            if (min_ver is None or version >= min_ver) and (max_ver is None or version < max_ver)
        ),
        0
    )
    command_mapping = {
        2: f'/give {_owner} minecraft:player_head[minecraft:profile="{_player}"] {_count}',
        1: f'/give {_owner} minecraft:player_head{{SkullOwner:"{_player}"}} {_count}',
        0: f'/give {_owner} minecraft:skull {_count} 3 {{SkullOwner:"{_player}"}}'
    }
    command = command_mapping.get(val, command_mapping[2])
    _source.get_server().execute(command)
    _source.reply(f"§b{_owner} 刚刚获取了{_count}个 {_player} 的头瞄~")

def parsar(source: CommandSource, ctx: CommandContext) -> None:
    if not source.is_player:
        source.reply("§c§l只有玩家可以执行此命令瞄~")
        return

    source = cast(PlayerCommandSource, source)

    owner   = source.player
    count   = 1     if "count"  not in ctx else ctx["count"]
    player  = owner if "player" not in ctx else ctx["player"]

    execute(source, owner, player, count)

