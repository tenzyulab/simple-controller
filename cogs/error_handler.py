from textwrap import dedent

from discord.ext.commands import (
    BadArgument,
    Bot,
    Cog,
    CommandError,
    CommandNotFound,
    Context,
    MissingPermissions,
)


class ErrorHandler(Cog):
    permissions_jp = {
        "view_channel": "チャンネルを見る",
        "manage_channels": "チャンネルの管理",
        "manage_roles": "ロールの管理",
        "manage_emojis": "絵文字の管理",
        "view_audit_log": "監査ログを表示",
        "view_guild_insights": "サーバーインサイトを見る",
        "manage_webhooks": "ウェブフックの管理",
        "manage_guild": "サーバー管理",
        "create_instant_invite": "招待を作成",
        "change_nickname": "ニックネームの変更",
        "manage_nicknames": "ニックネームの管理",
        "kick_members": "メンバーをキック",
        "ban_members": "メンバーをBAN",
        "send_messages": "メッセージを送信",
        "embed_links": "埋め込みリンク",
        "attach_files": "ファイルを添付",
        "add_reactions": "リアクションの追加",
        "external_emojis": "外部の絵文字の使用する",
        "mention_everyone": "@everyone、@here、全てのロールにメンション",
        "manage_messages": "メッセージの管理",
        "read_message_history": "メッセージ履歴を読む",
        "send_tts_messages": "テキスト読み上げメッセージを送信する",
        "connect": "接続",
        "speak": "発言",
        "stream": "動画",
        "use_voice_activation": "音声検出を使用",
        "priority_speaker": "優先スピーカー",
        "mute_members": "メンバーをミュート",
        "deafen_members": "メンバーのスピーカーをミュート",
        "move_members": "メンバーを移動",
        "administrator": "管理者",
    }

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        ignore_errors = (
            BadArgument,
            CommandNotFound,
        )
        message = None
        if isinstance(error, ignore_errors):
            return
        elif isinstance(error, MissingPermissions):
            missing = ", ".join(
                self.permissions_jp[perm] for perm in error.missing_perms
            )
            message = f"あなたに{missing}の権限がないため、このコマンドを実行できません。"
        if message is None:
            message = dedent(
                """
                想定されていないエラーが発生しました。
                よければ、このサーバーで報告してください。
                https://discord.gg/4nSKCE9RRn
                """
            )
        await ctx.send(message)


def setup(bot: Bot):
    bot.add_cog(ErrorHandler(bot))
