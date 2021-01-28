from discord.ext.commands import Bot, Cog, CommandError, Context, MissingPermissions


class ErrorHandler(Cog):
    permissions_jp = {
        "manage_channels": "チャンネルの管理",
        "manage_roles": "権限の管理",
        "create_instant_invite": "招待を作成",
        "send_messages": "メッセージを送信",
        "embed_links": "埋め込みリンク",
        "attach_files": "ファイルを添付",
        "add_reactions": "リアクションの追加",
        "external_emojis": "外部の絵文字の使用",
        "manage_messages": "メッセージの管理",
        "read_message_history": "メッセージ履歴を読む",
        "connect": "接続",
        "speak": "発言",
        "use_voice_activation": "音声検出を使用",
        "priority_speaker": "プライオリティスピーカー",
        "mute_members": "メンバーをミュート",
        "deafen_members": "メンバーのスピーカーをミュート",
        "move_members": "メンバーを移動",
        "administrator": "管理者",
    }

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        message = None
        if isinstance(error, MissingPermissions):
            missing = "、".join(
                self.permissions_jp[perm] for perm in error.missing_perms
            )
            message = f"あなたに{missing}の権限がないため、このコマンドを実行できません。"
        if message is None:
            message = "何らかの想定されていないエラーが発生しました。"
        await ctx.send(message)


def setup(bot: Bot):
    bot.add_cog(ErrorHandler(bot))
