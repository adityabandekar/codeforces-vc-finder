import random
import discord
from discord import app_commands
from discord.ext import commands
from cfapi import *


async def _find_vc(interaction: discord.Interaction, handles: str):
    handle_list = handles.split(" ")
    submission_map = {}
    for handle in handle_list:
        submissions = get_user_submissions(handle)
        if submissions is None:
            await interaction.followup.send(content=f"{handle} is not a codeforces user.")
            return
        print("Got submissions for " + str(handle))
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

    print("Number of contests found: " + str(len(good_contests)))
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
