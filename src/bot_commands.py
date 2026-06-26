import random
import discord
from discord import app_commands
from discord.ext import commands
from cfapi import *
from src import dbapi


async def _get_alts(interaction: discord.Interaction, user: str):
    user_id = user[2:-1]
    alt_list = dbapi.get_alts(user_id)
    if alt_list is None:
        await interaction.followup.send(content=f"They do not have any alts.")
    else:
        await interaction.followup.send(content="Their alts are: " + " ".join(alt_list))


async def _set_my_alts(interaction: discord.Interaction, alts: str):
    alt_list = alts.split(" ")
    for handle in alt_list:
        if get_user_submissions(handle) is None:
            await interaction.followup.send(content=f"{handle} is not a codeforces user.")
            return
    dbapi.set_alts(str(interaction.user.id), alt_list)
    await interaction.followup.send(content="Set your alts to: " + " ".join(alt_list))

async def _find_vc(interaction: discord.Interaction, handles: str):
    handle_list = []
    for handle in handles.split(" "):
        if len(handle) > 0 and handle[0] == '<': # scuffed way to check if its a discord @
            user_id = handle[2:-1]
            alts = dbapi.get_alts(user_id)
            if alts:
                handle_list.extend(alts)
            else:
                await interaction.followup.send(content=f"{handle} does not have any alts set.")
                return
        else:
            handle_list.append(handle)

    submission_map = {}

    for handle in handle_list:
        submissions = get_user_submissions(handle)
        if submissions is None:
            await interaction.followup.send(content=f"{handle} is not a codeforces user.")
            return
        submission_map[handle] = submissions

    contest_ids = get_cf_contest_ids()
    good_contests = contest_ids.copy()

    for handle in submission_map:
        submission_list = submission_map[handle]
        for submission in submission_list:
            if submission["contestId"] in contest_ids:
                good_contests.discard(submission["contestId"])

    if not good_contests:
        await interaction.followup.send(content="No contests satisfy the criteria.")
        return

    random_id = random.choice(list(good_contests))
    embed = discord.Embed(description=f"https://codeforces.com/contest/{random_id}")
    await interaction.followup.send(embed=embed)


def setup_commands(bot: commands.Bot):
    @bot.tree.command(name="find_vc",
                      description="Find a codeforces virtual contest")
    @app_commands.describe(handles="Codeforces handles")
    async def find_vc(interaction: discord.Interaction, handles: str):
        await interaction.response.defer()
        await _find_vc(interaction, handles)

    @bot.tree.command(name="set_my_alts",
                      description="Set your codeforces alts.")
    @app_commands.describe(alts="Alts")
    async def set_my_alts(interaction: discord.Interaction, alts: str):
        await interaction.response.defer()
        await _set_my_alts(interaction, alts)

    @bot.tree.command(name="get_alts",
                      description="Get someones codeforces alts.")
    @app_commands.describe(user="@username")
    async def get_alts(interaction: discord.Interaction, user: str):
        await interaction.response.defer()
        await _get_alts(interaction, user)
