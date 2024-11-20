from discord import Embed
import discord


async def get_user_info_embed(interaction: discord.Interaction, user: discord.User):
    embed = Embed(title="User Information", color=0x0000ff)
    embed.set_thumbnail(url=user.display_avatar.url)  # アバター画像を埋め込み

    # 基本情報を埋め込みに追加
    embed.add_field(name="Username", value=user.name, inline=True)
    embed.add_field(name="Display Name", value=user.display_name, inline=True)
    embed.add_field(name="User ID", value=user.id, inline=False)
    embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    print("-----------------------")
    print(user.name)
    print(user.display_name)
    print(user.id)
    print(user.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    print("-----------------------")

    # サーバーでの権限を取得
    if interaction.guild:
        try:
            # fetch_memberを使用してサーバーのユーザー情報を取得
            member = await interaction.guild.fetch_member(user.id)

            # すべての権限を取得し、カテゴリーごとに整理
            permissions = [perm.replace('_', ' ').title() for perm, value in member.guild_permissions if value]

            # 各カテゴリーに属する権限をリスト化
            admin_permissions = [perm for perm in permissions if perm == "Administrator"]
            management_permissions = [
                perm for perm in permissions if perm in [
                    "Manage Guild", "Manage Channels", "Manage Roles", "Manage Webhooks", "Manage Expressions",
                    "View Audit Log", "Manage Events", "Manage Threads", "Moderate Members"
                ]
            ]
            text_permissions = [
                perm for perm in permissions if perm in [
                    "Send Messages", "Send Tts Messages", "Manage Messages", "Embed Links", "Attach Files",
                    "Read Message History", "Mention Everyone", "Send Messages In Threads", "Create Public Threads",
                    "Create Private Threads", "Send Voice Messages", "Send Polls"
                ]
            ]
            voice_permissions = [
                perm for perm in permissions if perm in [
                    "Connect", "Speak", "Mute Members", "Deafen Members", "Move Members",
                    "Use Voice Activation", "Priority Speaker", "Request To Speak", "Use Soundboard"
                ]
            ]
            other_permissions = [
                perm for perm in permissions if perm not in admin_permissions + management_permissions +
                                                text_permissions + voice_permissions
            ]

            # 各カテゴリーをEmbedに追加
            embed.add_field(name="管理者権限", value=", ".join(admin_permissions) if admin_permissions else "None", inline=False)
            embed.add_field(name="サーバー管理系権限", value=", ".join(management_permissions) if management_permissions else "None", inline=False)
            embed.add_field(name="テキスト関連権限", value=", ".join(text_permissions) if text_permissions else "None", inline=False)
            embed.add_field(name="ボイスチャンネル関連権限", value=", ".join(voice_permissions) if voice_permissions else "None", inline=False)
            embed.add_field(name="その他の権限", value=", ".join(other_permissions) if other_permissions else "None", inline=False)

        except discord.NotFound:
            embed.add_field(name="Server Permissions", value="User not in server", inline=False)
    else:
        embed.add_field(name="Server Permissions", value="Command used outside a server", inline=False)

    return embed